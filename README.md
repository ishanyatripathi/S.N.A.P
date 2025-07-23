S.N.A.P. : Slide Navigation via Aerial Palms

S.N.A.P. is a gesture-controlled presentation tool that lets you navigate slides with just your hands — no remotes, no keyboards, no touch. Using real-time hand tracking powered by MediaPipe, it recognizes specific gestures like snapping and open palms to move forward, backward, or exit slides intuitively.

-------------------------------------
✨ Features

- 👉 Snap with your RIGHT hand to go to the NEXT slide
- 👈 Snap with your LEFT hand to go to the PREVIOUS slide
- ✋ Show BOTH OPEN PALMS to CLOSE the presentation
- 🧠 Gesture buffering and cooldown system to avoid accidental triggers
- 🖐️ Real-time hand tracking using MediaPipe
- 🛠️ Simple setup with OpenCV + PyAutoGUI

-------------------------------------
🛠 Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- PyAutoGUI

Install dependencies:
pip install opencv-python mediapipe pyautogui

-------------------------------------
🚀 How to Run

python snap.py

- Ensure your webcam is on
- Use gestures in front of the camera to control your slides
- Press 'q' to quit manually

-------------------------------------
💡 Gestures Guide

Gesture             -> Action
-------------------------------------
Right hand snap     -> Next slide
Left hand snap      -> Previous slide
Both palms open     -> Exit presentation

-------------------------------------
🔧 Customization Ideas

- Add gestures for starting presentation or toggling black screen
- Add on-screen text feedback
- Link with PowerPoint, PDF viewers, or OBS

-------------------------------------
🧠 Why S.N.A.P.?

S.N.A.P. (Slide Navigation via Aerial Palms) lets you interact with your slides naturally.
Perfect for tech talks, smart classrooms, or futuristic hands-free control.

-------------------------------------
📄 License

MIT License
