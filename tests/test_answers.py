"""

#app/test/test_answers.py
Handles all the tests related to answers
"""
from tests.base import Base
import json


class TestApp(Base):

    """Contains all the methods for testing answers"""

    def post_question_for_testing_purposes(self):
        """posts question to enable testing where existing question is needed"""


        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        result = self.client.post(
            'api/v1/questions', data=json.dumps(self.sample_data7), content_type='application/json',
             headers = {'Authorization' : 'Bearer '+ access_token })


        return result


    def post_answer_for_testing_purposes(self):
        """posts answer to enable testing where existing answer is needed"""

        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        result = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json', headers = {'Authorization' : 'Bearer '+ access_token })

        return result

    def test_user_can_answer_question(self):
        """checks that users can add an answer"""
        self.post_question_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        answer = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        mess = json.loads(answer.data.decode())


        self.assertEqual(answer.status_code, 201)
        self.assertEqual(mess['message'], "Success!! Your answer has been added")



    def test_user_cannot_answer_with_empty_content(self):
        """checks that user cannot add an empty answer"""
        self.post_question_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']


        result = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.empty_answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        mess = json.loads(result.data.decode())

        self.assertEqual(result.status_code, 409)
        self.assertEqual(mess['message'], "Too Short, Please add more input")


    def test_user_can_view_questions_with_the_most_answers(self):
        """checks that user can view the most answered question"""

        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        self.post_question_for_testing_purposes()

        self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer2),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        result = self.client.get(
            'api/v1/auth/questions/most_answered',
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        mess = json.loads(result.data.decode())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(mess['message'], "Here, are your most answered questions")


    def test_user_can_accept_answer_as_preffered(self):
        """checks that a user can choose and answer to be the preferred answer"""
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']

        accept_que=self.client.put(
            'api/v1/questions/1/answers/1/accept',
            data=json.dumps(self.answer2),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        mess = json.loads(accept_que.data.decode())

        self.assertEqual(accept_que.status_code, 200)
        self.assertEqual(mess['message'], "Success!! You have accepted this answer")


    def test_user_can_get_answers_to_specific_question(self):
        
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']  

        answer = self.client.get(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        mess = json.loads(answer.data.decode())

        self.assertEqual(answer.status_code, 200)  
        self.assertEqual(mess['message'], "Success!! Here are your answers")



    def test_user_must_enter_number_in_post_answer_uri(self):
        """checks that user doesnt do something like 'api/v1/questions/seven/answers'"""

        self.post_question_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        answer = self.client.post(
            'api/v1/questions/string/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        mess = json.loads(answer.data.decode())

        self.assertEqual(answer.status_code, 400)
        self.assertEqual(mess['message'], "Sorry, questionid must be a number or an integer")


    def test_user_must_enter_integer_in_get_answer_url(self):
        """checks that user doesnt do something like 'api/v1/questions/seven/answers'"""

        
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()
        result = json.loads(self.que.data.decode())
        access_token = result['access_token']  

        answer = self.client.get(
            'api/v1/questions/string/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        mess = json.loads(answer.data.decode())

        self.assertEqual(answer.status_code, 400)   
        self.assertEqual(mess['message'], "Sorry, questionid must be a number or an integer")




    def test_user_cannot_post_same_answer_twice(self):
        """checks that user cannot post exact same answer twice for the same question"""
        self.post_question_for_testing_purposes()
        access_que = json.loads(self.que.data.decode())
        access_token = access_que['access_token']

        self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        que = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        mess = json.loads(que.data.decode())

        self.assertEqual(que.status_code, 409)
        self.assertEqual(mess['message'], "Please enter a different answer, you cannot enter the same answer twice")


    def test_user_must_have_posted_question_to_accept_answer_as_preffered(self):
        """checks that a user can choose and answer to be the preferred answer"""
        self.post_question_for_testing_purposes()
        self.post_answer_for_testing_purposes()

        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.signup_details2),
            content_type='application/json')

        self.login2=self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(self.login_details2),
            content_type='application/json')

        result = json.loads(self.login2.data.decode())
        access_token = result['access_token']

        accept_que=self.client.put(
            'api/v1/questions/1/answers/1/accept',
            data=json.dumps(self.answer2),
            content_type='application/json',  headers = {'Authorization' : 'Bearer '+ access_token })

        mess = json.loads(accept_que.data.decode())

        self.assertEqual(accept_que.status_code, 401)
        self.assertEqual(mess['message'], "Sorry, you cant accept this answer since you didnt post the question")

        