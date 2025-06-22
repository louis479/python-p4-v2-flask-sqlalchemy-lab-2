from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(SerializerMixin, db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship("Review", back_populates="customer")

    items = association_proxy('reviews', 'item')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': [review.to_dict() for review in self.reviews]  # Serializing reviews
        }
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': [review.serialize() for review in self.reviews if review.customer_id == self.id]
        }

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(SerializerMixin, db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship("Review", back_populates="item")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': [review.serialize() for review in self.reviews if review.item_id == self.id]
        }
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.to_dict() for review in self.reviews]  # Serializing reviews
        }

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer': self.customer.to_dict() if self.customer else None,  # Serialize customer object
            'item': self.item.to_dict() if self.item else None  # Serialize item object
        }

    def serialize(self):
        return {
            'id': self.id,
            'comment': self.comment,  # Ensure the comment is serialized correctly
            'customer_id': self.customer_id,
            'item_id': self.item_id
        }
