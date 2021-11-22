import os
from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('NPR_MP3 player')
root.geometry('550x400')

# Initialize Pygame Mixer
pygame.mixer.init()

# Grab Song length Time info
def play_time():
    # Check for double timing
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000

    # Throw up temp label to get data
    # slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')

    # convert to time format
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    # Get the current song tuple number
    # current_song = song_box.curselection()
    # Grab song title from the playlist
    song = song_box.get(ACTIVE)
    # Add directory structure, add .mp3 to the song title
    path = os.getcwd()
    song_path = os.path.dirname(path)
    song = f"{song_path}/Sounds/" + f'{song}.mp3'
    # Load song with mutagen
    song_mut = MP3(song)
    # Get song length with Mutagen
    global song_length

    song_length = song_mut.info.length
    # Convert to Time Format
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    # Increase current_time by 1 sec
    current_time += 1

    if int(my_slider.get())==int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} of {converted_song_length}  ')

    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        # Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        # convert to time format
        converted_current_time = time.strftime('%H:%M:%S', time.gmtime(int(my_slider.get())))

        # output time to status Bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

        # Move this thing along by one second
        next_time = int(my_slider.get()) +1
        my_slider.config(value=next_time)

    # output time to status Bar
    # status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
    # Update slider position to current song position
    # my_slider.config(value=int(current_time))

    # update time
    status_bar.after(1000, play_time)

# Add Song function
def add_song():
    song = filedialog.askopenfilename(initialdir='Sounds/', title="Choose A Song",
                                      filetypes=(("mp3 Files", "*.mp3"), ("Any files", "*.*")))
    print(song)
    # Strip out the path and file type extention
    song = song.split('/')[-1]
    song = song.replace(".mp3", "")
    # Insert into the playlist
    song_box.insert(END, song)

# Add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='Sounds/', title="Choose Multiple Songs",
                                      filetypes=(("mp3 Files", "*.mp3"), ("Any files", "*.*")))
    # loop through song list and replace directory info and mp3
    for song in songs:
        song = song.split('/')[-1]
        song = song.replace(".mp3", "")
        # Insert into the playlist
        song_box.insert(END, song)


# Play selected song
def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    # print(song)
    path = os.getcwd()
    song_path = os.path.dirname(path)
    song = f"{song_path}/Sounds/"+f'{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Call the ply_time function to get song length
    play_time()

    # Update slider to position
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)


# Create Global Pause variable
global paused
paused = False

# Pause and Unpause the Current song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # pause
        pygame.mixer.music.pause()
        paused = True

# Stop playing current song
global stopped
stopped = False
def stop():
    # Reset slider and status Bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # Stop song from playing
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # Clear the status bar
    status_bar.config(text='')

    # Set Stop variable to True
    global stopped
    stopped = True

# Play the Next song in the playlist
def next_song():
    # Reset slider and status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song tuple number
    next_one = song_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]+1
    # Grab song title from the playlist
    song = song_box.get(next_one)

    # Add directory structure, add .mp3 to the song title
    path = os.getcwd()
    song_path = os.path.dirname(path)
    song = f"{song_path}/Sounds/" + f'{song}.mp3'
    # play the song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in the playlist listbox
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(next_one)

    # Highlight the selected bar
    song_box.selection_set(next_one, last=None)

# Play previous song in te playlist
def previous_song():
    # Reset slider and status Bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song tuple number
    next_one = song_box.curselection()
    # Add one to the current song number
    next_one = next_one[0] - 1
    # Grab song title from the playlist
    song = song_box.get(next_one)

    # Add directory structure, add .mp3 to the song title
    path = os.getcwd()
    song_path = os.path.dirname(path)
    song = f"{song_path}/Sounds/" + f'{song}.mp3'
    # play the song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in the playlist listbox
    song_box.selection_clear(0, END)

    # Activate new song bar
    song_box.activate(next_one)

    # Highlight the selected bar
    song_box.selection_set(next_one, last=None)

# Delete a song
def delete_song():
    stop()
    # Delete Currently selected song from the playlist
    song_box.delete(ANCHOR)
    # Stop the music
    pygame.mixer.music.stop()

# Delete all songs from playlist
def delete_all_songs():
    stop()
    # Delete all songs from the playlist
    song_box.delete(0, END)
    # Stop the music
    pygame.mixer.music.stop()

# Create slider function
def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    path = os.getcwd()
    song_path = os.path.dirname(path)
    song = f"{song_path}/Sounds/" + f'{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# Define volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

    # Get current volume
    current_volume = pygame.mixer.music.get_volume()
    slider_label.config(text=f'{int(current_volume * 100)} %')


def mute():
    pygame.mixer.music.set_volume(0)
    current_volume = pygame.mixer.music.get_volume()
    slider_label.config(text=f'{int(current_volume * 100)} %')
    volume_slider.config(value=0)

def unmute():
    pygame.mixer.music.set_volume(0.25)
    current_volume = pygame.mixer.music.get_volume()
    slider_label.config(text=f'{int(current_volume * 100)} %')
    volume_slider.config(value=0.25)


# Creat Master frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# Create Playlist Box
song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground='green', selectforeground="black")
song_box.grid(row=0, column=0)

# Create Player Control Images
back_btn_img = PhotoImage(file='Images/prev50.png')
forwoard_btn_img = PhotoImage(file='Images/next50.png')
play_btn_img = PhotoImage(file='Images/play-button.png')
pause_btn_img = PhotoImage(file='Images/pause.png')
stop_btn_img = PhotoImage(file='Images/stop50_new.png')

# Create Player Control Frame
controls_frame = LabelFrame(master_frame, text='Controls')
controls_frame.grid(row=1, column=0, pady=10, columnspan=2)

# Create volume label frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

# Create Player Control Buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forwoard_button = Button(controls_frame, image=forwoard_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda:pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forwoard_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Song Menu
add_song_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
# Add many song to playlist
add_song_menu.add_command(label="Add Many Song to Playlist", command=add_many_songs)

# Create delete song menu
remove_song_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all song from playlist", command=delete_all_songs)

# Create status bar
status_bar =Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create Music Position slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=500)
my_slider.grid(row=2, column=0, pady=10, columnspan=2)

# Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.grid(row=0, column=0, padx=20, columnspan=2)

# Create Temporary Slider label
slider_label = Label(volume_frame, text='100 %')
slider_label.grid(row=1, column=0, padx=10, columnspan=2)

mute_button = Button(volume_frame, text="Mute", command=mute)
mute_button.grid(row=3, column=0)

unmute_button = Button(volume_frame, text="Unmute", command=unmute)
unmute_button.grid(row=3, column=1)

root.mainloop()
