#!/bin/bash
# Chicham - AWS EC2 deployment bootstrap script
# This runs as EC2 user data on instance launch

set -e

# Install dependencies
yum update -y
yum install -y python3.11 python3.11-pip git

# Clone the repo
cd /home/ec2-user
git clone https://github.com/ratalie/aws-nova.git
cd aws-nova

# Install Python dependencies
python3.11 -m pip install -r requirements.txt

# Create systemd service for Streamlit
cat > /etc/systemd/system/chicham.service << 'EOF'
[Unit]
Description=Chicham Streamlit App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/aws-nova
ExecStart=/usr/local/bin/streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0
Restart=always
Environment=AWS_DEFAULT_REGION=us-east-1
Environment=PYTHONPATH=/home/ec2-user/aws-nova

[Install]
WantedBy=multi-user.target
EOF

chown -R ec2-user:ec2-user /home/ec2-user/aws-nova
systemctl daemon-reload
systemctl enable chicham
systemctl start chicham
