-- Создание таблицы квизов
CREATE TABLE quizzes (
    quiz_id Serial PRIMARY KEY ,
    video_file_id TEXT,
    sub_file_id TEXT,
    title VARCHAR(255),
    description TEXT,
    -- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы вопросов
CREATE TABLE questions (
    question_id serial PRIMARY KEY ,
    quiz_id INT,
    question_text TEXT,
    -- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
);

-- Создание таблицы вариантов ответов
CREATE TABLE options (
    option_id Serial PRIMARY KEY ,
    question_id INT,
    option_text TEXT,
    is_correct BOOLEAN,
    -- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

-- Создание таблицы ответов пользователей
CREATE TABLE user_answers (
    user_answer_id Serial PRIMARY KEY ,
    quiz_id INT,
    question_id INT,
    user_id INT,
    chosen_option_id INT,
    -- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
    FOREIGN KEY (chosen_option_id) REFERENCES options(option_id) ON DELETE CASCADE
);

CREATE TABLE USERS(
    user_id int PRIMARY KEY,
    first_name VARCHAR(100),
    quiz_id BIGINT
);