from flask import Blueprint, render_template, request, redirect, url_for
from datebase.classes import User, Info
from datebase import db_session
from flask_login import current_user

profile_edit_page = Blueprint('profile_edit', __name__, template_folder='templates')


@profile_edit_page.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    if current_user.is_authenticated:
        user_id = current_user.id
        session_db = db_session.create_session()
        user = session_db.query(User).filter_by(id=user_id).first()

        if request.method == 'POST':
            user.name = request.form.get('name')
            user.surname = request.form.get('surname')
            user.patronymic = request.form.get('patronymic')
            user.login = request.form.get('login')

            if user.role == 'student':
                info = session_db.query(Info).filter_by(user_id=user_id).first()

                if info:
                    info.stud_class = request.form.get('class')
                    info.balance = request.form.get('balance')
                    info.alergies = request.form.get('alergies')
                    info.preferences = request.form.get('preferences')

            session_db.commit()
            session_db.close()

            return redirect(url_for('main_page.mainpage'))

        if user.role == 'student':
            info = session_db.query(Info).filter_by(user_id=user_id).first()

            if info.stud_class and info.balance and info.alergies and info.preferences:
                context = {
                    'name': user.name,
                    'surname': user.surname,
                    'patronymic': user.patronymic,
                    'class': info.stud_class,
                    'login': user.login,
                    'balance': info.balance,
                    'alergies': info.alergies,
                    'preferences': info.preferences}

            else:
                context = {
                    'name': user.name,
                    'surname': user.surname,
                    'patronymic': user.patronymic,
                    'class': '',
                    'login': user.login,
                    'balance': '',
                    'alergies': '',
                    'preferences': ''}

        else:
            context = {
                'name': user.name,
                'surname': user.surname,
                'patronymic': user.patronymic,
                'login': user.login,
                'class': '',
                'balance': '',
                'alergies': '',
                'preferences': ''
            }

        session_db.close()
        return render_template('profile_edit.html', **context)
    else:
        return render_template('login.html')