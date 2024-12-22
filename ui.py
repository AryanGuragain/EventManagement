import os
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
import traceback
import tkinter.messagebox as messagebox

# Refined Color Palette - Professional and Minimalistic
PRIMARY_COLOR = "#2C3E50"      # Charcoal Blue - Elegant Base Color
SECONDARY_COLOR = "#34495E"    # Dark Slate Blue - Subtle Depth
ACCENT_COLOR = "#ECF0F1"       # Light Cloud Gray - Clean Background
BUTTON_COLOR = "#2980B9"       # Calm Blue - Sophisticated Interaction
TEXT_COLOR = "#2C3E50"         # Dark Charcoal for Readability

def show_error(error):
    messagebox.showerror("Error", str(error))
    traceback.print_exc()

try:
    # Create the main window
    root = tk.Tk()
    root.title("Samaaye Events")
    root.geometry("1200x900")  # Adjust initial window size
    root.configure(bg=ACCENT_COLOR)
    root.update_idletasks()  # Ensure proper window initialization

    # Header - Professional, sleek design
    header = tk.Frame(root, bg=PRIMARY_COLOR, height=80)
    header.grid(row=0, column=0, sticky="ew")

    logo = tk.Label(header, text="Samaaye Interactives", bg=PRIMARY_COLOR, fg=ACCENT_COLOR, 
                    font=("Helvetica", 24))
    logo.pack(side=tk.LEFT, padx=30, pady=20)

    menu = tk.Frame(header, bg=PRIMARY_COLOR)
    menu.pack(side=tk.RIGHT, padx=30)

    for menu_item in ["Events", "Tickets", "Stats", "My Account"]:
        menu_label = tk.Label(menu, text=menu_item, bg=PRIMARY_COLOR, fg=ACCENT_COLOR, 
                              font=("Helvetica", 14))
        menu_label.pack(side=tk.LEFT, padx=20)

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
            "image": os.path.join(os.path.dirname(__file__), "/home/sameer-man-shrestha/Desktop/python/EventManagement/abc.png"),
            "ticket_price": 500,
            "available_tickets": 100
        },
        {
            "title": "Nepal Premier League",
            "date": "19 Dec",
            "time": "9:15 AM onwards",
            "location": "TU Cricket Ground",
            "image": os.path.join(os.path.dirname(__file__), "/home/sameer-man-shrestha/Desktop/python/EventManagement/npl.png"),
            "ticket_price": 750,
            "available_tickets": 250
        },
        {
            "title": "Grasslands Carnival",
            "date": "5 Dec",
            "time": "4:30 PM onwards",
            "location": "Patan Durbar Square",
            "image": os.path.join(os.path.dirname(__file__), "/home/sameer-man-shrestha/Desktop/python/EventManagement/grass.jpg"),
            "ticket_price": 350,
            "available_tickets": 75
        },
    ]

    # Function to handle ticket purchase
    def purchase_ticket(event):
        # Create a custom dialog for ticket purchase
        purchase_window = tk.Toplevel(root)
        purchase_window.title(f"Purchase Ticket - {event['title']}")
        purchase_window.geometry("400x500")
        purchase_window.configure(bg=ACCENT_COLOR)

        # Event Details
        tk.Label(purchase_window, text=event['title'], 
                 font=("Helvetica", 20), 
                 bg=ACCENT_COLOR, fg=PRIMARY_COLOR).pack(pady=10)
        tk.Label(purchase_window, text=f"Date: {event['date']}", 
                 font=("Helvetica", 14), 
                 bg=ACCENT_COLOR, fg=TEXT_COLOR).pack()
        tk.Label(purchase_window, text=f"Time: {event['time']}", 
                 font=("Helvetica", 14), 
                 bg=ACCENT_COLOR, fg=TEXT_COLOR).pack()
        tk.Label(purchase_window, text=f"Location: {event['location']}", 
                 font=("Helvetica", 14), 
                 bg=ACCENT_COLOR, fg=TEXT_COLOR).pack(pady=(0,20))

        # Ticket Price and Available Tickets
        tk.Label(purchase_window, text=f"Ticket Price: NPR {event['ticket_price']}", 
                 font=("Helvetica", 16), 
                 bg=ACCENT_COLOR, fg=BUTTON_COLOR).pack()
        tk.Label(purchase_window, text=f"Available Tickets: {event['available_tickets']}", 
                 font=("Helvetica", 14), 
                 bg=ACCENT_COLOR, fg=TEXT_COLOR).pack(pady=(0,20))

        # Number of Tickets Selection
        tk.Label(purchase_window, text="Number of Tickets:", 
                 font=("Helvetica", 14), 
                 bg=ACCENT_COLOR, fg=TEXT_COLOR).pack()
        ticket_var = tk.IntVar(value=1)
        ticket_spinbox = tk.Spinbox(purchase_window, from_=1, to=event['available_tickets'], 
                                    textvariable=ticket_var, width=10, 
                                    font=("Helvetica", 14))
        ticket_spinbox.pack(pady=10)

        # Total Price Calculation
        total_var = tk.StringVar()
        def update_total(*args):
            total = ticket_var.get() * event['ticket_price']
            total_var.set(f"Total: NPR {total}")

        ticket_var.trace('w', update_total)
        total_label = tk.Label(purchase_window, textvariable=total_var, 
                               font=("Helvetica", 16), 
                               bg=ACCENT_COLOR, fg=BUTTON_COLOR)
        total_label.pack(pady=10)

        # Purchase Confirmation
        def confirm_purchase():
            num_tickets = ticket_var.get()
            total = num_tickets * event['ticket_price']
            
            # Simulate payment process
            result = messagebox.askyesno("Confirm Purchase", 
                                         f"Confirm purchase of {num_tickets} ticket(s) for {event['title']}?\n\nTotal: NPR {total}")
            if result:
                messagebox.showinfo("Purchase Successful", 
                                    f"You've purchased {num_tickets} ticket(s) for {event['title']}!")
                purchase_window.destroy()

        purchase_button = tk.Button(purchase_window, text="Purchase", 
                                    command=confirm_purchase, 
                                    bg=BUTTON_COLOR, fg=ACCENT_COLOR, 
                                    font=("Helvetica", 16))
        purchase_button.pack(pady=20)

    # Function to create event cards
    def create_event_card(parent, event):
        # Main card frame
        card = tk.Frame(parent, bg="white", relief=tk.FLAT, borderwidth=1, 
                        highlightthickness=1, highlightbackground=SECONDARY_COLOR, padx=20, pady=20)
        card.config(width=380, height=500)  
        card.grid_propagate(False)  
        
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

        # Event Date
        date_label = tk.Label(content_frame, text=event["date"], 
                              bg="white", fg=BUTTON_COLOR, 
                              font=("Helvetica", 16))
        date_label.pack(fill=tk.X, padx=15, pady=10)

        # Event Title
        title_label = tk.Label(
            content_frame, text=event["title"], bg="white", fg=PRIMARY_COLOR, 
            font=("Helvetica", 18), wraplength=380, justify="center"
        )
        title_label.pack(pady=10)

        # Event Time and Location
        time_label = tk.Label(content_frame, text=event["time"], bg="white", fg=TEXT_COLOR, 
                              font=("Helvetica", 12))
        time_label.pack()

        location_label = tk.Label(content_frame, text=event["location"], bg="white", fg=TEXT_COLOR, 
                                  font=("Helvetica", 12))
        location_label.pack()

        # Price Information
        price_label = tk.Label(content_frame, text=f"NPR {event['ticket_price']}", 
                               bg="white", fg=BUTTON_COLOR, 
                               font=("Helvetica", 14))
        price_label.pack(pady=10)

        # Bind click event
        def open_purchase(e):
            purchase_ticket(event)

        # Bind click event to the card and its children
        widgets_to_bind = [card, content_frame] + list(content_frame.winfo_children())
        for widget in widgets_to_bind:
            widget.bind("<Button-1>", open_purchase)
            widget.bind("<Enter>", lambda e: root.config(cursor="hand2"))
            widget.bind("<Leave>", lambda e: root.config(cursor=""))

        return card

    # Function to calculate number of columns based on screen size
    def get_number_of_columns():
        screen_width = root.winfo_width()
        if screen_width >= 1200:
            return 3  # Large screens - 3 columns
        elif screen_width >= 800:
            return 2  # Medium screens - 2 columns
        else:
            return 1  # Small screens - 1 column

    # Function to update event cards layout dynamically based on screen size
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

    # Initial layout update
    update_event_cards()

    # Bind event to update layout when window is resized
    def resize_handler(event):
        # Only update if the event is for the root window
        if event.widget == root:
            update_event_cards()

    root.bind("<Configure>", resize_handler)

    # Run the application
    root.mainloop()

except Exception as e:
    show_error(e)
