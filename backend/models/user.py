from database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    
    # Relacionamento 1:1 com UserProfile (antes chamado ProfileModel)
    profile = db.relationship('UserProfile', back_populates='user', uselist=False)
