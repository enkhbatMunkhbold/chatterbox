#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, User, Message

fake = Faker()

def make_messages():
    print('clearing existing data...')
    User.query.delete()
    Message.query.delete()

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
        usernames = [user.usernames for user in users]

        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)

    db.session.add_all(messages)
    db.session.commit()
    print(f'Created {len(messages)} messages')        

if __name__ == '__main__':
    with app.app_context():
        make_messages()
