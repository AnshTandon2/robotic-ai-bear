import requests
import os


def generate_speech(input_text, output_file, api_key):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "model": "tts-1",
        "input": input_text,
        "voice": "alloy"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx errors

        with open(output_file, "wb") as f:
            f.write(response.content)
        
        print("Speech generated successfully. Output file:", output_file)
    except requests.exceptions.RequestException as e:
        print("Error generating speech:", e)

# Example usage
api_key = "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"
input_text = "Today is a wonderful day to build something people love!"
output_file = "speech.mp3"

generate_speech(input_text, output_file, api_key)