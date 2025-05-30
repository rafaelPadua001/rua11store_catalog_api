import sqlite3
from datetime import datetime

class Coupon:
    def __init__(self, id, user_id, client_id, title, code, discount, start_date, end_date, image_path, created_at, updated_at):
        self.id = id
        self.user_id = user_id
        self.client_id = client_id
        self.title = title
        self.code = code
        self.discount = discount
        self.start_date = start_date
        self.end_date = end_date
        self.image_path = image_path
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'client_id': self.client_id,
            'title': self.title,
            'code': self.code,
            'discount': self.discount,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'image_path': self.image_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    
    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            client_id=row["client_id"],
            title=row["title"],
            user_id=row["user_id"],
            code=row["code"],
            discount=row["discount"],
            start_date=datetime.fromisoformat(row["start_date"]),
            end_date=datetime.fromisoformat(row["end_date"]),
            created_at=datetime.fromisoformat(row["created_at"]) if "created_at" in row and row["created_at"] else None,
            updated_at=datetime.fromisoformat(row["updated_at"]) if "updated_at" in row and row["updated_at"] else None,
            image_path=row["image_path"] if "image_path" in row.keys() else None
        )
