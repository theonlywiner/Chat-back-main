from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BookSeries(db.Model):
    __tablename__ = 'book_series'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, unique=True)
    books = db.relationship('Books', backref='series', lazy=True)

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.BigInteger, primary_key=True)
    series_id = db.Column(db.BigInteger, db.ForeignKey('book_series.id'))
    name = db.Column(db.Text, unique=True)
    chapters = db.relationship('Chapters', backref='book', lazy=True)

class Authors(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.BigInteger, primary_key=True)
    info = db.Column(db.Text, unique=True)
    chapters = db.relationship('Chapters', backref='author', lazy=True)

class Chapters(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.BigInteger, primary_key=True)
    book_id = db.Column(db.BigInteger, db.ForeignKey('books.id'))
    name = db.Column(db.Text)
    author_id = db.Column(db.BigInteger, db.ForeignKey('authors.id'))
    full_content = db.Column(db.Text)
    paragraphs = db.relationship('Paragraphs', backref='chapter', lazy=True)

class Paragraphs(db.Model):
    __tablename__ = 'paragraphs'
    id = db.Column(db.BigInteger, primary_key=True)
    chapter_id = db.Column(db.BigInteger, db.ForeignKey('chapters.id'))
    ancient_text = db.Column(db.Text)
    modern_text = db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)