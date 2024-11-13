# Telegram Automation Project

**A Python-based Telegram Automation Project**

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

This project automates interactions on Telegram, such as joining channels, collecting links, and analyzing chats for suspicious activity. It uses the **Telethon** library to interact with the Telegram API and offers functionalities useful for monitoring and research purposes.

## Features

- **Join Telegram Channels**: Automatically joins channels based on specified keywords.
- **Link Collection**: Collects up to a defined number of links from each joined channel.
- **Message Analysis**: Analyzes messages in each joined channel for suspicious keywords and flags them.


## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pratz10101/telegram-channel-monitor.git
   cd telegram-channel-monitor
   ```

2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project’s root directory:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   SESSION_NAME=your_session_name
   ```

## Usage

To run the entire automation workflow:

```bash
python src/main.py
```

- **main.py** will automatically:
  - Join channels based on keywords from `joinchannel.py`.
  - Collect links from joined channels via `collect_links.py`.
  - Analyze messages for suspicious content through `analyze_messages.py`.

## Configuration

- **Suspicious Keywords**: Modify `sus_keys.csv` to add or update keywords for detecting suspicious activity.
- **Database**: 
  - `joined_channel.db` stores information about joined channels.
  - `links_collected.db` stores collected links.
- **Limits**: The number of links per channel can be set in `config.py`.

## Contributing

Feel free to open issues, suggest improvements, or submit pull requests. Contributions are welcome and appreciated.

## License

This project is licensed under the [MIT License](LICENSE).
