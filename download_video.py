import yt_dlp
import sqlite3 as db
import bot
import psycopg2
from conn_preset import conn_str

video_id = '%(id)s'

class VideoTransfuse:
    def __init__(self, url_video, channel_id):
        self.url_video = url_video
        self.channel_id = channel_id

    def save_youtube_video(self):
        try:
            ydl_opts = {
                'format': 'mp4',
                'outtmpl': f'vid_{video_id}.mp4'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.url_video)
        except:
            print('invalid link')

    def save_youtube_subtitles(self):
        try:
            ydl_opts_sub = {
                'writeautomaticsub': True,
                'subtitlesformat': 'srt',
                "skip_download": True,
                'outtmpl': f'sub_{video_id}'
            }
            with yt_dlp.YoutubeDL(ydl_opts_sub) as ydl:
                ydl.download(self.url_video)
        except:
            print('invalid link')


    def save_in_db(self):
        video_id_str = self.url_video.split('=')[1]
        file_id = bot.send_video(self.channel_id, video_id_str)

        with psycopg2.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('insert into quizzes (video_file_id, sub_file_id) values (%s, %s)',
                               [file_id[0], file_id[1]])
                conn.commit()
                print('succesful')


vid = VideoTransfuse('https://www.youtube.com/watch?v=J3mSVfMgZfA', '-1002105419957')
# vid.save_youtube_video()
# vid.save_youtube_subtitles()
vid.save_in_db()