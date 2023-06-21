# GitHub Repository Analyzer

The GitHub Repository Analyzer is an automated repository analyzer tool that allows you to analyze the technical complexity of GitHub user repositories using OpenAI's GPT language model. It fetches a user's repositories from their GitHub user URL, preprocesses the code, and applies prompt engineering to determine the complexity of the code. The tool identifies the most technically complex repository and provides a GPT-generated justification for the selection.

## Features

- Fetches a user's repositories from their GitHub user URL.
- Preprocesses code to manage memory and handle large files.
- Applies prompt engineering for code complexity evaluation.
- Identifies the most complex repository and provides a GPT-generated justification.
- Simple and user-friendly web interface.
- Deployed on a hosting platform for easy access.

## How to Use

1. Visit the website of the GitHub Repository Analyzer tool. 
2. Enter the GitHub user URL of the user whose repositories you want to analyze.
3. Click the "Analyze" button to initiate the analysis process.
4. The tool will fetch the repositories, preprocess the code, and evaluate the complexity.
5. Once the analysis is complete, the tool will display the repository complexity scores, the most complex repository, and the GPT analysis justification.
6. Access the most complex repository by clicking on the provided link.

## Deployment

The GitHub Repository Analyzer tool can be deployed on a hosting platform such as Vercel, Netlify, or GitHub Pages. To deploy it on GitHub Pages:

1. Fork this repository to your GitHub account.
2. Ensure you have an `index.html` file containing the HTML structure and JavaScript functions for the user interface.
3. Update the necessary API endpoints or configuration variables in the JavaScript code to match your deployment setup.
4. Push the changes to your forked repository.
5. Go to the repository's settings on GitHub.
6. Scroll down to the "GitHub Pages" section.
7. Select the branch you want to use for GitHub Pages (e.g., `main` or `master`).
8. Optionally, choose a custom domain or leave it as the default GitHub Pages URL.
9. Click "Save" to deploy the tool.
10. Visit the deployed website of the GitHub Repository Analyzer using the provided GitHub Pages URL.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

Feel free to contribute and improve this tool by submitting issues or pull requests.
