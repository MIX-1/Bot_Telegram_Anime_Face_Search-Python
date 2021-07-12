import cv2
import os.path

def detect(filename, cascade_file = "lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (10, 10))
    count = 0
    faces_out = []
    for (x, y, w, h) in faces:
        count += 1
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)
        cv2.putText(image, str(count), (x + w, y + h), cv2.FONT_ITALIC, 1, (0, 0, 0), 3)
        cropped = image[y:y + h, x:x + w]
        faces_out.append(cropped)

    numb = open('count_for_bot.txt').read()
    name = "out_img_to_bot" + numb + ".png"
    cv2.imwrite("history_bot/" + name, image)
    open('count_for_bot.txt', 'w').write(str(int(numb) + 1))
    return faces_out
