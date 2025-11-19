from database import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    is_subcategory = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    
    # Relacionamento opcional para subcategorias
    subcategories = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    products = db.relationship(
        'Product',
        back_populates="category",
        cascade="all, delete-orphan",
        foreign_keys="Product.category_id"
    )


    def save(self):
        """Salva ou atualiza a categoria"""
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar categoria: {e}")
            db.session.rollback()
            return False

    def update(self, **kwargs):
        """Atualiza campos da categoria"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()

    def delete(self):
        """Exclui a categoria"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar categoria: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def get_all():
        try:
            return Category.query.all()
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return []

    @staticmethod
    def get_by_id(category_id):
        try:
            return Category.query.get(category_id)
        except Exception as e:
            print(f"Erro ao buscar categoria por ID: {e}")
            return None

    @staticmethod
    def get_by_user(user_id):
        try:
            return Category.query.filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Erro ao buscar categorias do usuário: {e}")
            return []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_subcategory": self.is_subcategory,
            "parent_id": self.parent_id,
            "user_id": self.user_id,
            "products": [product.to_dict_basic() for product in self.products] if self.products else []
        }
