from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .client import Client
from .products import Product
from .ticket import Ticket
from .ticket_detail import TicketDetail
from .users import User

