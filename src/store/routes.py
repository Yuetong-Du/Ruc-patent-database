from store import app, db, bcrypt
from store.forms import *
from store.models import User, Product, Order, OrderDetail, Applicant, Visitor
from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime


@app.route('/')
@app.route("/home") # home page
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)


@app.route("/register",methods=["GET", 'POST']) # register
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.role.data == "1":
            role = Applicant()
            table_name = "Applicant"
            table = Applicant
        elif form.role.data == "2":
            role = Visitor()
            table_name = "Visitor"
            table = Visitor
        hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode("utf-8")
        role.username = form.username.data
        role.email = form.email.data
        role.password = hashed_password
        db.session.add(role)
        db.session.commit()
        user = User()
        user.table_name = table_name
        user.table_id = table.query.filter_by(email=form.email.data).first().id
        user.username=form.username.data
        user.email=form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Your account was created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login",methods=["GET",'POST']) # login
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.role.data == "1":
            table = Applicant
            table_name="Applicant"
        elif form.role.data == "2":
            table = Visitor
            table_name = "Visitor"
        user = table.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            table_id = user.id
            user_user = User.query.filter_by(table_id=table_id,table_name=table_name).first()
            login_user(user_user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login failed, please check your character name, email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout") # logout
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/applicant/<string:username>/account") # asking applicants to fill in detailed info
@login_required
def applicant_account(username):
    if current_user.table_name != "Applicant":
        abort(403)
    Applicant1 = Applicant.query.filter_by(id=current_user.table_id).first()
    if Applicant1.affliated_organization == "null" or Applicant1.address == "null" or Applicant1.telephone == "null":
        flash("Please complete your detailed information as soon as possible","warning")
        return redirect(url_for("applicant_detail_manage"))
    return render_template("applicant_account.html", username=username)


@app.route("/visitor/<string:username>/account") # asking visitors to update their detailed info
@login_required
def visitor_account(username):
    if current_user.table_name != "Visitor":
        abort(403)
    visitor1 = Visitor.query.filter_by(id=current_user.table_id).first() # looking for visitor info and set it into an object
    if visitor1.telephone == "null": # if any of the info is not submitted
        flash("Please complete your shipper information as soon as possible","warning")
        return redirect(url_for("Visitor_detail_manage"))
    return render_template("visitor_account.html", username=username)


@app.route("/update/info",methods=["GET","POST"])
@login_required
def update_info():
    if current_user.table_name == "Applicant":
        table = Applicant
    elif current_user.table_name == "Visitor":
        table = Visitor
    form = UpdateInfo()
    role = table.query.filter_by(id=current_user.table_id).first()
    if form.validate_on_submit():
        role.username = form.username.data
        role.email = form.email.data
        db.session.add(role)
        db.session.commit()
        user = User.query.filter_by(id=current_user.id).first()
        user.username = form.username.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for("home"))
    if request.method == "GET":
        form.username.data = role.username
        form.email.data = role.email
    return render_template("update_info.html", form=form)

@app.route("/update/password",methods=["GET","POST"])
@login_required
def update_password():
    if current_user.table_name == "Applicant":
        table = Applicant
    elif current_user.table_name == "Visitor":
        table = Visitor
    form = UpdatePasswordForm()
    role = table.query.filter_by(id=current_user.table_id).first()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode("utf-8")
        role.password = hashed_password
        role.confirm_password = form.confirm_password.data
        db.session.add(role)
        db.session.commit()
        flash('Your password has been updated', 'success')
        return redirect(url_for("home"))
    return render_template("update_password.html", form=form)
    

@app.route("/applicant/detail", methods=["POST","GET"])
@login_required
def applicant_detail_manage():
    if current_user.table_name != "Applicant":
        abort(403)
    address = Applicant.query.filter_by(id=current_user.table_id).first()
    form = UpdateApplicantForm()
    if form.validate_on_submit():
        address.affliated_organization = form.affliated_organization.data
        address.address = form.address.data
        address.telephone = form.telephone.data
        db.session.commit()
        flash("Shipping address updated successfully!","success")
    elif request.method =="GET":
        form.affliated_organization.data = address.affliated_organization
        form.address.data = address.address
        form.telephone.data = address.telephone
    return render_template("update_applicant.html",form=form)

@app.route("/visitor/detail",methods=["GET","POST"])
@login_required
def visitor_detail_manage(): # supplier_shipper_manage
    if current_user.table_name != "Visitor":
        abort(403)
    form = UpdateVisitorForm()
    visitor1 = Visitor.query.filter_by(id=current_user.table_id).first() # look for visitor info
    if form.validate_on_submit():
        visitor1.telephone = form.telephone.data
        db.session.add(visitor1)
        db.session.commit()
        flash("Profile updated successfully","success")
    elif request.method == "GET":
        form.telephone.data = visitor1.telephone
    return render_template("update_visitor.html", form=form)

@app.route("/visitor/products")
@login_required
def visitor_product_manage(): # supplier_product_manage, index page for product management
    if current_user.table_name != "Visitor":
        abort(403)
    visitor_id = current_user.id
    products = Product.query.filter_by(id=visitor_id).all()
    return render_template("visitor_product_manage.html",products=products)


@app.route("/visitor/products/new", methods=["GET","POST"])
@login_required
def visitor_new_product(): # supplier_new_product # add a new product
    if current_user.table_name != "Visitor":
        abort(403)
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data,price=form.price.data,count=form.count.data,supplier_id=current_user.table_id)
        db.session.add(product)
        db.session.commit()
        flash("Your product was added successfully", "success")
        return redirect(url_for("visitor_product_manage"))
    return render_template("visitor_new_product.html",form=form)


@app.route("/visitor/product/update/<int:id>",methods=["GET","POST"]) # update a product
@login_required
def visitor_update_product(id):
    if current_user.table_name != "Visitor" or \
            Product.query.filter_by(id=id).first().visitor.id != current_user.table_id: # \ here means changing for another line
        abort(403) # what is the visitor here?
    form = UpdateProductForm()
    if form.validate_on_submit():
        product = Product.query.filter_by(id = id).first()
        product.name = form.name.data
        product.price = form.price.data
        product.count = form.count.data
        db.session.add(product)
        db.session.commit()
        flash("Your product has been updated successfully", "success")
    elif request.method == "GET":
        product = Product.query.filter_by(id=id).first()
        form.name.data = product.name
        form.price.data = product.price
        form.count.data = product.count
    return render_template("visitor_update_product.html", id=id, form=form)


@app.route("/visitor/product/delete/<int:id>",methods=["POST","GET"])
@login_required
def visitor_delete_product(id):
    if current_user.table_name != "Visitor" or \
            Product.query.filter_by(id=id).first().visitor.id != current_user.table_id:
        abort(403)
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    flash("Your product has been deleted successfully","success")
    return redirect(url_for("visitor_product_manage"))


@app.route("/applicant/product/add/<int:id>", methods=["POST","GET"])
@login_required
def add_product(id):
    if current_user.table_name != "Applicant":
        abort(403)
    cart = Order.query.filter_by(applicant_id=current_user.table_id, status=0).first()
    if cart:
        if OrderDetail.query.filter_by(order_id=cart.id, product_id=id).first() is None:
            order_detail = OrderDetail(count=1, order_id=cart.id, product_id=id)
            db.session.add(order_detail)
            db.session.commit()
            flash("This product has been successfully added to the shopping cart", "success")
            return redirect(url_for("home"))
        else:
            flash("This product is already in the shopping cart", "warning")
            return redirect(url_for("home"))
    else:
        cart = Order(applicant_id=current_user.table_id)
        db.session.add(cart)
        db.session.commit()
        order_detail = OrderDetail(count=1, order_id=cart.id, product_id=id)
        db.session.add(order_detail)
        db.session.commit()
        flash("This product has been successfully added to the shopping cart", "success")
        return redirect(url_for("home"))
    

@app.route("/applicant/cart")
@login_required
def shopping_cart():
    if current_user.table_name != "Applicant":
        abort(403)
    applicant1 = Applicant.query.filter_by(id=current_user.table_id).first()
    if applicant1.affliated_organization == "null" or applicant1.address == "null" or applicant1.telephone == "null":
        flash("Please complete your detailed information as soon as possible","warning")
        return redirect(url_for("applicant_detail_manage"))
    cart = Order.query.filter_by(Applicant_id=current_user.table_id, status=0).first()
    if cart is not None:
        orderdetails = OrderDetail.query.filter_by(order_id=cart.id).all()
        price = 0
        for orderdetail in orderdetails:
            product = Product.query.filter_by(id=orderdetail.product_id).first()
            price = price+orderdetail.count*product.price
        cart.total_price = price
        db.session.add(cart)
        db.session.commit()
        return render_template("shopping_cart.html", orderdetails=orderdetails,cart=cart)
    else:
        cart = Order(Applicant_id=current_user.table_id)
        db.session.add(cart)
        db.session.commit()
        orderdetails = None
        return render_template("shopping_cart.html", orderdetails=orderdetails,cart=cart)


@app.route("/applicant/product/delete/<int:id>",methods=["POST","GET"])
@login_required
def delete_product_from_shopping_cart(id):
    if current_user.table_name != "Applicant":
        abort(403)
    cart = Order.query.filter_by(Applicant_id=current_user.table_id, status=0).first()
    orderdetail = OrderDetail.query.filter_by(order_id=cart.id, product_id=id).first()
    db.session.delete(orderdetail)
    db.session.commit()
    flash("Delete successfully", "success")
    return redirect(url_for("shopping_cart"))


@app.route("/applicant/product/increase/<int:id>",methods=["POST","GET"])
@login_required
def add_by_1(id):
    if current_user.table_name != "Applicant":
        abort(403)
    cart = Order.query.filter_by(Applicant_id=current_user.table_id, status="0").first()
    orderdetail = OrderDetail.query.filter_by(order_id=cart.id, product_id=id).first()
    condition = orderdetail.count+1<=Product.query.filter_by(id=id).first().count and orderdetail.count>0
    while condition:
        orderdetail.count = orderdetail.count+1
        db.session.add(orderdetail)
        db.session.commit()
        flash("Increase successfully", "success")
        break
    return redirect(url_for("shopping_cart"))


@app.route("/applicant/product/reduce/<int:id>",methods=["POST","GET"])
@login_required
def delete_by_1(id):
    if current_user.table_name != "Applicant":
        abort(403)
    cart = Order.query.filter_by(Applicant_id=current_user.table_id, status="0").first()
    orderdetail = OrderDetail.query.filter_by(order_id=cart.id, product_id=id).first()
    condition = orderdetail.count<=Product.query.filter_by(id=id).first().count and orderdetail.count-1>0
    while condition:
        orderdetail.count = orderdetail.count-1
        db.session.add(orderdetail)
        db.session.commit()
        flash("Reduce successfully", "success")
        break
    return redirect(url_for("shopping_cart"))


@app.route("/applicant/confirm_order/<int:id>",methods=["POST","GET"])
@login_required
def confirm_order(id):
    if current_user.table_name != "Applicant" or \
            Order.query.filter_by(id=id).first().Applicant_id!=current_user.table_id:
        abort(403)
    cart = Order.query.filter_by(id=id).first()
    for detail in cart.orderdetails:
        product = Product.query.filter_by(id=detail.product_id).first()
        if detail.count > product.count:
            if product.count > 0:
                flash("Insufficient supply","warning")
                detail.count = 1
                db.session.add(detail)
                db.session.commit()
                return redirect(url_for("shopping_cart"))
            else:
                flash("Insufficient supply", "warning")
                row = detail
                db.session.delete(row)
                db.session.commit()
                return redirect(url_for("shopping_cart"))
        else:
            product.count = product.count - detail.count
            db.session.add(product)
            db.session.commit()
    cart.status = 1
    cart.start_time = datetime.now()
    db.session.add(cart)
    db.session.commit()
    return redirect(url_for("shopping_cart"))


@app.route("/applicant/orders")
@login_required
def applicant_order_manage(): # customer_order_manage
    if current_user.table_name != "Applicant":
        abort(403)
    unshipped_orders = Order.query.filter_by(Applicant_id=current_user.table_id,status=1).all()
    delivering_orders = Order.query.filter_by(Applicant_id=current_user.table_id, status=2).all()
    completed_orders = Order.query.filter_by(Applicant_id=current_user.table_id, status=3).all()
    return render_template("order_manage.html", unshipped_orders=unshipped_orders,delivering_orders=delivering_orders,completed_orders=completed_orders)


@app.route("/order/<int:id>")
@login_required
def show_order_details(id):
    if current_user.table_name == "Applicant":
        if Order.query.filter_by(id=id).first().Applicant_id != current_user.table_id:
            abort(403)
    order = Order.query.filter_by(id=id).first()
    address = order.customer # ???
    details = order.orderdetails
    return render_template("show_order_details.html",order=order,address=address,details=details)


@app.route("/applicant/order/cancel/<int:id>")
@login_required
def cancel_order(id):
    order =Order.query.filter_by(id=id).first()
    if current_user.table_name != "Applicant" or order.Applicant_id != current_user.table_id:
        abort(403)
    if order.status != 1:
        flash("The order has been shipped","danger")
        return redirect(url_for("applicant_order_manage"))
    else:
        details = order.orderdetails
        for detail in details:
            product = Product.query.filter_by(id=detail.product_id).first()
            product.count = product.count + detail.count
            db.session.add(product)
            db.session.commit()
            db.session.delete(detail)
            db.session.commit()
        db.session.delete(order)
        db.session.commit()
        flash("Your order has been canceled successful!","success")
        return redirect(url_for("applicant_order_manage"))


@app.route("/customer/order/confirm/<int:id>")
@login_required
def customer_confirm_order(id):
    if current_user.table_name != "Customer":
        abort(403)
    order = Order.query.filter_by(id=id).first()
    order.status = 3
    order.end_time = datetime.now()
    db.session.add(order)
    db.session.commit()
    flash("You have confirmed the order", "success")
    return redirect(url_for("applicant_order_manage"))


@app.route("/visitor/orders")
@login_required
def visitor_order_manage():
    if current_user.table_name != "Visitor":
        abort(403)
    unshipped_orders = Order.query.filter_by(status=1).all()
    return render_template("order_manage.html", unshipped_orders=unshipped_orders)


@app.route("/visitor/orders/confirm_delive/<int:id>")
@login_required
def visitor_confirm_order(id):
    if current_user.table_name != "Visitor":
        abort(403)
    order = Order.query.filter_by(id=id).first()
    order.status = 2
    db.session.add(order)
    db.session.commit()
    flash("Order shipped successfully","success")
    return redirect(url_for("visitor_order_manage"))
