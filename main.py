import cv2
import numpy as np

# Capture background image
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened() == False:
        cap = cv2.VideoCapture(1)
    if cap.isOpened() == False:
        raise Exception("Camera not found")
    
    while cap.isOpened():
        r,frame = cap.read()
        if r:
            frame = cv2.resize(frame,(720,480))
            frame = cv2.flip(frame,1)
            cv2.imshow("Camera (Press 'c' to capture background)",frame)
            if cv2.waitKey(1) & 0xff == ord("c"):
                cv2.imwrite("background.png",frame)
                break
        else: break

    # Main logic
    background = cv2.imread("background.png")
    while cap.isOpened():
        r,frame = cap.read()
        if r:
            frame = cv2.resize(frame,(720,480))
            frame = cv2.flip(frame,1)
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            lower = np.array([88, 80, 120], dtype=np.uint8)
            upper = np.array([102, 255, 255], dtype=np.uint8)
            mask = cv2.inRange(hsv,lower,upper)

            # remove noise
            mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
            mask = cv2.dilate(mask,np.ones((3,3),np.uint8))

            inv_mask = cv2.bitwise_not(mask)
            part1 = cv2.bitwise_and(frame,frame,mask=inv_mask)
            part2 = cv2.bitwise_and(background,background,mask=mask)
            final = cv2.addWeighted(part1,1,part2,1,0)
            combined = np.hstack((frame,final))
            cv2.imshow("Camera (Press 'q' to quit)",combined)
            if cv2.waitKey(1) & 0xff == ord("q"):
                break
        else: break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    try:
        cap.release()
        cv2.destroyAllWindows()
    except: pass