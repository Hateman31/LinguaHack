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


@bot.message_handler(commands=['study'])
def start(msg):
    kb = types.InlineKeyboardMarkup()
    for quiz in sql_handler.quizes_list:
        name_quiz = quiz.replace('_', ' ')
        button = types.InlineKeyboardButton(name_quiz, callback_data=quiz)
        kb.add(button)

    bot.send_message(
        msg.chat.id
        , text=f'👋Приветствуем вас, {msg.from_user.first_name}, в нашем чайном домике!\n'
                                       f'Курсы в которых ваше восприятие чая может улучшиться☕:',
                     reply_markup=kb)


@bot.callback_query_handler(func=lambda x: True)
def choose_quiz(query):
    if query.data in sql_handler.quizes_list:
        current_quiz_id = query.data

        str_quiz_id = str(sql_handler.get_info(config_sql, sql_handler.get_quiz_id, f"'{current_quiz_id}'"))

        questions = sql_handler.get_info(config_sql, sql_handler.take_quiz_question, str_quiz_id)
        random_question = choice(questions)

        str_question_id = str(sql_handler.get_info(config_sql, sql_handler.get_question_id, f"'{random_question}'"))

        possible_answers_list = sql_handler.get_info(config_sql, sql_handler.take_possible_answers, str_question_id)

        print(possible_answers_list)

        kb_answer = types.InlineKeyboardMarkup()
        button_list = []

        for answer_num in range(0, len(possible_answers_list), 2):
            answer = possible_answers_list[answer_num]

            is_correct = str(possible_answers_list[answer_num + 1])

            button = types.InlineKeyboardButton(answer, callback_data=is_correct)
            button_list.append(button)
            answer_num += 2
        kb_answer.add(*button_list)

        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id,
                              text=random_question, reply_markup=kb_answer)

        questions.remove(random_question)


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
