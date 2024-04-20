-- Внесени данных в таблицу квизы
INSERT INTO public.quizzes (quiz_id, title, description) VALUES (1, 'Урок_1', 'For beginner');
INSERT INTO public.quizzes (quiz_id, title, description) VALUES (2, 'Урок_2', 'For advanced');
INSERT INTO public.quizzes (quiz_id, title, description) VALUES (3, 'Урок_3', 'For genius');

-- Внесени данных в таблицу вопросы
INSERT INTO public.questions (quiz_id, question_text) VALUES (1, 'My mother (to have) a bad headache.');
INSERT INTO public.questions (quiz_id, question_text) VALUES (1, 'my friend (to study) two foreign languages?');
INSERT INTO public.questions (quiz_id, question_text) VALUES (2, 'The teacher (to give out) us English magazines at every lesson.');
INSERT INTO public.questions (quiz_id, question_text) VALUES (2, 'Every morning, she (to hurry) to the University.');

-- Внесени данных в таблицу варианты ответов
INSERT INTO public.options (question_id, option_text, is_correct) VALUES (1, 'has', True);
INSERT INTO public.options (question_id, option_text, is_correct) VALUES (1, 'am', False);
INSERT INTO public.options (question_id, option_text, is_correct) VALUES (1, 'has got', False);

INSERT INTO public.options (question_id, option_text, is_correct) VALUES (2, 'Do my friend studys ...', False);
INSERT INTO public.options (question_id, option_text, is_correct) VALUES (2, 'Do study...', False);
INSERT INTO public.options (question_id, option_text, is_correct) VALUES (2, 'Does my friend study...', True);

INSERT INTO public.options (question_id, option_text, is_correct) VALUES (3, 'gives out', True);
INSERT INTO public.options (question_id, option_text, is_correct) VALUES (3, 'give out', False);
INSERT INTO public.options (question_id, option_text, is_correct) VALUES (3, 'will give out', False);

INSERT INTO public.options (question_id, option_text, is_correct) VALUES (4, 'hurry', False);
INSERT INTO public.options (question_id, option_text, is_correct) VALUES (4, 'hurries', True);
INSERT INTO public.options (question_id, option_text, is_correct) VALUES (4, 'will hurry', False);

INSERT INTO public.speech_test (quiz_id, question_text, answer) VALUES (1, 'What is the title of that TV show', 'Friends');
INSERT INTO public.speech_test (quiz_id, question_text, answer) VALUES (1, 'What language do they speak in this TV series?', 'English');