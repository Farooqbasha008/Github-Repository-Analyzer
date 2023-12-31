import re
import streamlit as st
import requests
from github import Github
from github.GithubException import GithubException, UnknownObjectException
import nbformat
from pygments import lex
from pygments.lexers.python import PythonLexer
from pygments.token import Token
import openai
from collections import defaultdict
import textwrap
from IPython.display import display, Markdown , HTML


# Set the maximum number of tokens allowed for GPT input
MAX_TOKENS = 4096

# Cache to store previously generated evaluations
evaluation_cache = {}


def get_user_repositories(github_user_url):
    # Extract the username from the GitHub user URL
    match = re.search(r"github\.com/([A-Za-z0-9_-]+)", github_user_url)
    if match:
        username = match.group(1)
    else:
        raise ValueError("Invalid GitHub URL")

    # Use the GitHub API to retrieve the user's repositories
    g = Github()  # Initialize the GitHub API client
    user = g.get_user(username)
    repositories = user.get_repos()

    return repositories


def preprocess_code(code):
    # Remove comments from the code
    code = re.sub(r"#.*", "", code)

    # Tokenize the code using pygments
    tokens = list(lex(code, PythonLexer()))

    # Create a list to store the tokenized code
    tokenized_code = []

    # Traverse the tokens and extract the token values
    for token in tokens:
        token_value = token[1]

        # Skip tokens with empty value or only containing whitespace
        if not token_value.strip():
            continue

        # Shorten long identifiers
        if len(token_value) > 20:
            token_value = token_value[:17] + "..."

        # Append the token value to the list
        tokenized_code.append(token_value)

    # Truncate or summarize code snippets that exceed the maximum token limit
    if len(tokenized_code) > MAX_TOKENS:
        tokenized_code = tokenized_code[:MAX_TOKENS]
        tokenized_code.append("...")  # Add ellipsis to indicate summary

    # Join the tokens back into code
    preprocessed_code = " ".join(tokenized_code)

    return preprocessed_code


def fetch_code_snippets(repository):
    code_snippets = []

    try:
        # Use the GitHub API to retrieve the contents of each file in the repository
        contents = repository.get_contents("")

        combined_code = ""

        for content_file in contents:
            # Fetch only Python files and Jupyter notebooks
            if content_file.path.endswith(".py"):
                # Fetch the code snippet from the file
                code_url = content_file.download_url
                response = requests.get(code_url)
                code = response.text

                # Preprocess the code
                preprocessed_code = preprocess_code(code)
                combined_code += preprocessed_code + " "

            elif content_file.path.endswith(".ipynb"):
                # Fetch the code cells from the Jupyter notebook
                code_url = content_file.download_url
                response = requests.get(code_url)
                nb = nbformat.reads(response.text, nbformat.NO_CONVERT)
                code_cells = [cell.source for cell in nb.cells if cell.cell_type == "code"]

                # Preprocess each code cell
                for code_cell in code_cells:
                    preprocessed_code = preprocess_code(code_cell)
                    combined_code += preprocessed_code + " "

        if not combined_code:
            raise UnknownObjectException(status=404, data="No code snippets found", headers={})  # Raise exception if no code snippets found

        # Split the combined code into chunks if it exceeds the maximum token limit
        code_chunks = [combined_code[i:i + MAX_TOKENS] for i in range(0, len(combined_code), MAX_TOKENS)]

        for i, chunk in enumerate(code_chunks):
            code_snippets.append((repository.name, f"chunk_{i + 1}", chunk, len(chunk)))

    except UnknownObjectException:
        # Skip repositories without code snippets
        return []

    return code_snippets


def evaluate_code_complexity(code):
    # Generate the evaluation using GPT-3.5 Turbo
    prompt = f"Code: {code}\n\nEvaluate the complexity of the code snippet based on the following criteria:\n\n" \
             "1. Code Length: Longer code tends to be more complex as it may contain more logic, branches, and dependencies.\n" \
             "2. Control Flow: The complexity increases with the presence of nested loops, conditional statements, and complex branching logic.\n" \
             "3. Function and Class Complexity: Functions or methods with a high number of lines, parameters, or local variables can be harder to understand and maintain.\n" \
             "4. Code Duplication: Repeated code blocks increase complexity and make maintenance more difficult. Identifying and removing code duplication is essential.\n" \
             "5. Code Coupling: High coupling, where modules or components depend heavily on each other, increases complexity. Lower coupling and better modularization lead to simpler code.\n" \
             "6. Code Dependencies: Complex dependencies between modules or libraries can make code harder to understand, test, and maintain. Minimizing dependencies and using clear interfaces can help manage complexity.\n" \
             "7. Code Documentation: The availability and quality of comments, documentation, and inline explanations impact code complexity. Well-documented code is generally easier to comprehend.\n" \
             "8. Naming Conventions: Meaningful and consistent naming of variables, functions, and classes improves code readability and reduces complexity.\n" \
             "9. Error Handling: Proper error handling, exception handling, and defensive programming techniques can help manage complexity when dealing with unexpected scenarios.\n" \
             "10. Code Readability: Clear formatting, indentation, and code style guidelines contribute to code readability and reduce complexity.\n\n" \
             "Please provide a complexity score between 0.1 and 1 for the code snippet based on the provided criteria."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    # Extract the complexity score from the response
    complexity_score_text = response.choices[0].text.strip()
    complexity_score_matches = re.findall(r"\d+(\.\d+)?", complexity_score_text)
    complexity_score = float(complexity_score_matches[0])

    if complexity_score_matches:
        complexity_score = float(complexity_score_matches[0])
    else:
        complexity_score = 0.0

    return complexity_score


def analyze_github_user(github_user_url, api_key):
    openai.api_key = api_key

    try:
        st.info("Analyzing GitHub user...")
        repositories = get_user_repositories(github_user_url)
        repository_scores = {}

        for repository in repositories:
            if repository.size == 0:
                st.warning(f"Skipping empty repository: {repository.name}")
                continue

            repository_name = repository.name
            repository_scores[repository_name] = evaluate_repository_complexity(repository)

        # Arrange the repositories in descending order of complexity
        sorted_repositories = sorted(repository_scores.items(), key=lambda x: x[1], reverse=True)

        # Display the repository names and complexity scores
        st.markdown("### Repository Complexity Scores:")
        for repo, score in sorted_repositories:
            st.markdown(f"- **Repository:** {repo}, **Complexity Score:** {score}")

        # Display the name and complexity score of the most complex repository
        if sorted_repositories:
            most_complex_repo = sorted_repositories[0]
            st.markdown("\n### Most Complex Repository:")
            st.markdown(f"- **Repository:** {most_complex_repo[0]}, **Complexity Score:** {most_complex_repo[1]}")

            # Use GPT to justify the selection of the most complex repository
            justification_prompt = f"Justify the selection of the most complex repository: {most_complex_repo[0]}."
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=justification_prompt,
                max_tokens=128,
                n=1,
                stop=None,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            justification = response.choices[0].text.strip()

            formatted_justification = "\n".join(textwrap.wrap(justification, width=125))
            st.markdown("### Justification by the GPT:")
            st.markdown(formatted_justification)

            # Get the URL of the most complex repository
            most_complex_repo_url = f"{github_user_url}/{most_complex_repo[0]}"

            # Display the hyperlink to the most complex repository
            st.markdown(f"### [Click here to go to the Most Complex Repository of the user]({most_complex_repo_url})")

        else:
            st.warning("No repositories with code snippets found.")

    except Exception as e:
        st.error(f"Error occurred: {str(e)}")


# Streamlit app
def main():
    st.title("GitHub User Code Complexity Analyzer")
    github_user_url = st.text_input("Enter the GitHub user URL:")
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    if st.button("Analyze"):
        analyze_github_user(github_user_url, api_key)


# Run the Streamlit app
if __name__ == "__main__":
    main()
