from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required')
        existing_name = self.__class__.query.filter_by(name=name).first()
        if existing_name:
            raise ValueError('Name must be unique')
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError('Phone number must be exactly 10 digits and only numbers')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError('Content should be atleast 250 characters long')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError('Summary should not exceed 250 characters long')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be Fiction or Non-Fiction')
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title is required')
        clickbaity_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        
        if not any(phrase in title for phrase in clickbaity_phrases):
            raise ValueError("Title must contain one of the following phrases: 'Won't Believe', 'Secret', 'Top', or 'Guess'")
    
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
