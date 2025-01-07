import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

# Using the same color scheme as the booking app for consistency
PRIMARY_COLOR = "#2C3E50"      # Charcoal Blue
SECONDARY_COLOR = "#34495E"    # Dark Slate Blue
ACCENT_COLOR = "#ECF0F1"       # Light Cloud Gray
BUTTON_COLOR = "#2980B9"       # Calm Blue
TEXT_COLOR = "#2C3E50"         # Dark Charcoal

class TicketViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Samaaye Events - Tickets")
        self.root.geometry("800x600")
        
        # Initialize database
        self.setup_database()
        
        # Create GUI
        self.create_header()
        self.create_main_content()
        
        # Load initial tickets
        self.refresh_tickets()
        
    def setup_database(self):
        """Setup SQLite database if it doesn't exist"""
        conn = sqlite3.connect('samaaye_events.db')
        cursor = conn.cursor()
        
        # Create bookings table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                mobile TEXT NOT NULL,
                event_title TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                event_location TEXT NOT NULL,
                ticket_quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_header(self):
        """Create the header with navigation"""
        header = tk.Frame(self.root, bg=PRIMARY_COLOR)
        header.pack(fill="x", padx=0, pady=0)
        
        # Company logo and name
        company_name = tk.Label(header, text="Samaaye events", 
                              font=("Arial", 16), bg=PRIMARY_COLOR, fg=ACCENT_COLOR)
        company_name.pack(side="left", padx=20, pady=10)
        
        # Navigation buttons
        nav_buttons = ["Events", "Tickets", "Stats", "My Account"]
        for button in nav_buttons:
            btn = tk.Button(header, text=button, bg=PRIMARY_COLOR, 
                          fg=ACCENT_COLOR, bd=0)
            btn.pack(side="left", padx=20, pady=10)

    def create_main_content(self):
        """Create the main content area"""
        content_frame = tk.Frame(self.root, bg=ACCENT_COLOR)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(content_frame, text="Booked Tickets", 
                        font=("Arial", 24, "bold"), bg=ACCENT_COLOR, fg=TEXT_COLOR)
        title.pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(content_frame, bg=ACCENT_COLOR)
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search:", bg=ACCENT_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", padx=5)
        
        tk.Button(search_frame, text="Search", bg=BUTTON_COLOR, fg=ACCENT_COLOR,
                 command=self.search_tickets).pack(side="left", padx=5)
        
        tk.Button(search_frame, text="Reset", bg=BUTTON_COLOR, fg=ACCENT_COLOR,
                 command=self.refresh_tickets).pack(side="left", padx=5)
        
        # Create Treeview for tickets
        columns = ("ID", "Name", "Mobile", "Event", "Date", "Time", "Location", 
                  "Quantity", "Total Price", "Booking Date")
        
        self.tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=20)
        
        # Configure column headings and widths
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_tickets(c))
            width = 100 if col not in ["Name", "Event", "Location"] else 150
            self.tree.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click event for ticket details
        self.tree.bind('<Double-1>', self.show_ticket_details)

    def refresh_tickets(self):
        """Refresh the tickets display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = sqlite3.connect('samaaye_events.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM bookings ORDER BY booking_date DESC')
            
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
                
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {str(e)}")

    def search_tickets(self):
        """Search tickets based on name, mobile number, or event title"""
        search_term = self.search_var.get().strip()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not search_term:
            self.refresh_tickets()
            return
            
        try:
            conn = sqlite3.connect('samaaye_events.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM bookings 
                WHERE name LIKE ? OR mobile LIKE ? OR event_title LIKE ?
                ORDER BY booking_date DESC
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
                
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error searching database: {str(e)}")

    def sort_tickets(self, column):
        """Sort tickets by clicking on column headers"""
        # Get all items
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children("")]
        
        # Sort items
        items.sort()
        
        # Rearrange items in sorted positions
        for index, (_, item) in enumerate(items):
            self.tree.move(item, "", index)

    def show_ticket_details(self, event):
        """Show detailed information for selected ticket"""
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item)['values']
        
        details_window = tk.Toplevel(self.root)
        details_window.title("Ticket Details")
        details_window.geometry("400x500")
        details_window.configure(bg=ACCENT_COLOR)
        
        # Create labels for each piece of information
        labels = ["ID:", "Name:", "Mobile:", "Event:", "Date:", "Time:", 
                 "Location:", "Quantity:", "Total Price:", "Booking Date:"]
        
        for i, (label, value) in enumerate(zip(labels, values)):
            tk.Label(details_window, text=label, font=("Arial", 12, "bold"), 
                    bg=ACCENT_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=20, pady=5)
            tk.Label(details_window, text=str(value), font=("Arial", 12), 
                    bg=ACCENT_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=40, pady=5)

def main():
    root = tk.Tk()
    app = TicketViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()