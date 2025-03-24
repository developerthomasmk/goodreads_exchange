import datetime
from app.config import db


class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class Book(db.Model):
    __tablename__ = 'books'
    
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', name='fk_user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    genre = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.Enum('Available', 'Exchanged', name='book_status'), default='Available')
    owner = db.relationship('User', backref=db.backref('owner', lazy=True))
    
    def to_dict(self):
        return{
            'book_id': self.book_id,
            'username': self.owner.name,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'description': self.description,
            'status': self.status
        }