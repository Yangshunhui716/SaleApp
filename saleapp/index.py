import cloudinary.uploader
from flask import Flask, render_template, request, redirect, session
import math
import dao
from saleapp import app, login, admin, db
from flask_login import login_user, current_user, logout_user
from decorators import anonymous_required

@app.route("/")
def index():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    page = request.args.get("page")
    prods = dao.load_products(q=q, cate_id=cate_id, page=page)
    pages = math.ceil(dao.count_product()/app.config["PAGE_SIZE"])
    return render_template("index.html", prods=prods, pages=pages)

@app.route("/sign_up", methods=['get', 'post'])
def sign_up():
    error_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get("pswd")
        confirmpswd = request.form.get("confirmpswd")

        if password.__eq__(confirmpswd):
            username = request.form.get("username")
            name = request.form.get("name")
            avatar = request.files.get("avatar")
            avatar_path = None

            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']
            try:
                dao.add_user(name=name, username=username, password=password, avatar=avatar_path)
                return redirect("/log_in")
            except:
                db.session.rollback()
                error_msg = "Hệ thông đang lỗi. Vui lòng truy cập lại sau!"

        else:
            error_msg = "Mật khẩu không khớp!"

    return render_template("signUp.html", error_msg=error_msg)

@app.route("/log_in", methods=['get', 'post'])
@anonymous_required
def log_in():
    error_msg = None

    if request.method.__eq__('POST'):
        username = request.form.get("username")
        password = request.form.get("pswd")

        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            return redirect("/")
        else:
            error_msg = "Tài khoản hoặc mật khẩu không hợp lệ!"

    return render_template("logIn.html", error_msg=error_msg)

@login.user_loader
def get_user(id):
    return dao.get_user_by_id(id)

@app.route("/log_out")
def log_out():
    logout_user()
    return redirect("/log_in")

@app.route("/admin_login", methods=['post'])
def admin_login_process():
    if current_user.is_authenticated:
        return redirect('/admin')

    error_msg = None

    if request.method.__eq__('POST'):
        username = request.form.get("username")
        password = request.form.get("pswd")

        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            return redirect("/admin")
        else:
            error_msg = "Tài khoản hoặc mật khẩu không hợp lệ!"

    return render_template("logIn.html", error_msg=error_msg)

@app.route("/products/<int:id>")
def details(id):

    return render_template("detail.html", prod=dao.get_product_by_id(id))

@app.context_processor
def common_attribute():
    return {
        "cates": dao.load_categories()
    }

@app.route("/cart")
def cart():
    session['cart'] = {
        "1": {
            "id": "1",
            "name": "Iphone 15",
            "price": 15000,
            "quantity": 1
        },
        "2": {
            "id": "2",
            "name": "Samsung Galaxy",
            "price": 10000,
            "quantity": 3
        }
    }
    return render_template("cart.html")

if __name__== "__main__":
    with app.app_context():
        app.run(debug=True)