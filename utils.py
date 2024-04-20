from pathlib import Path

def get_video(quiz_id):
    video = open(f'./media/{quiz_id}.mp4', 'rb')
    return video

if __name__ == '__main__':
    print(len(get_video(1)))