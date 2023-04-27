import os

from flask import Blueprint, request, render_template, current_app
from sem3.db_work import select
from sem3.sql_provider import SQLProvider
from sem3.access import login_required, external_required
from datetime import datetime
# возвращает шаблон controller mvc

blueprint_info = Blueprint('bp_info', __name__, template_folder='templates')
provider_info = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql')) #создается экземпляр объекта sql provider

# тестовый обработчик


@blueprint_info.route('/elist_table', methods=['GET', 'POST'])
@login_required  # функция start_report передается декоратору @login_required в качестве аргумента
@external_required
def elist_table():
    today_d = datetime.today()
    arr=['Номер регистрации', 'Тип причала', 'Название корабля', 'Дата разгрузки']
    if request.method == 'GET':
        return render_template('input_name_info.html')
    else:
        input_surename = request.form.get('input_surename')
        input_date = request.form.get('input_date')
        if input_date and input_surename:
            sql1 = provider_info.get('check_emp_exist.sql', input_surename=input_surename, input_date=input_date)
            check_emp, sch = select(current_app.config['dbconfig'], sql1)
            print(check_emp)
            if check_emp:
                _sql = provider_info.get('elist_table.sql', input_surename=input_surename, input_date=input_date, today_d=today_d)
                sol_result, schema = select(current_app.config['dbconfig'], _sql)
                return render_template('db_result.html', schema=arr, result=sol_result, search='Информация о разгрузках')
            else:
                return render_template('input_name_info.html', message='Информация о сотруднике не найдена')
        else:
            return render_template('input_name_info.html', message='Введите все необходимые данные')


@blueprint_info.route('/history')
def history():
    return render_template('history.html')


