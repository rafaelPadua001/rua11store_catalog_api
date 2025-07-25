from models.seo import Seo
from database import db

class SeoController:

    @staticmethod
    def get_all_seo():
        seo_items = Seo.query.all()
        return [item.to_dict() for item in seo_items]

    @staticmethod
    def get_seo_by_id(seo_id):
        print(seo_id)
        return Seo.query.get(seo_id)

    @staticmethod
    def get_seo_by_route(route):
        route = str(route)
        print(route)
        return Seo.query.filter_by(route=route).first()

    @staticmethod
    def save_seo(seo_data):
        seo = Seo(
            route=seo_data.get('route'),
            metatitle=seo_data.get('metaTitle'),
            metadescription=seo_data.get('metaDescription'),
            metakeywords=seo_data.get('metaKeywords'),
            ogtitle=seo_data.get('ogTitle'),
            ogdescription=seo_data.get('ogDescription'),
            ogimage=seo_data.get('ogImage', {}).get('url') if isinstance(seo_data.get('ogImage'), dict) else seo_data.get('ogImage')
        )
        db.session.add(seo)
        db.session.commit()

    @staticmethod
    def update_seo(seo_id, seo_data):
        seo = Seo.query.get(seo_id)
        if seo:
            seo.route = seo_data.get('route', seo.route)
            seo.metatitle = seo_data.get('metaTitle', seo.metaTitle)
            seo.metadescription = seo_data.get('metaDescription', seo.metaDescription)
            seo.metakeywords = seo_data.get('metaKeywords', seo.metaKeywords)
            seo.ogtitle = seo_data.get('ogTitle', seo.ogTitle)
            seo.ogdescription = seo_data.get('ogDescription', seo.ogDescription)
            seo.ogimage = seo_data.get('ogImage', {}).get('url') if isinstance(seo_data.get('ogImage'), dict) else seo_data.get('ogImage')

            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_seo(seo_id):
        seo = Seo.query.get(seo_id)
        if seo:
            db.session.delete(seo)
            db.session.commit()
            return True
        return False
