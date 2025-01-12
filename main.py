# from tkinter import *
# from tkinter import ttk

# from Book import Book 
# from CreateEvent import CreateEvent
# from ViewTickets import ViewTickets
# from ViewEvents import ViewEvents
# from CancelTicket import CancelTicket

# # Initialize main application window
# top = Tk()
# top.geometry('700x800')  # Start with a larger window size for big screens
# top.title('Event Management')
# top.configure(bg="#f4f4f9")  # Light background color for a more professional look

# # Gradient Banner
# banner_frame = Frame(top, bg="#4B0082", height=100)  # Dark Indigo gradient background
# banner_frame.pack(fill=X, padx=0, pady=0)

# # Title Label in the banner
# Label(
#     banner_frame,
#     text="Event Management System", 
#     bg="#4B0082",  # Dark Indigo background
#     fg="white", 
#     font=("Helvetica", 26, 'bold'), 
#     width=50, 
#     height=2
# ).pack(pady=(20, 10))

# # Frame for buttons
# button_frame = Frame(top, bg="#f4f4f9")
# button_frame.pack(pady=40, fill=BOTH, expand=True)

# # Button Style
# def create_button(text, command):
#     return ttk.Button(button_frame, text=text, command=command, style='TButton')

# # Button Style Configuration
# style = ttk.Style()
# style.configure('TButton',
#                 font=('Helvetica', 14, 'bold'),
#                 padding=15,
#                 width=20,
#                 anchor='center')

# style.map('TButton', background=[('active', '#9932cc')], foreground=[('active', 'white')])  # Hover effect

# # Grid Layout Configuration
# button_frame.columnconfigure(0, weight=1)
# button_frame.columnconfigure(1, weight=1)
# button_frame.rowconfigure(0, weight=1)
# button_frame.rowconfigure(1, weight=1)
# button_frame.rowconfigure(2, weight=1)

# # Create buttons with grid layout
# create_button('Book Ticket', lambda: Book()).grid(row=0, column=0, padx=20, pady=20, sticky='ew')
# create_button('Create Event', lambda: CreateEvent()).grid(row=0, column=1, padx=20, pady=20, sticky='ew')
# create_button('View Tickets', lambda: ViewTickets()).grid(row=1, column=0, padx=20, pady=20, sticky='ew')
# create_button('View Events', lambda: ViewEvents()).grid(row=1, column=1, padx=20, pady=20, sticky='ew')
# create_button('Cancel Ticket', lambda: CancelTicket()).grid(row=2, column=0, padx=20, pady=20, sticky='ew')
# create_button('Quit App', lambda: top.destroy()).grid(row=2, column=1, padx=20, pady=20, sticky='ew')

# # Footer Label with professional design
# Label(
#     top,
#     text="© 2023 Event Management Project | FOCP Designed by Aryan Guragain & Co.",
#     bg="#f4f4f9",
#     fg="#4B0082",  # Dark Indigo footer text
#     font=("Helvetica", 10, 'italic')
# ).pack(side=BOTTOM, pady=(20, 10))

# # Make the window responsive
# top.grid_rowconfigure(0, weight=1)
# top.grid_rowconfigure(1, weight=1)
# top.grid_rowconfigure(2, weight=1)

# top.mainloop()
from tkinter import *
from tkinter import ttk

from Book import Book 
from CreateEvent import CreateEvent
from ViewTickets import ViewTickets
from ViewEvents import ViewEvents
from CancelTicket import CancelTicket

# Initialize main application window
top = Tk()
top.geometry('700x800')  # Start with a larger window size for big screens
top.title('Event Management')
top.configure(bg="#f4f4f9")  # Light background color for a more professional look

# Gradient Banner
banner_frame = Frame(top, bg="#4B0082", height=100)  # Dark Indigo gradient background
banner_frame.pack(fill=X, padx=0, pady=0)

# Title Label in the banner
Label(
    banner_frame,
    text="Event Management System", 
    bg="#4B0082",  # Dark Indigo background
    fg="white", 
    font=("Helvetica", 26, 'bold'), 
    width=50, 
    height=2
).pack(pady=(20, 10))

# Frame for buttons
button_frame = Frame(top, bg="#f4f4f9")
button_frame.pack(pady=40, fill=BOTH, expand=True)

# Button Style
def create_button(text, command):
    return ttk.Button(button_frame, text=text, command=command, style='TButton')

# Button Style Configuration
style = ttk.Style()
style.configure('TButton',
                font=('Helvetica', 14, 'bold'),
                padding=15,
                width=20,
                anchor='center')

style.map('TButton', background=[('active', '#9932cc')], foreground=[('active', 'white')])  # Hover effect

# Grid Layout Configuration
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.rowconfigure(0, weight=1)
button_frame.rowconfigure(1, weight=1)
button_frame.rowconfigure(2, weight=1)
button_frame.rowconfigure(3, weight=1)  # Added an extra row for the new button

# Create buttons with grid layout
create_button('Book Ticket', lambda: Book()).grid(row=0, column=0, padx=20, pady=20, sticky='ew')
create_button('Create Event', lambda: CreateEvent()).grid(row=0, column=1, padx=20, pady=20, sticky='ew')
create_button('View Tickets', lambda: ViewTickets()).grid(row=1, column=0, padx=20, pady=20, sticky='ew')
create_button('View Events', lambda: ViewEvents()).grid(row=1, column=1, padx=20, pady=20, sticky='ew')
create_button('Cancel Ticket', lambda: CancelTicket()).grid(row=2, column=0, padx=20, pady=20, sticky='ew')
create_button('Show Graph', lambda: ShowGraph()).grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky='ew')  # New button for graph
create_button('Quit App', lambda: top.destroy()).grid(row=2, column=1, padx=20, pady=20, sticky='ew')

# Footer Label with professional design
Label(
    top,
    text="© 2023 Event Management Project | FOCP Designed by Aryan Guragain & Co.",
    bg="#f4f4f9",
    fg="#4B0082",  # Dark Indigo footer text
    font=("Helvetica", 10, 'italic')
).pack(side=BOTTOM, pady=(20, 10))

# Make the window responsive
top.grid_rowconfigure(0, weight=1)
top.grid_rowconfigure(1, weight=1)
top.grid_rowconfigure(2, weight=1)

top.mainloop()