import requests
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

def list_tokens(valid=None):
    endpoint = f"{base_url}/_synapse/admin/v1/registration_tokens"
    params = {}
    if valid is not None:
        params['valid'] = 'true' if valid else 'false'
    
    response = requests.get(endpoint, headers=get_headers(), params=params)
    if response.status_code == 200:
        tokens = response.json().get('registration_tokens', [])
        if tokens:
            print("Registration Tokens:")
            for token in tokens:
                print(f"Token: {token['token']}")
                print(f"  Uses Allowed: {token['uses_allowed']}")
                print(f"  Pending: {token['pending']}")
                print(f"  Completed: {token['completed']}")
                expiry_time = token.get('expiry_time')
                if expiry_time:
                    expiry_time = datetime.utcfromtimestamp(expiry_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  Expiry Time: {expiry_time}")
                print()
        else:
            print("No registration tokens found.")
    else:
        print(f"Failed to list tokens: {response.status_code}")
        print(response.json())

def query_token(token):
    endpoint = f"{base_url}/_synapse/admin/v1/registration_tokens/{token}"
    response = requests.get(endpoint, headers=get_headers())
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to query token: {response.status_code}")
        print(response.json())

def create_token():
    token = get_user_input("Enter token (leave blank for random): ", required=False)
    uses_allowed = get_user_input("Enter number of uses allowed (leave blank for unlimited): ", required=False)
    expiry_date_str = get_user_input("Enter expiry date (mm/dd/yyyy, leave blank for no expiry): ", required=False)
    length = get_user_input("Enter length of randomly generated token (leave blank for default 16): ", required=False)
    
    payload = {}
    if token:
        payload['token'] = token
    if uses_allowed:
        payload['uses_allowed'] = int(uses_allowed)
    if expiry_date_str:
        expiry_date = datetime.strptime(expiry_date_str, "%m/%d/%Y")
        payload['expiry_time'] = int(expiry_date.timestamp() * 1000)  # Convert to milliseconds
    if length:
        payload['length'] = int(length)

    endpoint = f"{base_url}/_synapse/admin/v1/registration_tokens/new"
    response = requests.post(endpoint, headers=get_headers(), json=payload)
    if response.status_code == 200:
        print("Token created successfully!")
        print(response.json())
    else:
        print(f"Failed to create token: {response.status_code}")
        print(response.json())

def update_token(token):
    uses_allowed = get_user_input("Enter new number of uses allowed (leave blank to keep unchanged): ", required=False)
    expiry_date_str = get_user_input("Enter new expiry date (mm/dd/yyyy, leave blank to keep unchanged): ", required=False)
    
    payload = {}
    if uses_allowed:
        payload['uses_allowed'] = int(uses_allowed)
    if expiry_date_str:
        expiry_date = datetime.strptime(expiry_date_str, "%m/%d/%Y")
        payload['expiry_time'] = int(expiry_date.timestamp() * 1000)  # Convert to milliseconds

    endpoint = f"{base_url}/_synapse/admin/v1/registration_tokens/{token}"
    response = requests.put(endpoint, headers=get_headers(), json=payload)
    if response.status_code == 200:
        print("Token updated successfully!")
        print(response.json())
    else:
        print(f"Failed to update token: {response.status_code}")
        print(response.json())

def delete_token(token):
    endpoint = f"{base_url}/_synapse/admin/v1/registration_tokens/{token}"
    response = requests.delete(endpoint, headers=get_headers())
    if response.status_code == 200:
        print("Token deleted successfully!")
    else:
        print(f"Failed to delete token: {response.status_code}")
        print(response.json())

def main():
    print("Registration Token Management Script")
    print("1. List all tokens")
    print("2. Query a single token")
    print("3. Create a new token")
    print("4. Update a token")
    print("5. Delete a token")
    choice = input("Select an option: ")
    
    if choice == '1':
        valid = get_user_input("Only list valid tokens? (true/false, leave blank for all): ", required=False)
        if valid.lower() == 'true':
            list_tokens(valid=True)
        elif valid.lower() == 'false':
            list_tokens(valid=False)
        else:
            list_tokens()
    elif choice == '2':
        token = get_user_input("Enter token: ")
        query_token(token)
    elif choice == '3':
        create_token()
    elif choice == '4':
        token = get_user_input("Enter token: ")
        update_token(token)
    elif choice == '5':
        token = get_user_input("Enter token: ")
        delete_token(token)
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
