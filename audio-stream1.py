import asyncio
import requests
import base64
import websockets
import sys
from hume import HumeStreamClient, StreamSocket
from hume.models.config import ProsodyConfig
import json
import sounddevice as sd
import numpy as np

hume_api_url = "wss://api.hume.ai/v0/stream/models"
api_key = "bCG35BFIKBTw1GQlFZB9epg64emMa22W1JZnCmfRqH4GaLSd"

async def main():
    async with websockets.connect(hume_api_url, extra_headers={"X-Hume-Api-Key": api_key}) as websocket:
            # Set the duration and sample rate for recording
            duration = 10  # in seconds
            sample_rate = 44100  # in Hz

            # Record audio from the microphone
            print("Recording audio...")
            audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
            sd.wait()

            # Convert the audio data to a byte array
            audio_bytes = (audio * 32767).astype(np.int16).tobytes()

            # Encode the audio data as base64
            encoded_data = base64.b64encode(audio_bytes).decode("utf-8")

            json_message = {
                "models": {
                    "language": {}
                },
                "raw_text": True,
                "data": encoded_data
            }

            json_message_str = json.dumps(json_message)
            # Send the JSON message to the socket
            await websocket.send(json_message_str)

            # Receive the result from the socket
            result = await websocket.recv()

            # Save the result to a file
            with open("output.json", "w") as f:
                json.dump(result, f)

            print("Streaming and processing complete.")

asyncio.run(main())
