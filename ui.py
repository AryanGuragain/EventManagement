import os
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
import traceback
import tkinter.messagebox as messagebox
import subprocess
import platform
import sys

# Refined Color Palette
PRIMARY_COLOR = "#2C3E50"
SECONDARY_COLOR = "#34495E"
ACCENT_COLOR = "#ECF0F1"
BUTTON_COLOR = "#2980B9"
TEXT_COLOR = "#2C3E50"

# Function to display error messages
def show_error(error):
    messagebox.showerror("Error", str(error))
    traceback.print_exc()

# Function to handle ticket purchase
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
# Function to handle menu clicks
def handle_menu_click(item):
    try:
        if item == "Tickets":
            ticket_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ticket.py")
            subprocess.Popen([sys.executable, ticket_path]).wait()
        elif item == "My Account":
            main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
            subprocess.Popen([sys.executable, main_path]).wait()  # Open main.py
        else:
            messagebox.showinfo("Info", f"{item} menu item clicked!")
    except Exception as e:
        show_error(f"Error: {e}")

# Function to calculate the number of columns based on the window width
def get_number_of_columns():
    screen_width = root.winfo_width()
    if screen_width >= 1200:
        return 3
    elif screen_width >= 800:
        return 2
    return 1

# Function to update event cards
def update_event_cards():
    for widget in container.winfo_children():
        widget.destroy()

    num_columns = get_number_of_columns()
    for i, event in enumerate(events):
        row, column = divmod(i, num_columns)
        card = create_event_card(container, event)
        card.grid(row=row, column=column, padx=15, pady=20, sticky="nsew")
        container.grid_columnconfigure(column, weight=1)
        container.grid_rowconfigure(row, weight=1)

# Function to create an event card
def create_event_card(parent, event):
    card = tk.Frame(parent, bg="white", relief=tk.FLAT, borderwidth=1,
                    highlightthickness=1, highlightbackground=SECONDARY_COLOR, padx=20, pady=20)
    card.config(width=380, height=500)
    card.grid_propagate(False)

    content_frame = tk.Frame(card, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True)

    try:
        img_path = event.get("image", "")
        if img_path and os.path.exists(img_path):
            img = Image.open(img_path).resize((380, 220), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            image_label = tk.Label(content_frame, image=img, bg="white")
            image_label.image = img
            image_label.pack(pady=10)
        else:
            tk.Label(content_frame, text="Image Not Found", bg="white", fg="red").pack(pady=5)
    except Exception as e:
        tk.Label(content_frame, text="Image Error", bg="white", fg="red").pack(pady=5)

    tk.Label(content_frame, text=event["date"], bg="white", fg=BUTTON_COLOR, font=("Helvetica", 16)).pack(fill=tk.X)
    tk.Label(content_frame, text=event["title"], bg="white", fg=PRIMARY_COLOR, font=("Helvetica", 18)).pack(fill=tk.X, pady=(5, 0))
    tk.Label(content_frame, text=event["time"], bg="white", fg=TEXT_COLOR, font=("Helvetica", 12)).pack(fill=tk.X)
    tk.Label(content_frame, text=event["location"], bg="white", fg=TEXT_COLOR, font=("Helvetica", 12)).pack(fill=tk.X)

    bottom_frame = tk.Frame(content_frame, bg="white")
    bottom_frame.pack(fill=tk.X, padx=15, pady=(10, 0))

    tk.Label(bottom_frame, text=f"NPR {event['ticket_price']}", bg="white", fg=BUTTON_COLOR, font=("Helvetica", 12)).pack(side=tk.LEFT)
    tk.Button(bottom_frame, text="Buy Tickets", bg=BUTTON_COLOR, fg=ACCENT_COLOR, font=("Helvetica", 12),
              command=lambda: purchase_ticket(event)).pack(side=tk.RIGHT)

    return card

# Main Application
try:
    root = tk.Tk()
    root.title("Samaaye Interactives")

    # Set window state based on the operating system
    if platform.system() == "Windows":
        root.state('zoomed')
    elif platform.system() == "Darwin":
        root.attributes('-fullscreen', True)
    else:
        root.geometry("1200x800")

    root.configure(bg=ACCENT_COLOR)

    header = tk.Frame(root, bg=PRIMARY_COLOR, height=80)
    header.grid(row=0, column=0, sticky="ew")

    # Add logo image instead of text
    try:
        logo_path = "Samaaye Interactives.jpg"
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path).resize((150, 80), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(header, image=logo_img, bg=PRIMARY_COLOR)
            logo_label.image = logo_img
            logo_label.pack(side=tk.LEFT, padx=30, pady=20)
        else:
            tk.Label(header, text="Logo Not Found", bg=PRIMARY_COLOR, fg="red", font=("Helvetica", 16)).pack(side=tk.LEFT, padx=30)
    except Exception as e:
        show_error(f"Error loading logo: {e}")

    menu = tk.Frame(header, bg=PRIMARY_COLOR)
    menu.pack(side=tk.RIGHT, padx=30)

    for menu_item in ["Events", "Tickets", "My Account"]:
        menu_label = tk.Label(menu, text=menu_item, bg=PRIMARY_COLOR, fg=ACCENT_COLOR, font=("Helvetica", 14))
        menu_label.pack(side=tk.LEFT, padx=20)
        menu_label.bind("<Button-1>", lambda e, item=menu_item: handle_menu_click(item))

    title = tk.Label(root, text="Upcoming Events", bg=ACCENT_COLOR, fg=PRIMARY_COLOR, font=("Helvetica", 32))
    title.grid(row=1, column=0, pady=30)

    container = tk.Frame(root, bg=ACCENT_COLOR)
    container.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    events = [
        {"title": "The Big 3 (2nd Show)", "date": "5 Dec", "time": "6:00 PM onwards", "location": "LOD, Thamel",
         "image": "abc.png", "ticket_price": 500, "available_tickets": 100},
        {"title": "Nepal Premier League", "date": "19 Dec", "time": "9:15 AM onwards", "location": "TU Cricket Ground",
         "image": "npl.png", "ticket_price": 750, "available_tickets": 250},
        {"title": "Grasslands Carnival", "date": "5 Dec", "time": "4:30 PM onwards", "location": "Patan Durbar Square",
         "image": "grass.jpg", "ticket_price": 350, "available_tickets": 75}
    ]

    update_event_cards()
    root.bind("<Configure>", lambda e: update_event_cards() if e.widget == root else None)
    root.mainloop()

except Exception as e:
    show_error(e)