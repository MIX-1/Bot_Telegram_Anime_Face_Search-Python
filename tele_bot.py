import telebot
import detect_bot
import db_mongo
import os
import cv2
import compare_bot

bot = telebot.TeleBot('1894384254:AAEmkAHVww2cUUCFRmLocNax9d20Rrgapfw');

anime = ["Нет"]
temp_photo = [0]


@bot.message_handler(commands=["add"])
def info_text(message):
    msg = bot.send_message(message.from_user.id, "Если хочешь внести персонажа следуй следующим инструкциям:\n"
                                                 "Сначала отправь фото аниме-персонажа"
                                                 "(Требования: на фото один персонаж, качество не больше full hd,"
                                                 "лицо должно быть четко различимо и без различных искажений)")
    bot.register_next_step_handler(msg, input_photo)


def input_photo(message):
    temp = open("temp.jpg", "wb+")
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    temp.write(downloaded_file)
    if compare_bot.adding_check() == -1:
        bot.send_message(message.from_user.id, "Фото не подходит, попробуйте другое (Заново напишите \"/add\")")
        quit()
    face = detect_bot.detect("temp.jpg")
    if len(face) == 0:
        bot.send_message(message.from_user.id, "Не вижу персонажа, попробуй другое фото (Заново напишите \"/add\")")
        quit()
    os.remove("/home/aleksandr/практика/lbpcascade_animeface/temp.jpg")
    temp = open("temp.jpg", "wb+")
    cv2.imwrite("temp.jpg", face[0])
    temp_photo[0] = temp
    msg = bot.send_message(message.from_user.id, "Из какого аниме персонаж? Напиши (Если аниме нет, то напиши \"нет\")")
    bot.register_next_step_handler(msg, input_anime)


def input_anime(message):
    anime[0] = message.text
    msg = bot.send_message(message.from_user.id, "Напиши имя персонажа")
    bot.register_next_step_handler(msg, input_name)


def input_name(message):
    name = message.text
    msg_fail = db_mongo.name_check(name)
    if len(msg_fail) > 1:
        msg = bot.send_message(message.from_user.id, msg_fail + " (Заново напишите \"/add\")")
        bot.register_next_step_handler(msg, info_text)
        quit()
    numb = open('count_db.txt').read()
    filename = "file" + numb + ".jpg"
    open('count_db.txt', 'w').write(str(int(numb) + 1))
    db_mongo.input_db(temp_photo[0], filename, anime[0], name)
    os.remove("/home/aleksandr/практика/lbpcascade_animeface/temp.jpg")
    bot.send_message(message.from_user.id, name + " теперь в базе")


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, я бот-распознаватель аниме лиц. "
                                               "Отправь картинку, и я найду на ней аниме-лица.\n"
                                               "Я только учюсь, не обижайся на меня, если что-то не так!\n"
                                               "Если есть вопросы напиши: /help")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Вот что я умею на данный момент:\n"
                                               "[Привет] - здороваюсь\n"
                                               "[/help] - помощь\n"
                                               "[*отправленное фото*] - нахожу аниме-лица и их обладателей\n"
                                               "[История] - показываю последнии 5 отработаных фото за все время\n"
                                               "[/add] - добавить в базу персонажа")
    elif message.text == "История":
        count = int(open("count_for_bot.txt").read())
        count_history = 5
        if count < 5:
            count_history = count
        if count == 0:
            bot.send_message(message.from_user.id, "Пока нет обработанных фото:(\nТвоё может стать первым!!!"
                                                   "\nПопробуй!")
        else:
            bot.send_message(message.from_user.id, "Вот последнии " + str(count_history) +
                             " обработанных фото от всех пользователей:")
            for i in range(1, count_history + 1, 1):
                name = "history_bot/out_img_to_bot" + str(count - i) + ".png"
                bot.send_photo(message.from_user.id, open(name, 'rb'), str(i) + "-ое фото")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(content_types=["photo"])
def get_photo(message):
    numb = int(open('count_db.txt').read())
    if numb == 0:
        bot.send_message(message.from_user.id, "В базе нет данных внесите через команду /add")
        quit()
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    open("image1.jpg", 'wb').write(downloaded_file)
    faces = detect_bot.detect("image1.jpg")
    os.remove("/home/aleksandr/практика/lbpcascade_animeface/image1.jpg")
    count = int(open("count_for_bot.txt").read())
    name = "history_bot/out_img_to_bot" + str(count - 1) + ".png"
    bot.send_photo(message.from_user.id, open(name, 'rb'), "Я нашел на фото " + str(len(faces)) +
                   " аниме-персонажей\nЕсли кого-то не нашёл, то извини!")
    count = 0
    for face in faces:
        count = count + 1
        ans = compare_bot.compare_with_db(face)
        if ans == -1:
            bot.send_message(message.from_user.id, str(count) + ": нет в базе (либо я не смог найти)")
        else:
            filename = "file" + str(ans) + ".jpg"
            bot.send_message(message.from_user.id, str(count) + ": " + db_mongo.get_name(filename) + " из аниме " +
                             db_mongo.get_anime(filename))


bot.polling(none_stop=True, interval=0)
