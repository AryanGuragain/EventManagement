import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For working with images

# Create the main window
root = tk.Tk()
root.title("Events")
root.geometry("900x700")
root.configure(bg="#f4f4f4")

# Header
header = tk.Frame(root, bg="#d168f7", height=80)
header.pack(fill=tk.X)

logo = tk.Label(header, text="XYZ Company", bg="#d168f7", fg="white", font=("Arial", 20, "bold"))
logo.pack(side=tk.LEFT, padx=20, pady=20)

menu = tk.Frame(header, bg="#d168f7")
menu.pack(side=tk.RIGHT, padx=20)

for menu_item in ["Events", "Tickets", "Stats", "My Account"]:
    menu_label = tk.Label(menu, text=menu_item, bg="#d168f7", fg="white", font=("Arial", 14))
    menu_label.pack(side=tk.LEFT, padx=10)

# Title
title = tk.Label(root, text="Events", bg="#f4f4f4", fg="#000", font=("Arial", 24, "bold"))
title.pack(pady=10)

# Event Cards Container
container = tk.Frame(root, bg="#f4f4f4")
container.pack(padx=20, pady=10)

# Sample Event Data with Image Paths
events = [
    {
        "title": "The Big 3 (2nd Show)",
        "date": "5 Dec",
        "time": "6:00 PM onwards",
        "location": "LOD, Thamel",
        "image": "C:\\Users\\ACER\\Desktop\\python p\\EventManagement\\abc.png",  # Replace with your image path
    },
    {
        "title": "Nepal Premier League",
        "date": "19 Dec",
        "time": "9:15 AM onwards",
        "location": "TU Cricket Ground",
        "image": "C:\\Users\\ACER\\Desktop\\python p\\EventManagement\\npl.png",   # Replace with your image path
    },
    {
        "title": "Grasslands Carnival",
        "date": "5 Dec",
        "time": "4:30 PM onwards",
        "location": "Patan Durbar Square",
        "image": "C:\\Users\\ACER\\Desktop\\python p\\EventManagement\\grass.jpg",  # Replace with your image path
    },
]

# Function to create event cards
def create_event_card(parent, event):
    card = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=2)
    card.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")

    # Event Image
    try:
        img = Image.open(event["image"])
        img = img.resize((180, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        image_label = tk.Label(card, image=img, bg="white")
        image_label.image = img  # Keep a reference to avoid garbage collection
        image_label.pack(pady=5)
    except Exception as e:
        error_label = tk.Label(card, text="Image Not Found", bg="white", fg="red")
        error_label.pack(pady=5)

    # Event Date
    date_label = tk.Label(card, text=event["date"], bg="red", fg="white", font=("Arial", 16, "bold"))
    date_label.pack(fill=tk.X)

    # Event Title
    title_label = tk.Label(
        card, text=event["title"], bg="white", fg="black", font=("Arial", 14, "bold"), wraplength=180, justify="center"
    )
    title_label.pack(pady=10)

    # Event Time and Location
    time_label = tk.Label(card, text=event["time"], bg="white", fg="gray", font=("Arial", 12))
    time_label.pack()

    location_label = tk.Label(card, text=event["location"], bg="white", fg="gray", font=("Arial", 12))
    location_label.pack()

    # Buy Ticket Button
    buy_button = tk.Button(card, text="Buy Ticket", bg="orange", fg="white", font=("Arial", 12, "bold"))
    buy_button.pack(pady=10, padx=5)

    return card

# Create rows of event cards
for i in range(2):  # Two rows
    row_frame = tk.Frame(container, bg="#f4f4f4")
    row_frame.pack()

    for event in events:
        create_event_card(row_frame, event)

# Run the application
root.mainloop()