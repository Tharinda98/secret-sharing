#import libraries
import numpy as np
import cv2
import time


# Capturing video through webcam
webcam = cv2.VideoCapture(0)

#define variables
bit_stream=[] 
charactor_list=[]
detected=False
end_time = 0
start_time = 0

#identity charactor list
letters=[" ","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

# Start a while loop
while(1):
      
    
    # webcam in image frames ignores the boolean value
    _, imageFrame = webcam.read()
  
    #convert imageframe from BGR(Blue-Green-Red) color space to HSV(Hue-Saturation-Value)
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
  
    #lower threshold
    lower_flashlight = np.array([0, 0, 255], np.uint8)
    #upper threshold
    upper_flashlight = np.array([0, 0, 255], np.uint8)

    #create a binary mask in the rang of lower and upper thresholds
    flash_mask = cv2.inRange(hsvFrame, lower_flashlight, upper_flashlight)
      
    #creates a 5x5 kernel filled with ones 
    kernal = np.ones((5, 5), "uint8")
    
    #hickening of the white areas in the image.
    flash_mask = cv2.dilate(flash_mask, kernal)

    #preserver only the white parts of the image
    res_flash = cv2.bitwise_and(imageFrame, imageFrame,
                               mask = flash_mask)
   
 
    # Creating contour to track flash
    contours, hierarchy = cv2.findContours(flash_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)


    #creating the bit stream with only 1's 
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
    

    #draw a bounding box around the detected contours and display text on the image if the area of the contour is greater than 300
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
        
    # display an image in a window with a given window name
    cv2.imshow("Flash Light Detection in Real-TIme", imageFrame)


    #print(bit_stream)

    # Check if 5 seconds have elapsed and reset the bit stream
    if((end_time) and (start_time)):
        # print(start_time)
        # print(end_time)
        if (not detected):
            end_time=time.time()
        if end_time - start_time > 2:
            count=len(bit_stream)
            bit_stream = []
            if count>0:
                print(count)
                charactor=letters[count-1]
                print("detected charactor:",charactor) 
                charactor_list.append(charactor)
                start_time = time.time()
                end_time = time.time()
                #print(charactor_list)
                
            
            elif end_time - start_time > 10:
                cv2.destroyAllWindows()
                message = ''.join(charactor_list)
                print("message recieved:",message)
                break
            
    #close the video stream and destroy all windows when the user presses the 'q' key
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break