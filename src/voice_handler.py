"""Voice Handler with proper resource management"""
import whisper
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
from loguru import logger
from pathlib import Path
import atexit

from src.constants import MAX_RECORDING_DURATION, SAMPLE_RATE
from src.exceptions import VoiceInputError

class VoiceHandler:
    """Handle voice input/output with cleanup"""
    
    def __init__(self, config):
        self.config = config
        self.audio_dir = Path("data/audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        model_size = config.get("WHISPER_MODEL", "base")
        logger.info(f"Loading Whisper model: {model_size}...")
        self.whisper_model = whisper.load_model(model_size)
        logger.info("Whisper loaded")
        
        self.sample_rate = SAMPLE_RATE
        self.duration = MAX_RECORDING_DURATION
        
        # Register cleanup
        atexit.register(self.cleanup)
    
    async def listen(self) -> str:
        """Record and transcribe with error handling"""
        audio_path = self.audio_dir / "user_input.wav"
        
        try:
            print("Recording... (5 seconds)")
            
            audio_data = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )
            sd.wait()
            print("Processing...")
            
            sf.write(audio_path, audio_data, self.sample_rate)
            result = self.whisper_model.transcribe(
                str(audio_path),
                language='en',
                fp16=False
            )
            
            transcription = result["text"].strip()
            logger.info(f"Transcribed: {transcription}")
            
            return transcription
            
        except Exception as e:
            logger.error(f"Voice input error: {e}")
            raise VoiceInputError(f"Failed to process voice input: {str(e)}")
        finally:
            # Cleanup temp file
            if audio_path.exists():
                try:
                    audio_path.unlink()
                except:
                    pass
    
    async def speak(self, text: str):
        """Convert text to speech with cleanup"""
        audio_path = self.audio_dir / "agent_response.mp3"
        
        try:
            print("Speaking...")
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(audio_path))
            
            audio = AudioSegment.from_mp3(str(audio_path))
            play(audio)
            
            logger.info("Audio playback complete")
            
        except Exception as e:
            logger.error(f"Voice output error: {e}")
        finally:
            # Cleanup temp file
            if audio_path.exists():
                try:
                    audio_path.unlink()
                except:
                    pass
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            # Clean audio directory
            for file in self.audio_dir.glob("*.wav"):
                file.unlink()
            for file in self.audio_dir.glob("*.mp3"):
                file.unlink()
            logger.info("Voice handler cleaned up")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
