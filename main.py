from flask import Flask, render_template, url_for, request, redirect
from loginforms import AdminLoginForm, UserLoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pizza-shmizza_secret_key'

ADMIN_FLAG = False
USER_FLAG = False


@app.route('/')
@app.route('/main')
def main():
    if USER_FLAG:
        return render_template('header_logined')
    else:
        return render_template('header_unlogined.html')


@app.route('/admin')
def admin_page():
    if ADMIN_FLAG:
        return "Admin Page"
    else:
        return redirect('/admin_login')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        global ADMIN_FLAG
        ADMIN_FLAG = True
        return redirect('/admin')
    return render_template('admin_login.html', title='Авторизация', form=form)


@app.route('/search/<string:desired>')
def search(desired):
    return desired


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()
    if form.validate_on_submit():
        global USER_FLAG
        USER_FLAG = True
        return redirect('/')
    return render_template('user_login.html', title='Авторизация', form=form)


@app.route('/account/<int:id>')
def account(id):
    if USER_FLAG:
        return str(id) + " Аккаунт"
    else:
        return redirect('/user_login')


@app.route('/about')
def about():
    return 'Страница о нас'


if __name__ == "__main__":
    app.run(debug=True)
