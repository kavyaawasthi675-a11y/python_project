import tkinter as tk
import numpy as np
import sounddevice as sd
import threading

SAMPLE_RATE = 44100
DURATION = 0.5


notes = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88,
    "C2": 523.25
}


colors = [
    "#ff4d4d",
    "#ff9933",
    "#ffff66",
    "#66ff66",
    "#66ccff",
    "#6699ff",
    "#cc66ff",
    "#ff66b3"
]

def play_tone(freq):
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)

    
    tone = np.sin(freq * 2 * np.pi * t)

    # Smooth fade in/out
    fade = int(0.02 * SAMPLE_RATE)
    tone[:fade] *= np.linspace(0, 1, fade)
    tone[-fade:] *= np.linspace(1, 0, fade)

    sd.play(tone, SAMPLE_RATE)
    sd.wait()

def play(freq):
    threading.Thread(target=play_tone, args=(freq,), daemon=True).start()

# ---------------- GUI ----------------

root = tk.Tk()
root.title("🎹 Colorful Musical Keyboard")
root.geometry("900x350")
root.configure(bg="#1e1e2f")

title = tk.Label(
    root,
    text="🎵 Colorful Musical Keyboard 🎵",
    font=("Arial", 22, "bold"),
    bg="#1e1e2f",
    fg="white"
)
title.pack(pady=20)

frame = tk.Frame(root, bg="#1e1e2f")
frame.pack()

for i, (note, freq) in enumerate(notes.items()):
    btn = tk.Button(
        frame,
        text=note,
        font=("Arial", 18, "bold"),
        bg=colors[i],
        fg="black",
        width=7,
        height=8,
        relief="raised",
        bd=5,
        activebackground="white",
        command=lambda f=freq: play(f)
    )
    btn.grid(row=0, column=i, padx=5)

# Keyboard Mapping
key_map = {
    "a": "C",
    "s": "D",
    "d": "E",
    "f": "F",
    "g": "G",
    "h": "A",
    "j": "B",
    "k": "C2"
}

def key_press(event):
    key = event.keysym.lower()
    if key in key_map:
        play(notes[key_map[key]])

root.bind("<Key>", key_press)

info = tk.Label(
    root,
    text="Mouse: Click the colorful keys\nKeyboard: A S D F G H J K",
    font=("Arial", 13),
    bg="#1e1e2f",
    fg="white"
)
info.pack(pady=20)

root.mainloop()