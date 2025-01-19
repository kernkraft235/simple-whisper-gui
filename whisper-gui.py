"""
A minimal GUI for transcribing an audio file with OpenAI Whisper.

Usage (CLI):
  python whisper_gui.py [--help]

GUI Operation:
  1. Double-click or run `python whisper_gui.py`.
  2. Select an audio file from the dialog.
  3. The script automatically transcribes it into a .txt with the same name.
  4. Output file is placed in the same directory as the original audio.
"""

import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import whisper

# ----------------------#
#    CONFIG VARIABLES   #
# ----------------------#
MODEL_NAME = "turbo"  # Choose from: tiny, base, small, medium, large, etc.
ENABLE_TIMESTAMPS = True

def print_help():
    """Print usage information."""
    help_text = """\
Usage: whisper_gui.py [--help]

No command-line arguments are needed for GUI operation:
1. Double-click or run `python whisper_gui.py`.
2. A file dialog will prompt you to select an audio file.
3. The transcript will be written to the same folder with a .txt extension.
"""
    print(help_text)

def transcribe_audio(audio_path):
    """
    Transcribe the given audio file using OpenAI Whisper.
    Returns the transcribed text. If timestamps are enabled,
    includes simple timestamp markers in the text.
    """
    model = whisper.load_model(MODEL_NAME)
    result = model.transcribe(audio_path, verbose=False)

    if ENABLE_TIMESTAMPS and "segments" in result:
        # Construct a transcript with segment-level timestamps
        transcript_with_timestamps = []
        for seg in result["segments"]:
            start_time = seg["start"]
            end_time = seg["end"]
            text_segment = seg["text"].strip()
            segment_str = f"[{start_time:.2f} - {end_time:.2f}] {text_segment}"
            transcript_with_timestamps.append(segment_str)
        return "\n".join(transcript_with_timestamps)
    else:
        # Just return the full text
        return result["text"]

def select_file_and_transcribe():
    """
    Opens a file dialog, prompts for an audio file, then transcribes and saves to TXT.
    """
    audio_path = filedialog.askopenfilename(
        title="Select an Audio File",
        filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg *.wma *.mp4 *.webm *.mov *.mkv"), 
                   ("All Files", "*.*")]
    )
    if not audio_path:
        return  # User canceled

    try:
        messagebox.showinfo("Transcribing", "Please wait while the file is transcribed...")
        transcript = transcribe_audio(audio_path)

        # Create output filename, same name but .txt extension
        base, _ = os.path.splitext(audio_path)
        output_path = base + ".txt"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        messagebox.showinfo("Success", f"Transcription saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def main():
    """Main entry point: checks for --help and otherwise launches the GUI."""
    if "--help" in sys.argv:
        print_help()
        sys.exit(0)

    # Create a basic Tkinter window
    root = tk.Tk()
    root.title("Whisper Transcription")
    root.geometry("300x150")

    label = tk.Label(root, text="Click the button to select an audio file.")
    label.pack(pady=20)

    btn = tk.Button(root, text="Select Audio File", command=select_file_and_transcribe)
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
