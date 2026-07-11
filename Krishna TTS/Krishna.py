import tkinter as tk
from tkinter import ttk
import threading
try:
    import pyttsx3
    engine = pyttsx3.init()
except Exception:
    pyttsx3 = None
    engine = None
    # delay importing messagebox until tkinter is ready

root = tk.Tk()
root.title("Dev TTS Studio")
root.geometry("600x500")


def get_voices():
    return engine.getProperty('voices')


voices = get_voices()


def update_voice_list():
    voice_names = [voice.name for voice in voices]

    voice_combo["values"] = voice_names

    if voice_names:
        voice_combo.current(0)


def speak():

    text = text_box.get("1.0", tk.END).strip()

    if not text:
        return

    if engine is None:
        tk.messagebox.showerror("Missing Dependency", "pyttsx3 is not installed. Install it with: pip install pyttsx3")
        return

    selected_voice = voice_combo.current()

    if selected_voice >= 0:
        engine.setProperty(
            'voice',
            voices[selected_voice].id
        )

    engine.setProperty(
        'rate',
        rate_slider.get()
    )

    engine.setProperty(
        'volume',
        volume_slider.get() / 100
    )

    threading.Thread(
        target=lambda: (
            engine.say(text),
            engine.runAndWait()
        )
    ).start()


def stop():
    if engine is None:
        return
    engine.stop()


# Language
ttk.Label(root, text="Language").pack()

language_combo = ttk.Combobox(
    root,
    values=["English", "Hindi", "Telugu"]
)

language_combo.pack()

language_combo.current(0)


# Voice
ttk.Label(root, text="Voice").pack()

voice_combo = ttk.Combobox(root)

voice_combo.pack(fill="x", padx=20)

update_voice_list()


# Rate
ttk.Label(root, text="Rate").pack()

rate_slider = tk.Scale(
    root,
    from_=50,
    to=300,
    orient="horizontal"
)

rate_slider.set(150)

rate_slider.pack(fill="x", padx=20)


# Pitch
ttk.Label(root, text="Pitch").pack()

pitch_slider = tk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal"
)

pitch_slider.set(50)

pitch_slider.pack(fill="x", padx=20)


# Volume
ttk.Label(root, text="Volume").pack()

volume_slider = tk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal"
)

volume_slider.set(100)

volume_slider.pack(fill="x", padx=20)


# Text box
ttk.Label(root, text="Text").pack()

text_box = tk.Text(
    root,
    height=10
)

text_box.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


# Buttons
button_frame = tk.Frame(root)

button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Speak",
    command=speak
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Stop",
    command=stop
).pack(side="left", padx=5)


root.mainloop()