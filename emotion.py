import requests
import cv2
import base64
import sys

# Define the Hume API endpoint
hume_api_url = "wss://api.hume.ai/v0/stream/models "
# Define your API key
api_key = "bCG35BFIKBTw1GQlFZB9epg64emMa22W1JZnCmfRqH4GaLSd"
# Open the computer's camera
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Failed to open camera.")
    sys.exit(1)

while True:
    try:
        ret, frame = cap.read()
        # if not ret:
        #     print("Error: Failed to capture frame.")
        #     break
        # Convert the frame to base64
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        payload = {
            'image': img_base64,
            'api_key': api_key
        }
        response = requests.post(hume_api_url, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Retrieve the outputs from the Hume API
        outputs = response.json()
        # Process the outputs as needed
        # ...

        # Display the frame with the detected emotions
        cv2.imshow('Emotion Detection', frame)
        
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to the Hume API:", e)
        break

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
