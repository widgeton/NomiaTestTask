# Запуск
В папке проекта необходимо применить миграции командой `python manage.py migrate`. Затем создать суперпользовотеля
командой `python manage.py createsuperuser`. Запустить сервер и перейти по адресу `127.0.0.1:8000/admin/` и ввести
данные ранее созданного пользователя. После этого можно приступить к созданию опросов.

Чтобы создать опрос необходимо в таблице **Surveys** создать запись без заполнения поля для первого вопроса. Затем
создать вопросы через таблицу **Questions** с привязкой к ранее созданному опросу. Далее необходимо вернуться в таблицу
**Surveys** и установить первый вопрос. После этого создать через таблицу **AnswerChoices** варианты ответа для каждого
вопроса с привязкой к своему вопросу и следующему вопросу. Таким образом создать дерево опроса.