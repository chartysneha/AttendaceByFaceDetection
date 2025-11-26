Attendance by Face Detection

A simple and effective attendance marking system using OpenCV, face_recognition, and Python for automatic real-time face-based attendance.

Overview

This project implements a face detection + recognition attendance system that can:

Detect faces in real time using the system camera

Recognize known faces from a stored image dataset

Automatically mark attendance with name, date, and time

Save attendance records into a .csv file

Support adding new student images easily

Algorithm: Face Recognition + Greedy Matching

The system uses face encodings and greedy comparison:

Convert training images into 128-D face encodings

For each frame from the camera:

Detect faces

Extract face encodings

Compare encodings greedily with known dataset

Compute similarity using distance threshold

Select the best matching face

Mark attendance only once per student

Requirements

Python 3.7+

OpenCV

NumPy

face_recognition

dlib (automatically installed with face_recognition)

Installation

Install required packages:

pip install opencv-python
pip install face_recognition
pip install numpy
pip install dlib

Usage
Running the Program
python main.py

Folder Structure
Attendance-Face-Detection/
├── main.py                     # Main program: detection + attendance logic
├── encode_faces.py             # Encodes training images
├── attendance.csv              # Auto-generated attendance file
├── Images/                     # Folder for student images
│   ├── <name1>.jpg
│   ├── <name2>.jpg
│   └── ...
└── README.md

How It Works
1. Load Training Images

Reads all images in the Images/ folder

Extracts face encodings

Stores names from file names

2. Real-Time Face Detection

Opens webcam using OpenCV

Detects faces in each frame

3. Greedy Face Matching

Compares the detected face encoding with known encodings

Selects the closest match

Applies distance threshold for accuracy

4. Attendance Marking

Writes:

Name

Date

Time

…into attendance.csv

Ensures attendance is only marked once per person

Example
from main import FaceAttendanceSystem

system = FaceAttendanceSystem()

# Start recognition
system.start_recognition()

Notes

Keep images clear and front-facing

Use JPG/PNG format

Recommended size: 300×300px

Better lighting gives better accuracy

System marks attendance only once per session

Future Enhancements (Optional)

Store attendance in a database

Add voice notification

Use GUI with Tkinter

Add multiple camera support
