import asyncio
import websockets
import cv2
import base64
import sys
import json

# Define the Hume API endpoint
hume_api_url = "wss://api.hume.ai/v0/stream/models"
# Define your API key
api_key = "bCG35BFIKBTw1GQlFZB9epg64emMa22W1JZnCmfRqH4GaLSd"  # Replace with your actual API key
# Open the computer's camera
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Failed to open camera.")
    cap.release()
    sys.exit(1)

async def send_to_hume_api():
    try:
        async with websockets.connect(hume_api_url, extra_headers={"X-Hume-Api-Key": api_key}) as websocket:
            print("WebSocket connection established.")
            while True:
                print("Camera opened successfully:", cap.isOpened())
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    break
                # Convert the frame to base64
                _, img_encoded = cv2.imencode('.jpg', frame)
                img_base64 = base64.b64encode(img_encoded).decode('utf-8')
                # Define the payload with the necessary parameters
                payload = {
                    "models": {
                        "language": {}
                    },
                    "raw_text": True,
                    "data": img_base64  # Assuming you want to send image data
                }
                # to ensure time out

                # Send the payload as a JSON-formatted string
                try:
                  await websocket.send(json.dumps(payload))
                  print("Payload sent successfully.")
                except Exception as e:
                  print("Error sending payload:", e)

                # Receive the response
                response = await websocket.recv()
                outputs = json.loads(response)
                print(json.dumps(outputs, indent=2) + "\n")
                # Format the outputs in the desired structure

                formatted_outputs = {
                  "language": {
                    "predictions": []
                  }
                }

                # for prediction in outputs["language"]["predictions"]:
                #   formatted_prediction = {
                #     "text": prediction["text"],
                #     "position": prediction["position"],
                #     "emotions": []
                #   }
                #   for emotion in prediction["emotions"]:
                #     formatted_emotion = {
                #       "name": emotion["name"],
                #       "score": emotion["score"]
                #     }
                #     formatted_prediction["emotions"].append(formatted_emotion)
                #   formatted_outputs["language"]["predictions"].append(formatted_prediction)

                # Dump the formatted outputs into sending.json
                with open('sending.json', 'w') as file:
                  json.dump(formatted_outputs, file)
                
                await asyncio.sleep(0)  # Add a small delay to prevent blocking
            
    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket connection closed unexpectedly: {e}")

    finally:
        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

# Run the async function
asyncio.run(send_to_hume_api())
