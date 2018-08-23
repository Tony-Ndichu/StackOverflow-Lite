"""

#app/api/models/answer.py
This is the answer model
"""
from datetime import datetime
from ..database.connect import conn, cur


class AnswerModel():
    """handles operations for the answers"""

    def __init__(self, answer):
        self.answer = answer
        self.answer_date = datetime.now()

    def get_all_answers():
        """retrieve all users from the database"""
        answer_list = []
        conn
        que = cur.execute("SELECT * FROM answers")

        try:
            que
        except (Exception, psycopg2.DatabaseError) as error:
            print (error)
            conn
            cur

        result = cur.fetchall()

        for i in result:
            answer_list.append(dict(answer_id = i[0] , user_id = i[3], question_id = i[2], answer_body = i[3], preffered = i[4]))

        return answer_list


    def save_answer(user_id, question_id, answer_body):
        """save new answer"""

        data = dict(userid=user_id, questionid=question_id,
                    answerbody=answer_body)

        submit = cur.execute("""INSERT INTO answers(user_id, question_id, answer_body, accepted , created_at) VALUES 
                    (%(userid)s, %(questionid)s, %(answerbody)s, false, current_timestamp )""", data)

        conn.commit()

        return "Successfully added answer"

    def confirm_que_poster(current_user_id, question_id):
        """confirm that the user trying to accept an answer actually posted the question"""

        fetch_question = "SELECT * FROM questions WHERE id = %s;"
        fetched_question = cur.execute(fetch_question, [question_id])
        result = cur.fetchall()

        for i in result:
            if i[1] != current_user_id:
                return "Sorry, you can't accept this answer since you didnt post the original question"

    def check_if_already_accepted(answer_id):
        """check if user already accepted the answers"""

        fetch_question = "SELECT * FROM answers WHERE id = %s;"
        fetched_question = cur.execute(fetch_question, [answer_id])
        result = cur.fetchall()

        for i in result:
            if i[4] == 'true':
                return "You have already accepted this answer"

    def accept_answer(answer_id):
        """accepts and answeer"""

        update_que = "UPDATE answers SET accepted = true WHERE id = %s;"
        cur.execute(update_que, [answer_id])
        conn.commit()

        return "Successfully accepted answer"

    def get_answers_to_a_question(questionid):
        """gets all the answers to a question"""
        answer_list = []

        fetch_user_answers = "SELECT * FROM answers WHERE question_id = %s;"
        fetched_answers = cur.execute(fetch_user_answers, [questionid])
        result = cur.fetchall()

        for i in result:
            answer_list.append(dict(answer_id=i[0], user_id=i[
                1], question_id=i[2], answer_body=i[3], accepted=i[4]))

        return answer_list