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
