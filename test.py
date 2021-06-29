import telebot;
import detect_bot
import os

bot = telebot.TeleBot('1894384254:AAEmkAHVww2cUUCFRmLocNax9d20Rrgapfw');

@bot.message_handler(content_types=["text"])

def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, я бот-распознаватель аниме лиц. "
                                               "Отправь картинку и я найду на ней аниме-лица\n"
                                               "Я только учюсь не обижайся на меня, если что-то не так!\n"
                                               "Если есть вопросы напиши: /help")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Вот что я умею на данный момент:\n"
                                               "[Привет] - здороваюсь\n"
                                               "[/help] - помощь\n"
                                               "[*отправленное фото*] - нахожу аниме-лица\n"
                                               "[История] - показываю последнии 5 отрабоатнных файлов\n")
    elif message.text == "История":
        bot.send_message(message.from_user.id, "История!")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.message_handler(content_types=["photo"])
def get_photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    open("image.jpg", 'wb').write(downloaded_file)
    detect_bot.detect("image.jpg")
    os.remove("/home/aleksandr/практика/lbpcascade_animeface/image.jpg")
    name = "history_bot/out_img_to_bot" + str(int(open("count_for_bot.txt").read()) - 1) + ".png"
    bot.send_photo(message.from_user.id, open(name, 'rb'), "Вот кого я нашел!)")

bot.polling(none_stop=True, interval=0)
