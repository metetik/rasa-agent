sudo zerotier-one -d

source /home/codespace/daa-api-venv/bin/activate

cd /workspaces/rasa-agent/daa-api

# Start the API server
nohup fastapi run main.py &