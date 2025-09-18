from . import db

class Product(db.Model):
    __tablename__ = "products"
    id_product = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    details = db.relationship("TicketDetail", backref="product")

    def __repr__(self):
        return f"<Product {self.id_product}: {self.description} - Precio {self.price} - Stock {self.stock}>"

    def set_description(self, description):
        self.description = description

    def set_price(self, price):
        self.price = price

    def set_stock(self, stock):
        self.stock = stock

    def get_description(self, description):
        return self.description

    def get_price(self, price):
        return self.price

    def get_stock(self, stock):
        return self.stock
