### Step 1: Prepare the Server

1. **Update and Upgrade the System:**
    
    ```bash
    sudo apt update && sudo apt upgrade
    ```
    
2. **Install Necessary Packages:**
    
    ```bash
    sudo apt install -y lsb-release wget apt-transport-https nano net-tools ufw
    ```
    
3. Configure DNS Settings:
    
    Using your domain provider create 2 A records for:
    
    *matrix.domain.com*
    
    *domain.com*
    

### Step 2: Install PostgreSQL

1. **Install PostgreSQL and Dependencies:**
    
    ```bash
    sudo apt install postgresql postgresql-contrib libpq5 libpq-dev
    ```
    
2. **Configure PostgreSQL:**
    
    ```bash
    sudo -u postgres bash
    
    createuser --pwprompt synapse_user
    createdb --encoding=UTF8 --locale=C --template=template0 --owner=synapse_user synapse
    
    exit
    ```
    
    Edit the PostgreSQL configuration files as needed:
    
    ```bash
    sudo nano /etc/postgresql/14/main/postgresql.conf
    
    add:
    listen_addresses = 'localhost'          # what IP address(es) to listen on;
    
    sudo nano /etc/postgresql/14/main/pg_hba.conf
    
    add:
    local   synapse         synapse_user                            md5
    ```
    

### Step 3: Install Matrix

1. **Add Matrix Repository Key:**
    
    ```bash
    sudo wget -O /usr/share/keyrings/matrix-org-archive-keyring.gpg <https://packages.matrix.org/debian/matrix-org-archive-keyring.gpg>
    ```
    
2. **Add Matrix Repository:**
    
    ```bash
    echo "deb [signed-by=/usr/share/keyrings/matrix-org-archive-keyring.gpg] <https://packages.matrix.org/debian/> $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/matrix-org.list
    sudo apt update
    ```
    
3. **Install Matrix Synapse:**
    
    ```bash
    sudo apt install matrix-synapse-py3
    ```
    
4. **Enable and Start Matrix Synapse:**
    
    ```bash
    sudo systemctl enable matrix-synapse
    sudo systemctl start matrix-synapse
    sudo systemctl status matrix-synapse
    ```
    
5. **Configure Matrix Synapse:**
Edit the `homeserver.yaml` file as needed:
    
    ```bash
    sudo nano /etc/matrix-synapse/homeserver.yaml
    ```
    

### Step 4: Install Caddy

1. **Add Caddy Repository Key:**
    
    ```bash
    curl -1sLf '<https://dl.cloudsmith.io/public/caddy/stable/gpg.key>' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    ```
    
2. **Add Caddy Repository:**
    
    ```bash
    curl -1sLf '<https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt>' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
    sudo apt update
    ```
    
3. **Install Caddy:**
    
    ```bash
    sudo apt install caddy
    ```
    
4. **Configure Caddy:**
Create or edit the Caddyfile as needed:
    
    ```bash
    sudo nano /etc/caddy/Caddyfile
    ```
    

### Step 5: Install a Local Firewall

1. **Configure UFW (Uncomplicated Firewall):**
    
    ```bash
    sudo ufw allow 22
    sudo ufw allow 80
    sudo ufw allow 443
    sudo ufw allow 8448
    sudo ufw enable
    sudo ufw status
    
    ```
    

### Step 6: Final Steps

1. **Restart Services:**
    
    ```bash
    sudo systemctl restart matrix-synapse.service
    sudo systemctl restart postgresql.service
    sudo systemctl restart caddy.service
    
    ```
    

### Verification

1. **Verify Service Status:**
    
    ```bash
    sudo systemctl status matrix-synapse
    sudo systemctl status postgresql
    sudo systemctl status caddy
    
    ```
    
2. **Test Matrix Synapse Connectivity:**
    
    ```bash
    curl -v <http://matrix.your.domain:8448>
    curl -v <https://matrix.your.domain:8448>
    
    ```
    
3. **Reboot the Server:**
    
    ```bash
    sudo reboot
    
    ```
