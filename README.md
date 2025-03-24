# Fallogical

Fallogical is an application that listens to conversations, detects logical fallacies in real-time, and interrupts with explanations when fallacies are identified. It uses local Ollama models for AI processing.

## Features

- Real-time audio recording and transcription
- Logical fallacy detection using local Ollama AI models
- Voice interruptions with fallacy explanations
- Support for detecting common logical fallacies like ad hominem, straw man, appeal to authority, etc.

## Requirements

- Python 3.8+
- Ollama installed and running on your system
- Microphone for audio input
- Speakers for audio output

## Setup

1. Clone this repository
2. Install Ollama if you haven't already:
   - Visit [ollama.com](https://ollama.com/) for installation instructions
   - For macOS: `brew install ollama`
3. Pull a language model (if you don't have any already):
   - `ollama pull llama3.2` (or another model of your choice)
4. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

You can run the application with the provided startup script:

```
./start_fallogical.sh
```

This script will:
1. Activate the virtual environment
2. Make sure Ollama is running
3. List available models
4. Start the Fallogical application

Alternatively, you can run it manually:

```
source venv/bin/activate
python main.py
```

## Testing Fallacy Detection

To test the fallacy detection without using a microphone, you can run:

```
python test_fallacy_detection.py [model_name]
```

Where `[model_name]` is optional and defaults to `llama3.2`. The script will run through several example statements that contain logical fallacies and show how the AI identifies them.

## Customizing the Model

You can use a different Ollama model by editing the last line in `main.py`:

```python
app = FallogicalApp(model_name="your-model-name")
```

Available models can be checked with:

```
ollama list
```

## How it Works

1. The application continuously records audio from your microphone
2. The audio is transcribed to text using local speech recognition
3. The transcribed text is analyzed for logical fallacies using your local Ollama model
4. If a fallacy is detected, the application interrupts the conversation with a voice explanation

## Note

This application requires an active internet connection for the transcription and AI analysis services. 