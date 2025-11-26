import cv2 
import numpy as np 
import face_recognition 
import os
import zipfile
import shutil
from datetime import datetime
import sys

# --- Configuration ---
# ⚠ ACTION REQUIRED: CHANGE THIS PATH TO YOUR ACTUAL FOLDER PATH!
path = r'c:\Users\SNEHA\OneDrive\Pictures\Camera Roll\Face_Image_project (2).zip'
# Example: If your pictures are in C:\MyProject\KnownFaces, use r'C:\MyProject\KnownFaces'
# ---------------------

# --- 1. Load Images and Get Encodings ---
def findEncodings(path):
    """
    Loads images from the specified folder path and calculates face encodings.
    """
    images = []
    classNames = []
    encodeList = []

    # Get the list of all files in the directory
    try:
        myList = os.listdir(path)
    except FileNotFoundError:
        print(f"ERROR: The folder '{path}' was not found.")
        print("Please create the folder and place face images inside.")
        # Return three items to prevent the ValueError
        return [], [], [] 

    if not myList:
        print(f"ERROR: The folder '{path}' is empty. Cannot run attendance system.")
        return [], [], []

    print(f"Found {len(myList)} items in folder. Processing images...")

    for img_file in myList:
        # Only process common image files
        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Read the image
            current_img = cv2.imread(os.path.join(path, img_file))
            if current_img is None:
                print(f"Warning: Could not read image file {img_file}. Skipping.")
                continue

            images.append(current_img)
            # Extract name from the filename
            classNames.append(os.path.splitext(img_file)[0])

    # Calculate encodings
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)

        if len(encode) > 0:
            encodeList.append(encode[0])
        else:
            print(f"Warning: No face found in image for {classNames[-1]}. Skipping encoding.")
            classNames.pop() 

    print("Encoding Completed!")
    return encodeList, classNames, [] # Return three items (the last one is unused but prevents ValueError)


# --- 2. Attendance Logging Function ---
def markAttendance(name):
    """
    Records the name and current time into a CSV log file (AttendanceLog.csv).
    """
    with open('AttendanceLog.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0]) 

        # Only mark attendance if the name hasn't been logged in this session
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            dateString = now.strftime('%Y-%m-%d')
            f.writelines(f'\n{name},{dtString},{dateString},Present')
            print(f"ATTENDANCE MARKED: {name} at {dtString}")


# --- Main Execution ---

# Create the AttendanceLog file with headers if it doesn't exist
if not os.path.exists('AttendanceLog.csv'):
    with open('AttendanceLog.csv', 'w') as f:
        f.write('Name,Time,Date,Status')

# 1. Prepare known-faces folder (handle zip paths)
if not os.path.isdir(path):
    # If user pointed to a zip file, extract it next to the zip and use the extracted folder
    if os.path.isfile(path) and path.lower().endswith('.zip'):
        extract_dir = os.path.splitext(path)[0]
        try:
            if not os.path.exists(extract_dir):
                print(f"Extracting '{path}' to '{extract_dir}'...")
                with zipfile.ZipFile(path, 'r') as zf:
                    zf.extractall(extract_dir)
            path = extract_dir
        except Exception as e:
            print(f"Failed to extract zip file: {e}")

# Get encodings for all known faces
encodeListKnown, classNames, _ = findEncodings(path)

if not encodeListKnown:
    print("WARNING: No known faces available. Running camera in detection-only mode.")
    # Continue running; attendance marking will be skipped because there are no known encodings
    encodeListKnown = []
    classNames = []

# 2. Initialize the camera 
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera. Check camera index (0) or permissions.")
    sys.exit()

print("Camera active. Press 'q' to quit.")

# Main camera loop
while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame.")
        break
        
    # Resize frame for faster processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Find faces and their encodings in the current camera frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # Loop through detected faces and compare
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        if encodeListKnown:
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.55)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                
                # Rescale the face location coordinates back to the original image size (x4)
                y1, x2, y2, x1 = [i * 4 for i in faceLoc]
                
                # Draw green rectangle for recognized face
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                
                markAttendance(name)
            else:
                # Draw red rectangle for UNKNOWN face
                y1, x2, y2, x1 = [i * 4 for i in faceLoc]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, 'UNKNOWN', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        else:
            # No known faces: always mark as UNKNOWN (detection-only mode)
            y1, x2, y2, x1 = [i * 4 for i in faceLoc]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, 'UNKNOWN', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


    # Display the output window
    cv2.imshow('Face Attendance System', img)
    
    # Wait for 'q' key press to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("\nSystem closed. Check AttendanceLog.csv for results.")