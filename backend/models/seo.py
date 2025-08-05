from database import db

class Seo(db.Model):
    __tablename__ = 'seo'

    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(255), nullable=False, unique=True)
    metatitle = db.Column(db.String(255), nullable=True)
    metadescription = db.Column(db.Text, nullable=True)
    metakeywords = db.Column(db.Text, nullable=True)
    ogtitle = db.Column(db.String(255), nullable=True)
    ogdescription = db.Column(db.Text, nullable=True)
    ogimage = db.Column(db.String(255), nullable=True)

    def __init__(self, route, metatitle=None, metadescription=None, metakeywords=None,
                 ogtitle=None, ogdescription=None, ogimage=None):
        self.route = route
        self.metatitle = metatitle
        self.metadescription = metadescription
        self.metakeywords = metakeywords
        self.ogtitle = ogtitle
        self.ogdescription = ogdescription
        self.ogimage = ogimage

    def to_dict(self):
        return {
            "id": self.id,
            "route": self.route,
            "metaTitle": self.metatitle,
            "metaDescription": self.metadescription,
            "metaKeywords": self.metakeywords,
            "ogTitle": self.ogtitle,
            "ogDescription": self.ogdescription,
            "ogImage": self.ogimage
        }
