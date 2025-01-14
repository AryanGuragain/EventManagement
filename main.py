import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess

# Color Scheme
PRIMARY_COLOR = "#2C3E50"  # Charcoal Blue
SECONDARY_COLOR = "#34495E"  # Dark Slate Blue
ACCENT_COLOR = "#ECF0F1"  # Light Cloud Gray
BUTTON_COLOR = "#2980B9"  # Calm Blue
TEXT_COLOR = "#2C3E50"  # Dark Charcoal

# Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "root123"

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel - Samaaye Events")
        self.root.geometry("1200x800")
        self.root.configure(bg=ACCENT_COLOR)

        # Database setup
        self.setup_database()

        # Create UI
        self.create_header()
        self.create_main_content()
        self.display_total_tickets()
        self.display_event_tickets()

    def setup_database(self):
        """Ensure the database and table exist."""
        conn = sqlite3.connect('samaaye_events.db')
        cursor = conn.cursor()
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
        """Create the header section."""
        header = tk.Frame(self.root, bg=PRIMARY_COLOR)
        header.pack(fill="x")

        title = tk.Label(header, text="Admin Dashboard - Samaaye Events", 
                        font=("Helvetica", 24, "bold"), bg=PRIMARY_COLOR, fg=ACCENT_COLOR)
        title.pack(pady=20)

    def create_main_content(self):
        """Create the main content area."""
        main_frame = tk.Frame(self.root, bg=ACCENT_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Grid configuration
        main_frame.grid_rowconfigure(0, weight=3)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=0)

        # Create frames
        self.pie_chart_frame = tk.Frame(main_frame, bg=ACCENT_COLOR)
        self.pie_chart_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.line_graph_frame = tk.Frame(main_frame, bg=ACCENT_COLOR)
        self.line_graph_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.stats_frame = tk.Frame(main_frame, bg=ACCENT_COLOR)
        self.stats_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=5, pady=5)

        # Stats labels
        self.net_sales_label = tk.Label(self.stats_frame, text="Total Revenue (Rs):\n0.00", 
                                      font=("Helvetica", 18, "bold"), bg=ACCENT_COLOR, 
                                      fg=PRIMARY_COLOR, justify="left")
        self.net_sales_label.pack(pady=20, padx=10, anchor="nw")

        self.total_tickets_label = tk.Label(self.stats_frame, text="Total Tickets Sold:\n0", 
                                          font=("Helvetica", 18, "bold"), bg=ACCENT_COLOR, 
                                          fg=PRIMARY_COLOR, justify="left")
        self.total_tickets_label.pack(pady=20, padx=10, anchor="nw")

        # Event tickets frame
        self.event_tickets_frame = tk.Frame(self.stats_frame, bg=ACCENT_COLOR)
        self.event_tickets_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Buttons frame
        buttons_frame = tk.Frame(self.stats_frame, bg=ACCENT_COLOR)
        buttons_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Action buttons
        add_event_button = tk.Button(buttons_frame, text="Add Event", 
                                   bg=BUTTON_COLOR, fg=ACCENT_COLOR, 
                                   font=("Helvetica", 14), command=self.add_event)
        add_event_button.pack(fill="x", padx=10, pady=(10, 5))

        edit_event_button = tk.Button(buttons_frame, text="Edit Event", 
                                    bg=BUTTON_COLOR, fg=ACCENT_COLOR, 
                                    font=("Helvetica", 14), command=self.edit_event)
        edit_event_button.pack(fill="x", padx=10, pady=5)

        delete_event_button = tk.Button(buttons_frame, text="Delete Event", 
                                      bg=BUTTON_COLOR, fg=ACCENT_COLOR, 
                                      font=("Helvetica", 14), command=self.delete_event)
        delete_event_button.pack(fill="x", padx=10, pady=(5, 10))

        # Show graphs
        self.show_ticket_sales_graph()
        self.show_booking_line_graph()

    def show_ticket_sales_graph(self):
        """Display a pie chart of net sales by event."""
        try:
            conn = sqlite3.connect('samaaye_events.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT event_title, SUM(total_price) AS net_sales
                FROM bookings
                GROUP BY event_title
                ORDER BY net_sales DESC
            ''')
            data = cursor.fetchall()
            conn.close()

            if not data:
                messagebox.showinfo("No Data", "No sales data available.")
                return

            event_titles = [row[0] for row in data]
            net_sales = [row[1] for row in data]
            total_sales = sum(net_sales)
            labels = [
                f"{title}\nRs {sales:.2f} ({(sales / total_sales) * 100:.1f}%)"
                for title, sales in zip(event_titles, net_sales)
            ]

            fig = Figure(figsize=(5, 5), dpi=70)
            ax = fig.add_subplot(111)
            ax.pie(
                net_sales,
                labels=labels,
                autopct=None,
                startangle=90,
                colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            )
            ax.set_title("Net Sales by Event (Rs)", fontsize=16, weight='bold')

            for widget in self.pie_chart_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.pie_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching sales data: {str(e)}")

    def show_booking_line_graph(self):
        """Display a line graph showing the number of tickets booked up to date for different events."""
        try:
            conn = sqlite3.connect('samaaye_events.db')
            cursor = conn.cursor()

            # Get booking data grouped by event title and date
            cursor.execute('''
                SELECT event_title, booking_date, SUM(ticket_quantity) AS total_tickets
                FROM bookings
                GROUP BY event_title, booking_date
                ORDER BY booking_date ASC
            ''')
            data = cursor.fetchall()
            conn.close()

            if not data:
                messagebox.showinfo("No Data", "No booking data available.")
                return

            # Prepare data for plotting
            event_dates = sorted(set(row[1][:10] for row in data)) # Extract and sort unique dates
            events = sorted(set(row[0] for row in data))  # Extract and sort unique events
            cumulative_tickets = {event: [0] * len(event_dates) for event in events}

            # Calculate cumulative tickets for each event
            for row in data:
                event_title, booking_date, total_tickets = row
                date_index = event_dates.index(booking_date[:10])
                for i in range(date_index, len(event_dates)):
                    cumulative_tickets[event_title][i] += total_tickets

            # Create a matplotlib figure
            fig = Figure(figsize=(5, 5), dpi=70)
            ax = fig.add_subplot(111)

            # Plot line graph for each event
            for event in events:
                ax.plot(event_dates, cumulative_tickets[event], marker='o', linestyle='-', label=event)

            ax.set_title("Cumulative Tickets Booked Over Time", fontsize=16, weight='bold')
            ax.set_xlabel("Booking Date")
            ax.set_ylabel("Total Tickets")
            ax.legend()

            # Clear previous graph if any
            for widget in self.line_graph_frame.winfo_children():
                widget.destroy()

            # Embed the graph in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.line_graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching booking data: {str(e)}")

    def view_tickets_info(self):
        """Display information about who purchased which tickets with price."""
        top = tk.Toplevel(self.root)
        top.title("Tickets Info")
        top.geometry("900x500")

        # Treeview for displaying data
        tree = ttk.Treeview(top, columns=("ID", "Name", "Mobile", "Event Title", 
                                          "Tickets", "Price"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Mobile", text="Mobile")
        tree.heading("Event Title", text="Event Title")
        tree.heading("Tickets", text="Tickets")
        tree.heading("Price", text="Price (Rs)")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        try:
            conn = sqlite3.connect('samaaye_events.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, name, mobile, event_title, ticket_quantity, total_price 
                FROM bookings
            ''')
            data = cursor.fetchall()
            conn.close()

            # Insert data into Treeview
            for row in data:
                tree.insert("", "end", values=row)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching tickets data: {str(e)}")

        # Delete Ticket Button
        delete_btn = tk.Button(top, text="Delete Selected Ticket", bg="red", fg="white", font=("Helvetica", 12),
                               command=lambda: self.delete_ticket(tree))
        delete_btn.pack(pady=10)

    def delete_ticket(self, tree):
        """Delete the selected ticket."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("No Selection", "Please select a ticket to delete.")
            return

        ticket_id = tree.item(selected_item, "values")[0]
        try:
            conn = sqlite3.connect('samaaye_events.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bookings WHERE id = ?', (ticket_id,))
            conn.commit()
            conn.close()
            tree.delete(selected_item)
            messagebox.showinfo("Success", "Ticket deleted successfully.")
            self.display_total_tickets()  # Refresh stats
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting ticket: {str(e)}")

    def add_event(self):
        """Handle adding an event."""
        try:
            subprocess.Popen(["python", "CreateEvent.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open CreateEvent.py: {str(e)}")

    def edit_event(self):
        """Handle editing an event."""
        # Implement the logic to edit an event
        messagebox.showinfo("Edit Event", "Edit Event functionality not implemented yet.")

    def delete_event(self):
        """Handle deleting an event."""
        # Implement the logic to delete an event
        messagebox.showinfo("Delete Event", "Delete Event functionality not implemented yet.")


class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login - Samaaye Events")
        self.root.geometry("400x300")
        self.root.configure(bg="skyblue")
        self.create_login_ui()

    def create_login_ui(self):
        frame = tk.Frame(self.root, bg="skyblue")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame, text="Admin Login", 
                font=("Helvetica", 24, "bold"), 
                bg="skyblue", fg=ACCENT_COLOR).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(frame, text="Username:", 
                font=("Helvetica", 14), 
                bg="skyblue", fg=ACCENT_COLOR).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.username_entry = tk.Entry(frame, font=("Helvetica", 14))
        self.username_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        tk.Label(frame, text="Password:", 
                font=("Helvetica", 14), 
                bg="skyblue", fg=ACCENT_COLOR).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.password_entry = tk.Entry(frame, font=("Helvetica", 14), show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=10, sticky="ew")

        frame.grid_columnconfigure(1, weight=1)

        login_btn = tk.Button(frame, text="Login", 
                            bg=BUTTON_COLOR, fg=ACCENT_COLOR, 
                            font=("Helvetica", 14), command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=20, padx=10)
        
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="darkblue", fg="white"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg=BUTTON_COLOR, fg=ACCENT_COLOR))
        
        self.root.bind('<Return>', lambda event: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.root.destroy()
            main()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

def main():
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    LoginScreen(login_root)
    login_root.mainloop()
