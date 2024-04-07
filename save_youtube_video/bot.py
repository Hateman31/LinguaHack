import telebot

bot = telebot.TeleBot('7180122363:AAE0hWh5EwZyFjeelJ_Gc_qSKCeJ4ZwTrtY')

def send_video(channel_id):
    try:
        video = open('video1.mp4', 'rb')
        msg = bot.send_video(channel_id, video)
        file_id = msg.video.file_id
        return file_id
    except:
        print('video not found')

