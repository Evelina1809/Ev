import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app, json
from sem3.access import login_required, group_required
from sem3.db_work import call_proc, select
from sem3.sql_provider import SQLProvider

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql')) #создается экземпляр объекта sql provider


# with open('data_files/report.json', 'r') as file:
#     report_config = json.load(file)
# current_app.config['report_config'] = report_config


# добавить описание отчетов в json и сделать выпадающий список для отчетов
#todo

report_list = [
    {'rep_name': 'Отчет о регистрации сотрудников', 'rep_id':'1'},
    {'rep_name':'Отчет о количестве прибывших кораблей', 'rep_id': '2'}
]

report_url = {
    '1': {'create_rep': 'bp_report.create_rep1', 'view_rep': 'bp_report.view_rep1'},
    '2': {'create_rep': 'bp_report.create_rep2', 'view_rep': 'bp_report.view_rep2'}
}


# Отчет 1: Показывает количество сотрудников, зарегистрированных в определенный месяц и год
# Отчет 2: Показывает количество кораблей, зарегистрированных в порту в определенную дату (дд.мм.гггг)


@blueprint_report.route('/', methods=['GET', 'POST'])
@login_required  # функция start_report передается декоратору @login_required в качестве аргумента
@group_required
def start_report():
    if request.method == 'GET': #первый ли раз на этой стр
        return render_template('menu_report.html', report_list=report_list)
    else:
        # пользователь выбирает кнопку какую то
        rep_id = request.form.get('rep_id')
        if request.form.get('create_rep'):
            # проверяет с каким именем была вызвана кнопка
            url_rep = report_url[rep_id]['create_rep']
        else:
            # еслми не create то view
            url_rep = report_url[rep_id]['view_rep']
        return redirect(url_for(url_rep))


@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@login_required
@group_required  # функция report_page1 передается декоратору @group_required в качестве аргумента
def create_rep1():
    if request.method == 'GET':
        return render_template('input_employ_rep.html')
    else:
        input_year = request.form.get('year_name')
        input_month = request.form.get('month_name')
        sql_emp = provider.get('check_rep_emp.sql', input_month=input_month, input_year=input_year)
        # sql_emp = provider.get('rep_emp_out.sql', input_month=input_month, input_year=input_year)
        check_emp = select(current_app.config['dbconfig'], sql_emp)
        if int(check_emp[0][0][0]) >= 1:
            return render_template('input_employ_rep.html', errone='Отчет уже создан')
        else:
            if input_year and input_month:
                res = call_proc(current_app.config['dbconfig'], 'empls_rep', input_month, input_year)
                return render_template('menu_report.html', message='Отчет создан')


@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@login_required
@group_required  # функция report_page1 передается декоратору @group_required в качестве аргумента
def view_rep1():
    arr=['количество сотрудников', 'месяц', 'год']
    if request.method == 'GET':
        return render_template('input_employ_rep.html')
    else:
        input_year = request.form.get('year_name')
        input_month = request.form.get('month_name')
        sql_emp = provider.get('check_rep_emp.sql', input_month=input_month, input_year=input_year)
        check_emp = select(current_app.config['dbconfig'], sql_emp)
        if int(check_emp[0][0][0]) == 0:
            return render_template('input_employ_rep.html', errtwo='Отчет не создан')
        else:
            _sql = provider.get('rep_emp_out.sql', input_month=input_month, input_year=input_year)
            sol_result, schema = select(current_app.config['dbconfig'], _sql)
            return render_template('db_result.html', schema=arr, result=sol_result,
                                   search='Количество  сотрудников, нанятых в указаннный год, месяц')


@blueprint_report.route('/create_rep2',  methods=['GET', 'POST'])
@login_required
@group_required  # функция report_page1 передается декоратору @group_required в качестве аргумента
def create_rep2():
    if request.method == 'GET':
        return render_template('input_ships_rep.html')
    else:
        input_date = request.form.get('date_name')
        sql_ships = provider.get('check_rep_ships.sql', input_date= input_date)
        check_ships = select(current_app.config['dbconfig'], sql_ships)
        if int(check_ships[0][0][0]) >= 1:
            return render_template('input_ships_rep.html', errone='Отчет уже создан')
        else:
            if input_date:
                res = call_proc(current_app.config['dbconfig'], 'ships_rep', input_date)
                return render_template('menu_report.html', message='Отчет создан')


@blueprint_report.route('/view_rep2' , methods=['GET', 'POST'])
@login_required
@group_required  # функция report_page1 передается декоратору @group_required в качестве аргумента
def view_rep2():
    arr=['количество кораблей', 'дата']
    if request.method == 'GET':
        return render_template('input_ships_rep.html')
    else:
        input_date = request.form.get('date_name')
        sql_ships = provider.get('check_rep_ships.sql', input_date=input_date)
        check_ships = select(current_app.config['dbconfig'], sql_ships)
        if int(check_ships[0][0][0]) == 0:
            return render_template('input_ships_rep.html', errtwo='Отчет не создан')
        else:
            _sql = provider.get('rep_ships_out.sql', input_date=input_date)
            sol_result, schema = select(current_app.config['dbconfig'], _sql)
            return render_template('db_result.html', schema=arr, result=sol_result,
                                   search='Количество короблей, зарегистрированных в указаннный день')