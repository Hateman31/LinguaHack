import yt_dlp
import bot
import psycopg2
from conn_preset import conn_str

video_id = '%(id)s'
class VideoTransfuse:
    # В url_video передавать список ↓↓↓
    def __init__(self, channel_id, url_video):
        self.url_video = url_video
        self.channel_id = channel_id
    # Сохраняем видео ↓↓↓
    def save_youtube_video(self):
        try:
            for url in self.url_video:
                ydl_opts = {
                    'format': 'mp4',
                    'outtmpl': f'vid_{video_id}.mp4'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(url)
        except:
            print('invalid link')
    # А здесь сохраняем субититры) ↓↓↓
    def save_youtube_subtitles(self):
        try:
            for url in self.url_video:
                ydl_opts_sub = {
                    'writeautomaticsub': True,
                    'subtitlesformat': 'srt',
                    "skip_download": True,
                    'outtmpl': f'sub_{video_id}'
                }
                with yt_dlp.YoutubeDL(ydl_opts_sub) as ydl:
                    ydl.download(url)
        except:
            print('invalid link')


    def save_in_db(self):
        try:
            for url in self.url_video:
                video_id_str = url.split('=')[1] # Берем id видео для удобного сохранения
                file_id = bot.send_video(self.channel_id, video_id_str)

                with psycopg2.connect(conn_str) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute('insert into quizzes (video_file_id, sub_file_id) values (%s, %s)',
                                       [file_id[0], file_id[1]])
                        conn.commit()
                        print('succesful video -', self.url_video.index(url))
        except TypeError:
            print('files missing')
