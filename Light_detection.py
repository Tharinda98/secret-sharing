# Python code for Multiple Color Detection
  
  
import numpy as np
import cv2
import time



# Capturing video through webcam
webcam = cv2.VideoCapture(0)
bit_stream=[] 
detected=False
end_time = 0
start_time = 0
letters=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
# Start a while loop
while(1):
      
    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()
  
    # Convert the imageFrame in 
    # BGR(RGB color space) to 
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
  
    lower_flashlight = np.array([0, 0, 255], np.uint8)
    upper_flashlight = np.array([0, 0, 255], np.uint8)
    flash_mask = cv2.inRange(hsvFrame, lower_flashlight, upper_flashlight)
      
    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")
    
    flash_mask = cv2.dilate(flash_mask, kernal)
    res_flash = cv2.bitwise_and(imageFrame, imageFrame,
                               mask = flash_mask)
   
 
    # Creating contour to track flash
    contours, hierarchy = cv2.findContours(flash_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
     
    if (contours):
        if not detected:
            # Set start time
            start_time = time.time()
            detected=True
            bit_stream.append(1)
        
    else:
        if detected:
            # Set end time
            end_time = time.time()
            #bit_stream.append(0)
            detected=False
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        
        if(area > 300):
            
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (255, 0, 0), 2)
              
            cv2.putText(imageFrame, "Flash", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 255, 0))
        
    # Program Termination
    cv2.imshow("Flash Light Detection in Real-TIme", imageFrame)
    print(bit_stream)

    # Check if 5 seconds have elapsed and reset the bit stream
    if((end_time) and (start_time)):
        if (not detected):
            end_time=time.time()
        if end_time - start_time > 5:
            count=bit_stream.count(1)
            print(letters[count])   
            bit_stream = []
            start_time = time.time()



    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break