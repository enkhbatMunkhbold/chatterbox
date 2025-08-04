#!/usr/bin/env python3

from random import choice as rc
from datetime import date

from faker import Faker

from app import app
from models import db, User, Message

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print('clearing existing data...')

        # Check if tables exist before trying to delete from them
        try:
            # Check if users table exists and has data
            user_count = User.query.count()
            if user_count > 0:
                User.query.delete()
                print('Deleted existing users')
            else:
                print('No existing users to delete')
        except Exception as e:
            print('Users table does not exist yet, skipping user deletion')

        try:
            # Check if messages table exists and has data
            message_count = Message.query.count()
            if message_count > 0:
                Message.query.delete()
                print('Deleted existing messages')
            else:
                print('No existing messages to delete')
        except Exception as e:
            print('Messages table does not exist yet, skipping message deletion')

        print('Creating users...')
        users = []
        user_data = [
            {'username': 'paul', 'password': 'password123'},
            {'username': 'freddie', 'password': 'password123'},
            {'username': 'taylor', 'password': 'password123'},
            {'username': 'john', 'password': 'password123'},
            {'username': 'bryan', 'password': 'password123'}
        ]

        for user_info in user_data:
            user = User(username = user_info['username'])
            user.set_password(user_info['password'])
            users.append(user)
            db.session.add(user)

        db.session.commit()
        print(f'Created {len(users)} users')

        print('Creating messages...')

        messages = []
        for i in range(20):
            usernames = [user.username for user in users]

            message = Message(
                body=fake.sentence(),
                username=rc(usernames),
                user_id=rc(users).id
            )
            messages.append(message)

        db.session.add_all(messages)
        db.session.commit()
        print(f'Created {len(messages)} messages')        

