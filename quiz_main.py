import logging
import re
import config

import sql_handler
import telebot
import sql_request

# from pprint import pprint
from telebot import types
from connection_str import config_sql
from random import choice


telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['study'])
def start(msg):
    kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Let's go☕", callback_data='quiz')
    kb.add(button)
    bot.send_message(msg.chat.id, f'Желаете начать обучение?', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: re.match(r'quiz', call.data))
def issue_of_quizzes(query):
    # Проверяем есть ли пользователь в БД (если нет - записываем в бд, и ставим на 1-ый урок):
    is_registered = sql_handler.check_quiz_id(config_sql, sql_request.sql_request_lib['check_quiz_id'],
                                              query.from_user.id)
    if not is_registered:
        sql_handler.editing_info(config_sql, sql_request.sql_request_lib['write_user'], query.from_user.id,
                                 query.from_user.first_name, 1)
        user_quiz_id = 1
    else:
        user_quiz_id = is_registered[0]
    # user_quiz_id - хранит на каком квизе пользователь
    print('ID квиза, пользователя:', user_quiz_id)

    kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Пройти квиз☕', callback_data=f'quest_{user_quiz_id}')
    kb.add(button)

    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id,
                          text=f'Квиз №{user_quiz_id}', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: re.match(r'quest_', call.data))
def issue_of_questions(query):
    # Вывод, не пройденных, вопросов и варианты ответов:
    quiz_id = sql_handler.check_quiz_id(config_sql, sql_request.sql_request_lib['check_quiz_id'],
                                        query.from_user.id)[0]
    # Получаем список, не пройденных, вопросов и их id, по конкретному квизу:
    available_questions = sql_handler.get_available_quest(config_sql, sql_request.sql_request_lib['available_quest'],
                                                          query.from_user.id, quiz_id)

    print(quiz_id)
    if query.data[6:] == f'{quiz_id}' and available_questions:
        print(available_questions)
        question_text, question_id = choice(available_questions)
        print('quest_id: ', question_id)

        # Получаем список вариантов ответов, и их id, на конкретный вопрос:
        answer_options = sql_handler.get_info(config_sql, sql_request.sql_request_lib['answer_options'], question_id)
        print(answer_options)

        kb = types.InlineKeyboardMarkup()
        button_list = []
        for answer in answer_options:
            answer_text, answer_id, is_correct = answer
            button_list.append(types.InlineKeyboardButton(text=answer_text,
                                                          callback_data=f'answer_{quiz_id}_{question_id}_'
                                                                        f'{answer_id}_{is_correct}'))
        kb.add(*button_list)

        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id,
                              text=question_text, reply_markup=kb)
    else:
        next_quiz_id = int(quiz_id) + 1

        next_available_questions = sql_handler.get_available_quest(config_sql,
                                                                   sql_request.sql_request_lib['available_quest'],
                                                                   query.from_user.id, next_quiz_id)
        if next_available_questions:
            sql_handler.editing_info(config_sql, sql_request.sql_request_lib['update_quiz_id'], next_quiz_id,
                                     query.from_user.id)

            kb = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Let's go next☕", callback_data='quiz')
            kb.add(button)

            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id,
                                  text=f'Поздравляем, вы прошли {quiz_id} квиз🎉', reply_markup=kb)
        else:
            kb = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Начать заново?♾",
                                                callback_data='restart')
            kb.add(button)
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id,
                                  text='🤯Вы прошли все возможные курсы - не возможно!!!\n'
                                       'Наши искренние поздравления❤\n'
                                       "(Если нажать кнопку ниже:\n"
                                       "Ваш результат будет стерт как древние цивилизации)👽",
                                  reply_markup=kb)


@bot.callback_query_handler(func=lambda call: re.match(r'answer_', call.data))
def checking_responses(query):
    # Проверям какой ответ выбрал пользователь, если правильный - записываем в бд(ответ)
    if query.data[-4:] == 'True':
        data_list = query.data.split('_')
        print(data_list)

        # quiz_id = data_list[1]
        # question_id = data_list[2]
        # user_id = query.from_user.id
        # chosen_option_id = data_list[3]
        sql_handler.editing_info(config_sql, sql_request.sql_request_lib['write_correct_answer'], data_list[1],
                                 data_list[2], query.from_user.id, data_list[3])

        query.data = f'quest_{data_list[1]}'
        issue_of_questions(query)

    elif query.data[-5:] == 'False':
        bot.answer_callback_query(callback_query_id=query.id, text='К сожалению, не верно❌')


@bot.callback_query_handler(func=lambda call: re.match(r'restart', call.data))
def rewrite(query):
    sql_handler.editing_info(config_sql, sql_request.sql_request_lib['update_quiz_id'], 1, query.from_user.id)
    sql_handler.editing_info(config_sql, sql_request.sql_request_lib['delete_user_answers'], query.from_user.id)
    query.data = f'quiz'
    issue_of_quizzes(query)


bot.set_my_commands(commands=[types.BotCommand('/study',
                                               'Время пить чай🍵')])
bot.polling()
