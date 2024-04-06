import speech_recognition as sr
import pyttsx3
import openai
import os


openai.api_key = os.getenv('OPENAI_API_KEY')

assistant_id = os.getenv('OPENAI_ASSISTANT_ID')

listener = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen_command():
    try:
        with sr.Microphone() as source:
            print('Escuchando...')
            voice = listener.listen(source)
            command = listener.recognize_google_cloud(voice)
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                return command
    except Exception as e:
        print(f"Error: {e}")
    return ''


def query_gpt(text):
    try:
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=text,
          temperature=0.5,
          max_tokens=150,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error al consultar GPT-3: {e}")
    return "Lo siento, tuve un problema al procesar tu solicitud."


while True:
    command = listen_command()
    if command:
        print(f"Comando recibido: {command}")
        response = query_gpt(command)
        print(f"Respuesta: {response}")
        speak(response)
