#!/bin/bash

echo "🎙️ Setting up voice capabilities..."

# Create full voice handler
cat > src/voice_handler.py << 'VOICEEOF'
"""Voice Handler - Full voice input/output"""
import whisper
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
from loguru import logger
from pathlib import Path
import numpy as np

class VoiceHandler:
    """Handle voice input/output using Whisper + gTTS"""
    
    def __init__(self, config):
        self.config = config
        self.audio_dir = Path("data/audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        model_size = config.get("WHISPER_MODEL", "base")
        logger.info(f"Loading Whisper model: {model_size}...")
        self.whisper_model = whisper.load_model(model_size)
        logger.info("Whisper loaded")
        
        self.sample_rate = 16000
        self.duration = 5
    
    async def listen(self) -> str:
        """Record audio and transcribe with Whisper"""
        try:
            audio_path = self.audio_dir / "user_input.wav"
            print("Recording... (speak now, 5 seconds)")
            
            audio_data = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )
            sd.wait()
            print("Processing...")
            
            sf.write(audio_path, audio_data, self.sample_rate)
            result = self.whisper_model.transcribe(str(audio_path), language='en', fp16=False)
            
            transcription = result["text"].strip()
            logger.info(f"Transcribed: {transcription}")
            return transcription
        except Exception as e:
            logger.error(f"Error: {e}")
            return ""
    
    async def speak(self, text: str):
        """Convert text to speech and play"""
        try:
            audio_path = self.audio_dir / "agent_response.mp3"
            print("Speaking...")
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(audio_path))
            
            audio = AudioSegment.from_mp3(str(audio_path))
            play(audio)
            
            logger.info("Audio playback complete")
        except Exception as e:
            logger.error(f"Error: {e}")
VOICEEOF

echo "✅ Voice handler created!"

# Create simple voice output demo
cat > test_voice_simple.py << 'TESTEOF'
#!/usr/bin/env python3
"""Simple voice output test"""
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

text = "You have 2 overdue invoices, totaling one thousand one hundred dollars."
print(f"Agent will say: {text}")

tts = gTTS(text=text, lang='en', slow=False)
tts.save("temp.mp3")

audio = AudioSegment.from_mp3("temp.mp3")
play(audio)

print("Done!")
TESTEOF

chmod +x test_voice_simple.py

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Install dependencies: pip install openai-whisper gtts sounddevice soundfile pydub"
echo "2. Install ffmpeg: brew install ffmpeg"
echo "3. Test: python test_voice_simple.py"

