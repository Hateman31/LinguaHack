import psycopg2
from connection_str import config_sql

view_all_quizes = """
SELECT title FROM public.quizzes
"""
take_quiz_question = """
SELECT question_text FROM public.questions
WHERE quiz_id = 
"""
get_quiz_id = """
SELECT quiz_id FROM public.quizzes
WHERE title = 
"""
get_question_id = """SELECT question_id FROM public.questions
WHERE question_text = 
"""
take_possible_answers = """SELECT option_text, is_correct FROM public.options
WHERE question_id = 
"""


def repacking(list_quizes):
    if len(list_quizes) > 1:
        comfortable_list = []
        for tuple_ in list_quizes:
            for str_ in tuple_:
                comfortable_list.append(str_)
        return comfortable_list
    else:
        return list_quizes[0][0]


def get_info(conn_str, sql, extension_str=''):
    with psycopg2.connect(conn_str) as conn:
        print('Connection is created')
        with conn.cursor() as cursor:
            cursor.execute(sql + extension_str)
            all_records = cursor.fetchall()
            print('Connection was close')
    # print(len(all_records))
    result = repacking(all_records)
    return result


quizes_list = get_info(config_sql, view_all_quizes)


# def getaa(sql, quiz_id='1'):
#     result = sql + quiz_id
#     return result
#
#
# print(getaa(take_quiz_question))
