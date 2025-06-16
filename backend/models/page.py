from database import db

class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)

    def __init__(self, name, title, content):
        self.name = name
        self.title = title
        self.content = content
