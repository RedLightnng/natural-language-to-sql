import tkinter as tk
from tkinter import ttk
import requests
import mysql.connector
import re

# main class for the application.
class SQLGeneratorApp:
    # UI
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Query Generator")

        self.db_label = ttk.Label(root, text="Database Name:")
        self.db_label.pack(pady=10)

        self.db_entry = ttk.Entry(root, width=30)
        self.db_entry.pack(pady=10)

        self.user_label = ttk.Label(root, text="Database User:")
        self.user_label.pack(pady=10)

        self.user_entry = ttk.Entry(root, width=30)
        self.user_entry.pack(pady=10)

        self.password_label = ttk.Label(root, text="Database Password:")
        self.password_label.pack(pady=10)

        self.password_entry = ttk.Entry(root, width=30, show="*")
        self.password_entry.pack(pady=10)

        self.input_label = ttk.Label(root, text="Enter a natural language query:")
        self.input_label.pack(pady=10)

        self.input_entry = ttk.Entry(root, width=50)
        self.input_entry.pack(pady=10)

        self.generate_button = ttk.Button(root, text="Generate SQL Query", command=self.generate_sql_query)
        self.generate_button.pack(pady=10)

        self.sql_output_label = ttk.Label(root, text="Generated SQL Query:")
        self.sql_output_label.pack(pady=10)

        self.sql_output_text = tk.Text(root, height=5, width=50)
        self.sql_output_text.pack(pady=10)

        self.status_label = ttk.Label(root, text="Status:")
        self.status_label.pack(pady=10)

        self.status_button = ttk.Button(root, text="Unknown", state=tk.DISABLED)
        self.status_button.pack(pady=10)


    # gets user inputs from TKinter and calls the OpenAI key to send the query as a prompt
    def generate_sql_query(self):
        # Get user inputs
        db_name = self.db_entry.get()
        db_user = self.user_entry.get()
        db_password = self.password_entry.get()
        user_input = self.input_entry.get()

        openai_url = "https://UwUYourURLHere.com"  # Replace with your reverse proxy URL
        openai_api_key = "UwU-YourKeyHere-UwU"  # Replace with your OpenAI API key

        headers = {
            "Authorization": "Bearer PLACEHOLDER", #Replace with the approrpiate header
            "Content-Type": "application/json",
        }

        # main prompt for the openAI API
        payload = {
            "model": "pai-001-light",
            "prompt": f"request : {user_input}. \n Fulfill the request by providing MySQL code for it. only provide the code required, in ``` CODE ``` format. do not create a database, do not explain and do not include any header or comments in the code. Only the code is required.",
            "max_tokens": 500,
        }

        # get the respnse from the API and and print the original + the filtered response separated with ########

        try:
            response = requests.post(openai_url, json=payload, headers=headers)
            response.raise_for_status()
            generated_sql_query = response.json()["choices"][0]["text"].strip()
            print(generated_sql_query)
            print("#################################################################################################################")

            # markdown checks to filter out ``` 
            match4 = re.search(r'``` CODE(.+?)```', generated_sql_query, re.DOTALL)
            if match4:
                generated_sql_query = match4.group(1)
            else:
                match1 = re.search(r'```sql(.+?)```', generated_sql_query, re.DOTALL)
                if match1:
                    generated_sql_query = match1.group(1)
                else:
                    match2 = re.search(r'```(.+?)```', generated_sql_query, re.DOTALL)
                    if match2:
                        generated_sql_query = match2.group(1)
                    else:
                        match3 = re.search(r'```mysql(.+?)```', generated_sql_query, re.DOTALL)
                        if match3:
                            generated_sql_query = match3.group(1)

            generated_sql_query = generated_sql_query
            print(generated_sql_query)
            # Display the generated SQL query
            self.sql_output_text.delete(1.0, tk.END)
            self.sql_output_text.insert(tk.END, generated_sql_query)

            self.execute_sql_query(db_name, db_user, db_password, generated_sql_query)

        except requests.exceptions.RequestException as e:
            # Display an error message for OpenAI API request failure
            self.sql_output_text.delete(1.0, tk.END)
            self.sql_output_text.insert(tk.END, f"Error generating SQL query: {e}")

            # Update status button
            self.status_button["text"] = "Error"
            self.status_button["state"] = tk.NORMAL
            self.status_button.configure(style="Error.TButton")

        except KeyError:
            # Handle missing key in JSON response (e.g., choices or text)
            self.sql_output_text.delete(1.0, tk.END)
            self.sql_output_text.insert(tk.END, "Error parsing OpenAI response")

            # Update status button
            self.status_button["text"] = "Error"
            self.status_button["state"] = tk.NORMAL
            self.status_button.configure(style="Error.TButton")

    def execute_sql_query(self,db_name, db_user, db_password, sql_query):
    # Connect to the MySQL database
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user=db_user,
                password=db_password,
                database=db_name
            )

            cursor = connection.cursor()

            # Split the queries and execute them one by one
            queries = sql_query.split(';')
            for query in queries:
                if query.strip():  # Check if the query is not an empty string
                    cursor.execute(query)

            # Commit the changes
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()
            # Update status button for success
            self.status_button["text"] = "Success"
            self.status_button["state"] = tk.NORMAL
            self.status_button.configure(style="Success.TButton")

        except mysql.connector.Error as e:
            # Handle MySQL errors
            error_message = f"Error executing SQL query: {e}"

            self.sql_output_text.delete(1.0, tk.END)
            self.sql_output_text.insert(tk.END, error_message)

            # Update status button for error
            self.status_button["text"] = "Error"
            self.status_button["state"] = tk.NORMAL
            self.status_button.configure(style="Error.TButton")

if __name__ == "__main__":
    root = tk.Tk()

    # Define styles for the status button
    style = ttk.Style()
    style.configure("Success.TButton", foreground="green")
    style.configure("Error.TButton", foreground="red")

    app = SQLGeneratorApp(root)
    root.mainloop()