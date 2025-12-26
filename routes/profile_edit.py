from flask_login import login_required, logout_user, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from datebase.classes import User, Info
from datebase import db_session

profile_edit_page = Blueprint('profile_edit', __name__, template_folder='templates')

@login_required
@profile_edit_page.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    user_id = current_user.id
    session_db = db_session.create_session()
    user = session_db.query(User).filter_by(id=user_id).first()

    if request.method == 'POST':
        user.login = request.form.get('login')
        password = request.form.get('password')
        second_password = request.form.get('second_password')
        if password and password == second_password:
            user.password = generate_password_hash(password)

        if user.role == 'student':
            info = session_db.query(Info).filter_by(user_id=user_id).first()

            if info:
                info.alergies = request.form.get('alergies')
                info.preferences = request.form.get('preferences')

        session_db.commit()
        session_db.close()

        return redirect(url_for('profile_page.profilepage'))

    if user.role == 'student':
        info = session_db.query(Info).filter_by(user_id=user_id).first()

        context = {
            'name': user.name,
            'surname': user.surname,
            'patronymic': user.patronymic,
            'login': user.login,
            'balance': info.balance if info else '0 рублей',
            'stud_class': info.stud_class if info else 'не указан',
            'alergies': info.alergies if info else 'не указана',
            'preferences': info.preferences if info else 'не указаны',
        }

    else:
        context = {
            'name': user.name,
            'surname': user.surname,
            'patronymic': user.patronymic,
            'login': user.login,
            'stud_class': '',
            'balance': '',
            'alergies': '',
            'preferences': ''
        }

    session_db.close()
    return render_template('profile_edit.html', **context)
