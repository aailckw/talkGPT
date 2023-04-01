import argparse
import os
import openai
import subprocess
import speech_recognition as sr
import pyttsx3

LANGUAGES = {
  "en": "english",
  "zh-hans": "chinese"
}


def speak(text, language):
    engine = pyttsx3.init()

    if language == "chinese":
        # Set voice for Chinese
        for voice in engine.getProperty('voices'):
            if "chinese" in voice.languages:
                engine.setProperty("voice", voice.id)
                break
    else:
        # Set voice for English
        for voice in engine.getProperty('voices'):
            if "english" in voice.languages:
                engine.setProperty("voice", voice.id)
                break

    engine.say(text)
    engine.runAndWait()

def transcribe_speech(language: str) -> str:
    
    """
        Records audio from the microphone and transcribes it into text.

        Args:
            language: A string indicating the language of the speech to be transcribed.

        Returns:
            A string containing the transcribed text.

        Raises:
            sr.RequestError: If there is an error with the API request.
            sr.UnknownValueError: If the speech could not be transcribed.
    """
  
    print("\n\nListening...")
    
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print(audio)
        
        transcript = recognizer.recognize_whisper(audio, language=language)
        print(transcript)
        
        return transcript


def send_request(language: str, words: str) -> None:
    
    """
        Sends a request to the OpenAI API and speaks out the response.

        Args:
            language: A string indicating the language of the chat message.
            words: A string containing the chat message to be sent.

        Returns:
            None.

        Raises:
            openai.error.OpenAIError: If there is an error with the OpenAI API request.
    """
    
    openai.api_key = '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'
    
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0301",
      messages=[
        {
            "role": "user", 
            "content": words
        }
      ]
    )

    answer = completion.choices[0].message["content"]
    print(answer)

    out = answer.replace('\n', " ")
    speak(out, language)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language",
        type=str,
        choices=sorted(LANGUAGES.keys()),
        default="en",
        metavar="LANGUAGE",
        help="language to talk, available: {%(choices)s}",
    )

    options = parser.parse_args()
    language = LANGUAGES[options.language]

    print(language)

    while True:
        input_words = transcribe_speech(language)
        send_request(language, input_words)
