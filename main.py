import requests
import uuid
from gtts import gTTS, lang
from playsound import playsound
import azure.cognitiveservices.speech as speechsdk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import api_keys

# Constant variables
API_KEY = api_keys.translate_api_key
ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"
LOCATION = "global"
LOCALS = {"Croatian": "hr-HR", 
            "Czech": "cs-CZ", 
            "Danish": "da-DK", 
            "Dutch": "nl-NL", 
            "English": "en-US", 
            "Finnish": "fi-FI", 
            "French": "fr-FR", "German": 
            "de-DE", "Greek": "el-GR", 
            "Hungarian": "hu-HU", 
            "Italian": "it-IT", 
            "Japanese": "ja-JP", 
            "Korean": "ko-KR", 
            "Norwegian": "no-NO", 
            "Polish": "pl-PL", 
            "Portuguese": "pt-PT", 
            "Romanian": "ro-RO", 
            "Russian": "ru-RU", 
            "Spanish": "es-ES", 
            "Swedish": "sv-SE", 
            "Turkish": "tr-TR"}

SUPPORTED_LANG = lang.tts_langs()

HEADERS = {
    'Ocp-Apim-Subscription-Key': API_KEY,
    'Ocp-Apim-Subscription-Region': LOCATION,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

if __name__ == "__main__":
    # Initialize GUI
    window = Tk()
    window.title("Speech Translator")
    window.geometry('300x150')

    # Create a label for the text entry box
    label = Label(window, 
        text="What language do you want to translate to?", 
        font=("Arial Bold", 12))

    entry1 = Combobox(window)
    # Get the list of supported languages for speech
    entry1['values'] = ([x for x in LOCALS.keys()])

    label1 = Label(window, text="to")

    entry2 = Combobox(window)
    # Get the list of supported languages for translation
    entry2['values'] = ([x for x in SUPPORTED_LANG.values()])

    def play_translation(translated_input, language):
        try:
            # Create tts object of the translated text
            tts_of_input = gTTS(text=translated_input, lang=language, slow=False)
            # Save the audio file
            tts_of_input.save("output.mp3")
            # Return the audio file and play it
            return playsound("output.mp3")

        except Exception as e:
            return messagebox.showerror("Error", "Error: " + str(e))

    def translate(input_text, language):
        # Set the params for the request
        params = {
            'api-version': '3.0',
            'to': f'{language}'
        }

        # Set the data for the request
        body = [{
            'text': f'{input_text}'
        }]

        try:
            # Send the request
            request = requests.post(ENDPOINT, headers=HEADERS, params=params, json=body)
            response = request.json()
        except Exception as e:
            return messagebox.showerror("Error", "Error: " + str(e))
            
        # Get the translated text from the response
        translated_text = response[0]['translations'][0]['text']
        # Put into play_translation function
        play_translation(translated_text, language)

    def from_mic(locale):
        # Create a speech translation config with specified subscription key and service region.
        speech_config = speechsdk.SpeechConfig(subscription=api_keys.speech_api_key,
                                                region="northeurope", 
                                                speech_recognition_language=LOCALS[locale])

        # Creates a recognizer with the given settings
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        # Starts speech recognition, and returns after a single utterance is recognized
        result = speech_recognizer.recognize_once_async().get()
        return result.text

    # Execute when the button is clicked
    def main():
        label1 = Label(window, text="Start talking!")
        label1.pack()
        window.update()
        # Get speech in text
        input_text = from_mic(entry1.get())
        # Show the text in the label
        label2 = Label(window, text="I heard: " + input_text)
        label2.pack()
        window.update()
        language = entry2.get()
        # get key of value
        language = list(SUPPORTED_LANG.keys())[list(SUPPORTED_LANG.values()).index(language)]
        # Translate the text
        translate(input_text, language)

    # Create button and assign function to button when clicked
    btn = Button(window, text="Click to record", command=main)

    # Pack everything
    label.pack()
    entry1.pack()
    label1.pack()
    entry2.pack()
    btn.pack()
    window.mainloop()