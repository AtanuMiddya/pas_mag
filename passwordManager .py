import json
import base64
import os

FILE_NAME = "passwords.json"

def load_data():
    """
    Loads existing data from the JSON file. 
    Returns an empty dictionary if the file doesn't exist.
    """
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, ValueError):
            # Handle case where file exists but is empty/corrupt
            return {}
    return {}

def save_data(data):
    """
    Saves the dictionary to the JSON file with indentation for readability.
    """
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

def encode_password(password):
    """
    Converts a plain string into a Base64 encoded string.
    Note: This is obfuscation, not strong encryption!
    """
    password_bytes = password.encode("utf-8")
    base64_bytes = base64.b64encode(password_bytes)
    return base64_bytes.decode("utf-8")

def decode_password(encoded_password):
    """
    Converts a Base64 string back into a readable string.
    """
    base64_bytes = encoded_password.encode("utf-8")
    password_bytes = base64.b64decode(base64_bytes)
    return password_bytes.decode("utf-8")

def add_password(data):
    service = input("Enter Service Name (e.g., Facebook): ").strip()
    if service in data:
        print("⚠️  Service already exists! Use 'Delete' to remove it first.")
        return

    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    
    # Store the password in encoded format
    encrypted_pw = encode_password(password)
    
    data[service] = {
        "username": username,
        "password": encrypted_pw
    }
    
    save_data(data)
    print("✅ Entry added successfully!")

def view_passwords(data):
    if not data:
        print("📭 No passwords saved yet.")
        return

    print("\n--- Saved Services ---")
    for service in data:
        print(f"- {service}")
    print("----------------------")

def search_password(data):
    service = input("Enter Service Name to search: ").strip()
    
    if service in data:
        creds = data[service]
        # Decode the password before showing it to the user
        real_password = decode_password(creds["password"])
        
        print(f"\n🔍 {service} Account:")
        print(f"   Username: {creds['username']}")
        print(f"   Password: {real_password}")
    else:
        print("❌ Service not found.")

def delete_password(data):
    service = input("Enter Service Name to delete: ").strip()
    
    if service in data:
        del data[service]
        save_data(data)
        print("🗑️  Entry deleted.")
    else:
        print("❌ Service not found.")

def main():
    data = load_data()
    
    while True:
        print("\n🔐 PASSWORD MANAGER MENU")
        print("1. Add Password")
        print("2. View All Services")
        print("3. Search Password")
        print("4. Delete Password")
        print("5. Exit")
        
        choice = input("Enter option: ")
        
        if choice == '1':
            add_password(data)
        elif choice == '2':
            view_passwords(data)
        elif choice == '3':
            search_password(data)
        elif choice == '4':
            delete_password(data)
        elif choice == '5':
            print("👋 Exiting Password Manager.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()