import os
from typing import Optional, Dict
from flask import Blueprint, request, render_template, current_app, session, redirect, url_for
from sem3.db_work import select_dict
from sem3.sql_provider import SQLProvider
# возвращает шаблон controller mvc

blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql')) #создается экземпляр объекта sql provider


@blueprint_auth.route('/')
def authentication():
    return render_template('refuse.html')


@blueprint_auth.route('/start_auth', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login:
            user_info = define_user(login, password)
            if user_info:
                user_dict = user_info[0]
                session['user_id'] = user_dict['user_id']
                session['user_group'] = user_dict['user_group']
                session.permanent = True
                return redirect(url_for('menu_choice'))
            else:
                return render_template('input_login.html', message='полльзоват не найден')
        return render_template('input_login.html', message='повторите ввод')


def define_user(login: str, password: str) -> Optional[Dict]:
    sql_internal = provider.get('internal_user.sql', login=login, password=password)
    sql_external = provider.get('external_user.sql', login=login, password=password)
    user_info = None
    for sql_search in [sql_internal, sql_external]:
        user_info = select_dict(current_app.config['dbconfig'], sql_search)
        if user_info:
            break
    return user_info