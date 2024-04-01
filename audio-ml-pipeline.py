import asyncio
import requests
import base64
import sys
import websockets
import json
import sounddevice as sd
import numpy as np

json_objects = []

emotions_scores = {
    "Admiration": 0.0,
    "Adoration": 0.0,
    "Aesthetic Appreciation": 0.0,
    "Amusement": 0.0,
    "Anger": 0.0,
    "Annoyance": 0.0,
    "Anxiety": 0.0,
    "Awe": 0.0,
    "Awkwardness": 0.0,
    "Boredom": 0.0,
    "Calmness": 0.0,
    "Concentration": 0.0,
    "Confusion": 0.0,
    "Contemplation": 0.0,
    "Contempt": 0.0,
    "Contentment": 0.0,
    "Craving": 0.0,
    "Determination": 0.0,
    "Disappointment": 0.0,
    "Disapproval": 0.0,
    "Disgust": 0.0,
    "Distress": 0.0,
    "Doubt": 0.0,
    "Ecstasy": 0.0,
    "Embarrassment": 0.0,
    "Empathic Pain": 0.0,
    "Enthusiasm": 0.0,
    "Entrancement": 0.0,
    "Envy": 0.0,
    "Excitement": 0.0,
    "Fear": 0.0,
    "Gratitude": 0.0,
    "Guilt": 0.0,
    "Horror": 0.0,
    "Interest": 0.0,
    "Joy": 0.0,
    "Love": 0.0,
    "Nostalgia": 0.0,
    "Pain": 0.0,
    "Pride": 0.0,
    "Realization": 0.0,
    "Relief": 0.0,
    "Romance": 0.0,
    "Sadness": 0.0,
    "Sarcasm": 0.0,
    "Satisfaction": 0.0,
    "Desire": 0.0,
    "Shame": 0.0,
    "Surprise (negative)": 0.0,
    "Surprise (positive)": 0.0,
    "Sympathy": 0.0,
    "Tiredness": 0.0,
    "Triumph": 0.0
}

# importning the necessary api to be used for the ML model
hume_api_url = "wss://api.hume.ai/v0/stream/models"
api_key = "bCG35BFIKBTw1GQlFZB9epg64emMa22W1JZnCmfRqH4GaLSd"

async def main():
    async with websockets.connect(hume_api_url, extra_headers={"X-Hume-Api-Key": api_key}) as websocket:
        # the duration you want to keep on talking audio input
        duration = 10  # in seconds
        sample_rate = 44100  # in Hz

        # Record audio from the microphone
        print("Recording audio...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()

        # need to convert to byte array in order to further professr
        audio_bytes = (audio * 32767).astype(np.int16).tobytes()

        # conversion to base65 to be fed into the ML model
        encoded_data = base64.b64encode(audio_bytes).decode("utf-8")

        # chunk the data so that 10,0000 characters can be processed at a time
        chunks = [encoded_data[i:i + 10000] for i in range(0, len(encoded_data), 10000)]

        for chunk in chunks:
            json_message = {
                "models": {
                    "language": {}
                },
                "raw_text": True,
                "data": chunk
            }

            # store the json data directly, send, and recieve socket data
            json_message_str = json.dumps(json_message)
            await websocket.send(json_message_str)
            result = await websocket.recv()

            json_objects.append(json.loads(result))
            # save json results into file for further processing
            # with open("output.json", "a") as f:
            #     f.write(result + ",\n")
            for data in json_objects:
                for language_data in data.get("language", []):
                    for prediction_data in language_data.get("predictions", []):
                        for each_emotion_json in prediction_data.get("emotions", []):
                            emotions_scores[each_emotion_json["emotion"]] = each_emotion_json["score"]

            # for language_data in json_objects["language"]:
            #     for prediction_data in language_data["predictions"]:
            #         for each_emotion_json in prediction_data["emotions"]:
            #             emotions_scores[each_emotion_json["emotion"]] = each_emotion_json["score"]

        print("Streaming and processing complete.")
        print("JSON Contents", json_objects)
        print("Emotion Scores", emotions_scores)

asyncio.run(main())