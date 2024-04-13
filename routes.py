# routes.py
from flask import render_template, request, redirect, url_for
from models import db, User,  Member, Trainer, Admin, Session, Goals, Classes, ClassMembers, RoomBookings, EquipmentMaintenance, Payments
from . import app
from flask_login import current_user
from flask_login import login_user
from flask import flash


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        # Create new user
        new_user = Member(username=username, password=password,
                          email=email, first_name=first_name, last_name=last_name)

        # Add new user to database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Query database for user
        user = User.query.filter_by(username=username).first()

        # Check password and log user in
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('admin_dashboard'))

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('trainer_dashboard'))

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('member_dashboard'))

    return render_template('login.html')


@app.route('/member/profile', methods=['GET', 'POST'])
def member_profile():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        # Update member profile
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email

        # Commit changes to database
        db.session.commit()

        return redirect(url_for('member_dashboard'))

    # For GET request, display current user info
    return render_template('member_profile.html', user=current_user)


@app.route('/member/dashboard')
def member_dashboard():
    # Query database for user's data
    user_data = Member.query.filter_by(id=current_user.id).first()

    # Pass user data to template
    return render_template('member_dashboard.html', user_data=user_data)


@app.route('/trainer/profile', methods=['GET', 'POST'])
def trainer_profile():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        # Update trainer profile
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email

        # Commit changes to database
        db.session.commit()

        return redirect(url_for('trainer_dashboard'))

    # For GET request, display current user info
    return render_template('trainer_profile.html', user=current_user)


@app.route('/view_profile/<int:member_id>')
def view_profile(member_id):
    # Query database for member's data
    member_data = Member.query.get(member_id)

    # Pass member data to template
    return render_template('view_profile.html', member_data=member_data)


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        # Get form data
        session_date = request.form.get('session_date')
        session_time = request.form.get('session_time')

        # Create new session
        new_session = Session(member_id=current_user.id,
                              session_date=session_date, session_time=session_time)

        # Add new session to database
        db.session.add(new_session)
        db.session.commit()

        return redirect(url_for('dashboard'))

    # For GET request, display current user's schedule
    sessions = Session.query.filter_by(member_id=current_user.id).all()
    return render_template('schedule.html', sessions=sessions)


@app.route('/book_room', methods=['GET', 'POST'])
def book_room():
    if request.method == 'POST':
        # Get form data
        room = request.form.get('room')
        booking_datetime = request.form.get('booking_datetime')

        # Create new room booking
        new_booking = RoomBookings(
            admin_id=current_user.id, room=room, booking_datetime=booking_datetime)

        # Add new booking to database
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('dashboard'))

    # For GET request, display current bookings
    bookings = RoomBookings.query.filter_by(admin_id=current_user.id).all()
    return render_template('book_room.html', bookings=bookings)
