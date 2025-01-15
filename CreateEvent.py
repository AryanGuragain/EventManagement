import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import shutil
import os
from PIL import Image, ImageTk

class CreateEventWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Create New Event - Samaaye Events")
        self.root.geometry("600x900")
        self.root.configure(bg="#ECF0F1")
        
        # Initialize image variables
        self.image_path = None
        self.image_preview = None
        
        # Create images directory if it doesn't exist
        self.images_dir = "event_images"
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        
        self.setup_database()
        self.create_ui()

    def setup_database(self):
        """Create or update events table with the correct schema."""
        try:
            conn = sqlite3.connect('samaaye_events.db')
            cursor = conn.cursor()
            
            # First, check if the table exists
            cursor.execute('''
                SELECT name FROM sqlite_master WHERE type='table' AND name='events'
            ''')
            table_exists = cursor.fetchone() is not None
            
            if table_exists:
                # Get current columns
                cursor.execute('PRAGMA table_info(events)')
                columns = [column[1] for column in cursor.fetchall()]
                
                # If available_tickets column doesn't exist, create it
                if 'available_tickets' not in columns:
                    cursor.execute('''
                        ALTER TABLE events 
                        ADD COLUMN available_tickets INTEGER DEFAULT 0
                    ''')
                    # Update existing rows to set available_tickets equal to total_tickets
                    cursor.execute('''
                        UPDATE events 
                        SET available_tickets = total_tickets 
                        WHERE available_tickets IS NULL OR available_tickets = 0
                    ''')
            else:
                # Create new table with all required columns
                cursor.execute('''
                    CREATE TABLE events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        location TEXT NOT NULL,
                        ticket_price REAL NOT NULL,
                        total_tickets INTEGER NOT NULL,
                        available_tickets INTEGER NOT NULL,
                        image_path TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error setting up database: {str(e)}")

    def create_ui(self):
        """Create the user interface."""
        # Title
        title_label = tk.Label(self.root, text="Create New Event", 
                              font=("Helvetica", 24, "bold"), 
                              bg="#ECF0F1", fg="#2C3E50")
        title_label.pack(pady=20)

        # Create a canvas with scrollbar
        canvas = tk.Canvas(self.root, bg="#ECF0F1")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ECF0F1")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=560)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=(20,0))
        scrollbar.pack(side="right", fill="y")

        # Event Details
        labels = ['Event Title:', 'Description:', 'Date (YYYY-MM-DD):', 
                 'Time (HH:MM):', 'Location:', 'Ticket Price (Rs):', 
                 'Total Tickets:']
        
        self.entries = {}
        
        for i, label in enumerate(labels):
            tk.Label(scrollable_frame, text=label, 
                    font=("Helvetica", 12), 
                    bg="#ECF0F1", fg="#2C3E50").pack(anchor="w", pady=(10,0))
            
            if label == 'Description:':
                entry = tk.Text(scrollable_frame, height=4, 
                              font=("Helvetica", 11))
            else:
                entry = tk.Entry(scrollable_frame, 
                               font=("Helvetica", 11))
            entry.pack(fill="x", pady=(0,10))
            self.entries[label] = entry

        # Image Upload Section
        tk.Label(scrollable_frame, text="Event Image:", 
                font=("Helvetica", 12), 
                bg="#ECF0F1", fg="#2C3E50").pack(anchor="w", pady=(10,0))

        # Image Preview Frame
        self.preview_frame = tk.Frame(scrollable_frame, bg="#ECF0F1")
        self.preview_frame.pack(fill="x", pady=10)
        
        # Upload Button
        upload_btn = tk.Button(scrollable_frame, text="Upload Image", 
                             bg="#27AE60", fg="white",
                             font=("Helvetica", 11),
                             command=self.upload_image)
        upload_btn.pack(pady=5)

        # Create Button
        create_btn = tk.Button(scrollable_frame, text="Create Event", 
                             bg="#2980B9", fg="white",
                             font=("Helvetica", 12, "bold"),
                             command=self.create_event)
        create_btn.pack(pady=20)

    def upload_image(self):
        """Handle image upload."""
        file_types = [('Image files', '*.png *.jpg *.jpeg *.gif *.bmp')]
        filename = filedialog.askopenfilename(title="Select Image", 
                                            filetypes=file_types)
        
        if filename:
            try:
                # Load and resize image for preview
                image = Image.open(filename)
                image.thumbnail((200, 200))  # Resize for preview
                photo = ImageTk.PhotoImage(image)
                
                # Update preview
                if hasattr(self, 'preview_label'):
                    self.preview_label.destroy()
                
                self.preview_label = tk.Label(self.preview_frame, 
                                            image=photo, 
                                            bg="#ECF0F1")
                self.preview_label.image = photo  # Keep a reference
                self.preview_label.pack()
                
                self.image_path = filename
                
            except Exception as e:
                messagebox.showerror("Error", f"Error loading image: {str(e)}")

    def create_event(self):
        """Handle event creation."""
        try:
            # Get values from entries
            values = {}
            for label, entry in self.entries.items():
                if isinstance(entry, tk.Text):
                    values[label] = entry.get("1.0", "end-1c").strip()
                else:
                    values[label] = entry.get().strip()

            # Validate inputs
            if not all(values.values()):
                messagebox.showerror("Error", "All fields are required!")
                return

            # Validate date format
            try:
                datetime.strptime(values['Date (YYYY-MM-DD):'], '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return

            # Validate time format
            try:
                datetime.strptime(values['Time (HH:MM):'], '%H:%M')
            except ValueError:
                messagebox.showerror("Error", "Invalid time format! Use HH:MM")
                return

            # Validate numeric values
            try:
                price = float(values['Ticket Price (Rs):'])
                tickets = int(values['Total Tickets:'])
                if price < 0 or tickets < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid price or ticket quantity!")
                return

            # Handle image
            final_image_path = None
            if self.image_path:
                # Generate unique filename
                _, ext = os.path.splitext(self.image_path)
                new_filename = f"event_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
                final_image_path = os.path.join(self.images_dir, new_filename)
                
                # Copy image to events directory
                shutil.copy2(self.image_path, final_image_path)

            # Save to database
            conn = sqlite3.connect('samaaye_events.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (
                    title, description, date, time, location, 
                    ticket_price, total_tickets, available_tickets, image_path
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                values['Event Title:'],
                values['Description:'],
                values['Date (YYYY-MM-DD):'],
                values['Time (HH:MM):'],
                values['Location:'],
                price,
                tickets,
                tickets,  # Initially, available tickets equals total tickets
                final_image_path
            ))
            
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Event created successfully!")
            self.root.destroy()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error creating event: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = CreateEventWindow()
    app.root.mainloop()