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

class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or not all(k in data for k in ['username', 'password']):
                return {'error': 'Missing required fields'}, 400
            
            user = User.query.filter_by(username=data['username']).first()
            if not user:
                return {'error': 'Invalid credentials'}, 401
            
            if not user._password_hash:
                return {'message': 'Invalid credentials'}, 401
            
            if user.authenticate(data['password']):
                session['user_id'] = user.id
                return user_schema.dump(user), 200
            
            return {'message': 'Invalid credentials'}, 401
        
        except Exception as e:
            return {'error': str(e)}, 500
        
api.add_resource(Login, '/login')

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if user_id:
            user = db.session.get(User, user_id)
            if user:
                user_data = user_schema.dump(user)
                return user_data, 200
            return {'error': 'Not authenticated'}, 401
        return {'error': 'Not authenticated'}, 401
    
api.add_resource(CheckSession, '/check_session')

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204
    
api.add_resource(Logout, '/logout')

class Messages(Resource):
    def get(self):
        try:
            user_id = session.get('user_id')
            if not user_id:
                return {'error': 'Not authenticated'}, 401

            user = db.session.get(User, user_id)
            if not user:
                return {'error': 'User not found'}, 404

            ordered_messages = Message.query.order_by(Message.created_at).all()
            messages_data = []
            for message in ordered_messages:
                message_data = message_schema.dump(message)
                messages_data.append(message_data)

            return messages_data, 200
        
        except Exception as e:
            return {'error': f'Internal server error: {str(e)}'}, 500
    
    def post(self):
        try:
            user_id = session.get('user_id')
            if not user_id:
                return {'error': 'Not authenticated'}, 401

            user = db.session.get(User, user_id)
            if not user:
                return {'error': 'User not found'}, 404

            data = request.get_json()
            if not data['body']:
                return {'error': 'Missing required field: body is required'}, 400

            new_message = Message(
                body=data['body'],
                username=user.username,
                user_id=user_id
            )

            db.session.add(new_message)
            db.session.commit()

            return message_schema.dump(new_message), 201
        
        except ValidationError as ve:
            db.session.rollback()
            return {'error': ve.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': f'Internal server error: {str(e)}'}, 500
        
api.add_resource(Messages, '/messages')


    # if request.method == 'GET':
    #     ordered_messages = Message.query.order_by('created_at').all()
    #     messages = [message.to_dict() for message in ordered_messages]
    #     return make_response( messages, 200 )
    # elif request.method == 'POST':
    #     data = request.get_json()
    #     new_message = Message(
    #         body = data['body'],
    #         username = data['username']  
    #     )

    #     db.session.add(new_message)
    #     db.session.commit()

    #     return make_response( new_message.to_dict(), 201 )

class MessageById(Resource):
    def get(self, message_id):
        message = Message.query.filter_by(id=message_id).first()

        if not message:
            return {'error': 'Message not found'}, 404
        
        return message_schema.dump(message), 200
    
    def patch(self, message_id):
        message = Message.query.filter_by(id=message_id).first()

        if not message:
            return {'error': 'Message not found'}, 404
        
        try:
            data = request.get_json()

            if not data:
                return {'error': 'No data provided'}, 404
            
            updated_message = message_schema.load(data, instance=message, partial=True)
            db.session.commit()

            return message_schema.dump(updated_message), 200
        
        except ValidationError as ve:
            return {'error': ve.messages}, 400
        except Exception as e:
            return {'error': f'Internal server error {str(e)}'}, 500
        
    def delete(self, message_id):
        try:
            user_id = session.get('user_id')
            if not user_id:
                return {'error': 'Not authenticated'}, 401
            
            message = Message.query.get(message_id)
            if not message:
                return {'error': 'Message not found'}, 404
            
            if message.user_id != user_id:
                return {'error': 'Unauthorized access to message'}, 403
            
            serialized_message = message_schema.dump(message)
            try:
                db.session.delete(message)
                db.session.commit()
                return {
                    'message': 'Message deleted successfully',
                    'deleted_message': serialized_message
                }, 200
            
            except Exception as e:
                db.session.rollback()
                return {'error': f'Internal server error {str(e)}'}, 500
        except Exception as e:
            return {'error': f'Internal server error {str(e)}'}, 500
        
api.add_resource(MessageById, '/messages/<int:message_id>')

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
