from flask import json
from saleapp import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
    products = relationship('Product', backref="category", lazy=True)

    def __str__(self):
        return self.name

class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
    price = Column(Float, default=0.0)
    image = Column(String(300), default="https://res.cloudinary.com/dy1unykph/image/upload/v1740037805/apple-iphone-16-pro-natural-titanium_lcnlu2.webp")
    cate_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name

if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        c1 = Category(name="Laptop")
        c2 = Category(name="Mobile")
        c3 = Category(name="Tablet")

        # db.session.add_all([c1, c2, c3])

        with open("data/product.json", encoding="utf-8") as f:
            products = json.load(f)

            for p in products:
                db.session.add(Product(**p))

        db.session.commit()