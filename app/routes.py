import os
import uuid
from flask import current_app, flash, jsonify, redirect, render_template, request, send_from_directory, session, url_for
from app.config import db
from werkzeug.utils import secure_filename
from app.models import Book, ExchangeRequest, User


def init_routes(app):
    
    @app.route('/uploads/images/<path:filename>')
    def image_file(filename):
        return send_from_directory('uploads/images', filename)
    
    @app.route('/')
    def initial():
        return redirect(url_for('login'))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']        
            user = User.query.filter_by(email=email, password=password).first()
            print("MyPrint:::",user)

            if user:
                session['user_id'] = user.user_id
                return redirect(url_for('home'))
            else:
                flash("Invalid email or password", "danger")

        return render_template('login.html')
    
    
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            data = request.get_json()

            if not data:
                return jsonify({"message": "Invalid request, expected JSON"}), 400
                
            existing_user = User.query.filter_by(email=data["email"]).first()
            if existing_user:
                return jsonify({"message": "Email already registered"}), 400
            
            new_user = User(
                name=data["name"],
                email=data["email"],
                password=data["password"],
                phone=data["phone"],
                location=data["location"],
                latitude=float(data["latitude"]),
                longitude=float(data["longitude"])
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                return jsonify({"message": "Registration successful"}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": "Error registering user", "error": str(e)}), 500
        
        return render_template('register.html')
    
    
    @app.route('/home')
    def home():
        return render_template('home.html')
    
    @app.route('/get_books', methods=['GET'])
    def get_books():
        current_user_id = session.get('user_id')
        books = Book.query.filter((Book.user_id != current_user_id) & (Book.status == 'Available')).all()
        books_data =[book.to_dict() for book in books]
        return jsonify(books_data)
    
    
    @app.route('/mybooks')
    def my_books():
        return render_template('my_books.html')
    
    
    @app.route('/get_my_books', methods=['GET'])
    def get_my_books():
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'User not logged in'}), 401

        books = Book.query.filter_by(user_id=current_user_id).all()
        book_list = [book.to_dict() for book in books]

        return jsonify({'books': book_list})
    
    
    
    @app.route('/addbook', methods=['GET', 'POST'])
    def add_book():
        if request.method == 'GET':
            return render_template('add_books.html')

        if request.method == 'POST':
            current_user_id = session.get('user_id')
            if not current_user_id:
                return jsonify({'error': 'User not logged in'}), 401
            
            title = request.form.get('title')
            author = request.form.get('author', '')
            genre = request.form.get('genre', '')
            description = request.form.get('description', '')
            
            file = request.files['bookImage']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            
            print(unique_filename)
                    
            new_book = Book(
                user_id=current_user_id,
                title=title,
                author=author,
                genre=genre,
                description=description,
                status='Available',
                image=unique_filename
            )

            db.session.add(new_book)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Book added successfully!'})
        
        
        
        
        
    @app.route('/view_book/<int:book_id>')
    def view_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return "Book not found", 404

        return render_template('book_details.html', book=book)


    @app.route('/get_book_details/<int:book_id>')
    def get_book_details(book_id):
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        return jsonify(book.to_dict())

    @app.route('/exchange_book/<int:book_id>', methods=['POST'])
    def exchange_book(book_id):
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'User not logged in'}), 401

        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        if book.user_id == current_user_id:
            return jsonify({'error': 'You cannot exchange your own book'}), 400

        if book.status == 'Exchanged':
            return jsonify({'error': 'Book already exchanged'}), 400

        new_request = ExchangeRequest(requester_id=current_user_id, receiver_id=book.user_id, book_id=book_id)
        db.session.add(new_request)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Book exchange requested successfully!'})
    
    
    
    @app.route('/delete_book/<int:book_id>', methods=['POST', 'GET'])
    def delete(book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted successfully'}, 200
        else:
            return {'message': 'Book not found'}, 404
        
        
        
        
    @app.route('/update-request-status/<int:req_id>')
    def update_req_status(req_id):
        status = request.form.get('status')

        request = ExchangeRequest.query.get(req_id)
        if request and request.status == 'Pending':
            book = Book.query.get(req_id)
            if book and book.status == 'Available':
                request.status = 'Exchanged'
                book.status = status
                db.session.commit()
                return jsonify(success=True)
            return jsonify(success=False)
        return jsonify(success=False)
        
        
        
    @app.route('/history')
    def my_history():
        user_id = session.get('user_id')
    
        if not user_id:
            return redirect('/login')

        exchange_requests = ExchangeRequest.query.filter_by(receiver_id=user_id).all()
        print("A",exchange_requests, user_id)
        
        books_exchanged = Book.query.filter_by(user_id=user_id, status='Exchanged').all()
        print("B",books_exchanged)

        borrowed_requests = ExchangeRequest.query.filter(
            ExchangeRequest.requester_id == user_id
        ).all()
        borrowed_books = [req.book for req in borrowed_requests]
        print("C",borrowed_books)

        return render_template('history.html', exchange_requests=exchange_requests,  books_exchanged=books_exchanged, books_borrowed=borrowed_books)
        
        
        
        
        
    @app.route('/book-return/<int:req_id>')
    def return_book(req_id):
        request = ExchangeRequest.query.get(req_id)
        if request and request.status != 'Pending':
            book = Book.query.get(req_id)
            if book and book.status == 'Exchanged':
                request.status = 'Available'
                book.status = 'Returned'
                db.session.commit()
                return jsonify(success=True)
            return jsonify(success=False)
        return jsonify(success=False)
    
    
    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))