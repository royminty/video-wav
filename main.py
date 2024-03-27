from pytube import YouTube
import os
import tkinter
import customtkinter
import subprocess

def startDownload():
  try: 
    path = 'PUT YOUR PATH HERE WHERE YOU WANT YOUR FILE CONVERTED'
    ytLink = link.get()
    ytObject = YouTube(ytLink, on_progress_callback=on_progress)
    video = ytObject.streams.get_highest_resolution()
    title.configure(text=ytObject.title, text_color="white")
    finishLabel.configure("")
    video.download()

    # Get the downloaded file's name
    file_name = video.default_filename

    # Convert the downloaded MP4 to WAV using FFmpeg
    convert_mp4_to_wav(file_name, path)

    finishLabel.configure(text="Downloaded and Converted!")
  except Exception as e: 
    print(e)
    finishLabel.configure(text="Download Error", text_color="red")

def on_progress(stream, chunk, bytes_remaining):
  total_size = stream.filesize
  bytes_downloaded = total_size - bytes_remaining
  percentage_of_completion = bytes_downloaded / total_size * 100
  per = str(int(percentage_of_completion))
  progPercent.configure(text=per + '%')
  progPercent.update()

  # Update Progress Bar
  progressBar.set(float(percentage_of_completion) / 100)

def convert_mp4_to_wav(input_file, output_path):
    # Output file name (WAV)
    output_file = os.path.join(output_path, os.path.splitext(input_file)[0] + ".wav")
    
    # FFmpeg command to convert MP4 to WAV
    command = f"ffmpeg -i \"{input_file}\" \"{output_file}\""
    
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting to WAV: {e}")
    
    # Optional: Remove the original MP4 file
    os.remove(input_file)

# System Settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("720x400")
app.title("YouTube Downloader")

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Insert youtube link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progress Percentage
progPercent = customtkinter.CTkLabel(app, text="0%")
progPercent.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# Download Button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

# Run app
app.mainloop()

