# Dynamic Website Saver and Publisher

This script allows you to save a dynamic website and its associated resources to your local machine and publish the changes to a remote Git repository. Made speicifically for easier publishing on Github pages. 

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `gitpython` library

## Installation

1. Clone the repository to your local machine.
2. Install the required libraries using pip:

```
pip install requests beautifulsoup4 gitpython
```

## Usage

1. Open the `saver.py` file in a text editor.
2. Update the following variables in the script:

- `GITHUB_TOKEN`: Your GitHub token with the necessary permissions to push to the remote repository.
- `REMOTE_URL`: The URL of the remote Git repository you want to push the changes to.
- `BASE_URL`: The base URL of the website you want to save.
- `DIRECTORY`: The directory where you want to save the website files.
- `GIT_AUTHOR_NAME`: Your name as the author of the Git commit.
- `GIT_AUTHOR_EMAIL`: Your email address as the author of the Git commit.

3. Save the changes to the script.
4. Open a terminal and navigate to the directory where the script is saved.
5. Run the following command to execute the script:

```
python saver_publish.py
```

6. Follow the prompts in the terminal to save the website files and publish the changes to the remote Git repository.

## Contributing

If you find any issues with the script or have suggestions for improvements, please feel free to open an issue or submit a pull request on GitHub.

## License

This script is licensed under the Apache License 2.0 License. See the `LICENSE` file for more information.
