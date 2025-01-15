import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import traceback
import subprocess
import platform

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
    if item == "Tickets":
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tickets_path = os.path.abspath(os.path.join(current_dir, "ticket.py"))
        try:
            subprocess.Popen(["python3", tickets_path])
        except Exception as e:
            show_error(f"Error launching ticket.py: {str(e)}")
    else:
        messagebox.showinfo("Info", f"{item} menu item clicked!")

# Function to create an event card widget
def create_event_card(parent, event, row, column):
    card = tk.Frame(parent, bg="white", relief=tk.FLAT, borderwidth=1,
                    highlightthickness=1, highlightbackground=SECONDARY_COLOR, padx=20, pady=20)
    card.config(width=380, height=500)
    card.grid_propagate(False)

    content_frame = tk.Frame(card, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Reduce the image size for better layout
    try:
        img_path = event.get("image", "")
        if img_path and os.path.exists(img_path):
            img = Image.open(img_path).resize((380, 180), Image.LANCZOS)  # Reduced size
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

# Function to calculate the number of columns based on the screen size
def get_number_of_columns():
    screen_width = root.winfo_width()
    if screen_width >= 1200:
        return 3  # 3 columns for wide screens
    elif screen_width >= 800:
        return 2  # 2 columns for medium screens
    return 1  # 1 column for smaller screens

# Function to update the layout of event cards
def update_event_cards(event=None):
    for widget in container.winfo_children():
        widget.grid_forget()  # Forget the old widgets before updating

    num_columns = get_number_of_columns()  # Get the number of columns dynamically
    num_rows = (len(events) // num_columns) + (1 if len(events) % num_columns > 0 else 0)  # Calculate rows

    # Create event cards and place them in the grid
    for i, event in enumerate(events):
        row, column = divmod(i, num_columns)
        card = create_event_card(container, event, row, column)
        card.grid(row=row, column=column, padx=15, pady=20, sticky="nsew")

    # Adjust grid column and row weights for resizing
    for col in range(num_columns):
        container.grid_columnconfigure(col, weight=1)
    for row in range(num_rows):
        container.grid_rowconfigure(row, weight=1)

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

    container = tk.Frame(root, bg=ACCENT_COLOR)
    container.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # List of 6 events (Ensure all 6 events are present)
    events = [
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
    ]

    update_event_cards()  # Initial render of events
    root.bind("<Configure>", lambda e: update_event_cards() if e.widget == root else None)

    root.bind("<Escape>", lambda e: root.state('normal'))
    root.mainloop()

except Exception as e:
    show_error(e)