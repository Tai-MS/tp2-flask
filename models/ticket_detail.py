from . import db

class TicketDetail(db.Model):
    __tablename__ = "ticket_detail"
    id_detail = db.Column(db.Integer, primary_key=True)
    id_ticket = db.Column(db.Integer, db.ForeignKey("tickets.id_ticket"), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey("products.id_product"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<TicketDetail {self.id_detail} - Ticket {self.id_ticket} - Producto {self.id_product} - Cantidad {self.cantidad} - Subtotal {self.subtotal}>"

    def set_id_ticket(self, id_ticket):
        self.id_ticket = id_ticket

    def set_id_product(self, id_product):
        self.id_product = id_product

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_unit_price(self, unit_price):
        self.unit_price = unit_price

    def set_subtotal(self, subtotal):
        self.subtotal = subtotal

    def get_id_ticket(self, id_ticket):
        return self.id_ticket 

    def get_id_product(self, id_product):
        return self.id_product 

    def get_cantidad(self, cantidad):
        return self.cantidad 

    def get_unit_price(self, unit_price):
        return self.unit_price 

    def get_subtotal(self, subtotal):
        return self.subtotal 
