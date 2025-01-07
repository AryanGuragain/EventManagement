# Event Management UI

## Overview
The Event Management UI is a Python-based application designed to help users browse and book tickets for various events. The application features a user-friendly interface, responsive design, and robust functionality for managing event bookings.

## Features

### `ui.py`
- **Enhanced Event Cards**: View event details with a "View Details" button that opens a modal with more information.
- **Improved Responsiveness**: Layout adjustments for better usability on smaller screens.
- **Search Functionality**: Filter events by title using a search bar.

### `ui2.py`
- **Booking Confirmation Email**: Sends a confirmation email to users after successful bookings (requires SMTP configuration).
- **Input Validation**: Ensures mobile numbers and MPINs meet specified formats.
- **Booking Summary**: Displays a detailed breakdown of ticket prices and totals.

### `ticket.py`
- **Improved Navigation**: Easy switching between different sections of the application.
- **User  Feedback**: Provides feedback messages for actions like ticket purchases.
- **Event Filtering**: Filter events based on categories or types.

## Improvements
- **Code Refactoring**: Enhanced code readability and maintainability.
- **Error Handling**: Improved error messages for database operations.
- **User  Interface Enhancements**: Updated color schemes and added button hover effects.

## Bug Fixes
- **Image Loading Issues**: Resolved problems with images not loading correctly.
- **Database Connection Handling**: Ensured proper closure of database connections.

## How to Use
1. **Browsing Events**:
   - Open `ui.py` to view upcoming events.
   - Use the search bar to filter events by title.
   - Click on "View Details" for more information about an event.

2. **Booking Tickets**:
   - In the ticket booking interface (`ui2.py`), adjust the ticket quantity as needed.
   - Fill in your details in the booking form, ensuring valid mobile numbers and MPINs.
   - Click the "BOOK TICKET" button to confirm your booking. A confirmation email will be sent to your registered email address.

3. **Navigating the Application**:
   - Use the navigation menu in `ticket.py` to switch between sections like Events, Tickets, Stats, and My Account.
     
[Screenshot from 2025-01-07 14-35-08](https://github.com/user-attachments/assets/5279d218-23dc-4f8b-91d3-f3e241bb318e)
![Screenshot from 2025-01-07 14-35-14](https://github.com/user-attachments/assets/ec779dda-a0f9-4e45-ad88-b2d687bae77f)
![Screenshot from 2025-01-07 14-35-19](https://github.com/user-attachments/assets/9db9892e-6a53-4af8-a4d6-fffa11021504)
## Installation
To run the application, ensure you have Python and the required libraries installed. You can install the necessary libraries using the following command:
```bash
pip install tkinter pillow!
