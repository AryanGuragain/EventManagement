import os
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
import traceback
import tkinter.messagebox as messagebox
import subprocess
import platform

# Refined Color Palette - Professional and Minimalistic
PRIMARY_COLOR = "#2C3E50"      # Charcoal Blue - Elegant Base Color
SECONDARY_COLOR = "#34495E"    # Dark Slate Blue - Subtle Depth
ACCENT_COLOR = "#ECF0F1"       # Light Cloud Gray - Clean Background
BUTTON_COLOR = "#2980B9"       # Calm Blue - Sophisticated Interaction
TEXT_COLOR = "#2C3E50"         # Dark Charcoal for Readability

# Function to maximize window across different platforms
def maximize_window(root):
    system = platform.system().lower()
    
    if system == "windows":
        root.geometry("1200x1800")
    elif system == "darwin":  # macOS
        # First set the position and size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        # macOS does not have a direct way to maximize, so we set the geometry to cover the screen
    else:  # Linux and other Unix-like systems
        root.attributes('-zoomed', True)

# Function to restore window size
def restore_window(root):
    system = platform.system().lower()
    
    if system == "windows":
        root.state('normal')
        root.geometry('1024x768')  # Reset to a reasonable default size
    elif system == "darwin":  # macOS
        root.geometry('1024x768')  # Reset to a reasonable default size
    else:  # Linux and other Unix-like systems
        root.attributes('-zoomed', False)
        root.geometry('1024x768')  # Reset to a reasonable default size

# Function to display error message in a message box
def show_error(error):
    messagebox.showerror("Error", str(error))
    traceback.print_exc()

# Function to handle ticket purchase by launching ui2.py with event data
def purchase_ticket(event):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to ui2.py
    ui2_path = os.path.join(current_dir, "ui2.py")
    
    try:
        # Pass event data as command-line arguments
        subprocess.Popen([
            "python3", ui2_path,
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
        print("Tickets menu item clicked!")  # Debug statement
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to ticket.py
        tickets_path = os.path.join(current_dir, "ticket.py")
        
        try:
            subprocess.Popen(["python3", tickets_path])
        except Exception as e:
            show_error(f"Error launching ticket.py: {str(e)}")
    elif item == "Events":
        print("Events menu item clicked!")  # Debug statement
        messagebox.showinfo("Info", "Events menu item clicked!")
    elif item == "Stats":
        print("Stats menu item clicked!")  # Debug statement
        messagebox.showinfo("Info", "Stats menu item clicked!")
    elif item == "My Account":
        print("My Account menu item clicked!")  # Debug statement
        messagebox.showinfo("Info", "My Account menu item clicked!")

# Function to create an event card widget
def create_event_card(parent, event):
    # Main card frame
    card = tk.Frame(parent, bg="white", relief=tk.FLAT, borderwidth=1, 
                    highlightthickness=1, highlightbackground=SECONDARY_COLOR, padx=20, pady=20)
    card.config(width=380, height=500)  # Set the width and height
    card.grid_propagate(False)  # Prevent the card from resizing based on its contents
    
    # Create a container for all widgets
    content_frame = tk.Frame(card, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Event Image
    try:
        img_path = event.get("image", "")
        if img_path and os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((380, 220), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            image_label = tk.Label(content_frame, image=img, bg="white")
            image_label.image = img  # Keep a reference to avoid garbage collection
            image_label.pack(pady=10)
        else:
            error_label = tk.Label(content_frame, text="Image Not Found", bg="white", fg="red")
            error_label.pack(pady=5)
    except Exception as e:
        print(f"Error loading image: {e}")
        error_label = tk.Label(content_frame, text="Image Error", bg="white", fg="red")
        error_label.pack(pady=5)

    # Info container frame (for left-aligned text)
    info_frame = tk.Frame(content_frame, bg="white")
    info_frame.pack(fill=tk.X, padx=15, pady=10)

    # Event Date
    date_label = tk.Label(info_frame, text=event["date"], 
                          bg="white", fg=BUTTON_COLOR, 
                          font=("Helvetica", 16), anchor="w")
    date_label.pack(fill=tk.X)

    # Event Title
    title_label = tk.Label(
        info_frame, text=event["title"], bg="white", fg=PRIMARY_COLOR, 
        font=("Helvetica", 18), anchor="w", justify="left"
    )
    title_label.pack(fill=tk.X, pady=(5,0))

    # Event Time and Location
    time_label = tk.Label(info_frame, text=event["time"], bg="white", fg=TEXT_COLOR, 
                          font=("Helvetica", 12), anchor="w")
    time_label.pack(fill=tk.X)

    location_label = tk.Label(info_frame, text=event["location"], bg="white", fg=TEXT_COLOR, 
                              font=("Helvetica", 12), anchor="w")
    location_label.pack(fill=tk.X)

    # Bottom container for price and button
    bottom_frame = tk.Frame(content_frame, bg="white")
    bottom_frame.pack(fill=tk.X, padx=15, pady=(10,0))

    # Price Information (left side)
    price_label = tk.Label(bottom_frame, text=f"NPR {event['ticket_price']}", 
                           bg="white", fg=BUTTON_COLOR, 
                           font=("Helvetica", 14), anchor="w")
    price_label.pack(side=tk.LEFT)

    # Submit Button (right side)
    submit_button = tk.Button(bottom_frame, text="Buy Tickets", 
                             bg=BUTTON_COLOR, fg=ACCENT_COLOR,
                             font=("Helvetica", 12),
                             command=lambda: purchase_ticket(event))
    submit_button.pack(side=tk.RIGHT)

    # Bind click event
    def open_purchase(e):
        purchase_ticket(event)

    # Bind click event to the card and its children (except the button)
    widgets_to_bind = [card, content_frame, info_frame] + [
        w for w in info_frame.winfo_children() + content_frame.winfo_children() 
        if not isinstance(w, tk.Button)
    ]
    
    for widget in widgets_to_bind:
        widget.bind("<Button-1>", open_purchase)
        widget.bind("<Enter>", lambda e: root.config(cursor="hand2"))
        widget.bind("<Leave>", lambda e: root.config(cursor=""))

    return card

# Function to calculate the number of columns based on the screen size
def get_number_of_columns():
    screen_width = root.winfo_width()
    if screen_width >= 1200:
        return 3  # Large screens - 3 columns
    elif screen_width >= 800:
        return 2  # Medium screens - 2 columns
    else:
        return 1  # Small screens - 1 column

# Function to update the layout of event cards based on screen size
def update_event_cards(event=None):
    # Clear previous cards
    for widget in container.winfo_children():
        widget.destroy()

    num_columns = get_number_of_columns()

    # Create grid for event cards
    for i, event in enumerate(events):
        row = i // num_columns
        column = i % num_columns
        
        card = create_event_card(container, event)
        card.grid(row=row, column=column, padx=15, pady=20, sticky="nsew")
        
        # Configure grid column and row weights for responsiveness
        container.grid_columnconfigure(column, weight=1)
        container.grid_rowconfigure(row, weight=1)

try:
    # Create the main window
    root = tk.Tk()
    root.title("Samaaye Events")
    
    # Configure window properties after initialization
    root.update_idletasks()
    
    # Cross-platform window maximization
    maximize_window(root)
    
    root.configure(bg=ACCENT_COLOR)

    # Header - Professional, sleek design
    header = tk.Frame(root, bg=PRIMARY_COLOR, height=80)
    header.grid(row=0, column=0, sticky="ew")

    logo = tk.Label(header, text="Samaaye Events", bg=PRIMARY_COLOR, fg=ACCENT_COLOR, 
                    font=("Helvetica", 24))
    logo.pack(side=tk.LEFT, padx=30, pady=20)

    menu = tk.Frame(header, bg=PRIMARY_COLOR)
    menu.pack(side=tk.RIGHT, padx=30)

    for menu_item in ["Events", "Tickets", "Stats", "My Account"]:
        menu_label = tk.Label(menu, text=menu_item, bg=PRIMARY_COLOR, fg=ACCENT_COLOR, 
                              font=("Helvetica", 14))
        menu_label.pack(side=tk.LEFT, padx=20)
        # Bind click event to menu items
        menu_label.bind("<Button-1>", lambda e, item=menu_item: handle_menu_click(item))

    # Title - Clean, minimalistic
    title = tk.Label(root, text="Upcoming Events", bg=ACCENT_COLOR, fg=PRIMARY_COLOR, 
                     font=("Helvetica", 32))
    title.grid(row=1, column=0, pady=30)

    # Event Cards Container
    container = tk.Frame(root, bg=ACCENT_COLOR)
    container.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    # Configure grid weights for responsiveness
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Sample Event Data with Relative Image Paths
    events = [
        {
            "title": "The Big 3 (2nd Show)",
            "date": "5 Dec",
            "time": "6:00 PM onwards",
            "location": "LOD, Thamel",
            "image": os.path.join(os.path.dirname(__file__), "abc.png"),
            "ticket_price": 500,
            "available_tickets": 100
        },
        {
            "title": "Nepal Premier League",
            "date": "19 Dec",
            "time": "9:15 AM onwards",
            "location": "TU Cricket Ground",
            "image": os.path.join(os.path.dirname(__file__), "npl.png"),
            "ticket_price": 750,
            "available_tickets": 250
        },
        {
            "title": "Grasslands Carnival",
            "date": "5 Dec",
            "time": "4:30 PM onwards",
            "location": "Patan Durbar Square",
            "image": os.path.join(os.path.dirname(__file__), "grass.jpg"),
            "ticket_price": 350,
            "available_tickets": 75
        }
    ]

    # Initial layout update
    update_event_cards()

    # Bind event to update layout when window is resized
    def resize_handler(event):
        if event.widget == root:
            update_event_cards()

    root.bind("<Configure>", resize_handler)

    # Bind the Escape key to exit maximized mode
    def exit_maximized(event):
        restore_window(root)

    root.bind("<Escape>", exit_maximized)

    # Run the application
    root.mainloop()

except Exception as e:
    show_error(e)
