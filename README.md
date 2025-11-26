1**. Attendance by Face Detection**

A simple and effective attendance marking system using OpenCV, face_recognition, and Python for automatic real-time face-based attendance.

2**. Overview**

This project implements a face detection + recognition attendance system that can:

Detect faces in real time using the system camera

Recognize known faces from a stored image dataset

Automatically mark attendance with name, date, and time

Save attendance records into a CSV file

Support adding new student images easily

3. **Algorithm: Face Recognition + Greedy Matching**

The system uses face encodings and a greedy comparison approach:

Convert training images into 128-D face encodings

For each frame from the camera:

Detect faces

Extract face encodings

Compare encodings greedily with known dataset

Compute similarity using a distance threshold

Select the best matching face

Mark attendance only once per student

4. **Requirements**

Python 3.7+

OpenCV

NumPy

face_recognition

dlib (installed automatically with face_recognition)

5. **Installation**

Install required packages:

pip install opencv-python
pip install face_recognition
pip install numpy
pip install dlib

6. **Usage**
6.1 Running the Program
python main.py

7. **Folder Structure**
Attendance-Face-Detection/
├── main.py                     # Main program: detection + attendance logic
├── encode_faces.py             # Encodes training images
├── attendance.csv              # Auto-generated attendance file
├── Images/                     # Folder for student images
│   ├── <name1>.jpg
│   ├── <name2>.jpg
│   └── ...
└── README.md

**8.How It Works**
**8.1 Load Training Images**

Reads all images in the Images/ folder

Extracts face encodings

Stores names from file names

**8.2 Real-Time Face Detection**

Opens webcam using OpenCV

Detects faces in each frame

**8.3 Greedy Face Matching**

Compares detected face encodings with known encodings

Selects the closest match

Uses threshold to improve accuracy

**8.4 Attendance Marking**

Writes the following into attendance.csv:

Name

Date

Time

Ensures attendance is marked only once per person.

**9. Example**
from main import FaceAttendanceSystem

system = FaceAttendanceSystem()

# Start recognition
system.start_recognition()

**10. Notes**

Keep images clear and front-facing

Use JPG/PNG format

Recommended size: 300×300 px

Better lighting gives better accuracy

Attendance is marked only once per session

**11. Future Enhancements (Optional)**

Store attendance in a database

Add voice notifications

Create GUI using Tkinter

Support multiple cameras