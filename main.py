from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import RadioField

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
products = [{'id': 1, 'img_href': '../static/img/margarita.jpg', 'name': 'Маргарита', 'price': 500},
            {'id': 2, 'img_href': '../static/img/pepperoni.jpg', 'name': 'Пепперони', 'price': 500},
            {'id': 3, 'img_href': '../static/img/napoleon.jpg', 'name': 'Наполеон', 'price': 500},
            {'id': 4, 'img_href': '../static/img/olivki.jpg', 'name': 'Оливки', 'price': 500},
            {'id': 5, 'img_href': '../static/img/peres.jpg', 'name': 'Перес', 'price': 500},
            {'id': 6, 'img_href': '../static/img/caprichoza.jpg', 'name': 'Капричоза', 'price': 500}]

# корзина
cart = []


class SimpleForm(FlaskForm):
    example = RadioField('Label', choices=[
        (1, 'Маленькая'), (2, 'Средняя'), (3, 'Большая')],
                         default=2, coerce=int)


# главная страница
@app.route('/', methods=['POST', 'GET'])
@app.route('/main', methods=['POST', 'GET'])
def main():
    form = SimpleForm()
    if form.validate_on_submit() or request.method == 'POST':
        flag = False
        for i in cart:
            if i['id'] == request.form.get('ID'):
                if i['ing'] == request.form.getlist('ing'):
                    if i['size'] == form.example.data:
                        i['qty'] += int(request.form.get('qty'))
                        flag = True
        if flag:
            pass
        else:
            cart.append(
                {'id': request.form.get('ID'), 'ing': request.form.getlist('ing'), 'size': form.example.data,
                 'qty': int(request.form.get('qty'))})
    else:
        print(form.errors)
    print(cart)
    return render_template('index.html', len=len(products), products=products, form=form)


@app.route('/add_to_cart/<id>/', methods=['POST'])
def add_to_cart(id):
    cart.append({'id': id, 'qty': 1, 'ing': [], 'size': 20})
    print(cart)
    return redirect('/')


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


#
# @app.route('/cart', methods=['GET', 'POST'])
# def cart():
#     return render_template('cart.html', len=len(cart), cart=cart)


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
