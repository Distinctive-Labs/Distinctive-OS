import os
import json

class DOS:
    def __init__(self):
        print("Welcome to Distinctive Operating System (DOS)")
        self.user_file = 'users.json'
        self.current_user = None
        self.create_user_file()
        self.start()

    def create_user_file(self):
        """Create the users.json file if it doesn't exist."""
        if not os.path.exists(self.user_file):
            with open(self.user_file, 'w') as file:
                json.dump([], file)  # Initialize with an empty user list
            print(f"Created user file: {self.user_file}")

    def start(self):
        while True:
            command = input(self.get_prompt())
            self.process_command(command)

    def get_prompt(self):
        """Return the prompt string based on the current user."""
        if self.current_user:
            return f"{self.current_user}@DOS> "
        else:
            return "guest@DOS> "

    def process_command(self, command):
        args = command.split()
        if len(args) == 0:
            return
        cmd = args[0].lower()

        if cmd == "exit":
            print("Exiting DOS...")
            exit()
        elif cmd == "login" and len(args) > 2:
            self.login(args[1], args[2])
        elif cmd == "logout":
            self.logout()
        elif cmd == "change_user" and len(args) > 2:
            self.change_user(args[1], args[2])
        elif cmd == "status":
            self.status()
        elif cmd == "list":
            self.list_files()
        elif cmd == "open" and len(args) > 1:
            self.open_file(args[1])
        elif cmd == "edit" and len(args) > 1:
            self.edit_file(args[1])
        elif cmd == "create" and len(args) > 1:
            self.create_file(args[1])
        elif cmd == "delete" and len(args) > 1:
            self.delete_file(args[1])
        elif cmd == "rename" and len(args) > 2:
            self.rename_file(args[1], args[2])
        elif cmd == "run" and len(args) > 1:
            self.run_script(args[1])
        elif cmd == "add_user" and len(args) > 2:
            self.add_user(args[1], args[2])  # username and password
        elif cmd == "del_user" and len(args) > 1:
            self.delete_user(args[1])
        elif cmd == "list_users":
            self.list_users()
        elif cmd == "help":
            self.show_help()
        else:
            print("Command not recognized. Type 'help' for a list of commands.")

    def list_files(self):
        files = os.listdir('.')
        print("Files in current directory:")
        for file in files:
            print(f"- {file}")

    def open_file(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                print(f"--- {filename} ---")
                print(content)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def edit_file(self, filename):
        print(f"Editing file: {filename}")
        content = input("Enter content (type 'SAVE' on a new line to save):\n")
        if content.strip().lower() == "save":
            with open(filename, 'w') as file:
                file.write(content)
                print(f"File '{filename}' saved.")
        else:
            print("Edit canceled. Content not saved.")

    def create_file(self, filename):
        with open(filename, 'w') as file:
            print(f"File '{filename}' created.")

    def delete_file(self, filename):
        try:
            os.remove(filename)
            print(f"File '{filename}' deleted.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def rename_file(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            print(f"File '{old_name}' renamed to '{new_name}'.")
        except FileNotFoundError:
            print(f"File '{old_name}' not found.")
        except Exception as e:
            print(f"Error renaming file: {e}")

    def run_script(self, script_name):
        try:
            with open(script_name, 'r') as file:
                code = file.read()
                exec(code)  # Execute the script code
        except FileNotFoundError:
            print(f"Script '{script_name}' not found.")
        except Exception as e:
            print(f"Error executing script: {e}")

    def add_user(self, username, password):
        users = self.load_users()
        if username not in [user['username'] for user in users]:
            users.append({'username': username, 'password': password})
            self.save_users(users)
            print(f"User '{username}' added.")
        else:
            print(f"User '{username}' already exists.")

    def delete_user(self, username):
        users = self.load_users()
        users = [user for user in users if user['username'] != username]
        self.save_users(users)
        print(f"User '{username}' deleted.")

    def list_users(self):
        users = self.load_users()
        print("Current users:")
        for user in users:
            print(f"- {user['username']}")

    def login(self, username, password):
        users = self.load_users()
        for user in users:
            if user['username'] == username:
                if user['password'] == password:
                    self.current_user = username
                    print(f"User '{username}' logged in.")
                    return
                else:
                    print("Incorrect password.")
                    return
        print(f"User '{username}' not found. Please add the user first.")

    def logout(self):
        if self.current_user:
            print(f"User '{self.current_user}' logged out.")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    def change_user(self, username, password):
        self.logout()  # Logout current user
        self.login(username, password)  # Login new user

    def status(self):
        if self.current_user:
            print(f"Current logged-in user: {self.current_user}")
        else:
            print("No user is currently logged in.")

    def load_users(self):
        try:
            with open(self.user_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_users(self, users):
        with open(self.user_file, 'w') as file:
            json.dump(users, file)

    def show_help(self):
        print("""        
        Available commands:
        - login [username] [password] : Log in as a specified user
        - logout                       : Log out of the current user session
        - change_user [username] [password] : Switch to a specified user
        - status                       : Show the current logged-in user
        - list                         : List files in the current directory
        - open [file]                  : Open a file
        - edit [file]                  : Edit a text file
        - create [file]                : Create a new text file
        - delete [file]                : Delete a specified file
        - rename [old_name] [new_name] : Rename a specified file
        - run [app]                    : Run a script
        - add_user [username] [password] : Add a new user with a password
        - del_user [username]           : Delete a specified user
        - list_users                    : List all current users
        - exit                          : Exit DOS
        - help                          : Show this help message
        """)

if __name__ == "__main__":
    DOS()
