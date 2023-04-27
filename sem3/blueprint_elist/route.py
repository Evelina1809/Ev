import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from sem3.db_context_manager import DBContextManager
from sem3.sql_provider import SQLProvider
from sem3.db_work import select_dict, select
from sem3.access import login_required, group_required
from datetime import date, datetime

blueprint_elist = Blueprint('bp_elist', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_elist.route('/', methods=['GET', 'POST'])
@login_required
@group_required
def start_elist():
    db_config = current_app.config['dbconfig']
    if request.method == 'GET':
        sql = provider.get('reg_not_done.sql')
        regs = select_dict(db_config, sql)
        return render_template('reg_date_choice.html', regs=regs)
    else:
        input_reg = request.form.get('regID')
        session['regID'] = input_reg
        session['message'] = ''
        return redirect(url_for('bp_elist.add_date'))


@blueprint_elist.route('/add_date', methods=['POST', 'GET'])
@login_required
@group_required
def add_date():
    current_date = datetime.today()
    if request.method == 'GET':
        return render_template('input_date_unload.html')
    else:
        input_date = request.form.get('date_name')
        date_check = datetime.strptime(input_date, '%Y-%m-%d')
        if date_check < current_date:
            return render_template('input_date_unload.html', errone='Неверная дата разгрузки')
        else:
            session['input_date'] = input_date
            return redirect(url_for('bp_elist.order_elist'))


@blueprint_elist.route('/order', methods=['GET', 'POST'])
@login_required
@group_required
def order_elist():
    db_config = current_app.config['dbconfig']
    if request.method == 'GET':
        sql = provider.get('all_empl.sql', input_date=session['input_date'])
        session['all_empl'] = select_dict(db_config, sql)
        items = session['all_empl']
        basket_items = session.get('basket', {})# словарь словарей
        regID = session['regID']
        message =session['message']
        return render_template('basket_order_list.html', items=items, basket=basket_items, registration=regID, message=message)
    else:
        emp_id = request.form.get('eID')
        add_to_basket(emp_id)
        return redirect(url_for('bp_elist.order_elist'))


def add_to_basket(emp_id: str):
    db_config = current_app.config['dbconfig']
    _sql = provider.get('empls.sql', input_eID=emp_id)
    emp_description = select_dict(db_config, _sql)[0]
    curr_basket = session.get('basket', {})
    if emp_id in curr_basket:
        session['message']='Сотрудник уже в бригаде'
    else:
        curr_basket[emp_id] = {
            'eID': emp_description['eID'],
            'eProf': emp_description['eProf'],
            'eSurename': emp_description['eSurename'],
        }
        session['basket'] = curr_basket
        session['message'] = ''
        session.permanent = True
    return True


@blueprint_elist.route('/clear-basket')
@login_required
@group_required
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_elist.order_elist'))


@blueprint_elist.route('/save_order', methods=['POST','GET'])
@login_required
@group_required
def save_order():
    regID = session['regID']
    current_basket = session.get('basket', {})
    input_date = session['input_date']
    result = save_order_with_list(current_app.config['dbconfig'], regID, current_basket, input_date)
    if result:
        session.pop('basket')
        return render_template('order_created.html', regID=regID)
    else:
        return 'Что-то пошло не так'

#
#будем сохранять строчки в таблице user_orders заказов внося туда айди юзера и дату заказа


def save_order_with_list(dbconfig: dict, regID: int, curren_basket: dict, input_date: str):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('курсор не создан')
        for key in curren_basket:
            eID = curren_basket[key]['eID']
            _sql3 = provider.get('insert_elist.sql', regID=regID, eID=eID, input_date=input_date)
            result = cursor.execute(_sql3)
            print(result)
        return result
