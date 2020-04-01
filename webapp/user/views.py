from flask import Blueprint, render_template, flash, redirect, request, url_for
from io import TextIOWrapper
from webapp.db import db
from webapp.user.forms import SearchForm, RegistrationForm
from webapp.user.models import Client

import collections
import csv

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route("/registration")
def registration():
    title_reg = "Внесение данных в базу"
    form = RegistrationForm()
    return render_template("user/registration.html", title_reg=title_reg,
                           form=form)


@blueprint.route('/process-registration', methods=['POST'])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_client = Client(surname=form.surname.data,
                            name=form.name.data,
                            middle_name=form.middle_name.data,
                            incident_counter=form.incident_counter.data)
        db.session.add(new_client)
        db.session.commit()
        flash('Клиент добавлен в базу данных.')
        return redirect(url_for('user.search'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Ошибка в поле '{getattr(form, field).label.text}': - {error}")
        return redirect(url_for('user.registration'))
    flash('Пожалуйста, исправьте ошибки в форме')
    return redirect(url_for('user.registration'))


@blueprint.route('/process-upload', methods=['POST'])
def process_upload():
    if request.method == 'POST':
        f = request.files['fileupload']
        file_format = f.filename.rsplit(".", 1)[1]  # прописал csv в html-форме,
        if file_format != "csv":                    # но проверка лишней не бывает
            flash('Неподдерживаемый формат базы данных.')
            return redirect(url_for('user.registration'))
        f = TextIOWrapper(f, encoding="utf-8")
        reader = csv.reader(f)
        clients = []  # создаем список клиентов для подсчета инцидентов
        pairs_list = []  # список пар участников каждого ДТП
        for row in reader:
            pair = []
            row = row[0].split(";")
            clients.append(row[1])
            clients.append(row[2])
            pair.append(row[1])
            pair.append(row[2])
            pairs_list.append(pair)
        del clients[0:2]  # удаляем "Участник1", "Участник2"
        clients_counter = collections.Counter()
        for client in clients:
            clients_counter[client] += 1

        for client in clients_counter:     # подсчитываем все имена в списке
            client = client[0].split(" ")  # и формируем словарь типа
        clients = dict(clients_counter)    # "Имя": "Кол-во ДТП"

        potential_crime = []                 # Люди с 1 ДТП являются
        for key, value in clients.items():   # "тупиковой" вершиной графа,
            if value > 1:                    # значит цепь не замкнется,
                potential_crime.append(key)  # оставляем потенциальных

        nodes = []  # если в "паре" один из участников - тупиковая вершина,
        edges = []  # убираем всю "пару". "Пара" будет ребром.
        for pair in pairs_list:
            if pair[0] in potential_crime and pair[1] in potential_crime:
                nodes.append(pair[0])  # А мошенники - вершинами.
                nodes.append(pair[1])
                edges.append(pair)
        print(nodes)
        for client in clients.items():
            if client[0] in nodes:
                crime_status = 2
            elif client[1] > 1:
                crime_status = 1
            else:
                crime_status = 0
            full_name = client[0].split(" ")
            new_client = Client(surname=full_name[0],
                                name=full_name[1],
                                middle_name=full_name[2],
                                incident_counter=client[1],
                                crime_status=crime_status)
            db.session.add(new_client)
            db.session.commit()
        flash('База данных обновлена')
        return redirect(url_for('user.search'))


@blueprint.route("/search")
def search():
    title_auth = "Поиск клиента"
    form = SearchForm()
    return render_template("user/search.html", title_auth=title_auth,
                           form=form)


@blueprint.route('/process-search', methods=['POST'])
def process_search():
    form = SearchForm()
    if form.validate_on_submit():
        client = Client.query.filter(Client.surname==form.surname.data and Client.name==form.name.data and Client.middle_name==form.middle_name.data).first()
        if client:
            print(client)
            flash(str(client))
            return redirect(url_for('user.search'))
        else:
            flash('Клиент отсутствует в базе данных')
            return redirect(url_for('user.search'))


@blueprint.route('/wanted', methods=['GET'])
def wanted():
    page_title = "Черный список"
    potential = Client.query.filter(Client.crime_status == 1).order_by(Client.incident_counter.desc())
    syndicate = Client.query.filter(Client.crime_status == 2).order_by(Client.incident_counter.desc())
    if potential or syndicate:
        potential_list = []
        syndicate_list = []
        for client in potential:
            potential_list.append(str(client))
        for client in syndicate:
            syndicate_list.append(str(client))
        return render_template("user/crime_clients.html", page_title=page_title,
                               potential_list=potential_list,
                               syndicate_list=syndicate_list)
    else:
        flash('У нас только добропорядочные клиенты')
        return redirect(url_for('user.search'))
