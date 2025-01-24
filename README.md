# SQL Database Chatbot

## Overview
The SQL Database Chatbot is a user-friendly AI assistant designed to interact with a SQL Server database. It leverages the power of large language models (LLMs) and embeddings to understand natural language queries, generate SQL queries, execute them, and provide clear and concise answers based on the data available in the database.

## Features
Natural Language Understanding: The chatbot can understand and respond to natural language queries.
SQL Query Generation: Automatically generates SQL queries based on user input.
Error Handling: Provides detailed explanations for errors and suggests corrections.
User-Friendly Interface: Built with Streamlit for an intuitive and interactive user experience.
Setup
Prerequisites
Python 3.8 or later
SQL Server database
Ollama LLM and Embedding models
Installation

## Clone the repository:

git clone https://github.com/your-username/sql-database-chatbot.git
cd sql-database-chatbot

## Install the required dependencies:
pip install -r requirements.txt
Configure the database connection:

## Update the conn_str variable in the script with your SQL Server details:
server = "your_server_ip"
database = "your_database_name"
username = "your_username"
password = "your_password"

## Run the Streamlit app:
streamlit run app.py

## Usage
Open the Streamlit app in your web browser.
Enter your query in the chat input box.
Receive the response from the chatbot.

## Example
User Input:
What is the total number of records in the 'Customers' table?
Chatbot Response:
The total number of records in the 'Customers' table is 1000.
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or issues, please open an issue on the GitHub repository or contact the maintainer directly.
