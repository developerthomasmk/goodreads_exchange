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
    image = db.Column(db.String(100), nullable=False, unique=True)
    owner = db.relationship('User', backref=db.backref('owner', lazy=True))
    
    def to_dict(self):
        return{
            'book_id': self.book_id,
            'username': self.owner.name,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'description': self.description,
            'status': self.status,
            'image': self.image,
            'location': self.owner.location,
            'latitude': self.owner.latitude,
            'longitude': self.owner.longitude
        }
        

class ExchangeRequest(db.Model):
    __tablename__ = 'exchange_requests'
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    status = db.Column(db.Enum('Pending', 'Accepted', 'Declined', name='request_status'), default='Pending')
    
    sender = db.relationship('User', foreign_keys=[requester_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    book = db.relationship('Book', foreign_keys=[book_id])