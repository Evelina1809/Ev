from flask import Flask, url_for, request, render_template, redirect,  json, session
from blueprint_query.route import blueprint_query
from blueprint_info.route import blueprint_info
from blueprint_auth.route import blueprint_auth
from blueprint_elist.route import blueprint_elist
from blueprint_report.route import blueprint_report

from access import login_required
# viewer app

app = Flask(__name__)#обращение к текущему модулю

app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_query, url_prefix='/zaproses') #регистрация blueprint
app.register_blueprint(blueprint_info, url_prefix='/info') #регистрация blueprint
app.register_blueprint(blueprint_auth, url_prefix='/auth') #регистрация blueprint
app.register_blueprint(blueprint_elist, url_prefix='/elist') #регистрация blueprint
app.register_blueprint(blueprint_report, url_prefix='/report') #регистрация blueprint


with open('data_files/dbconfig.json', 'r') as f:
    db_config = json.load(f)
    app.config['dbconfig'] = db_config

with open('data_files/access.json', 'r') as file:
    access_config = json.load(file)
app.config['access_config'] = access_config


@app.route('/')
def start_func():
    if 'user_id' in session:
        return menu_choice()
    else:
        return render_template('start_request.html')


@app.route('/menu')
@login_required
def menu_choice():
    group = session.get('user_group')
    if group == 'director' or group == 'stevedor' or group == 'tallyman':
        return render_template('internal_user_menu.html')
    return render_template('external_user_menu.html')


@app.route('/exit')
def exit_func():
    session.clear()
    return render_template('exit_request.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005)
