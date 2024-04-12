sql_request_lib = {'available_quest': """
                                    SELECT question_text, question_id FROM public.questions
                                    LEFT JOIN (SELECT * FROM public.user_answers
											   WHERE user_id = %s)
                                    USING (question_id)
                                    WHERE questions.quiz_id = %s and user_answer_id IS NULL""",
                   'check_quiz_id': """
                                    SELECT quiz_id FROM public.users
                                    WHERE user_id = %s
                   """,
                   'write_user': """
                                    INSERT INTO public.users (user_id, first_name, quiz_id)
                                    VALUES (%s, %s, %s);
                   """,
                   'answer_options': """
                                    SELECT option_text, option_id, is_correct FROM public.options
                                    WHERE question_id = %s
                                      """,
                   'write_correct_answer': """
                                    INSERT INTO public.user_answers (quiz_id, question_id, user_id, chosen_option_id)
                                    VALUES (%s, %s, %s, %s);
                                      """,
                   'update_quiz_id': """
                                    UPDATE public.users
                                    SET quiz_id = %s
                                    WHERE user_id = %s
                                      """,
                   'delete_user_answers': """
                                    DELETE FROM public.user_answers 
                                    WHERE user_id = %s;
                                      """
                   }

