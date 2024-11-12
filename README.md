Telegram Channel Monitor

A Python-based tool to monitor Telegram channels, automatically join based on specified keywords, collect links from joined channels, and analyze messages for suspicious content. This project is built using Telethon for interaction with the Telegram API and is designed to identify potentially harmful or malicious activity within Telegram channels.

Features
Channel Joining: Automatically joins channels based on predefined keywords.
Link Collection: Collects links shared within joined channels.
Message Analysis: Analyzes messages for suspicious keywords and flags them if necessary.
Data Storage: Stores joined channels and collected links in SQLite databases.
Project Structure
bash
Copy code
Project/
├── src/
│   ├── joinchannel.py        # Module to join channels based on keywords
│   ├── collect_links.py      # Module to collect links from joined channels
│   ├── analyze_messages.py   # Module to scan messages for suspicious content
│   ├── config.py             # Configuration file for setting parameters
│   ├── db_utils.py           # Utility functions for database management
│   ├── sus_keys.csv          # CSV file containing suspicious keywords
├── joined_channel.db         # Database to store joined channel details
├── links_collected.db        # Database to store collected links
├── .env                      # Environment variables for Telegram API credentials
└── README.md                 # Project documentation
Setup and Installation
Prerequisites
Python 3.7+
A Telegram API account to get API_ID and API_HASH
Telethon package for Telegram interaction
dotenv package for environment variable management
Installation
Clone the repository

bash
Copy code
git clone https://github.com/yourusername/Telegram-Channel-Monitor.git
cd Telegram-Channel-Monitor
Create and activate a virtual environment

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
Configure API credentials

Create a .env file in the project root with the following variables:
makefile
Copy code
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_NAME=your_session_name
Add Suspicious Keywords

Update the sus_keys.csv file with keywords for monitoring suspicious activity.
Running the Project
Joining Channels

bash
Copy code
python src/joinchannel.py
Collecting Links

bash
Copy code
python src/collect_links.py
Analyzing Messages

bash
Copy code
python src/analyze_messages.py
Configuration
Update configuration in config.py to customize:

Maximum number of links per channel
Database paths for storing channel and link information
Database Structure
joined_channel.db: Stores details of joined channels (ID, name, access hash)
links_collected.db: Stores collected links from channels
Future Enhancements
Add automated alerting for flagged content
Generate reports for suspicious channels
Build a simple UI to manage keywords and view flagged content
Contributing
Fork the repository
Create a new branch (git checkout -b feature-branch)
Commit your changes (git commit -m "Add new feature")
Push to the branch (git push origin feature-branch)
Create a Pull Request
License
This project is licensed under the MIT License.#   T e l e g r a m - C h a n n e l - M o n i t o r  
 