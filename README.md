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

As of now, you can use this in Google Colab or in your local system.

# Google Colab
1. Open the Github_Automated_Analysis.ipynb in Google Colab.
2. Run the cells in the notebook .
3. Input the particulars and the results will be displayed.

# Local System
1. Download the app.py, index.html, result.html, styles.css files.
2. Make a folder named templates and keep index.html and result.html in it.
3. Make a folder named static and keep styles.css file in it.
4. Make a new folder and keep app.py , templates folder and static folder inside it.
5. Open cmd terminal.
6. Run the following command:
    pip install flask
7. After installation is done, Enter the following command:
    cd "path to the folder"
8. Then Run the tool by enetring
     flask run
9. The terminal will show the website url.
10. Copy the url and paste it in a browser and acces the tool.

# Note 

This is a very basic tool and still under development. Feel free to contribute.

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
