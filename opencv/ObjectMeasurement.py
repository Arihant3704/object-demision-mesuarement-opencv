import cv2
import utlis
import time
import csv
from datetime import datetime
import os

###################################
webcam = True
path = '1.jpg'
cap = cv2.VideoCapture(6)
cap.set(10, 160)
cap.set(3, 1920)
cap.set(4, 1080)
scale = 3
wP = 210 * scale
hP = 297 * scale
###################################

# Image save directory
img_save_dir = 'recorded_images'
if not os.path.exists(img_save_dir):
    os.makedirs(img_save_dir)

# CSV setup
csv_file_path = 'measurements.csv'
# Check if the file needs a header
write_header = not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0

# Open in append mode
csv_file = open(csv_file_path, 'a', newline='')
csv_writer = csv.writer(csv_file)

if write_header:
    csv_writer.writerow(['Timestamp', 'Width (cm)', 'Height (cm)', 'Image Filename'])


# Time tracking
last_record_time = 0
record_interval = 0.5  # 500 milliseconds

# Variables to hold the last known measurement
last_nW = 0
last_nH = 0
last_nPoints = None
last_obj_rect = None

try:
    while True:
        if webcam:
            success, img = cap.read()
            if not success:
                print("Failed to capture image from webcam. Exiting.")
                break
        else:
            img = cv2.imread(path)
            if img is None:
                print(f"Failed to read image from path: {path}. Exiting.")
                break

        imgContours, conts = utlis.getContours(img, minArea=50000, filter=4)
        if len(conts) != 0:
            biggest = conts[0][2]
            imgWarp = utlis.warpImg(img, biggest, wP, hP)
            imgContours2, conts2 = utlis.getContours(imgWarp,
                                                     minArea=2000, filter=4,
                                                     cThr=[50, 50], draw=False)

            if len(conts2) != 0:
                # Update measurements with the latest detected object
                for obj in conts2:
                    cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)
                    last_nPoints = utlis.reorder(obj[2])
                    last_nW = round((utlis.findDis(last_nPoints[0][0] // scale, last_nPoints[1][0] // scale) / 10), 1)
                    last_nH = round((utlis.findDis(last_nPoints[0][0] // scale, last_nPoints[2][0] // scale) / 10), 1)
                    last_obj_rect = obj[3]

            # Always display the last known measurement if available
            if last_nPoints is not None:
                cv2.arrowedLine(imgContours2, (last_nPoints[0][0][0], last_nPoints[0][0][1]),
                                (last_nPoints[1][0][0], last_nPoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgContours2, (last_nPoints[0][0][0], last_nPoints[0][0][1]),
                                (last_nPoints[2][0][0], last_nPoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                # Calculate positions for text based on the corner points
                # For width text (along the top edge)
                width_text_x = (last_nPoints[0][0][0] + last_nPoints[1][0][0]) // 2 - 50
                width_text_y = last_nPoints[0][0][1] - 15
                cv2.putText(imgContours2, '{}cm'.format(last_nW), (width_text_x, width_text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)

                # For height text (along the left edge)
                height_text_x = last_nPoints[0][0][0] - 80
                height_text_y = (last_nPoints[0][0][1] + last_nPoints[2][0][1]) // 2
                cv2.putText(imgContours2, '{}cm'.format(last_nH), (height_text_x, height_text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)

            # Check if it's time to record
            current_time = time.time()
            if current_time - last_record_time >= record_interval and last_nPoints is not None:
                last_record_time = current_time
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
                img_filename = f"{timestamp}.jpg"
                img_save_path = os.path.join(img_save_dir, img_filename)
                cv2.imwrite(img_save_path, imgContours2)  # Save the image with annotations
                csv_writer.writerow([timestamp, last_nW, last_nH, img_filename])

            cv2.imshow('A4', imgContours2)

        img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        cv2.imshow('Original', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    print("Cleaning up and closing files.")
    if 'csv_file' in locals() and not csv_file.closed:
        csv_file.close()
    cap.release()
    cv2.destroyAllWindows()
