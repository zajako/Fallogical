import os
import tempfile
import time
import subprocess
import speech_recognition as sr
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

class AudioTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.temp_dir = tempfile.gettempdir()
        
    def start_listening(self, callback):
        """
        Start listening to audio input and transcribe it.
        
        Args:
            callback: Function to call with transcribed text
        """
        self.is_listening = True
        
        with sr.Microphone() as source:
            print("Calibrating for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Listening! Speak clearly into the microphone.")
            
            while self.is_listening:
                try:
                    # Record audio in chunks to allow for near real-time processing
                    audio_data = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                    # Save audio to temporary file
                    temp_file = os.path.join(self.temp_dir, f"audio_{int(time.time())}.wav")
                    with open(temp_file, "wb") as f:
                        f.write(audio_data.get_wav_data())
                    
                    # Transcribe using built-in recognizer with Google (fallback)
                    try:
                        # First try using the Google recognizer as a fallback
                        transcription = self.recognizer.recognize_google(audio_data)
                    except:
                        # If that fails, try the local transcription
                        transcription = self._transcribe_audio_local(temp_file)
                    
                    if transcription and transcription.strip():
                        print(f"Transcribed: {transcription}")
                        callback(transcription)
                    
                    # Clean up temp file
                    os.remove(temp_file)
                    
                except sr.WaitTimeoutError:
                    pass
                except Exception as e:
                    print(f"Error during transcription: {e}")
    
    def stop_listening(self):
        """Stop listening to audio input"""
        self.is_listening = False
        
    def _transcribe_audio_local(self, audio_file_path):
        """
        Transcribe audio file using built-in Speech Recognition
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            # Try to use a local file-based Speech Recognition method
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                
            # Try using Google's recognizer as the primary method
            try:
                return self.recognizer.recognize_google(audio)
            except:
                # Fallback to a more basic recognition if Google fails
                try:
                    return self.recognizer.recognize_sphinx(audio)
                except:
                    # Last resort, just say we couldn't transcribe it
                    return "Speech could not be transcribed"
                    
        except Exception as e:
            print(f"Error transcribing audio locally: {e}")
            return "" 