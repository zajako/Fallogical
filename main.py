import os
import time
import threading
import signal
import sys
from dotenv import load_dotenv
import ollama
from audio_transcriber import AudioTranscriber
from fallacy_detector import FallacyDetector
from voice_interrupter import VoiceInterrupter

load_dotenv()

class FallogicalApp:
    def __init__(self, model_name="llama3.2"):
        self.transcriber = AudioTranscriber()
        self.fallacy_detector = FallacyDetector(model_name=model_name)
        self.interrupter = VoiceInterrupter()
        self.running = False
        self.recent_texts = []
        self.lock = threading.Lock()
        self.model_name = model_name
        
    def start(self):
        """Start the Fallogical application"""
        self.running = True
        
        # Set up signal handling for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        
        print("\n=== Fallogical - Logical Fallacy Detector (Ollama Version) ===")
        print(f"Using local Ollama model: {self.model_name}")
        print("This application listens to conversations and interrupts when it detects logical fallacies.")
        print("Press Ctrl+C to exit at any time.")
        
        # Check if Ollama is running and the model is available
        try:
            print("Checking Ollama availability...")
            models = ollama.list()
            model_names = [model['name'].split(':')[0] for model in models['models']]
            
            if self.model_name not in model_names:
                closest_match = next((m for m in model_names if self.model_name in m), None)
                if closest_match:
                    print(f"Model '{self.model_name}' not found exactly, using '{closest_match}' instead.")
                    self.model_name = closest_match
                    self.fallacy_detector.model_name = closest_match
                else:
                    print(f"Warning: Model '{self.model_name}' not found. Available models:")
                    for model in model_names:
                        print(f"  - {model}")
                    print(f"Proceeding with '{self.model_name}' anyway. If it fails, try using one of the above models.")
        except Exception as e:
            print(f"Warning: Could not connect to Ollama: {e}")
            print("Make sure Ollama is running on your system.")
        
        # Start the transcription process in a separate thread
        threading.Thread(target=self.transcriber.start_listening, args=(self.process_text,)).start()
        
        try:
            # Keep the main thread alive
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.shutdown()
            
    def process_text(self, text):
        """
        Process transcribed text to detect fallacies
        
        Args:
            text: Transcribed text from the audio
        """
        with self.lock:
            # Add text to recent texts
            self.recent_texts.append(text)
            # Keep only the last 5 texts to maintain context but limit API usage
            if len(self.recent_texts) > 5:
                self.recent_texts.pop(0)
            
            # Combine recent texts for context
            combined_text = " ".join(self.recent_texts)
        
        # Analyze the text for fallacies
        fallacy_result = self.fallacy_detector.analyze_text(combined_text)
        
        if fallacy_result:
            # Construct interruption message
            interruption = f"Fallacy detected: {fallacy_result['fallacy'].title()}. {fallacy_result['explanation']}. Example from the conversation: {fallacy_result['example']}"
            
            # Interrupt the conversation
            self.interrupter.interrupt(interruption)
    
    def shutdown(self):
        """Shut down the application gracefully"""
        print("\nShutting down Fallogical...")
        self.running = False
        self.transcriber.stop_listening()
        
    def handle_shutdown(self, signum, frame):
        """Signal handler for graceful shutdown"""
        self.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    # You can change the model name here to use a different Ollama model
    app = FallogicalApp(model_name="llama3.2")
    app.start() 