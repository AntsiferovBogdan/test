from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    surname = StringField("Фамилия", [DataRequired()],
                          render_kw={"class": "form-control",
                          "placeholder": "Фамилия клиента"}
                          )
    name = StringField("Имя", [DataRequired()],
                       render_kw={"class": "form-control",
                       "placeholder": "Имя клиента"}
                       )
    middle_name = StringField("Отчество", [DataRequired()],
                              render_kw={"class": "form-control",
                              "placeholder": "Отчество клиента"}
                              )
    submit = SubmitField("Найти", render_kw={
                             "class": "btn btn-success btn-lg btn-block"
                             }
                         )


class RegistrationForm(FlaskForm):
    surname = StringField("Фамилия", [DataRequired()],
                          render_kw={"class": "form-control",
                          "placeholder": "Фамилия клиента"}
                          )
    name = StringField("Имя", [DataRequired()],
                       render_kw={"class": "form-control",
                       "placeholder": "Имя клиента"}
                       )
    middle_name = StringField("Отчество", [DataRequired()],
                              render_kw={"class": "form-control",
                              "placeholder": "Отчество клиента"}
                              )
    incident_counter = IntegerField("Количество инцидентов",
                                    render_kw={"class": "form-control"},
                                    default=1)
    submit = SubmitField("Добавить", render_kw={
                             "class": "btn btn-success btn-lg btn-block"
                             }
                         )
