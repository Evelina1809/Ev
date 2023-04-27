import os

from flask import Blueprint, request, render_template, current_app, json
from sem3.db_work import select
from sem3.sql_provider import SQLProvider
from sem3.access import login_required, group_required
# возвращает шаблон controller mvc

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql')) #создается экземпляр объекта sql provider

# тестовый обработчик


@blueprint_query.route('choice', methods=['GET'])
@login_required
@group_required
def choice():
    if request.method == 'GET':
        return render_template('choice_select.html', massage="")


@blueprint_query.route('/queries', methods=['GET', 'POST'])
@login_required
@group_required
def queries():
    arr = ['ID регистрации', 'Дата прибытия судна', 'Дата отправления судна', 'ID работника', 'ID причала', 'ID корабля']
    if request.method == 'GET':
        return render_template('reg_form.html', massage="")
    else:
        input_year = request.form.get('year_name')
        input_month = request.form.get('month_name')
        if input_year and input_month:
            _sql = provider.get('registration.sql', input_year=input_year, input_month=input_month)
            sol_result, schema = select(current_app.config['dbconfig'], _sql)
            return render_template('db_result.html', schema=arr, result=sol_result, search='Регистрация кораблей в указаннный год, месяц')
        else:
            return render_template('reg_form.html', massage="Repeat again")


@blueprint_query.route('/querie2', methods=['GET', 'POST'])
@login_required
@group_required
def querie2():
    arr = ['ID работника', 'Часы, проведенные на разгрузках']
    if request.method == 'GET':
        return render_template('reg_form.html', massage="")
    else:
        input_year = request.form.get('year_name')
        input_month = request.form.get('month_name')
        if input_year and input_month:
            _sql = provider.get('razgruz.sql', input_year=input_year, input_month=input_month)
            sol_result, schema = select(current_app.config['dbconfig'], _sql)
            return render_template('db_result.html', schema=arr, result=sol_result, search='Работники участвовали в разгрузках в указанный временной промежуток')
        else:
            return render_template('reg_form.html', massage="Repeat again")