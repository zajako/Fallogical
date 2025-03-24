#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    # Start ollama in the background
    ollama serve &
    # Give it some time to start up
    sleep 5
else
    echo "Ollama service is already running."
fi

# List available models
echo "Available Ollama models:"
ollama list

# Start the Fallogical application
echo "Starting Fallogical application..."
python main.py 