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
        f = TextIOWrapper(f, encoding="utf-8")  # у меня были проблемы
        reader = csv.reader(f)                  # с кодировкой на mac
        incidents_list = []                     # если что, используйте
        for row in reader:                      # data_2.csv с гитхаба
            row = row[0].split(";")
            incidents_list.append(row[1])
            incidents_list.append(row[2])
        del incidents_list[0:2]
        people_counter = collections.Counter()

        for people in incidents_list:
            people_counter[people] += 1

        for people in people_counter:
            people = people[0].split(" ")
        people_counter = dict(people_counter)

        for people in people_counter.items():
            full_name = people[0].split(" ")
            new_client = Client(surname=full_name[0],
                                name=full_name[1],
                                middle_name=full_name[2],
                                incident_counter=people[1])
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
    page_title = "Потенциальные мошенники"
    crime_clients = Client.query.filter(Client.incident_counter > 1).order_by(Client.incident_counter.desc())
    if crime_clients:
        crime_list = []
        for client in crime_clients:
            client = str(client)
            crime_list.append(client)
        return render_template("user/crime_clients.html", page_title=page_title,
                               crime_list=crime_list)
    else:
        flash('У нас только добропорядочные клиенты')
        return redirect(url_for('user.search'))
