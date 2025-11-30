import json
import os
import sys

# Configuration: Paths to the JSON files
# Assumes script is run from the project root or same level as 'data' folder
DATA_DIR = 'data'
TOOLS_DATA_FILE = os.path.join(DATA_DIR, 'tools_data.json')
TOOLS_ICONS_FILE = os.path.join(DATA_DIR, 'tools_icons.json')

class ToolManager:
    def __init__(self):
        self.tools_data = {}
        self.tools_icons = {}
        self.check_environment()
        self.load_data()

    def check_environment(self):
        """Ensures the data directory exists."""
        if not os.path.exists(DATA_DIR):
            print(f"Error: Directory '{DATA_DIR}' not found.")
            print("Please run this script from the root of the repository where the 'data' folder exists.")
            sys.exit(1)

    def load_json_file(self, filepath):
        """Reads a JSON file with robust error handling."""
        if not os.path.exists(filepath):
            print(f"Warning: '{filepath}' not found. A new one will be created upon saving.")
            return {}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"\nCRITICAL ERROR: '{filepath}' contains invalid JSON.")
            print(f"Details: {e}")
            print("Fix the file manually before running this script to prevent data loss.")
            sys.exit(1)
        except PermissionError:
            print(f"\nCRITICAL ERROR: No permission to read '{filepath}'.")
            sys.exit(1)
        except Exception as e:
            print(f"\nUnexpected error reading '{filepath}': {e}")
            sys.exit(1)

    def load_data(self):
        """Loads both data files into memory."""
        print("Loading data files...")
        self.tools_data = self.load_json_file(TOOLS_DATA_FILE)
        self.tools_icons = self.load_json_file(TOOLS_ICONS_FILE)
        print("Data loaded successfully.\n")

    def save_json_file(self, filepath, data):
        """Writes data to a JSON file with error handling."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4) # 4 spaces indent as per your style
                # Add a newline at end of file for good measure
                f.write('\n')
            print(f"Successfully saved to '{filepath}'.")
        except PermissionError:
            print(f"Error: Permission denied writing to '{filepath}'. Check file permissions.")
        except Exception as e:
            print(f"Error: Failed to save '{filepath}'. Details: {e}")

    def save_all(self):
        """Saves both data structures."""
        self.save_json_file(TOOLS_DATA_FILE, self.tools_data)
        self.save_json_file(TOOLS_ICONS_FILE, self.tools_icons)

    def get_input(self, prompt, required=True):
        """Helper to get user input with optional validation."""
        while True:
            value = input(prompt).strip()
            if required and not value:
                print("Error: This field cannot be empty.")
                continue
            return value

    def list_categories(self):
        """Returns a list of current categories."""
        return list(self.tools_data.keys())

    def add_category(self):
        print("\n--- Add New Category ---")
        name = self.get_input("Enter Category Name (e.g., 'Converters'): ")

        if name in self.tools_data:
            print(f"Error: Category '{name}' already exists.")
            return

        icon = self.get_input(f"Enter Bootstrap Icon Class for '{name}' (e.g., 'bi-gear'): ")

        # Initialize in data structures
        self.tools_data[name] = []
        self.tools_icons[name] = icon

        print(f"Category '{name}' added pending save.")
        self.save_all()

    def add_tool(self):
        print("\n--- Add New Tool ---")
        categories = self.list_categories()

        if not categories:
            print("No categories found. Please add a category first.")
            return

        print("Available Categories:")
        for idx, cat in enumerate(categories):
            print(f"{idx + 1}. {cat}")

        # Select Category
        while True:
            selection = self.get_input("Select Category Number: ")
            if not selection.isdigit():
                print("Please enter a number.")
                continue
            idx = int(selection) - 1
            if 0 <= idx < len(categories):
                selected_cat = categories[idx]
                break
            print("Invalid selection. Try again.")

        print(f"\nAdding tool to category: '{selected_cat}'")

        # Gather Tool Data
        t_name = self.get_input("Tool Name: ")
        t_desc = self.get_input("Description: ")

        # Auto-guess URL based on category and tool name
        # Heuristic: tools/{category_lower}/{tool_name_snake_case}.html
        default_url = ""
        try:
            safe_cat = selected_cat.lower().replace(" ", "_")
            safe_name = t_name.lower().replace(" ", "_")
            default_url = f"tools/{safe_cat}/{safe_name}.html"
        except:
            pass

        t_url_input = self.get_input(f"URL (relative path) [Press Enter for '{default_url}']: ", required=False)

        if not t_url_input and default_url:
            t_url = default_url
        elif t_url_input:
            t_url = t_url_input
        else:
            print("Error: URL cannot be empty if auto-guess failed.")
            return # Or loop back, but simple return is safer for now

        # Determine Banner Image Path
        # Logic: Attempt to guess default banner path based on existing conventions
        # Convention seems to be: images/category_lower/filename_base.png
        # We will just ask the user, but provide a hint if possible.
        default_banner = ""
        try:
            # simple heuristic for suggestion
            base_name = os.path.splitext(os.path.basename(t_url))[0]
            cat_folder = selected_cat.lower()
            default_banner = f"images/{cat_folder}/{base_name}.png"
        except:
            pass

        t_banner = self.get_input(f"Banner Path [Press Enter for '{default_banner}']: ", required=False)
        if not t_banner and default_banner:
            t_banner = default_banner
        elif not t_banner:
             # Fallback if user entered nothing and we couldn't guess
             t_banner = "images/default.png"

        new_tool = {
            "name": t_name,
            "description": t_desc,
            "url": t_url,
            "banner": t_banner
        }

        self.tools_data[selected_cat].append(new_tool)
        print(f"Tool '{t_name}' added pending save.")
        self.save_all()

    def run(self):
        print("=======================================")
        print("   ASDK Toolkit Data Manager")
        print("=======================================")

        while True:
            print("\nMenu:")
            print("1. Add New Tool")
            print("2. Add New Category")
            print("3. Exit")

            choice = input("Enter choice (1-3): ").strip()

            if choice == '1':
                self.add_tool()
            elif choice == '2':
                self.add_category()
            elif choice == '3':
                print("Bye!")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    try:
        app = ToolManager()
        app.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Bye!")
        sys.exit(0)
