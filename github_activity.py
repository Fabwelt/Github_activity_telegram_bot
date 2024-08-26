import requests
import json
from datetime import datetime, timedelta, timezone
import os
import re
import time

# Load GitHub API token, username, Telegram bot token, and channel ID from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

# List of repositories to monitor
repositories = [
    'Repo1', 'Repo2', 'etc'
]

# File to keep track of posted commits
POSTED_COMMITS_FILE = 'posted_commits.txt'

# Function to escape Markdown special characters except hyphens and periods
def escape_markdown(text):
    escape_chars = r'\_*[]()~`>#+=|{}!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

# Function to fetch recent activity for a specific repository
def fetch_repo_activity(repo_name):
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/events'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repo activity for {repo_name}: {e}")
        return []

# Function to fetch commit details (including changed files)
def fetch_commit_details(repo_name, commit_sha):
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/commits/{commit_sha}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching commit details for {commit_sha} in {repo_name}: {e}")
        return {}

# Function to send a message to Telegram with retries
def send_message_to_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHANNEL_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to Telegram: {e}")
            if attempt < retries - 1:
                print(f"Retrying... ({attempt + 1}/{retries})")
                time.sleep(2)  # Wait before retrying
            else:
                print(f"Failed after {retries} attempts.")
                return {}

# Function to check if a commit has already been posted
def is_commit_posted(commit_sha):
    if os.path.exists(POSTED_COMMITS_FILE):
        with open(POSTED_COMMITS_FILE, 'r') as file:
            posted_commits = file.read().splitlines()
            return commit_sha in posted_commits
    return False

# Function to mark a commit as posted
def mark_commit_as_posted(commit_sha):
    with open(POSTED_COMMITS_FILE, 'a') as file:
        file.write(commit_sha + '\n')

def update_telegram_with_github_activity():
    # Calculate the time 72 hours ago using timezone-aware datetime
    time_limit = datetime.now(timezone.utc) - timedelta(hours=48)
    print(f"Time limit: {time_limit}")
    
    for repo_name in repositories:
        activities = fetch_repo_activity(repo_name)
        
        # Debug: print raw events
        print(f"Fetched {len(activities)} events for {repo_name}")
        
        # Filter and sort events by creation date (oldest first)
        events = [event for event in activities if event['type'] == 'PushEvent' and event['payload']['commits']]
        print(f"Filtered {len(events)} PushEvent activities for {repo_name}")
        
        # Sort the events by created_at
        events.sort(key=lambda e: e['created_at'])
        
        for event in events:
            # Parse event's creation date
            event_time = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            print(f"Processing event at {event_time} (repo: {repo_name})")
            
            # Process only events that occurred within the last 72 hours
            if event_time > time_limit:
                for commit in event['payload']['commits']:
                    commit_sha = commit['sha']
                    
                    # Check if this commit has already been posted
                    if is_commit_posted(commit_sha):
                        print(f"Commit {commit_sha} already posted. Skipping.")
                        continue
                    
                    commit_message = escape_markdown(commit['message'])
                    commit_date = event_time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Fetch commit details to get the list of changed files
                    commit_details = fetch_commit_details(repo_name, commit_sha)
                    
                    # Extract only filenames and extensions
                    files_changed = [escape_markdown(os.path.basename(file['filename'])) for file in commit_details.get('files', [])]
                    files_changed_text = "\n".join([f"- {file}" for file in files_changed]) if files_changed else "No files changed."

                    # Prepare the message with improved formatting
                    message = (
                        f"🚀 New Commit in *{escape_markdown(repo_name)}*\n\n"
                        f"*Message:* **{escape_markdown(commit_message)}**\n\n"
                        f"*Commit Date:* **{commit_date}**\n\n"
                        f"*Files Changed:*\n{files_changed_text}\n"
                    )
                    
                    # Send to Telegram
                    result = send_message_to_telegram(message)
                    print(result)  # Check if the message was successfully sent
                    
                    # Mark the commit as posted
                    if result and result.get('ok'):
                        mark_commit_as_posted(commit_sha)

# Run the main function
if __name__ == "__main__":
    update_telegram_with_github_activity()
