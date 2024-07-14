# SQL Chatbot

A Streamlit-based chatbot powered by Ollama & Open Source LLM for SQL queries.

## Features

- Natural language to SQL query conversion
- Read-only query execution for security
- Interactive chat interface
- Supports multiple database tables

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Ollama

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sql-chatbot.git
   cd sql-chatbot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_NAME=your_db_name
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit.

3. Start chatting with the bot to query your SQL database.
