import cv2
import datetime as dt

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(0)
 
# Check if camera opened successfully
if (cap.isOpened() is False): 
  print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
    start = dt.datetime.now(dt.UTC)
    # Capture frame-by-frame
    ret, img = cap.read()
    if not ret:
        break
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    duration = dt.datetime.now(dt.UTC) - start
    fps = round(10000000 / duration.microseconds)
 
    # draw process result and fps
    img_1 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.putText(img_1, f'fps: {fps}',
            (20, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 125, 125), 2)

    # show output
    cv2.imshow("post process result", img_1)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()
