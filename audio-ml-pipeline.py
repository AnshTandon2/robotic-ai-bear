import asyncio
import requests
import base64
import sys
import websockets
import json
import sounddevice as sd
import numpy as np

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

            # save json results into file for further processing
            with open("output.json", "a") as f:
                f.write(result + "\n")

        print("Streaming and processing complete.")

asyncio.run(main())