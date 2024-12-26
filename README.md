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

#### `ui.py`
- **Main Window**: The primary interface for browsing upcoming events.
  - **Header**: Displays the company logo and navigation menu.
  - **Event Cards**: Each card displays event details such as title, date, time, location, image, ticket price, and available tickets.
  - **Responsive Design**: Dynamically adjusts the layout based on the screen size.
  - **Ticket Purchase**: Clicking the "Buy Tickets" button launches the ticket booking interface (`ui2.py`) with the event details.

#### `ui2.py`
- **Ticket Booking Interface**: A separate window for booking tickets for a selected event.
  - **Event Details**: Displays event title, date, time, location, and ticket price.
  - **Ticket Quantity**: Users can adjust the ticket quantity using "+" and "-" buttons.
  - **Total Price Calculation**: Dynamically updates the total price based on the ticket quantity.
  - **Booking Form**: Collects user details such as name, mobile number, and MPIN.
  - **Booking Confirmation**: Provides a "BOOK TICKET" button to confirm the booking.

### What Changed
- **Dynamic Ticket Quantity Adjustment**: Added functionality to adjust ticket quantity using "+" and "-" buttons.
- **Real-time Price Update**: The total price updates dynamically as the ticket quantity changes.
- **Event Data Passing**: Event data is passed from `ui.py` to `ui2.py` as command-line arguments to pre-fill booking details.
