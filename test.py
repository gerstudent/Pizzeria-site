# для радио баттон
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import RadioField

SECRET_KEY = 'development'

app = Flask(__name__)
app.config.from_object(__name__)


class SimpleForm(FlaskForm):
    example = RadioField('Label', choices=[
        (1, 'description'), (2, 'whatever')],
                         default=1, coerce=int)


@app.route('/', methods=['post', 'get'])
def hello_world():
    form = SimpleForm()
    if form.validate_on_submit():
        print(form.example.data)
    else:
        print(form.errors)
    return render_template('test.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

# для чекбоксов
#
# from flask import Flask, request
#
# app = Flask(__name__)
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         print(request.form.getlist('hello'))
#
#     return '''<form method="post">
# <input type="checkbox" name="hello" value="world" checked>
# <input type="checkbox" name="hello" value="davidism" checked>
# <input type="submit">
# </form>'''
#
# app.run()