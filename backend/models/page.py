# models/page.py
class Page:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            title=row["title"],
            content=row["content"]
        )
