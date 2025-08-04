from marshmallow import validates, ValidationError, post_load, fields
from marshmallow_sqlalchemy import auto_field
from config import db, bcrypt, ma

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    messages = db.relationship('Message', backref='user', cascade="all, delete")

    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f"<User {self.username}>"

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'Message {self.name}  for {self.body}'


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
        exclude = ('_password_hash',)

    username = auto_field(required=True)
    password = fields.String(load_only=True, required=True)

    messages = fields.Nested('MessageSchema', many=True, dump_only=True)

    @validates('username')
    def validate_username(self, value, **kwargs):
        if len(value) < 2:
            raise ValidationError("Username must be at least 2 characters long")
        if not all(c.isalnum() or c.isspace() for c in value):
            raise ValidationError("Username must contain only letters, numbers, and spaces")

    @post_load
    def make_user(self, data, **kwargs):
        if isinstance(data, dict):
            password = data.pop('password', None)
            if not password:
                raise ValidationError("Password is required for registration")
            user = User(**data)
            user.set_password(password)
            return user
        return data

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        
    body = auto_field(required=True)
    username = auto_field(required=True)
    created_at = auto_field(required=True)

    @validates('username')
    def validate_username(self, value):
        if not value or len(value.strip()) < 2:
            raise ValidationError("User name must be at least 2 characters long")
        if len(value.strip()) > 30:
            raise ValidationError("User name must be 30 characters or less")
