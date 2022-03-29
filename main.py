from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from loginforms import AdminLoginForm, UserLoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'pizza_smizza secret key'
# работа с базой данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# флаги авторизации админа и пользователя
ADMIN_FLAG = False
USER_FLAG = False

# список пицц
products = [{'id': 1, 'img_href': '../static/img/pizza2.jpg', 'name': 'Маргарита', 'price': 500},
            {'id': 2, 'img_href': '../static/img/pizza2.jpg', 'name': 'Маргарита', 'price': 500}]

# пример корзины
cart = []


# главная страница
@app.route('/')
@app.route('/main')
def main():
    return render_template('index.html', len=len(products), products=products)


@app.route('/add_to_cart/<id>/', methods=['POST'])
def add_to_cart(id):
    cart.append({'id': id, 'qty': 1, 'ing': [], 'size': 20})
    print(cart)
    return redirect('/')


# класс пользователя
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# панель администратора
@app.route('/admin')
def admin_page():
    if ADMIN_FLAG:
        return "Admin Page"
    else:
        return redirect('/admin_login')


# авторизация администратора
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        global ADMIN_FLAG
        ADMIN_FLAG = True
        return redirect('/admin')
    return render_template('admin_login.html', title='Авторизация', form=form)


# страница поиска
@app.route('/search/<string:desired>')
def search(desired):
    return desired


# авторизация пользователя
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()
    if form.validate_on_submit():
        global USER_FLAG
        USER_FLAG = True
        return redirect('/')
    return render_template('user_login.html', title='Авторизация', form=form)


@app.route('/user_reg', methods=['GET', 'POST'])
def user_reg():
    return "Регистрация"


# страница пользователя
@app.route('/account/<int:id>')
def account(id):
    if USER_FLAG:
        return str(id) + " Аккаунт"
    else:
        return redirect('/user_login')


# страница о нас
@app.route('/about')
def about():
    return 'Страница о нас'


if __name__ == "__main__":
    app.run(debug=True)
