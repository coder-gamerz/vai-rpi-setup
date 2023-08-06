from Bard import Chatbot
from playsound import playsound
import speech_recognition as sr
from os import system
import whisper
import warnings
import sys
import pyttsx3
import os

token = 'ZgiKxb111lPf4ik-GlxBh3Zr2lxxmcUQvn8YaqMSrOQgqo9rQyJYpJ6wtdOY2RSJOYPBAA.'
tokents = 'sidts-CjEBSAxbGSUI8O3BrHRc2nRA5eyTLjwOZOoxWipMofGovM9w2iAMnuOaENb7V5nzhHuPEAA'

chatbot = Chatbot(token, tokents)

r = sr.Recognizer()
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-45)

tiny_model = whisper.load_model('tiny')
base_model = whisper.load_model('base')

warnings.filterwarnings("ignore", message='FP16 is not supported on CPU; using FP32 instead')

def prompt_bard(prompt):
    response = chatbot.ask(prompt)
    return response['content']

def speak(text):
    
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$: ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    
    else:
        engine.say(text)
        engine.runAndWait()

def main():
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        
        while True:
            
            while True:
                try:
                    print('\nSay "husky" to wake me up. \n')
                    audio = r.listen(source)
                    with open("wake_detect.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                    
                    result = tiny_model.transcribe('wake_detect.wav')
                    text_input = result['text']
                    
                    if 'husky' in text_input.lower().strip():
                        break
                    else:
                        print("No wake word found. Try again.")
                except Exception as e:
                    print("Error transcribing audio: ", e)
                    continue
            try:
                
                playsound('wake_detected.mp3')
                print("Wake word detected. Please speak your prompt to Bard. \n")
                
                audio = r.listen(source)
                with open("prompt.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                
                result = base_model.transcribe('prompt.wav')
                prompt_text = result['text']
                print("Sending to Bard:", prompt_text, '\n')
                
                if len(prompt_text.strip()) == 0:
                    print("Empty prompt. Please speak again.")
                    speak("Empty prompt. Please speak again.")
                    continue
            except Exception as e:
                print("Error transcribing audio: ", e)
                continue
            
            response = prompt_bard(prompt_text)
            
            if sys.platform.startswith('win'):
                 print('Bards response: ', response)
            else:
                
                print("\033[31m" + 'Bards response: ', response, '\n' + "\033[0m")
            speak(response)
            
if __name__ == '__main__':
    main()
