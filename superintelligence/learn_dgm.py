from superintelligence.registry import register
import os
import datetime
import numpy as np

def dgm_learn(sensory_data):
    """
    Save image and audio sensory input to disk for later training/analysis.
    """
    if not sensory_data:
        print("[DGM] No sensory data to learn from.")
        return False
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = "learned_data"
    os.makedirs(save_dir, exist_ok=True)
    # Save image if available
    image = sensory_data.get("image")
    if isinstance(image, np.ndarray):
        from PIL import Image
        img_path = os.path.join(save_dir, f"image_{timestamp}.png")
        Image.fromarray(image).save(img_path)
        print(f"[DGM] Saved image to {img_path}")
    else:
        print(f"[DGM] No image array to save: {image}")
    # Save audio if available
    audio = sensory_data.get("audio")
    if isinstance(audio, np.ndarray):
        import soundfile as sf
        audio_path = os.path.join(save_dir, f"audio_{timestamp}.wav")
        sf.write(audio_path, audio, 16000)
        print(f"[DGM] Saved audio to {audio_path}")
    else:
        print(f"[DGM] No audio array to save: {audio}")
    return True

register("learn", dgm_learn)
