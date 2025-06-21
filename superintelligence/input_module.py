"""
Handles multimodal input: sight (images/video) and sound (audio).
Simulates input for demo purposes.
"""

def get_multimodal_input(memory=None, user_text=None, config=None):
    # Simulate image and audio input
    image = "image_data: cat.jpg"
    audio = "audio_data: meow.wav"
    print(f"[Input] Received image: {image}, audio: {audio}")
    return {"image": image, "audio": audio, "user_text": user_text}
