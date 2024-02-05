from collections import namedtuple
from django.db import connection

QUERY = '''
SELECT srv_id,
       srv_name,
       passed,
       qst_id,
       qst_text,
       answered,
       answered * 100 / passed as qst_rate,
       qst_rank,
       ch_id,
       ch_text,
       chosen,
       chosen * 100 / answered as ch_rate
-- Считаем количество людей ответивших на первый вопрос опроса
FROM (SELECT srv.id AS srv_id,
             srv.name AS srv_name,
             COUNT(*) AS passed
      FROM survey_survey AS srv
      LEFT JOIN survey_answer AS ans ON ans.question_id = srv.first_question_id
      WHERE srv.id = %s)
-- Объединение с таблице вопросов опроса с подсчетом ответивших и их доли
JOIN (SELECT question_id AS qst_id,
             srv_id AS qst_srv_id,
             qst.text AS qst_text,
             COUNT(*) AS answered,
             DENSE_RANK() OVER (ORDER BY question_id) AS qst_rank
      FROM survey_question AS qst
      LEFT JOIN survey_answer AS ans ON qst.id = ans.question_id
      WHERE qst.srv_id = %s
      GROUP BY qst.id) ON srv_id = qst_srv_id
-- Объединение с таблицей вариантов ответа вопроса с подсчетом ответивших этими вариантами
JOIN (SELECT ch.id AS ch_id,
             ch.question_id AS ch_qst_id,
             ch.text AS ch_text,
             COUNT(ans.choice_id) AS chosen
      FROM survey_answerchoice AS ch
      LEFT JOIN survey_answer AS ans ON ch.id = ans.choice_id
      GROUP BY ch.id) ON ch_qst_id = qst_id;
'''

result = namedtuple('Result', ['srv_id', 'srv_name', 'passed', 'qst_id', 'qst_text', 'answered',
                               'qst_rate', 'qst_rank', 'ch_id', 'ch_text', 'chosen', 'ch_rate'])
survey = namedtuple('Survey', 'id, name, passed, questions')
question = namedtuple('Question', 'id, text, answered, rate, rank, choices')
choice = namedtuple('Choice', 'id, text, chosen, rate')


def get_survey(survey_id):
    results = request(QUERY, survey_id, survey_id)
    fst = results[0]
    srv = survey(fst.srv_id, fst.srv_name, fst.passed, {})
    for res in results:
        qst = srv.questions.setdefault(res.qst_id, question(res.qst_id, res.qst_text, res.answered,
                                                            res.qst_rate, res.qst_rank, []))
        qst.choices.append(choice(res.ch_id, res.ch_text, res.chosen, res.ch_rate))

    return srv


def request(query: str, *args):
    with connection.cursor() as cur:
        res = cur.execute(query, args)
        return [result(*row) for row in res.fetchall()]
