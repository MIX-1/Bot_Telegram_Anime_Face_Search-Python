import cv2
import sys
import os.path

def detect(filename, cascade_file = "../lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.05,
                                     minNeighbors = 5,
                                     minSize = (5, 5))
    count = 0
    faces_out = []
    for (x, y, w, h) in faces:
        count += 1
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, str(count), (x + w, y + h), cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
        cropped = image[y:y+h, x:x+w]
        faces_out.append(cropped)

    # count1 = 0
    # for face in faces2:
    #     count1 += 1
    #     name = "out" + str(count1) + ".png"
    #     cv2.imwrite("faces/" + name, face)

    cv2.imshow("AnimeFaceDetect", image)
    cv2.waitKey(0)
    numb = open('../count.txt').read()
    name = "out" + numb + ".png"
    cv2.imwrite("outs/" + name, image)
    open('../count.txt', 'w').write(str(int(numb) + 1))

if len(sys.argv) != 2:
    sys.stderr.write("usage: detect.py <filename>\n")
    sys.exit(-1)
    
detect(sys.argv[1])
