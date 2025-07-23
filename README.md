# Object Dimension Estimator with Web Interface


    
This project uses OpenCV to detect and measure objects placed on a standard A4 sheet of paper. It calculates the width and height of the object in centimeters and displays the results in real-time through a web interface.


<img width="1920" height="1080" alt="Screenshot from 2025-07-23 12-26-26" src="https://github.com/user-attachments/assets/db2f8208-13be-4bef-af04-79cc333688f5" />

## Features

-   **Real-time Object Detection:** Detects an A4 sheet and any object placed on it using a webcam.
-   **Accurate Measurements:** Calculates the dimensions of the object in centimeters.
-   **Data Logging:** Saves measurements (timestamp, width, height) and corresponding images.
-   **Web-Based UI:** A simple web page to display the latest measurement and image, updated automatically.

## Technologies Used

-   **Programming Language:** Python
-   **Libraries:**
    -   OpenCV: For image processing and computer vision.
    -   NumPy: For numerical operations.
    -   Flask: To create the web server that provides the data to the front end.
-   **Frontend:** HTML, CSS, JavaScript

## Setup Instructions

### Prerequisites

-   Python 3.x
-   A webcam

### Installation

1.  **Clone the repository (if applicable) or download the project files.**

2.  **Navigate to the project directory:**
    ```bash
    cd /home/arihant/Videos
    ```

3.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Project

You need to run two separate scripts in two different terminal windows.

**Terminal 1: Start the Object Measurement Script**

This script handles the computer vision part of the project. It captures video from the webcam, detects the A4 paper and the object, performs measurements, and saves the data.

```bash
python3 /home/arihant/Videos/opencv/ObjectMeasurement.py
```
*Keep this terminal running.*

**Terminal 2: Start the Web Server**

This script launches a Flask web server that reads the measurement data and serves the web interface.

```bash
python3 /home/arihant/Videos/server.py
```
*Keep this terminal running as well.*

## Accessing the Web Interface

Once both scripts are running, open your web browser and navigate to:

[http://127.0.0.1:5001](http://127.0.0.1:5001)

The page will display the most recent measurement and the corresponding annotated image. The data will automatically refresh every 2 seconds.

## Project Structure

-   `opencv/ObjectMeasurement.py`: The main script for video capture and processing.
-   `opencv/measurements.csv`: The CSV file where measurement data is logged.
-   `opencv/recorded_images/`: Directory where captured images are saved.
-   `server.py`: The Flask backend server.
-   `website/`: Directory containing the frontend files.
    -   `index.html`: The main HTML file.
    -   `style.css`: The stylesheet for the webpage.
    -   `script.js`: The JavaScript to fetch and display data.
-   `requirements.txt`: A list of all the Python dependencies.
-   `README.md`: This file.

