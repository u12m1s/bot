#!/bin/bash

# Try to find and activate a common virtual environment path
if [ -d "/opt/venv" ]; then
    source /opt/venv/bin/activate
elif [ -d "/usr/src/app/.venv" ]; then # Common for some Docker-based setups
    source /usr/src/app/.venv/bin/activate
elif [ -d "$HOME/.venv" ]; then # Another common path
    source $HOME/.venv/bin/activate
fi

# Check if a venv was activated, if not, proceed with system python3
if command -v python3 &>/dev/null; then
    echo "Using python3 from PATH."
    python3 setup_db.py
    python3 bot.py
else
    echo "python3 not found in PATH after venv activation attempts. This is unexpected."
    # Fallback (unlikely to work if python3 isn't found, but good for debugging)
    /usr/bin/python3 setup_db.py
    /usr/bin/python3 bot.py
fi