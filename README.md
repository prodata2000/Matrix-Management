# Synapse Administration Scripts

This repository contains Python scripts to manage various aspects of a Synapse server. The scripts included are:

1. User Management Script
2. Token Management Script
3. Federation Management Script

## Prerequisites

- Python 3.x
- `requests` library (`pip install requests`)

## Setup

1. Clone this repository:
    ```sh
    git clone https://github.com/prodata2000/Matrix-Management.git
    cd Matrix-Management
    ```

2. Create a configuration file named `config.txt` with the following content:
    ```txt
    admin_url=http://localhost:8008
    access_token=YOUR_ACCESS_TOKEN
    ```

    Replace `http://localhost:8008` with the base URL of your Synapse server's Admin API and `YOUR_ACCESS_TOKEN` with your actual admin access token.

3. Ensure you have the `requests` library installed:
    ```sh
    pip install requests
    ```

## User Management Script

### Description

This script allows you to manage user accounts on your Synapse server. It supports listing users, querying user details, creating or modifying user accounts, deactivating accounts, and resetting user passwords.

### Usage

Run the script:
```sh
python user_management.py
```

Follow the on-screen menu to select an operation:

1. **List users**
2. **Query user account**
3. **Create or modify user account**
4. **Deactivate user account**
5. **Reset user password**
6. **Exit**

## Token Management Script

### Description

This script allows you to manage registration tokens on your Synapse server. It supports listing tokens, querying token details, creating new tokens, updating tokens, and deleting tokens.

### Usage

Run the script:
```sh
python token_management.py
```

Follow the on-screen menu to select an operation:

1. **List all tokens**
2. **Query a single token**
3. **Create a new token**
4. **Update a token**
5. **Delete a token**
6. **Exit**

## Federation Management Script

### Description

This script allows you to manage federation status with other homeservers on your Synapse server. It supports listing all destinations, querying specific destination details, getting rooms federating with a specific destination, and resetting the connection timeout for a specific destination.

### Usage

Run the script:
```sh
python federation_management.py
```

Follow the on-screen menu to select an operation:

1. **List all destinations**
2. **Query specific destination details**
3. **Get rooms federating with a specific destination**
4. **Reset connection timeout for a specific destination**
5. **Exit**

## Example Configuration File

Create a file named `config.txt` with the following content:
```txt
admin_url=http://localhost:8008
access_token=YOUR_ACCESS_TOKEN
```

Replace `http://localhost:8008` with the base URL of your Synapse server's Admin API and `YOUR_ACCESS_TOKEN` with your actual admin access token.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
```

This README provides a clear and detailed guide for setting up and using the three scripts, making it easy for users to understand how to manage their Synapse server.
