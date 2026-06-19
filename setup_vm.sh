#!/bin/bash

APP_DIR=/home/azureuser/real_estate_flask

# Create virtual environment and install dependencies
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service file
sudo tee /etc/systemd/system/realestate.service > /dev/null <<EOF
[Unit]
Description=Real Estate Flask App
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/real_estate_flask
Environment="DB_TYPE=mysql"
Environment="DB_HOST=dbserversai.mysql.database.azure.com"
Environment="DB_USER=azsqladmin"
Environment="DB_PASS=Saiteja@2002"
Environment="DB_NAME=real_estate"
ExecStart=/home/azureuser/real_estate_flask/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
sudo tee /etc/nginx/sites-available/realestate > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/realestate /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Start services
sudo systemctl daemon-reload
sudo systemctl enable realestate
sudo systemctl start realestate
sudo systemctl restart nginx

echo "Deployment complete! Visit http://52.185.187.11"
