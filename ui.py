import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import traceback
import subprocess
import platform
import sqlite3

# Refined Color Palette - Professional and Minimalistic
PRIMARY_COLOR = "#2C3E50"      # Charcoal Blue - Elegant Base Color
SECONDARY_COLOR = "#34495E"    # Dark Slate Blue - Subtle Depth
ACCENT_COLOR = "#ECF0F1"       # Light Cloud Gray - Clean Background
BUTTON_COLOR = "#2980B9"       # Calm Blue - Sophisticated Interaction
TEXT_COLOR = "#2C3E50"         # Dark Charcoal for Readability

# Function to display error message in a message box
def show_error(error):
    messagebox.showerror("Error", str(error))
    traceback.print_exc()

# Function to handle ticket purchase by launching ui2.py with event data
def purchase_ticket(event):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ui2_path = os.path.abspath(os.path.join(current_dir, "ui2.py"))
    try:
        subprocess.Popen([
            "python", ui2_path,
            event["title"],
            event["date"],
            event["time"],
            event["location"],
            str(event["ticket_price"]),
            str(event["available_tickets"]),
        ])
    except Exception as e:
        show_error(f"Error launching ui2.py: {str(e)}")

# Function to handle menu item clicks
def handle_menu_click(item):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if item == "Tickets":
        tickets_path = os.path.abspath(os.path.join(current_dir, "ticket.py"))
        try:
            subprocess.Popen(["python3", tickets_path])
        except Exception as e:
            show_error(f"Error launching ticket.py: {str(e)}")
    elif item == "My Account":
        main_path = os.path.abspath(os.path.join(current_dir, "main.py"))
        try:
            subprocess.Popen(["python3", main_path])
        except Exception as e:
            show_error(f"Error launching main.py: {str(e)}")
    else:
        messagebox.showinfo("Info", f"{item} menu item clicked!")

# Function to create an event card widget
def create_event_card(parent, event):
    card = tk.Frame(parent, bg="white", relief=tk.FLAT, borderwidth=1,
                    highlightthickness=1, highlightbackground=SECONDARY_COLOR, padx=20, pady=20)
    card.config(width=530, height=700)  # Reduced width to 530 pixels
    card.grid_propagate(False)

    content_frame = tk.Frame(card, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Reduce the image size for better layout
    try:
        img_path = event.get("image", "")
        if img_path and os.path.exists(img_path):
            img = Image.open(img_path).resize((530, 300), Image.LANCZOS)  # Adjusted size for the image
            img = ImageTk.PhotoImage(img)
            image_label = tk.Label(content_frame, image=img, bg="white")
            image_label.image = img
            image_label.pack(pady=10)
        else:
            tk.Label(content_frame, text="Image Not Found", bg="white", fg="red").pack(pady=5)
    except Exception:
        tk.Label(content_frame, text="Image Error", bg="white", fg="red").pack(pady=5)

    # Info section with event details
    info_frame = tk.Frame(content_frame, bg="white")
    info_frame.pack(fill=tk.X, padx=15, pady=10)

    tk.Label(info_frame, text=event["date"], bg="white", fg=BUTTON_COLOR, font=("Helvetica", 16)).pack(fill=tk.X)
    tk.Label(info_frame, text=event["title"], bg="white", fg=PRIMARY_COLOR, font=("Helvetica", 18)).pack(fill=tk.X, pady=(5, 0))
    tk.Label(info_frame, text=event["time"], bg="white", fg=TEXT_COLOR, font=("Helvetica", 12)).pack(fill=tk.X)
    tk.Label(info_frame, text=event["location"], bg="white", fg=TEXT_COLOR, font=("Helvetica", 12)).pack(fill=tk.X)

    # Bottom section with the "Buy Tickets" button
    bottom_frame = tk.Frame(content_frame, bg="white")
    bottom_frame.pack(fill=tk.X, padx=15, pady=(10, 0))

    tk.Label(bottom_frame, text=f"NPR {event['ticket_price']}", bg="white", fg=BUTTON_COLOR, font=("Helvetica", 14)).pack(side=tk.LEFT)
    tk.Button(bottom_frame, text="Buy Tickets", bg=BUTTON_COLOR, fg=ACCENT_COLOR, font=("Helvetica", 12),
              command=lambda: purchase_ticket(event)).pack(side=tk.RIGHT)

    return card

# Function to update the layout of event cards
def update_event_cards(event=None):
    for widget in container.winfo_children():
        widget.grid_forget()  # Forget the old widgets before updating

    num_columns = 3  # Fixed number of columns
    num_rows = 4     # Fixed number of rows
    total_slots = num_columns * num_rows

    # Create event cards and place them in the grid
    for i, event in enumerate(events):
        row, column = divmod(i, num_columns)
        card = create_event_card(container, event)
        card.grid(row=row, column=column, padx=15, pady=20, sticky="nsew")

    # Fill remaining slots with empty frames if there are fewer events than total slots
    for i in range(len(events), total_slots):
        row, column = divmod(i, num_columns)
        empty_frame = tk.Frame(container, bg=ACCENT_COLOR, width=530, height=700)
        empty_frame.grid_propagate(False)
        empty_frame.grid(row=row, column=column, padx=15, pady=20, sticky="nsew")

    # Adjust grid column and row weights for resizing
    for col in range(num_columns):
        container.grid_columnconfigure(col, weight=1)
    for row in range(num_rows):
        container.grid_rowconfigure(row, weight=1)

def fetch_events_from_db():
    """Fetch events from the database and append to the events list."""
    try:
        conn = sqlite3.connect('samaaye_events.db')
        cursor = conn.cursor()
        cursor.execute('SELECT title, date, time, location, ticket_price, image_path FROM events')
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            event = {
                "title": row[0],
                "date": row[1],
                "time": row[2],
                "location": row[3],
                "ticket_price": row[4],
                "image": row[5] if row[5] else ""
            }
            events.append(event)
    except sqlite3.Error as e:
        show_error(f"Database Error: {str(e)}")

try:
    root = tk.Tk()
    root.title("Samaaye Events")
    root.update_idletasks()

    if platform.system() == "Windows":
        root.state('zoomed')
    elif platform.system() == "Darwin":  # macOS
        root.attributes('-fullscreen', True)
    elif platform.system() == "Linux":
        root.attributes('-zoomed', True)
    else:
        root.state('zoomed')

    root.configure(bg=ACCENT_COLOR)

    header = tk.Frame(root, bg=PRIMARY_COLOR, height=80)
    header.grid(row=0, column=0, sticky="ew")

    logo = tk.Label(header, text="Samaaye Events", bg=PRIMARY_COLOR, fg=ACCENT_COLOR, font=("Helvetica", 24))
    logo.pack(side=tk.LEFT, padx=30, pady=20)

    menu = tk.Frame(header, bg=PRIMARY_COLOR)
    menu.pack(side=tk.RIGHT, padx=30)

    for menu_item in ["Events", "Tickets", "Stats", "My Account"]:
        menu_label = tk.Label(menu, text=menu_item, bg=PRIMARY_COLOR, fg=ACCENT_COLOR, font=("Helvetica", 14))
        menu_label.pack(side=tk.LEFT, padx=20)
        menu_label.bind("<Button-1>", lambda e, item=menu_item: handle_menu_click(item))

    title = tk.Label(root, text="Upcoming Events", bg=ACCENT_COLOR, fg=PRIMARY_COLOR, font=("Helvetica", 32))
    title.grid(row=1, column=0, pady=30)

    # Create a canvas and a scrollbar
    canvas = tk.Canvas(root, bg=ACCENT_COLOR, width=1550)  # Adjusted canvas width for larger event cards
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Create the container frame inside the scrollable frame
    container = tk.Frame(scrollable_frame, bg=ACCENT_COLOR)
    container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Adjust the grid configuration to allow full width
    canvas.grid(row=2, column=0, sticky="nsew")
    scrollbar.grid(row=2, column=1, sticky="ns")

    # Configure the grid weights to allow the canvas to expand
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=0)  # Optional: if you want the scrollbar to have a fixed width

    # Initialize the events list
    events = []

    # List of hardcoded events
    events.extend([
        {"title": "The Big 3 (2nd Show)", "date": "5 Dec", "time": "6:00 PM onwards", "location": "LOD, Thamel",
         "image": os.path.join(os.path.dirname(__file__), "abc.png"), "ticket_price": 500, "available_tickets": 100},
        {"title": "Nepal Premier League", "date": "19 Dec", "time": "9:15 AM onwards", "location": "TU Cricket Ground",
         "image": os.path.join(os.path.dirname(__file__), "npl.png"), "ticket_price": 750, "available_tickets": 250},
        {"title": "Grasslands Carnival", "date": "5 Dec", "time": "4:30 PM onwards", "location": "Patan Durbar Square",
         "image": os.path.join(os.path.dirname(__file__), "grass.jpg"), "ticket_price": 350, "available_tickets": 75},
        {"title": "Rock Festival", "date": "10 Dec", "time": "5:00 PM onwards", "location": "City Center",
         "image": os.path.join(os.path.dirname(__file__), "images.jpeg"), "ticket_price": 600, "available_tickets": 150},
        {"title": "Tech Conference 2025", "date": "23 Dec", "time": "9:00 AM onwards", "location": "Kathmandu",
         "image": os.path.join(os.path.dirname(__file__), "maxresdefault.png"), "ticket_price": 800, "available_tickets": 200},
        {"title": "New Year's Eve Party", "date": "31 Dec", "time": "10:00 PM onwards", "location": "City Hall",
         "image": os.path.join(os.path.dirname(__file__), "TentCardversion.png"), "ticket_price": 1200, "available_tickets": 500},
    ])

    # Fetch events from the database
    fetch_events_from_db()
    fetch_events_from_db()
    fetch_events_from_db()
    fetch_events_from_db()

    update_event_cards()  # Initial render of events
    root.bind("<Configure>", lambda e: update_event_cards() if e.widget == root else None)

    root.bind("<Escape>", lambda e: root.state('normal'))
    root.mainloop()

except Exception as e:
    show_error(e)