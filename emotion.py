import requests
import cv2
import base64

# Define the Hume API endpoint
hume_api_url = "https://api.hume.com/emotion"
# Define your API key
api_key = "YOUR_API_KEY_HERE"
# Open the computer's camera
cap = cv2.VideoCapture(0)
# Read frames from the camera
while True:
  ret, frame = cap.read()
  # Convert the frame to base64
  _, img_encoded = cv2.imencode('.jpg', frame)
  img_base64 = base64.b64encode(img_encoded).decode('utf-8')
  # Send the image to the Hume API for emotion detection
  payload = {
    'image': img_base64,
    'api_key': api_key
  }
  response = requests.post(hume_api_url, json=payload)
  # Retrieve the outputs from the Hume API
  outputs = response.json()
  # Process the outputs as needed
  # ...
  # Display the frame with the detected emotions
  cv2.imshow('Emotion Detection', frame)
  # Exit the loop if 'q' is pressed
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
