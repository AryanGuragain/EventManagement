import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

# Refined Color Palette - Professional and Minimalistic
PRIMARY_COLOR = "#2C3E50"      # Charcoal Blue - Elegant Base Color
SECONDARY_COLOR = "#34495E"    # Dark Slate Blue - Subtle Depth
ACCENT_COLOR = "#ECF0F1"       # Light Cloud Gray - Clean Background
BUTTON_COLOR = "#2980B9"       # Calm Blue - Sophisticated Interaction
TEXT_COLOR = "#2C3E50"         # Dark Charcoal for Readability

class TicketBookingApp:
    def __init__(self, root, event):
        self.root = root
        self.root.title("Samaaye Events")
        self.root.geometry("800x600")

        self.event = event
        self.ticket_quantity = tk.IntVar(value=1)  # Initialize ticket quantity to 1
        
        # Header
        header = tk.Frame(root, bg=PRIMARY_COLOR)
        header.pack(fill="x", padx=0, pady=0)
        
        # Company logo and name
        company_name = tk.Label(header, text="Samaaye events", font=("Arial", 16), bg=PRIMARY_COLOR, fg=ACCENT_COLOR)
        company_name.pack(side="left", padx=20, pady=10)
        
        # Navigation buttons
        nav_buttons = ["Events", "Tickets", "Stats", "My Account"]
        for button in nav_buttons:
            if button == "Events":
                tk.Button(header, text=button, bg=PRIMARY_COLOR, fg=ACCENT_COLOR, bd=0, command=self.close_window).pack(side="left", padx=20, pady=10)
            else:
                tk.Button(header, text=button, bg=PRIMARY_COLOR, fg=ACCENT_COLOR, bd=0).pack(side="left", padx=20, pady=10)

        # Main content
        self.content = tk.Frame(root, bg=ACCENT_COLOR)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Event title
        self.event_title = tk.Label(self.content, text=event["title"], font=("Arial", 24, "bold"), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        self.event_title.pack(pady=10)

        # Event card
        self.event_frame = tk.Frame(self.content, bg=PRIMARY_COLOR, padx=20, pady=20)
        self.event_frame.pack(fill="x", pady=10)

        # Event details
        self.details_frame = tk.Frame(self.event_frame, bg=PRIMARY_COLOR)
        self.details_frame.pack(side="left", padx=20)
        
        self.date_label = tk.Label(self.details_frame, text=event["date"], font=("Arial", 16, "bold"), fg=ACCENT_COLOR, bg=PRIMARY_COLOR)
        self.date_label.pack()
        
        self.time_label = tk.Label(self.details_frame, text=event["time"], font=("Arial", 12), fg=ACCENT_COLOR, bg=PRIMARY_COLOR)
        self.time_label.pack()
        
        self.location_label = tk.Label(self.details_frame, text=event["location"], font=("Arial", 12), fg=ACCENT_COLOR, bg=PRIMARY_COLOR)
        self.location_label.pack()

        # Ticket quantity
        self.ticket_frame = tk.Frame(self.event_frame, bg=PRIMARY_COLOR)
        self.ticket_frame.pack(side="left", padx=20)
        
        tk.Label(self.ticket_frame, text="Tickets", fg=ACCENT_COLOR, bg=PRIMARY_COLOR).pack()
        quantity_frame = tk.Frame(self.ticket_frame, bg=PRIMARY_COLOR)
        quantity_frame.pack()
        
        tk.Button(quantity_frame, text="-", command=self.decrement_quantity).pack(side="left", padx=5)
        self.quantity_entry = tk.Entry(quantity_frame, width=3, justify="center", textvariable=self.ticket_quantity)
        self.quantity_entry.pack(side="left", padx=5)
        tk.Button(quantity_frame, text="+", command=self.increment_quantity).pack(side="left", padx=5)
        
        self.price_label = tk.Label(self.ticket_frame, text=f"Total Price: NPR {self.calculate_total_price()}", fg=ACCENT_COLOR, bg=PRIMARY_COLOR)
        self.price_label.pack(pady=5)
        
        # Booking form
        form_frame = tk.LabelFrame(self.content, text="Enter Details", padx=20, pady=20, bg=ACCENT_COLOR)
        form_frame.pack(fill="x", pady=20)
        
        labels = ["Your Name", "Mobile Number", "MPIN"]
        for label in labels:
            tk.Label(form_frame, text=label, bg=ACCENT_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=5)
            tk.Entry(form_frame).pack(fill="x", pady=5)
        
        tk.Button(form_frame, text="BOOK TICKET", bg=BUTTON_COLOR, fg=ACCENT_COLOR, 
                 font=("Arial", 12, "bold"), padx=20, pady=10).pack(fill="x", pady=10)

    def calculate_total_price(self):
        """Calculate the total price based on the ticket quantity and unit price."""
        return int(self.event['ticket_price']) * self.ticket_quantity.get()

    def update_price_label(self):
        """Update the price label to reflect the current total price."""
        self.price_label.config(text=f"Total Price: NPR {self.calculate_total_price()}")

    def increment_quantity(self):
        """Increment the ticket quantity by 1."""
        current_quantity = self.ticket_quantity.get()
        self.ticket_quantity.set(current_quantity + 1)
        self.update_price_label()  # Update the price label

    def decrement_quantity(self):
        """Decrement the ticket quantity by 1, but not below 1."""
        current_quantity = self.ticket_quantity.get()
        if current_quantity > 1:
            self.ticket_quantity.set(current_quantity - 1)
            self.update_price_label()  # Update the price label

    def close_window(self):
        """Close the Tkinter window."""
        self.root.destroy()

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python3 ui2.py <title> <date> <time> <location> <ticket_price> <available_tickets>")
        sys.exit(1)

    event_data = {
        "title": sys.argv[1],
        "date": sys.argv[2],
        "time": sys.argv[3],
        "location": sys.argv[4],
        "ticket_price": sys.argv[5],
        "available_tickets": sys.argv[6],
    }

    root = tk.Tk()
    app = TicketBookingApp(root, event_data)
    root.mainloop()