from pytube import YouTube
import requests
import sqlite3 as db
import bot

class VideoTransfuse:
    def __init__(self, url_video, channel_id):
        self.url_video = url_video
        self.channel_id = channel_id

    def save_from_youtube(self):
        try:
            video_data = YouTube(self.url_video)
            video_data.streams.get_highest_resolution().download(filename='video1.mp4')
        except:
            print('invalid link')

    def save_in_db(self):
        conn = db.connect('C:/sqlite_database/testLingua.db')
        cur = conn.cursor()
        file_id = bot.send_video(self.channel_id)

        cur.execute('insert into FileId values (?)', (file_id, ))

        conn.commit()
