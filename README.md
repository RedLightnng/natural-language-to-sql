# Introduction
The SQL Generator App is a simple GUI application built with Python and Tkinter. It allows users to generate SQL queries using natural language prompts and provides the generated SQL code in a user-friendly interface.

# Features
- Input Fields: Collects information such as Database Name, Database User, Database Password, and a natural language query from the user.

- Generate SQL Query Button: Utilizes the OpenAI API to generate SQL queries based on the provided natural language query.

- Generated SQL Query Display: Displays the generated SQL query in a text box, or displays the error. (if any)

Status Button: Shows the status of the execution status at MySQL's end after a query has been generated.

# Dependencies
- Tkinter: Python's standard GUI (Graphical User Interface) package.

- Requests: Python HTTP library for making API requests.

- MySQL Connector: Python driver for MySQL databases.


# Usage
1. Enter the required database information in the provided input fields.

2. Input a natural language query in the designated field.

3. Click the "Generate SQL Query" button to obtain the corresponding SQL code.

4. View the generated SQL query in the text box.

Extra Notes:
  - if the status is unknown after executing a query and the generated window is empty, click on the generate button again.
  - sometimes the AI may glitch and use ``` plus a weird encoding. watch out for that and look for errors in the console.
  - be descriptive and specify the elements in the table and their types when trying to add a new instance to the table as the app will not remember previous context [WIP]

# Note
- Ensure that the MySQL server is running and accessible before attempting to execute SQL queries.

- Replace the OpenAI API key and reverse proxy URL(if any) with your own credentials.

# Plans
- add the ability to remember context and respond more efficiently.
- Make better UI with more functionality.
