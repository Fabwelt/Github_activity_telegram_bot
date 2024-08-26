```markdown
# GitHub to Telegram Commit Notifier

This script monitors one or more GitHub (public and private) repositories for new commits and sends notifications to a specified Telegram channel. The script is designed to prevent duplicate notifications and includes retry logic to handle transient errors.

## Features

- Monitors multiple GitHub repositories for new commits (public as private).
- Posts commit messages, commit dates, and changed files to a Telegram channel.
- Prevents duplicate messages by tracking posted commits.
- Includes retry logic to handle network issues during Telegram message delivery.

## Prerequisites

- **Python 3.x**: Ensure you have Python 3 installed.
- **GitHub API Token**: Required to access GitHub repositories.
- **Telegram Bot Token**: Required to send messages to a Telegram channel.
- **Environment Variables**: Sensitive data such as tokens should be stored in environment variables.

## Setup

### 1. Clone the Repository

```
git clone https://github.com/yourusername/repo-name.git
cd repo-name
```

### 2. Install Dependencies

No external dependencies are required for this script. However, ensure you have `requests` installed. If not, you can install it via pip:

```
pip install requests
```

### 3. Set Up Environment Variables

You need to set the following environment variables to run the script:

- `GITHUB_TOKEN`: Your GitHub API token.
- `GITHUB_USERNAME`: Your GitHub username.
- `TELEGRAM_TOKEN`: Your Telegram bot token.
- `TELEGRAM_CHANNEL_ID`: The ID of the Telegram channel where you want to post updates.

#### Setting Environment Variables on Linux/macOS

You can add these lines to your `.bashrc`, `.bash_profile`, or `.zshrc` file:

```
export GITHUB_TOKEN='your_github_token'
export GITHUB_USERNAME='your_github_username'
export TELEGRAM_TOKEN='your_telegram_token'
export TELEGRAM_CHANNEL_ID='your_telegram_channel_id'
```

After adding these lines, reload your shell:

```
source ~/.bashrc  # or source ~/.bash_profile or source ~/.zshrc
```

#### Setting Environment Variables on Windows

You can set environment variables via the Command Prompt or System Properties.

Alternatively, use a `.env` file and `python-dotenv`:

1. **Install `python-dotenv`:**

    ```
    pip install python-dotenv
    ```

2. **Create a `.env` file:**

    ```
    GITHUB_TOKEN=your_github_token
    GITHUB_USERNAME=your_github_username
    TELEGRAM_TOKEN=your_telegram_token
    TELEGRAM_CHANNEL_ID=your_telegram_channel_id
    ```

3. **Load the `.env` file in the script:**

    Add the following to your script:

    ```python
    from dotenv import load_dotenv
    load_dotenv()  # Take environment variables from .env.
    ```

### 4. Edit the Script

Update the `repositories` list in the script with the names of the GitHub repositories you want to monitor:

```python
repositories = [
    'Repo1', 'Repo2', 'etc'
]
```

### 5. Run the Script

Run the script using Python:

```
python github_to_telegram.py
```

The script will start monitoring the specified repositories and posting updates to the Telegram channel.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
