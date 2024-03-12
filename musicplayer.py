import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import time
import colorsys
import pygame
import os

class music_player():
    
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Bind the closing event to on_close method

        # Title of the window
        self.root.title("Music Player")
        # Window Geometry
        self.root.geometry("500x500+500+200")
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = tk.StringVar()
        # Declaring Status Variable
        self.status = tk.StringVar()
        
        # Creating and Placing Main Frame to hold the gif
        mainframe = tk.Label(text="", fg="green", bg="black")
        mainframe.place(x=0, y=0, width=500, height=400)
        #Finding and loading gif
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "image.gif")
        Image.open(image_path)
        gif = Image.open(image_path)
        # Create a list of frames
        frames = []
        for i in range(gif.n_frames):
            gif.seek(i)
            frames.append(ImageTk.PhotoImage(gif))
        # Define a function to play the animation
        def play_animation(frame_idx):
            mainframe.config(image=frames[frame_idx])
            root.after(50, play_animation, (frame_idx+1) % len(frames))
        play_animation(0)
        
        # Creating and Placing Track Frame for Song label & status label
        trackframe = tk.LabelFrame(bg="black")
        trackframe.place(x=0, y=400, width=500, height=100)
        # Buttons
        playbtn = tk.Button(trackframe, text="⏵", command=self.playsong, width=2, height=1, font=("white rabbit",17,""), fg="green", bg="black")
        playbtn.grid(row=0, column=0, padx=10, pady=1)
        
        stopbtn = tk.Button(trackframe, text="⏸", command=self.stopsong, width=2, height=1, font=("white rabbit",17,""), fg="red", bg="black")
        stopbtn.grid(row=1, column=0, padx=10, pady=1)
        
        filebtn = tk.Button(trackframe, text="⏏", command=self.addsongs, width=2, height=1, font=("white rabbit",17,""), fg="blue", bg="black")
        filebtn.grid(row=2, column=0, padx=10, pady=1)
        
        # Progress Bar
        self.progbar = ttk.Progressbar(trackframe, length=437, mode="determinate")
        self.progbar.place(x=50, y=33)
        
        # Song List
        self.combostyle = ttk.Style()
        self.combostyle.theme_create("combostyle", parent="alt",
            settings={
                "TCombobox": {
                    "configure": {
                        "background": "black",
                        "selectbackground": "green",
                        "fieldbackground": "black",
                        "foreground": "green"
                    }
                },
                "TProgressbar": {
                    "configure": {
                        "troughcolor": "black",
                        "background": "green",
                        "thickness": "55"
                    }
                }
            }
        )
        self.combostyle.theme_use("combostyle")
        
        self.playlist = Combobox(trackframe, state="readonly", font=("white rabbit",16), width=35)
        self.playlist.place(x=50, y=6)
    
    # Rainbow Progress Bar
    def interpolate_color(self, hue):
        # Convert hue value to RGB color
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
    
    def animate_rainbow_effect(self):
        hue = 0  # Initial hue value
        increment = 0.01  # Increment step for hue transition
        self.color_swap = True
        while self.color_swap == True:
            color = self.interpolate_color(hue)
            self.combostyle.configure("TProgressbar", background=color)
            self.root.update()
            time.sleep(0.05)
            hue += increment
            if hue >= 1:
                hue = 0
    
    # File Button Logic - Select a directory, fill song list, and queue a song
    def addsongs(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            os.chdir(folder_path)
            songtracks = os.listdir()
            self.playlist['values'] = songtracks
            self.playlist.current(0)
    
    # Defining Play Song Function
    def playsong(self):
        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get())
        # Playing Selected Song
        pygame.mixer.music.play()
        # Start the Progress Bar
        song_length = pygame.mixer.Sound(self.playlist.get()).get_length()
        self.progbar['maximum'] = song_length
        self.progbar['value'] = 0
        self.update_progress()
        self.animate_rainbow_effect()

    def stopsong(self):
        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get())
        # Playing Selected Song
        pygame.mixer.music.stop()
        # Restart the Progress Bar
        self.color_swap = False
        self.progbar['value'] = 0
        self.progbar['maximum'] = 0
        self.combostyle.configure("TProgressbar", background="black")

    def update_progress(self):
        current_time = pygame.mixer.music.get_pos() / 1000
        self.progbar["value"] = current_time
        self.root.after(75, self.update_progress)
    
    def on_close(self):
        # Stop pygame mixer
        pygame.mixer.quit()
        # Close the window
        self.root.destroy()
        #End RGB loop for colors
        self.color_swap = False
# Creating TK Container
root = tk.Tk()
# Passing Root to MusicPlayer Class
music_player(root)
# Root Window Looping
root.mainloop()
