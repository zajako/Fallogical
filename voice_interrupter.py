import os
import tempfile
from gtts import gTTS
import simpleaudio as sa
import threading
import wave
from pydub import AudioSegment

class VoiceInterrupter:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.is_speaking = False
        self._lock = threading.Lock()
        
    def interrupt(self, message):
        """
        Convert message to speech and play it out loud
        
        Args:
            message: Message to speak
        """
        # Check if already speaking
        with self._lock:
            if self.is_speaking:
                return
            self.is_speaking = True
        
        try:
            # Generate speech in a separate thread to not block the main thread
            threading.Thread(target=self._speak, args=(message,)).start()
        except Exception as e:
            print(f"Error during interruption: {e}")
            with self._lock:
                self.is_speaking = False
            
    def _speak(self, message):
        """
        Internal method to handle text-to-speech conversion and playback
        
        Args:
            message: Message to speak
        """
        try:
            # Create temporary files for the audio
            temp_mp3 = os.path.join(self.temp_dir, f"interrupt_{id(message)}.mp3")
            temp_wav = os.path.join(self.temp_dir, f"interrupt_{id(message)}.wav")
            
            # Convert text to speech (MP3 format)
            tts = gTTS(text=message, lang='en', slow=False)
            tts.save(temp_mp3)
            
            # Convert MP3 to WAV format for simpleaudio
            sound = AudioSegment.from_mp3(temp_mp3)
            sound.export(temp_wav, format="wav")
            
            # Play the speech
            print(f"INTERRUPTION: {message}")
            
            # Play using simpleaudio
            wave_obj = sa.WaveObject.from_wave_file(temp_wav)
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Wait until sound has finished playing
            
            # Clean up
            try:
                os.remove(temp_mp3)
                os.remove(temp_wav)
            except:
                pass
                
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
        finally:
            with self._lock:
                self.is_speaking = False 