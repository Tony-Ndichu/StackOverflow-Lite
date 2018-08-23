"""
#app/api/answers/views.py
This is the module that handles question operations and their methods
"""

from flask import Flask, Blueprint
from flask_restful import reqparse, Api, Resource
from ..common import validator
from ..models.user import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token,
jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,)
from flask_jwt_extended import JWTManager


APP = Flask(__name__)


USER_BLUEPRINT = Blueprint('user', __name__)
API = Api(USER_BLUEPRINT, prefix='/api/v1')


class Registration(Resource):
    """
    this class deals with posting questions and getting all questions
    """

    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help='Please enter your first name.',

                        )

    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help='Please enter your last_name.',

                        )

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='Please enter your username.',

                        )

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='Please enter your email.',

                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Please enter your last_name.',

                        )

    @classmethod
    def post(cls):
        """Handles posting a user's registration"""
        data = cls.parser.parse_args()

        USER_LIST = UserModel.get_all_users()

        exists = validator.check_if_user_exists(
            USER_LIST, data['username'], data['email'])

        if exists:
            return {"message": exists}, 409

        verify_user_details = validator.user_detail_verification(
            data['first_name'], data['last_name'], data['username'])

        if verify_user_details:
            return {"message": verify_user_details}, 409

        create_user = UserModel.create_user(data['first_name'], data['last_name'], data[
                                            'username'], data['email'], data['password'])


        return {'message': 'Success!! User account has been created successfully'}, 201
 

class Login(Resource):
    """this class handles fetching a specific question and deleting it"""
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='Please enter your username.',

                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Please enter your email.',

                        )

    @classmethod
    def post(cls):
        """this handles a user's login"""
        data = cls.parser.parse_args()

        check_if_user_exists = UserModel.check_if_exists(data['username'])

        if not check_if_user_exists:
            return { "message" : "Sorry, we have no user with those credentials"}, 404

        user_check = UserModel.find_by_username(
            data['username'], data['password'])

    
        if user_check:
            access_token = create_access_token(identity = user_check, expires_delta=False)
            refresh_token = create_refresh_token(identity = user_check, expires_delta=False)

            return {"message": "Successfully logged in!!", "access_token" : access_token , "refresh_token" : refresh_token}, 200

        return {"message": "Sorry, wrong credentials" }, 401


class Logout(Resource):
    """logout a user and revoke his/her jwt identity"""

    @classmethod
    @jwt_required
    def post(cls):
        blacklist = set()
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return { "msg": "Successfully logged out" }, 200


class UserQuestions(Resource):
    """"get all the questions a user has ever asked on the platform"""
    @classmethod
    @jwt_required
    def get(slass):
        current_user_id = get_jwt_identity()

        get_user_questions = UserModel.get_user_questions(current_user_id)

        if get_user_questions:
            return { "message" : "Success!! Here are your questions" , "question_list" : get_user_questions }, 200
        return { "message" : "Sorry, you have no questions in our records"}, 404


API.add_resource(Registration, "/auth/signup")
API.add_resource(Login, "/auth/login")
API.add_resource(Logout, "/auth/logout")
API.add_resource(UserQuestions, "/auth/questions")


if __name__ == '__main__':
    APP.run()
