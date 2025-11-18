# controllers/variation_controller.py
from models.variation import Variation
from database import db

class VariationController:

    @staticmethod
    def insert_variations(product_id: int, product_name: str, variations_data: list):
        items = []

        for var in variations_data:
            variation = Variation(
                product_id=product_id,
                product_name=product_name,
                variation_type=var.get("type"),
                value=var.get("value"),
                quantity=var.get("quantity", 0)
            )

            db.session.add(variation)
            items.append(variation)

        db.session.commit()
        return items


    @staticmethod
    def delete_variations_by_product(product_id: int):
        Variation.query.filter_by(product_id=product_id).delete()
        db.session.commit()
