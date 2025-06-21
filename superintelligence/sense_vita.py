from superintelligence.registry import register

def vita_sense():
    try:
        import cv2
        import sounddevice as sd
        import numpy as np
        # Capture image from webcam
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            image = None
        else:
            # Convert image to a simple shape for display
            image = f"Image shape: {frame.shape}"
        # Capture 1 second of audio at 16kHz
        duration = 1  # seconds
        fs = 16000
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        audio_summary = f"Audio shape: {audio.shape}, dtype: {audio.dtype}"
        print("[VITA] Captured real image and audio.")
        return {"image": image, "audio": audio_summary}
    except Exception as e:
        print(f"[VITA] Error capturing real input: {e}")
        return {"image": "error", "audio": "error"}

register("sense", vita_sense)
