from . import db

class Ticket(db.Model):
    __tablename__ = "tickets"
    id_ticket = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey("clients.id_client"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False, default=0)

    details = db.relationship("TicketDetail", backref="ticket", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Ticket {self.id_ticket} - Cliente {self.id_client} - Date {self.date} - Total {self.total}>"

    def set_total(self, total):
        self.total = total

    def set_id_client(self, id_client):
        self.id_client = id_client

    def set_date(self, date):
        self.date = date

    def get_total(self, total):
        return self.total

    def get_id_client(self, id_client):
        return self.id_client

    def get_date(self, date):
        return self.date