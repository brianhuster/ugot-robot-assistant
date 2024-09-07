import os
import sys
import time
import requests
import json

from uexplore_interfaces import UExploreAiSpeech
from uexplore_interfaces import UExploreAudio
from uexplore_interfaces import UExploreDevice
from uexplore_interfaces import Color
from uexplore_control import AUDIO
from uexplore_control import DEVICE

SERVER_URL = 'http://192.168.1.104:5000/send_message'

class ugot_chat:
    def __init__(self):
        self.ugotAudio = UExploreAudio()
        self.ugotSpeech = UExploreAiSpeech()
        self.ugotDevice = UExploreDevice()
        self.ugotControlAudio = AUDIO
        self.ugotControlDevice = DEVICE

    def volume_control(self, level):
        fixlevel = max(0, min(100, level))
        self.ugotControlDevice.setVolume(100-fixlevel)
        self.ugotControlDevice.setVolume(fixlevel)

    def speech_to_text(self, begin_vad=3000, end_vad=1500, duration=5000, show_light=True, show_sound=True):
        if show_light:
            self.ugotDevice.show_light_effect(Color.GREEN, self.ugotDevice.Light.Effect.FLASHING)
        if show_sound:
            self.volume_control(100)
            self.ugotAudio.play_sound('volume_control', True)
        result = self.ugotControlAudio.setAudioAsr(begin_vad, end_vad, duration)
        if show_light:
            self.ugotDevice.show_light_effect(Color.BLACK, self.ugotDevice.Light.Effect.TURN_OFF)
        if result.code == 0 and result.data:
            return str(result.data)
        else:
            return ""

    def text_to_speech(self, content: str, wait=True):
        if content is None or len(content) == 0:
            return

        self.volume_control(100)
        for line in content.splitlines():
            line = line.strip()
            if len(line) == 0:
                continue
            self.ugotSpeech.play_tts(line, 0, wait)
        
    def send_message(self, text):
        response = requests.post(SERVER_URL, json={'text': text})
        if response.status_code == 200:
            data = response.json()
            return data['text']
        else:
            print(f"Error: {response.status_code}")


chatbot = ugot_chat()

chatbot.text_to_speech("Hi, I'm Gạo. I'm here to be your friend. How are you today?")

while True:
    question = chatbot.speech_to_text(duration=5000)
    print(f'speech_to_text result: {question}')

    if question is None or len(question) == 0:
        chatbot.text_to_speech('Sorry, I did not hear your question clearly.  Please try again')
        continue

    answer = chatbot.send_message(question)

    print(f'ask_chatbot_question answer: {answer}')

    if answer is None or len(answer) == 0:
        chatbot.text_to_speech('Sorry, no information found.  Please try again')
        continue

    chatbot.text_to_speech(answer)
