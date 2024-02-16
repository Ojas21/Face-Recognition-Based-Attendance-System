
# Face Recognition Based Attendance System

This is a Python-based project for automating attendance tracking using face recognition. The system captures images of individuals, recognizes their faces, and logs their attendance in a CSV file. It also provides functionality to train the system with new faces and send attendance reports via email.

## Features

- **Capture Images**: Allows users to capture images of individuals along with their unique IDs and names.
- **Train Images**: Trains the face recognition system with the captured images for accurate recognition.
- **Attendance Tracking**: Utilizes face recognition to track attendance in real-time and logs it in a CSV file.
- **Email Reports**: Sends attendance reports via email to designated recipients.

## Dependencies

- **OpenCV**: Used for image processing and face detection.
- **PIL (Python Imaging Library)**: Required for image manipulation.
- **NumPy**: Essential for numerical operations in image processing.
- **Tkinter**: Provides the graphical user interface (GUI) for the application.
- **Pandas**: Facilitates data manipulation and CSV file handling.
- **Datetime**: Used for timestamping attendance records.
- **SMTPLib**: Enables sending emails from the application.
- **cx_Freeze**: Utilized for creating executable files for deployment.

## Usage

1. Run the `main.py` file to launch the application.
2. Enter the ID and name of individuals, then click on "Take Images" to capture their images.
3. Train the face recognition system by clicking on "Train Images".
4. To track attendance, click on "Attendance". The system will recognize faces in real-time and log attendance.
5. Click on "Email" to send attendance reports via email.
6. Use "Quit" to exit the application.

## Building Executable

To create an executable for deployment, run the `setup.py` script with cx_Freeze. It will generate an executable file for the respective platform.

```bash
python setup.py build
```

## Note

- Ensure all dependencies are installed before running the application.
- Make sure to provide valid email credentials for sending reports.

## Author

This project is developed by OJAS THENGADI.


