# Tkinter Ticket Booking Application

## Overview
The Tkinter Ticket Booking Application is a user-friendly software designed to facilitate the booking of tickets for various events. Built using Python's Tkinter library, it provides a graphical interface for users to view events, purchase tickets, and manage their bookings. The application utilizes SQLite for database management, ensuring that all booking information is stored securely and efficiently.

## Features
- **Event Display**: Users can view a list of upcoming events, including details such as:
  - Event title
  - Date and time
  - Location
  - Ticket price
  - Available tickets
- **Ticket Booking**: Users can easily purchase tickets by filling out a booking form that includes:
  - Full name
  - Mobile number
  - MPIN for verification
- **Booking Management**: Users can view their booked tickets, search for specific bookings, and delete unwanted tickets.
- **Responsive Design**: The application layout adapts to different screen sizes, providing an optimal user experience on various devices.

## Technologies Used
- **Python 3.x**: The programming language used to build the application.
- **Tkinter**: The standard GUI toolkit for Python, used to create the graphical interface.
- **SQLite**: A lightweight database engine used to store booking information.
- **Pillow**: A Python Imaging Library used for handling images in the application.

## Installation Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/samaaye-events.git
   cd samaaye-events
   ```

2. **Install Required Packages**:
   Ensure you have Python 3.x installed. You can install the required packages using pip:
   ```bash
   pip install pillow
   ```

3. **Run the Application**:
   To start the application, execute the following command:
   ```bash
   python main.py
   ```

## Usage Instructions
1. **Viewing Events**:
   - Upon launching the application, users will see a list of upcoming events displayed as cards.
   - Each card contains essential information about the event, including the title, date, time, location, and ticket price.

2. **Booking Tickets**:
   - Click the "Buy Tickets" button on the desired event card.
   - Fill in the booking form with your details, including your full name, mobile number, and MPIN.
   - Confirm your booking to complete the ticket purchase.

3. **Managing Bookings**:
   - Navigate to the "Tickets" section to view all your bookings.
   - Use the search functionality to find specific bookings by name, mobile number, or event title.
   - Select a booking and click the "Delete" button to remove it from your list.

## Database Management
The application uses an SQLite database (`samaaye_events.db`) to store all booking information. The database is created automatically when the application is run for the first time. It includes a `bookings` table with the following fields:
- **ID** (Primary Key)
- **Name**
- **Mobile Number**
- **Event Title**
- **Event Date**
- **Event Time**
- **Event Location**
- **Ticket Quantity**
- **Total Price**
- **Booking Date** (Timestamp)

## Contributing
Contributions to the project are welcome! If you have suggestions for improvements or new features, please feel free to open an issue or submit a pull request.

### How to Contribute
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments
- Special thanks to the contributors and the open-source community for their support and resources.
- This project serves as an educational tool for learning about GUI development with Python and database management.


## Future Enhancements
- Implement user authentication for a more personalized experience.
- Add payment gateway integration for online payments.
- Enhance the UI/UX for better user engagement.
- Include a feature for event organizers to add and manage events.

## Conclusion
The Tkinter Ticket Booking Application is a comprehensive solution for managing event bookings. It combines a clean interface with robust functionality, making it an excellent choice for both users and event organizers.
```
