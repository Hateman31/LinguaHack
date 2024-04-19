import telebot

bot = telebot.TeleBot('7180122363:AAE0hWh5EwZyFjeelJ_Gc_qSKCeJ4ZwTrtY')

def send_video(channel_id, video_id):
    try:
        video = open(f'vid_{video_id}.mp4', 'rb')
        subtitles = open(f'sub_{video_id}.en.vtt', 'rb')

        msg_video = bot.send_video(channel_id, video)
        msg_sub = bot.send_document(channel_id, subtitles)

        file_id = [msg_video.video.file_id, msg_sub.document.file_id]
        return file_id
    except:
        print('file not found')

