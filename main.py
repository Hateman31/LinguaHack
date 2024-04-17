import logging
import sql_handler
import telebot

from telebot import types
import config
from sql_handler import quizes_list, take_quiz_question, get_quiz_id, get_possible_answers
from connection_str import config_sql
from random import choice
import recognition as rcg

telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(config.token)


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
def get_voice(msg):
    # file_id = msg.voice.file_id
    file_info = bot.get_file(msg.voice.file_id)
    
    downloaded_file = bot.download_file(file_info.file_path)
    print('Downloading file...')
    fname = f'./audio/{file_info.file_unique_id}.ogg'
    with open(fname, 'wb') as new_file:
        new_file.write(downloaded_file)
    print('File downloaded. Start recognition...')

    text = rcg.recognize(fname)
    print(f'Recognition finished! Text: {text}')

    bot.send_message(
        msg.chat.id
        , text = text
    )
    

bot.set_my_commands(commands=[types.BotCommand('/study', 'Время пить чай🍵')])

bot.polling()
