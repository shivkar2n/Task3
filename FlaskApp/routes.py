import os
from flask import (request, render_template, redirect, url_for, abort, flash)
from .models import User, Product, db
from . import app, login_manager
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import time
from multiprocessing import Process
from datetime import datetime as dt

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}
ending_hr = None
ending_min = None

def countdown(t,Product):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    Product.status = 0
    db.session.commit()
    print('Fire in the hole!!')

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/home')
def home():
    Products = Product.query.all()
    return render_template('Home.html',title="Home",Products=Products)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        for U in User.query.all():
            if request.form["Username"] == U.username and check_password_hash(U.password,request.form["Password"]):
                login_user(U)
                flash("Login successful!!")
                return redirect(url_for('home'))

        flash("Password or username incorrect!")
        return redirect(url_for('login'))

    return render_template('login.html',title="Login")

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        for U in User.query.all():
            if U.username == request.form["Username"]:
                flash("Username already taken")
                return redirect(url_for('register'))

        u = User(username=request.form["Username"],password=generate_password_hash(request.form["Password"]),description=request.form["Description"],location=request.form["Location"])
        db.session.add(u)
        db.session.commit()
        flash("Successfully registered! You can login now!")
        return redirect(url_for('home'))
    return render_template('register.html',title="Register")

@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    if request.method == 'POST':
        if current_user.is_authenticated:
            file = request.files['image']

            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('addproduct'))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.root_path,'static/image', filename))

                flash('file saved')
                P = Product(name=request.form["name"],condition=request.form["condition"],status=0,user_id=current_user.id,image_name=filename)
                db.session.add(P)
                db.session.commit()
                flash("successfully added!")
                return redirect(url_for('home'))
    return render_template('AddProducts.html',title="ProductPage")

@app.route('/product/<int:product_id>', methods=['GET','POST'])
@login_required
def product(product_id):
    if current_user.is_authenticated:
        P = Product.query.filter_by(id=product_id).first()
        # Timer thread which is product timer
        timer_process = None

        if request.method == 'POST':
            if current_user.id == P.user.id:
                # Post request by owner of the product
                if P.status == 0:
                    global ending_hr, ending_min
                    # This allows other users to bid
                    P.status = 1
                    db.session.commit()
                    hours = int(request.form["biddingtimehr"])
                    mins = int(request.form["biddingtimemin"])
                    ending_hr = dt.now().hour + hours
                    ending_min = dt.now().minute + mins

                    timer_process = Process(target=countdown(hours*3600 + mins*60,P),daemon=True)
                    timer_process.start()
                    return redirect(url_for('home'))
                else:
                    # This prevents other users from bidding
                    if timer_process and timer_process.is_alive():
                        timer_process.terminate()
                    P.status = 0

                # Commmit changes to variable
                db.session.commit()
                return redirect(url_for('product', product_id=P.id))
            else:
                # Post request by person bidding for the product
                if P.status:
                    P.soldstatus = 1
                    if P.price < int(request.form["price"]):
                        # Changes price if bid is higher
                        P.price = request.form["price"]
                        P.bidder_name = User.query.filter_by(id=current_user.id).first().username
                        db.session.commit()
                        return render_template('Product.html',Product=P,ending_hr=ending_hr,ending_min=ending_min)

                    else:
                        flash("You need to bid higher!!")

                else:
                    # If product is open for bidding
                    flash("This product is not open for bidding")

        return render_template('Product.html',Product=P,ending_hr=ending_hr,ending_min=ending_min)
    else:
        return redirect(url_for('home'))

@app.route('/myprofile')
@login_required
def myprofile():
    if current_user.is_authenticated:
        U = User.query.filter_by(id=current_user.id).first()
        Products = Product.query.all()
        return render_template('MyProfile.html',title="My Profile",User=U,Products=Products)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You logged out!')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
