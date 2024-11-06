from app.extensions import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80))


class ShopTag(Tag):
    def __init__(self) -> None:
        super().__init__()
        self.type = 'shop'

    def __repr__(self) -> str:
        return '<ShopTag {}>'.format(self.name)
    
    