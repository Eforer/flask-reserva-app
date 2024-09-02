from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.models import User, Reservation
from app.forms import RegistrationForm, LoginForm, ReservationForm
from datetime import datetime, timedelta

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create(form.username.data, form.email.data, form.password.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', title='Reservation Calendar')

@app.route('/get_available_slots', methods=['GET'])
@login_required
def get_available_slots():
    start = request.args.get('start')
    end = request.args.get('end')
    start_date = datetime.fromisoformat(start[:-1])  # Remove 'Z' from the end
    end_date = datetime.fromisoformat(end[:-1])

    events = []
    current_date = start_date
    while current_date <= end_date:
        available_slots = Reservation.get_available_slots(current_date.date())
        for slot in available_slots:
            slot_datetime = datetime.combine(current_date.date(), slot)
            events.append({
                'title': 'Available',
                'start': slot_datetime.isoformat(),
                'end': (slot_datetime + timedelta(hours=1)).isoformat(),
                'color': 'green'
            })
        current_date += timedelta(days=1)

    return jsonify(events)

@app.route('/make_reservation', methods=['POST'])
@login_required
def make_reservation():
    data = request.json
    date = datetime.fromisoformat(data['start'][:-1]).date()
    time = datetime.fromisoformat(data['start'][:-1]).time()
    
    try:
        Reservation.create(current_user.id, date, time)
        return jsonify({'status': 'success', 'message': 'Reservation created successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/cancel_reservation/<int:id>', methods=['POST'])
@login_required
def cancel_reservation(id):
    reservation = Reservation.get_by_id(id)
    if reservation and reservation.user_id == current_user.id:
        reservation.cancel()
        return jsonify({'status': 'success', 'message': 'Reservation cancelled successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Reservation not found or not authorized'})

@app.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    form = ReservationForm()
    if form.validate_on_submit():
        Reservation.create(current_user.id, form.date.data, form.time.data)
        flash('Your reservation has been made!')
        return redirect(url_for('my_reservations'))
    return render_template('reserve.html', title='Make a Reservation', form=form)

@app.route('/my_reservations')
@login_required
def my_reservations():
    reservations = Reservation.get_by_user(current_user.id)
    return render_template('my_reservations.html', title='My Reservations', reservations=reservations)

