#!/bin/bash

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Instructions for running the app
echo ""
echo "=== Setup Complete ==="
echo "To run Fallogical, use these commands:"
echo "source venv/bin/activate  # Activate the virtual environment (if not already activated)"
echo "python main.py            # Run the application"
echo ""
echo "Remember to set up your OpenAI API key in a .env file before running:"
echo "OPENAI_API_KEY=your_api_key_here" 