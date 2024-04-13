from telebot.async_telebot import AsyncTeleBot
import config as __cfg
import recognition
import asyncio
import json
import os

with open('users_states.json', 'r+') as f:
    states = json.load(f)

bot = AsyncTeleBot(__cfg.token)


def reset_state(user_id):
    with open("users_states.json", "r+") as jsonFile:
        data = json.load(jsonFile)
        if str(user_id) in data:
            data[str(user_id)] = 0
            jsonFile.seek(0)
            json.dump(data, jsonFile, indent=4)
            jsonFile.truncate()
        else:
            print(f"\033[31m\033[1mCannot reset: user {user_id} not found.")


def get_state(user_id):
    with open("users_states.json", "r+") as jsonFile:
        data = json.load(jsonFile)
        return data[str(user_id)]


def next_state(user_id):
    with open("users_states.json", "r+") as jsonFile:
        data = json.load(jsonFile)
        if str(user_id) in data:
            data[str(user_id)] += 1
            jsonFile.seek(0)
            json.dump(data, jsonFile, indent=4)
            jsonFile.truncate()
        else:
            data[str(user_id)] = 0
            jsonFile.seek(0)
            json.dump(data, jsonFile, indent=4)
            jsonFile.truncate()


@bot.message_handler(content_types=['voice'])
async def get_voice(msg):
    if get_state(msg.from_user.id) != 4:
        print(f"\033[31mRejected voice func to user {msg.from_user.id}: {msg.from_user.username}, "
              f"state {get_state(msg.from_user.id)}")
        return
    else:
        print(f"\033[32mAccepted voice func to user {msg.from_user.id}: {msg.from_user.username}")

    file_info = await bot.get_file(msg.voice.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    print('\033[33mDownloading file...')

    fpath = f'./audio/{file_info.file_unique_id}.ogg'

    with open(fpath, 'wb') as new_file:
        new_file.write(downloaded_file)

    print(f'\033[33mFile downloaded. Start recognition {fpath}... ')
    text = recognition.recognize(fpath)
    if text == "empty":
        print(f"Message from {msg.from_user.id}: {msg.from_user.username} - is empty.")
        await bot.reply_to(msg, "Please, say something in voice message.\n"
                                "(Пожалуйста, скажите что-нибудь в голосовом сообщении.)")
    else:
        print(f'\033[32mRecognition finished! Text: \033[0m{text}')
        await bot.reply_to(msg, text)

    os.remove(fpath)


asyncio.run(bot.polling())
