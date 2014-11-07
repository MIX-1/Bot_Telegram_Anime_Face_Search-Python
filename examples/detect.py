import cv2
import cv  
import sys

def detect(filename):
    cascade = cv2.CascadeClassifier("../lbpcascade_animeface.xml")
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (24, 24),
                                     flags = cv.CV_HAAR_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow("AnimeFaceDtect", image)
    cv2.waitKey(0)
    cv2.imwrite("out.png", image)
    
if __name__ == "__main__":
    detect(sys.argv[1])