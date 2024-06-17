import requests
import json
from datetime import datetime

# Function to read the configuration file
def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split('=')
            config[key] = value
    return config

# Read configuration from the file
config = read_config('config.txt')
base_url = config.get('admin_url')
access_token = config.get('access_token')

def get_headers():
    return {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

def get_user_input(prompt, required=True):
    while True:
        value = input(prompt)
        if value or not required:
            return value

def print_json(data):
    def format_entry(key, value):
        return f"\033[1m{key}:\033[0m {value}"

    ordered_keys = ["displayname", "name", "admin", "approved", "locked"]
    other_keys = [k for k in data if k not in ordered_keys]

    formatted_entries = [format_entry(key, data.get(key, 'N/A')) for key in ordered_keys]
    formatted_entries += [format_entry(key, data[key]) for key in other_keys]

    print("\n".join(formatted_entries))

def list_users():
    endpoint = f"{base_url}/_synapse/admin/v2/users"
    response = requests.get(endpoint, headers=get_headers())
    if response.status_code == 200:
        users = response.json().get('users', [])
        if users:
            print("User List:")
            for user in users:
                print_json(user)
                print()
        else:
            print("No users found.")
    else:
        print(f"Failed to list users: {response.status_code}")
        print_json(response.json())

def query_user(user_id):
    endpoint = f"{base_url}/_synapse/admin/v2/users/{user_id}"
    response = requests.get(endpoint, headers=get_headers())
    if response.status_code == 200:
        print_json(response.json())
    else:
        print(f"Failed to query user: {response.status_code}")
        print_json(response.json())

def create_or_modify_user(user_id):
    password = get_user_input("Enter password (leave blank to keep unchanged): ", required=False)
    displayname = get_user_input("Enter displayname (leave blank to keep unchanged): ", required=False)
    avatar_url = get_user_input("Enter avatar_url (leave blank to keep unchanged): ", required=False)
    admin = get_user_input("Set as admin (true/false, leave blank to keep unchanged): ", required=False)
    deactivated = get_user_input("Deactivate user (true/false, leave blank to keep unchanged): ", required=False)
    
    payload = {}
    if password:
        payload['password'] = password
    if displayname:
        payload['displayname'] = displayname
    if avatar_url:
        payload['avatar_url'] = avatar_url
    if admin:
        payload['admin'] = admin.lower() == 'true'
    if deactivated:
        payload['deactivated'] = deactivated.lower() == 'true'

    endpoint = f"{base_url}/_synapse/admin/v2/users/{user_id}"
    response = requests.put(endpoint, headers=get_headers(), json=payload)
    if response.status_code in [200, 201]:
        print("User created/modified successfully!")
        print_json(response.json())
    else:
        print(f"Failed to create/modify user: {response.status_code}")
        print_json(response.json())

def deactivate_user(user_id):
    endpoint = f"{base_url}/_synapse/admin/v1/deactivate/{user_id}"
    erase = get_user_input("Erase user data (true/false, leave blank for false): ", required=False)
    payload = {
        "erase": erase.lower() == 'true' if erase else False
    }
    response = requests.post(endpoint, headers=get_headers(), json=payload)
    if response.status_code == 200:
        print("User deactivated successfully!")
    else:
        print(f"Failed to deactivate user: {response.status_code}")
        print_json(response.json())

def reset_password(user_id):
    new_password = get_user_input("Enter new password: ")
    logout_devices = get_user_input("Logout devices (true/false, leave blank for true): ", required=False)
    payload = {
        "new_password": new_password,
        "logout_devices": logout_devices.lower() != 'false' if logout_devices else True
    }
    endpoint = f"{base_url}/_synapse/admin/v1/reset_password/{user_id}"
    response = requests.post(endpoint, headers=get_headers(), json=payload)
    if response.status_code == 200:
        print("Password reset successfully!")
    else:
        print(f"Failed to reset password: {response.status_code}")
        print_json(response.json())

def main():
    while True:
        print("\nUser Management Script")
        print("1. List users")
        print("2. Query user account")
        print("3. Create or modify user account")
        print("4. Deactivate user account")
        print("5. Reset user password")
        print("6. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            list_users()
        elif choice == '2':
            user_id = get_user_input("Enter user ID: ")
            query_user(user_id)
        elif choice == '3':
            user_id = get_user_input("Enter user ID: ")
            create_or_modify_user(user_id)
        elif choice == '4':
            user_id = get_user_input("Enter user ID: ")
            deactivate_user(user_id)
        elif choice == '5':
            user_id = get_user_input("Enter user ID: ")
            reset_password(user_id)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
