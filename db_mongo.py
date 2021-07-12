import pymongo
import gridfs


def mongodb_connect():
    client = pymongo.MongoClient("localhost", 27017)
    return client.anime_db


db = mongodb_connect()
fs = gridfs.GridFS(db)


def input_db(data, filename, anime, name):
    fs.put(data, filename=filename, anime=anime, name=name)


def get_id(filename):
    return db.fs.files.find_one({"filename": filename})["_id"]


def get_name(filename):
    return db.fs.files.find_one({"filename": filename})["name"]


def get_anime(filename):
    return db.fs.files.find_one({"filename": filename})["anime"]


def output_db(id):
    return fs.get(id).read()


def name_check(name):
    try:
        if db.fs.files.find_one({"name": name})["name"] == name:
            return "Этот персонаж уже есть в базе, попробуйте другого"
    except Exception:
        return " "
