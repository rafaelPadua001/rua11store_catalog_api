# models/page.py
class Page:
    def __init__(self, id, name, title, content):
        self.id = id
        self.name = name
        self.title = title
        self.content = content

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "content": self.content
        }

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            name=row["name"],
            title=row["title"],
            content=row["content"]
        )
