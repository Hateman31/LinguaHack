from telebot.async_telebot import AsyncTeleBot
import config as __cfg
import recognition
import asyncio
import json

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
            print(f"Cannot reset: user {user_id} not found.")


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


# There is problem
@bot.message_handler(content_types=['voice'])
async def get_voice(msg):
    try:
        user_stat = states[str(msg.from_user.id)]
        if user_stat != 4:
            print(f"Rejected voice func to user {msg.from_user.id}: {msg.from_user.username}")
            return
        else:
            print(f"Accepted voice func to user {msg.from_user.id}: {msg.from_user.username}")

        # There
        file_info = await bot.get_file(msg.voice.file_id)
        downloaded_file = await bot.download_file(file_info.file_unique_id)

        print('Downloading file...')

        fpath = f'./audio/{file_info.file_unique_id}.ogg'

        with open(fpath, 'wb') as new_file:
            new_file.write(downloaded_file)

        print('File downloaded. Start recognition...')
        text = recognition.recognize(fpath)
        print(f'Recognition finished! Text: {text}')

        await bot.send_message(msg.chat.id, text)

    except Exception as e:
        print(f"An error occurred: {e}")
        await bot.send_message(msg.chat.id, "Something went wrong... Try again later.")


asyncio.run(bot.polling())
