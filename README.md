# 1. Attendance by Face Detection

A simple and effective attendance marking system using **OpenCV**, **face_recognition**, and Python for automatic real-time face-based attendance.

---

# 2. Overview

This project can:

- Detect faces in real time using webcam  
- Recognize known faces from a stored dataset  
- Mark attendance with **name, date, and time**  
- Store attendance in a `.csv` file  
- Add new student images easily  

---

# 3. Algorithm: Face Recognition + Greedy Matching

## 3.1 Steps Used

1. Convert training images into **128-D face encodings**
2. For each frame captured:
   - Detect faces
   - Extract face encodings
   - Greedily match with known encodings
3. Compute similarity using distance threshold  
4. Select the **best matching face**  
5. Mark attendance **only once** per student  

---

# 4. Requirements

- Python 3.7+
- OpenCV
- NumPy
- face_recognition
- dlib

---

# 5. Installation

```bash
pip install opencv-python
pip install face_recognition
pip install numpy
pip install dlib
```

---

# 6. Usage

## 6.1 Run the Program

```bash
python main.py
```

---

# 7. Folder Structure

```
Attendance-Face-Detection/
├── main.py                     # Main detection + attendance logic
├── encode_faces.py             # Encodes training images
├── attendance.csv              # Auto-created attendance file
├── Images/                     # Folder for student images
│   ├── <name1>.jpg
│   ├── <name2>.jpg
│   └── ...
└── README.md
```

---

# 8. How It Works

## 8.1 Load Training Images
- Reads all images from the **Images/** folder  
- Extracts face encodings  
- Uses filenames as names  

## 8.2 Real-Time Face Detection
- Opens webcam  
- Detects faces in each frame  

## 8.3 Greedy Face Matching
- Compares extracted face encodings with database  
- Selects the **closest match**  
- Uses a threshold for accuracy  

## 8.4 Attendance Marking
Attendance is written to `attendance.csv` including:

- Name  
- Date  
- Time  

Marked **only once per person**.

---

# 9. Example

```python
from main import FaceAttendanceSystem

system = FaceAttendanceSystem()

system.start_recognition()
```

---

# 10. Notes

- Use clear, front-facing images  
- Recommended size: 300×300 px  
- Good lighting improves accuracy  
- Attendance is marked one time  

---

# 11. Future Enhancements

- Database support  
- Voice notifications  
- Tkinter GUI  
- Multi-camera support
