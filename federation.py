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

    ordered_keys = ["destination", "retry_last_ts", "retry_interval", "failure_ts", "last_successful_stream_ordering"]
    other_keys = [k for k in data if k not in ordered_keys]

    formatted_entries = [format_entry(key, data.get(key, 'N/A')) for key in ordered_keys]
    formatted_entries += [format_entry(key, data[key]) for key in other_keys]

    print("\n".join(formatted_entries))

def list_destinations():
    endpoint = f"{base_url}/_synapse/admin/v1/federation/destinations"
    response = requests.get(endpoint, headers=get_headers())
    if response.status_code == 200:
        destinations = response.json().get('destinations', [])
        if destinations:
            print("Federation Destinations:")
            for destination in destinations:
                print_json(destination)
                print()
        else:
            print("No federation destinations found.")
    else:
        print(f"Failed to list destinations: {response.status_code}")
        print_json(response.json())

def query_destination(destination):
    endpoint = f"{base_url}/_synapse/admin/v1/federation/destinations/{destination}"
    response = requests.get(endpoint, headers=get_headers())
    if response.status_code == 200:
        print_json(response.json())
    else:
        print(f"Failed to query destination: {response.status_code}")
        print_json(response.json())

def get_destination_rooms(destination):
    endpoint = f"{base_url}/_synapse/admin/v1/federation/destinations/{destination}/rooms"
    response = requests.get(endpoint, headers=get_headers())
    if response.status_code == 200:
        rooms = response.json().get('rooms', [])
        if rooms:
            print(f"Rooms federating with {destination}:")
            for room in rooms:
                print_json(room)
                print()
        else:
            print(f"No rooms federating with {destination}.")
    else:
        print(f"Failed to get destination rooms: {response.status_code}")
        print_json(response.json())

def reset_connection(destination):
    endpoint = f"{base_url}/_synapse/admin/v1/federation/destinations/{destination}/reset_connection"
    response = requests.post(endpoint, headers=get_headers(), json={})
    if response.status_code == 200:
        print("Connection reset successfully!")
    else:
        print(f"Failed to reset connection: {response.status_code}")
        print_json(response.json())

def main():
    while True:
        print("\nFederation Management Script")
        print("1. List all destinations")
        print("2. Query specific destination details")
        print("3. Get rooms federating with a specific destination")
        print("4. Reset connection timeout for a specific destination")
        print("5. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            list_destinations()
        elif choice == '2':
            destination = get_user_input("Enter destination: ")
            query_destination(destination)
        elif choice == '3':
            destination = get_user_input("Enter destination: ")
            get_destination_rooms(destination)
        elif choice == '4':
            destination = get_user_input("Enter destination: ")
            reset_connection(destination)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
