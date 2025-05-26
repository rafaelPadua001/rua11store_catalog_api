class Seo:
    def __init__(self, id, route, metaTitle, metaDescription, metaKeywords, ogTitle, ogDescription, ogImage):
        self.id = id
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

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            route=row["route"],
            metaTitle=row["title"],
            metaDescription=row["description"],
            metaKeywords=row["keywords"],
            ogTitle=row["og_title"],
            ogDescription=row["og_description"],
            ogImage=row["og_image"]
        )

