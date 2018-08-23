"""
#app/api/models/user.py
This is the user model
"""
import psycopg2
from ..database.connect import conn, cur
from werkzeug.security import generate_password_hash, \
    check_password_hash


class UserModel():
    """this handles user registration and authentication"""

    def get_all_users():
        """retrieve all users from the database"""
        user_list = []
        conn
        que = cur.execute("SELECT * FROM users")

        try:
            que
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn
            cur

        result = cur.fetchall()

        for i in result:
            user_list.append(result)

        return result

    def create_user(first_name, last_name, username, email, password):
        """save new user data"""

        data = dict(first_name=first_name, last_name=last_name,
                    username=username, email=email, password=generate_password_hash(password))

        submit = cur.execute("""INSERT INTO users (first_name, last_name, username, email, password, created_at) VALUES 
					(%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s, current_timestamp)""", data)

        conn.commit()

    def check_if_exists(username):
        """checks if user exists in system"""
        fetch_question = "SELECT * FROM users WHERE username = %s;"
        fetched_question = cur.execute(fetch_question, [username])
        result = cur.fetchall()

        return result

    def save_token(access_token):
        """save access_token"""
        save_que = "INSERT INTO tokens (token, expired) VALUES (%s, 'false');"
        cur.execute(save_que, [access_token])
        conn.commit()

    def expire_token():
        """turn the tken to expired"""
        update_que = cur.execute("UPDATE tokens SET expired = True WHERE expired = 'false';")
        conn.commit()

    def check_if_logged_out():
        """check if user is already logged out"""
        fetch_question = cur.execute("SELECT * FROM tokens WHERE expired = 'false';")
        result = cur.fetchall()

        if not result:
            return "You have already been logged out"

    def find_by_username(username, password):
        """check user dedtails on login"""
        user_list = []

        conn
        que = cur.execute("SELECT * FROM users")

        try:
            que
        except (Exception, psycopg2.DatabaseError) as error:
            conn
            cur
            que

        result = cur.fetchall()

        for i in result:

            if i[3] == username and check_password_hash(i[5], password):
                u_id = i[0]
                return u_id

    def get_user_questions(current_user_id):
        """retireves all the questions a user has ever asked on the platform"""

        question_list = []

        fetch_user_questions = "SELECT * FROM questions WHERE user_id = %s;"
        fetched_questions = cur.execute(
            fetch_user_questions, [current_user_id])
        result = cur.fetchall()

        for i in result:
            question_list.append(dict(question_id=i[0], user_id=i[
                1], title=i[2], description=i[3]))

        return question_list
