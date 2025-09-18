from datetime import datetime
from sqlite3 import IntegrityError
from flask import Flask, flash, redirect, request, render_template, url_for
from models import db, Client, Product, Ticket, TicketDetail, User
from flask_login import LoginManager, login_required, login_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tppython.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" 

@app.route("/crear")
def create_tables():
    with app.app_context():  
        db.create_all()

    admin = User(
        email="admin@gmail.com",
        name="Admin",
        lastname="Admin",
        password="admin",
        role="admin"
    )
    admin.set_and_hash_pass(admin.password)        
    db.session.add(admin)

    client1 = Client(
        email="cliente1@gmail.com",
        name="Juan",
        lastname="Perez",
        tel=12345678,
        address=1001,
        status=True
    )
    client2 = Client(
        email="cliente2@gmail.com",
        name="Maria",
        lastname="Gomez",
        tel=87654321,
        address=1002,
        status=True
    )
    db.session.add_all([client1, client2])

    product1 = Product(
        title="Producto A",
        description="Descripción del Producto A",
        price=100.0,
        stock=10
    )
    product2 = Product(
        title="Producto B",
        description="Descripción del Producto B",
        price=200.0,
        stock=5
    )
    db.session.add_all([product1, product2])

    db.session.commit()  

    ticket1 = Ticket(id_client=client1.id_client, date=datetime.today().date(), total=0)
    ticket2 = Ticket(id_client=client2.id_client, date=datetime.today().date(), total=0)
    ticket3 = Ticket(id_client=client1.id_client, date=datetime.today().date(), total=0)
    db.session.add_all([ticket1, ticket2, ticket3])
    db.session.commit()  

    detail1_1 = TicketDetail(
        id_ticket=ticket1.id_ticket,
        id_product=product1.id_product,
        cantidad=2,
        unit_price=product1.price,
        subtotal=2 * product1.price
    )
    detail1_2 = TicketDetail(
        id_ticket=ticket1.id_ticket,
        id_product=product2.id_product,
        cantidad=1,
        unit_price=product2.price,
        subtotal=1 * product2.price
    )
    ticket1.total = detail1_1.subtotal + detail1_2.subtotal

    detail2_1 = TicketDetail(
        id_ticket=ticket2.id_ticket,
        id_product=product1.id_product,
        cantidad=3,
        unit_price=product1.price,
        subtotal=3 * product1.price
    )
    ticket2.total = detail2_1.subtotal

    detail3_1 = TicketDetail(
        id_ticket=ticket3.id_ticket,
        id_product=product2.id_product,
        cantidad=2,
        unit_price=product2.price,
        subtotal=2 * product2.price
    )
    ticket3.total = detail3_1.subtotal

    db.session.add_all([detail1_1, detail1_2, detail2_1, detail3_1])
    db.session.commit()

    return "Tablas creadas"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/dashboard", methods = ["GET", "POST"])
@login_required
def dashboard():
    products = Product.query.all()  
    return render_template("dashboard.html", products=products)

@app.route("/ticket_detail/<int:ticket_id>/detail", methods=["GET", "POST"])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    method = request.form.get("_method", "").upper()

    if method == "DELETE":
        id_detail = request.form.get("id_detail")
        detail = TicketDetail.query.get(id_detail)

        if not detail:
            flash("Detail not found.", "danger")
        else:
            product = Product.query.get(detail.id_product)
            if product:
                product.stock += detail.cantidad

            db.session.delete(detail)
            db.session.commit()
            flash("Detail deleted.", "success")

        ticket.total = sum(d.subtotal for d in ticket.details)
        db.session.commit()
        return redirect(url_for("ticket_detail", ticket_id=ticket.id_ticket))
    elif request.method == "POST":
        id_product = request.form["id_product"]
        cantidad = int(request.form["quantity"])
        product = Product.query.get(id_product)

        if not product:
            return {"error": "Product not found"}, 404

        if product.stock < cantidad:
            flash("Insufficient stock.", "danger")
            return redirect(url_for("ticket_detail", ticket_id=ticket.id_ticket))

        unit_price = product.price
        subtotal = cantidad * unit_price

        product.stock -= cantidad

        new_detail = TicketDetail(
            id_ticket=ticket.id_ticket,
            id_product=id_product,
            cantidad=cantidad,
            unit_price=unit_price,
            subtotal=subtotal
        )
        db.session.add(new_detail)

        ticket.total = sum(d.subtotal for d in ticket.details) + subtotal

        db.session.commit()

        flash("Product added.", "success")



    return render_template("ticket_detail.html", ticket=ticket)


@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    method = request.form.get("_method", "")
    
    if method == 'PUT':
        try:
            id = request.form["id"]
            price = request.form["price"]
            stock = request.form["stock"]
            title = request.form["title"]
            desc = request.form["desc"]

            product = Product.query.filter_by(id_product=id).first()

            if not id:
                flash("ID is needed.", 'danger')
                return render_template("products.html", products=Product.query.all())
            
            if price:
                product.price = price
            if stock:
                product.stock = stock
            if title:
                product.title = title
            if desc:
                product.desc = desc

            db.session.commit()
            flash("Product updated.", 'success')
            return render_template("products.html", products=Product.query.all())
        except IntegrityError:
            db.session.rollback()
            flash("Internal database error.", "danger")
            return "Internal Error"
    elif method == "DELETE":
        try:
            product_id = request.form["id"]
            product = Product.query.get(product_id)

            if not product:
                flash("Product not found.", "danger")
                return render_template("products.html", products=Product.query.all())

            db.session.delete(product)
            db.session.commit()
            flash("Product deleted successfully.", "success")
            return render_template("products.html", products=Product.query.all())
        except IntegrityError:
            db.session.rollback()
            flash("Internal database error.", "danger")
            return "Internal Error"
    elif request.method == "POST":
        price = request.form["price"]
        stock = request.form["stock"]
        title = request.form["title"]
        desc = request.form["desc"]
        if not price or not stock or not title or not desc:
            flash("Missing fields.", 'danger')
            return render_template("products.html", products=Product.query.all())
        
        new_prod = Product(
            title=title,
            description=desc,
            price=price,
            stock=stock
        )
        db.session.add(new_prod)
            
        db.session.commit()
        flash("Product created.", 'success')
        return render_template("products.html", products=Product.query.all())
    
    return render_template("products.html", products=Product.query.all())

@app.route("/tickets", methods=["GET", "POST"])
@login_required
def tickets():
    method = request.form.get("_method", "")
    if method == "DELETE":
        ticket_id = request.form.get("id")
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            flash("Invoice not found.", "danger")
        else:
            db.session.delete(ticket)
            db.session.commit()
            flash("Invoice deleted.", "success")
        return redirect(url_for("tickets"))
    elif method == "PUT":
        ticket_id = request.form.get("ticket_id")
        total = request.form.get("total")

        if not ticket_id or not total:
            flash("Ticket ID or total missing.", "danger")
            return redirect(url_for("tickets"))

        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            flash("Ticket not found.", "danger")
            return redirect(url_for("tickets"))

        try:
            ticket.total = float(total)
            db.session.commit()
            flash("Invoice updated successfully.", "success")
        except ValueError:
            flash("Invalid total value.", "danger")

        return redirect(url_for("tickets"))
    elif request.method == "POST":
        id_client = request.form["client_id"]
        date_str = request.form["date"]

        if not id_client or not date_str:
            flash("Missing fields", "danger")
            return render_template("tickets.html", tickets=Ticket.query.all())

        clientExists = Client.query.filter_by(id_client=id_client).first()
        if clientExists == None or clientExists.status == False:
            flash("Client does not exists or is disabled.", "error")
            return render_template("tickets.html", tickets=Ticket.query.all())
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.", "danger")
            return render_template("tickets.html", tickets=Ticket.query.all())

        new_ticket = Ticket(
            id_client=id_client,
            date=date
        )
        db.session.add(new_ticket)
        db.session.commit()
        flash("Invoice created.", "success")
        return redirect(url_for("ticket_detail", ticket_id=new_ticket.id_ticket))


    return render_template("tickets.html", tickets=Ticket.query.all())

@app.route("/clients", methods = ["GET", "POST"])
@login_required
def clients():
    method = request.form.get("_method", "")
    
    if method == 'PUT':
        try:
            
            email = request.form["email"]
            name = request.form["name"]
            lastname = request.form["lastname"]
            address = request.form["address"]
            tel = request.form["tel"]
            status = request.form["status"]
            client = Client.query.filter_by(email=email).first()

            if client == None:
                flash("Client not found.", 'danger')
                return render_template("clients.html", clients=Client.query.all())

            if name:
                client.name = name
            if lastname:
                client.lastname = lastname
            if address:
                client.address = address
            if tel:
                client.tel = tel
            if status is not None and status != "":
                client.status = True if status.lower() in ("true", "1", "yes") else False

            db.session.commit()

            flash("Client updated successfully.", "success")
            return render_template("clients.html", clients=Client.query.all())

        except IntegrityError:
            db.session.rollback()
            flash("Internal database error.", "danger")
            return "Internal Error"
    elif request.method == "POST":
        try:
            email = request.form["email"]
            name = request.form["name"]
            lastname = request.form["lastname"]
            address = request.form["address"]
            tel = request.form["tel"]
            status = request.form["status"]
            if not email or not name or not lastname or not address or not tel:
                flash("Missing fields.", 'danger')
                return render_template("clients.html", clients=Client.query.all())

            client = Client.query.filter_by(email=email).first()
            if status == "True":
                status = True
            else:
                status = False
            if client:
                flash("Client already registered.", 'danger')
                return render_template("clients.html", clients=Client.query.all())
            
            new_client = Client(
                email=email,
                name=name,
                lastname=lastname,
                address=address,
                tel=tel,
                status=status
            )
            
            db.session.add(new_client)
            
            db.session.commit()
            flash("Client created.", 'success')
            return render_template("clients.html", clients=Client.query.all())


        except IntegrityError:
            db.session.rollback()
            flash("Internal database error.", "danger")
            return "Internal Error" 
    else:
        return render_template("clients.html", clients=Client.query.all())


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            if not email or not password:
                flash("Missing filds", 'danger')
                return render_template('login.html')
            
            user = User.query.filter_by(email=email).first()
            if not user:
                flash("User not found.", 'danger')
                return render_template('login.html')
            valid_password = user.verify_pass(password)

            if not valid_password:
                flash("Incorrect password or email.", 'danger')
                return render_template('login.html')
            login_user(user)  
            flash("Account created.", 'success')
            return redirect(url_for("dashboard"))
        except IntegrityError:
            db.session.rollback()
            return "error: email repetido"
    else:
        return render_template("login.html")


@app.route("/reports/invoices_by_client", methods=["GET", "POST"])
@login_required
def invoices_by_client():
    if request.method == "POST":
        client_id = request.form["client_id"]
        tickets = Ticket.query.filter_by(id_client=client_id).all()
        return render_template("report_invoices_client.html", tickets=tickets)
    return render_template("report_invoices_client.html")

@app.route("/reports/sales_by_period", methods=["GET", "POST"])
@login_required
def sales_by_period():
    tickets = []
    total_sales = 0
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        if start_date and end_date:  
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
                tickets = Ticket.query.filter(Ticket.date.between(start, end)).all()
                total_sales = sum(t.total for t in tickets)
            except ValueError:
                flash("Invalid format date", "danger")
        else:
            flash("Both dates needed", "warning")
    return render_template("report_sales_period.html", tickets=tickets, total=total_sales)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
