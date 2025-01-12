# Event Management System

This is an Event Management System built using Python and Tkinter for a graphical user interface (GUI). The system allows users to create events, view events, book and cancel tickets, and manage event-related tasks. Below is a detailed overview of the files included in this system.

## Features

- **Create Event**: Admins can create events and store event details.
- **Book Ticket**: Users can book tickets for available events.
- **Cancel Ticket**: Users can cancel previously booked tickets.
- **View Events**: Displays a list of all available events.
- **View Tickets**: Allows users to view their booked tickets.

## Requirements

- Python 3.x
- Tkinter (Usually comes pre-installed with Python)
- Any standard Python libraries for database management

## Files Description

1. **Book.py**

   This file contains the logic for booking tickets for available events. It interacts with the database to check availability and book tickets accordingly.

2. **Cancelticket.py**

   This file allows users to cancel their booked tickets. It handles removing ticket details from the database.

3. **createevent.py**

   This script is responsible for creating new events. It allows admins to enter event details such as name, date, and location, and saves these details to the database.

4. **database.py**

   This file contains the database-related logic, including saving and retrieving event and ticket information.

5. **UI.py**

   This file contains the graphical user interface (GUI) of the Event Management System built using Python's Tkinter library. It is responsible for displaying the main window where users can view available events and purchase tickets. Here's a breakdown of the main components:

   - **Main Window**: The main window is set up with a professional, minimalistic design using a refined color palette.
     - The window displays the title "Samaaye Events" with a header containing the logo and navigation menu.
   
   - **Event Cards**: The events are displayed as cards that show event details, including the event title, date, time, location, and a corresponding image (if available). Each card is clickable, and clicking on it opens a new window where users can purchase tickets.
   
   - **Ticket Purchase Window**: This window allows users to select the number of tickets they want to purchase, shows the total price, and confirms the ticket purchase. Users can confirm or cancel the purchase.
   
   - **Responsive Layout**: The layout of event cards is responsive and adapts to the screen size, showing 1, 2, or 3 columns depending on the width of the window.

   - **Error Handling**: The script includes error handling to display error messages if an issue arises, such as if an event's image cannot be found.

   - **Dependencies**:
     - Tkinter for the GUI.
     - PIL (Python Imaging Library) for image handling.

   The UI is designed to be simple and user-friendly, allowing users to easily navigate through events and book tickets.

---
