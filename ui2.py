import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Original Color Palette
COLORS = {
    'primary': '#2C3E50',    # Charcoal Blue - Elegant Base Color
    'secondary': '#34495E',   # Dark Slate Blue - Subtle Depth
    'accent': '#ECF0F1',     # Light Cloud Gray - Clean Background
    'button': '#2980B9',     # Calm Blue - Sophisticated Interaction
    'text': '#2C3E50',       # Dark Charcoal for Readability
    'success': '#27AE60',    # Complementary Green
    'error': '#E74C3C',      # Complementary Red
    'border': '#BDC3C7',     # Light Border
    'input_bg': '#FFFFFF',   # White
    'card_bg': '#FFFFFF'     # White
}

class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = kwargs.get('bg', COLORS['button'])
        self.default_fg = kwargs.get('fg', COLORS['accent'])
        
        self.configure(
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            font=('Helvetica', 11),
            cursor='hand2'
        )
        
        self.bind('<Enter>', lambda e: self.configure(bg=COLORS['secondary']))
        self.bind('<Leave>', lambda e: self.configure(bg=self.default_bg))

class ModernEntry(tk.Entry):
    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        
        self.configure(
            font=('Helvetica', 11),
            bg=COLORS['input_bg'],
            fg=COLORS['text'],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['button']
        )

class TicketBookingApp:
    def __init__(self, root, event):
        self.root = root
        self.root.title("Samaaye Events - Ticket Booking")
        self.root.geometry("1200x1800")
        self.root.configure(bg=COLORS['accent'])
        
        self.event = event
        self.ticket_quantity = tk.IntVar(value=1)
        
        # Configure grid weights for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self._create_header()
        self._create_content_container()
        
    def _create_header(self):
        header = tk.Frame(self.root, bg=COLORS['primary'], height=70)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)
        
        # Logo
        tk.Label(
            header,
            text="SAMAAYE EVENTS",
            font=("Helvetica", 20, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['accent']
        ).grid(row=0, column=0, padx=30, pady=15)
        
        # Navigation
        nav_frame = tk.Frame(header, bg=COLORS['primary'])
        nav_frame.grid(row=0, column=2, padx=30)
        
        for item in ["Events", "Tickets", "Stats", "My Account"]:
            ModernButton(
                nav_frame,
                text=item,
                bg=COLORS['primary'],
                fg=COLORS['accent']
            ).pack(side="left", padx=5)
    
    def _create_content_container(self):
        container = tk.Frame(self.root, bg=COLORS['accent'])
        container.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        container.grid_columnconfigure(0, weight=1)
        
        self._create_event_header(container)
        self._create_event_card(container)
        self._create_booking_form(container)
    
    def _create_event_header(self, parent):
        header_frame = tk.Frame(parent, bg=COLORS['accent'])
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        tk.Label(
            header_frame,
            text=self.event["title"],
            font=("Helvetica", 28, "bold"),
            bg=COLORS['accent'],
            fg=COLORS['text']
        ).pack(anchor="w")
    
    def _create_event_card(self, parent):
        card = tk.Frame(parent, bg=COLORS['primary'], bd=0, relief="flat")
        card.grid(row=1, column=0, sticky="ew", pady=(0, 30))
        card.grid_columnconfigure(1, weight=1)
        
        # Event info section
        info_frame = tk.Frame(card, bg=COLORS['primary'], pady=20, padx=30)
        info_frame.grid(row=0, column=0, sticky="w")
        
        tk.Label(
            info_frame,
            text=self.event["date"],
            font=("Helvetica", 18, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['accent']
        ).pack(anchor="w")
        
        tk.Label(
            info_frame,
            text=self.event["time"],
            font=("Helvetica", 14),
            bg=COLORS['primary'],
            fg=COLORS['accent']
        ).pack(anchor="w", pady=(5, 0))
        
        # Location section
        location_frame = tk.Frame(card, bg=COLORS['primary'], pady=20)
        location_frame.grid(row=0, column=1, sticky="e", padx=30)
        
        tk.Label(
            location_frame,
            text="VENUE",
            font=("Helvetica", 12),
            bg=COLORS['primary'],
            fg=COLORS['accent']
        ).pack(anchor="e")
        
        tk.Label(
            location_frame,
            text=self.event["location"],
            font=("Helvetica", 16, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['accent']
        ).pack(anchor="e", pady=(5, 0))
        
        # Ticket quantity section
        quantity_frame = tk.Frame(card, bg=COLORS['primary'], pady=20, padx=30)
        quantity_frame.grid(row=0, column=2, sticky="e")
        
        tk.Label(
            quantity_frame,
            text="Number of Tickets",
            font=("Helvetica", 12),
            bg=COLORS['primary'],
            fg=COLORS['accent']
        ).pack(anchor="e")
        
        selector = tk.Frame(quantity_frame, bg=COLORS['primary'])
        selector.pack(pady=(10, 5))
        
        ModernButton(
            selector,
            text="−",
            command=self.decrement_quantity,
            width=3,
            bg=COLORS['button'],
            fg=COLORS['accent']
        ).pack(side="left")
        
        quantity_display = tk.Frame(selector, bg=COLORS['accent'], padx=15, pady=5)
        quantity_display.pack(side="left", padx=8)
        
        tk.Label(
            quantity_display,
            textvariable=self.ticket_quantity,
            font=("Helvetica", 14, "bold"),
            bg=COLORS['accent'],
            fg=COLORS['text']
        ).pack()
        
        ModernButton(
            selector,
            text="+",
            command=self.increment_quantity,
            width=3,
            bg=COLORS['button'],
            fg=COLORS['accent']
        ).pack(side="left")
        
        self.price_label = tk.Label(
            quantity_frame,
            text=f"Total: NPR {self.calculate_total_price():,}",
            font=("Helvetica", 14, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['accent']
        )
        self.price_label.pack(anchor="e", pady=(5, 0))
    
    def _create_booking_form(self, parent):
        form_container = tk.Frame(parent, bg=COLORS['card_bg'], bd=1, relief="solid")
        form_container.grid(row=2, column=0, sticky="ew")
        form_container.grid_columnconfigure(0, weight=1)
        
        # Form header
        header = tk.Frame(form_container, bg=COLORS['primary'], height=50)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        tk.Label(
            header,
            text="Booking Details",
            font=("Helvetica", 14, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['accent']
        ).pack(side="left", padx=20, pady=10)
        
        # Form fields
        form_frame = tk.Frame(form_container, bg=COLORS['card_bg'], padx=30, pady=30)
        form_frame.grid(row=1, column=0, sticky="ew")
        form_frame.grid_columnconfigure(0, weight=1)
        
        self.entries = {}
        fields = [
            ("Full Name", "Enter your full name"),
            ("Mobile Number", "Enter your mobile number"),
            ("MPIN", "Enter your MPIN")
        ]
        
        for i, (label, placeholder) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label,
                font=("Helvetica", 12, "bold"),
                bg=COLORS['card_bg'],
                fg=COLORS['text']
            ).grid(row=i*2, column=0, sticky="w", pady=(0, 5))
            
            entry = ModernEntry(
                form_frame,
                placeholder=placeholder,
                width=50
            )
            entry.grid(row=i*2+1, column=0, sticky="ew", pady=(0, 15))
            self.entries[label] = entry
        
        ttk.Separator(form_frame).grid(row=len(fields)*2, column=0, sticky="ew", pady=20)
        
        ModernButton(
            form_frame,
            text="CONFIRM BOOKING",
            bg=COLORS['button'],
            fg=COLORS['accent'],
            font=("Helvetica", 12, "bold"),
            command=self.book_ticket
        ).grid(row=len(fields)*2+1, column=0, sticky="ew", pady=(0, 10))
    
    def calculate_total_price(self):
        return int(self.event['ticket_price']) * self.ticket_quantity.get()
    
    def update_price_label(self):
        self.price_label.config(text=f"Total: NPR {self.calculate_total_price():,}")
    
    def increment_quantity(self):
        if self.ticket_quantity.get() < int(self.event['available_tickets']):
            self.ticket_quantity.set(self.ticket_quantity.get() + 1)
            self.update_price_label()
        else:
            messagebox.showwarning("Maximum Limit", f"Only {self.event['available_tickets']} tickets available!")
    
    def decrement_quantity(self):
        if self.ticket_quantity.get() > 1:
            self.ticket_quantity.set(self.ticket_quantity.get() - 1)
            self.update_price_label()
    
    def book_ticket(self):
        # Validate form
        for label, entry in self.entries.items():
            if not entry.get() or entry.get() == entry.placeholder:
                messagebox.showwarning("Incomplete Form", f"Please enter your {label.lower()}")
                return
        
        # Show confirmation
        total = self.calculate_total_price()
        message = f"""
Booking Summary:
---------------
Event: {self.event['title']}
Date: {self.event['date']}
Time: {self.event['time']}
Location: {self.event['location']}
Tickets: {self.ticket_quantity.get()}
Total Amount: NPR {total:,}

Booking successful! A confirmation SMS will be sent to your mobile number.
"""
        messagebox.showinfo("Booking Confirmed", message)
        self.root.destroy()

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python3 ticket_booking.py <title> <date> <time> <location> <ticket_price> <available_tickets>")
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
