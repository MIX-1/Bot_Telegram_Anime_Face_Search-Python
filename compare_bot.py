from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import os.path
import db_mongo
import cv2

KEY = "4a5a72cac76b41ee872f2ac767b678a9"
ENDPOINT = "https://compare-anime-faces-telebot.cognitiveservices.azure.com/"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


def compare_with_db(face):
    open("temp.jpg", "wb+")
    cv2.imwrite("temp.jpg", face)
    detected_faces = face_client.face.detect_with_stream(image=open("temp.jpg", 'rb'), detection_model='detection_03')
    if not detected_faces:
        os.remove("/home/aleksandr/практика/lbpcascade_animeface/temp.jpg")
        return -1
    first_image_face_ID = detected_faces[0].face_id

    numb = int(open('count_db.txt').read())
    percentages_similar = []
    for i in range(numb):
        filename = "file" + str(i) + ".jpg"
        out = db_mongo.output_db(db_mongo.get_id(filename))
        out_image = open("temp1.jpg", "wb+")
        out_image.write(out)
        out_image.close()
        detected_faces2 = face_client.face.detect_with_stream(image=open("temp1.jpg", 'rb'),
                                                              detection_model='detection_03')
        second_image_face_IDs = list(map(lambda x: x.face_id, detected_faces2))
        similar_faces = face_client.face.find_similar(face_id=first_image_face_ID, face_ids=second_image_face_IDs)
        os.remove("/home/aleksandr/практика/lbpcascade_animeface/temp1.jpg")
        if similar_faces:
            percentages_similar.append({"percent": similar_faces[0].confidence, "number": i})

    if len(percentages_similar) == 0:
        os.remove("/home/aleksandr/практика/lbpcascade_animeface/temp.jpg")
        return -1
    maximum = {"percent": 0.5, "number": -1}
    for pair in percentages_similar:
        if pair["percent"] > 0.5 and pair["percent"] > maximum["percent"]:
            maximum["percent"] = pair["percent"]
            maximum["number"] = pair["number"]
    os.remove("/home/aleksandr/практика/lbpcascade_animeface/temp.jpg")
    return maximum["number"]


def adding_check():
    detected_faces = face_client.face.detect_with_stream(image=open("temp.jpg", 'rb'), detection_model='detection_03')
    if not detected_faces:
        return -1
    first_image_face_ID = detected_faces[0].face_id
    out = db_mongo.output_db(db_mongo.get_id("file0.jpg"))
    out_image = open("temp1.jpg", "wb+")
    out_image.write(out)
    out_image.close()
    detected_faces2 = face_client.face.detect_with_stream(image=open("temp1.jpg", 'rb'),
                                                          detection_model='detection_03')
    second_image_face_IDs = list(map(lambda x: x.face_id, detected_faces2))
    os.remove("/home/aleksandr/практика/lbpcascade_animeface/temp1.jpg")
    try:
        face_client.face.find_similar(face_id=first_image_face_ID, face_ids=second_image_face_IDs)
    except Exception:
        return -1
    return 1
