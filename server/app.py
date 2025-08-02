from flask import request, session
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from config import app, db, api
from models import User, Message, UserSchema, MessageSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)


@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or not all(k in data for k in ['username', 'password']):
                return {'error': 'Missing required fields: username and password are required'}, 400

            if User.query.filter_by(username=data['username']).first():
                return {'error': 'Username already exists'}, 400

            new_user = user_schema.load(data)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id

            return user_schema.dump(new_user), 201

        except ValidationError as e:
            return {'error': str(e)}, 400

        except Exception as e:
            print(f'Registration error: {str(e)}')
            return {'error': f'An error ocurred during registration: {str(e)}'}, 500

api.add_resource(Register, '/register')

# class Messages(Resource):
#     def get(self):
#         user_id = session.get('user_id')
#         if user_id:
#             user = db.session.get(User, user_id)
#             if user:
#                 user_data = user_schema


#     if request.method == 'GET':
#         ordered_messages = Message.query.order_by('created_at').all()
#         messages = [message.to_dict() for message in ordered_messages]
#         return make_response( messages, 200 )
#     elif request.method == 'POST':
#         data = request.get_json()
#         new_message = Message(
#             body = data['body'],
#             username = data['username']  
#         )

#         db.session.add(new_message)
#         db.session.commit()

#         return make_response( new_message.to_dict(), 201 )

# @app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
# def messages_by_id(id):
#     message = Message.query.filter_by(id=id).first()

#     if request.method == 'GET':
#         return make_response( message, 200 )
#     elif request.method == 'PATCH':
#         data = request.get_json()
#         for attr in data:
#             setattr(message, attr, data.get(attr))
#         db.session.add(message)
#         db.session.commit()
#         return make_response( message.to_dict(), 200 )
#     elif request.method == 'DELETE':
#         db.session.delete(message)
#         db.session.commit()

#         respond_body = {
#             "delete_successful": True,
#             "message": "Message deleted."
#         }

#         return make_response( respond_body, 200 )

if __name__ == '__main__':
    app.run(port=5555)
