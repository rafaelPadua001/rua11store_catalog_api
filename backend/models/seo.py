from database import db

class Seo(db.Model):
    __tablename__ = 'seo'

    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(255), nullable=False, unique=True)
    metaTitle = db.Column(db.String(255), nullable=True)
    metaDescription = db.Column(db.Text, nullable=True)
    metaKeywords = db.Column(db.Text, nullable=True)
    ogTitle = db.Column(db.String(255), nullable=True)
    ogDescription = db.Column(db.Text, nullable=True)
    ogImage = db.Column(db.String(255), nullable=True)

    def __init__(self, route, metaTitle=None, metaDescription=None, metaKeywords=None,
                 ogTitle=None, ogDescription=None, ogImage=None):
        self.route = route
        self.metaTitle = metaTitle
        self.metaDescription = metaDescription
        self.metaKeywords = metaKeywords
        self.ogTitle = ogTitle
        self.ogDescription = ogDescription
        self.ogImage = ogImage

    def to_dict(self):
        return {
            "id": self.id,
            "route": self.route,
            "metaTitle": self.metaTitle,
            "metaDescription": self.metaDescription,
            "metaKeywords": self.metaKeywords,
            "ogTitle": self.ogTitle,
            "ogDescription": self.ogDescription,
            "ogImage": self.ogImage
        }
