from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_bootstrap import Bootstrap
from models import db, User, HealthMetric, Goals, TrainerSchedule, Session, Class, Exercise, Bill, ClassRegistration, Payment, Room, RoomReservation, Equipment, EquipmentMaintennance
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from datetime import timedelta


username = "postgres"
password = "Nusrat1986!"
host = "localhost"
port = "5432"
dbname = "healthcareclub"

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'UkwZObVBRx'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
db.init_app(app)
login_manager.init_app(app)
bootstrap = Bootstrap(app)



@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
            
        else:
            flash('Failed to login!')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        role = request.form['role']
        birthdate = request.form.get('birthdate')

        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date() if birthdate else None

        new_user = User(username=username, password=password, email=email, first_name=first_name,
                        last_name=last_name, phone_number=phone_number, address=address,
                        role=role, birthdate=birthdate)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists, please choose another.')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.phone_number = request.form['phone_number']
        user.address = request.form['address']
        user.role = request.form['role']
        user.birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)


@app.route('/healthmetrics', methods=['GET', 'POST'])
@login_required
def health_metrics():

    if request.method == 'POST':
        weight = request.form['weight']
        height = request.form['height']
        muscle_percentage = request.form['muscle_percentage']
        fat_percentage = request.form['fat_percentage']
        blood_pressure_systolic = request.form['blood_pressure_systolic']
        blood_pressure_diastolic = request.form['blood_pressure_diastolic']
        resting_heart_rate = request.form['resting_heart_rate']
        notes = request.form['notes']
        date = request.form['date']
        
        new_health_metric = HealthMetric(member_id=current_user.user_id, weight=weight, height=height,
                                         muscle_percentage=muscle_percentage, fat_percentage=fat_percentage,
                                         blood_pressure_systolic=blood_pressure_systolic,
                                         blood_pressure_diastolic=blood_pressure_diastolic,
                                         resting_heart_rate=resting_heart_rate, notes=notes, date=date)
        db.session.add(new_health_metric)
        db.session.commit()
        flash('New health metric added successfully!', 'success')
        return redirect(url_for('health_metrics'))
    
    health_metrics = HealthMetric.query.filter_by(member_id=current_user.user_id).order_by(HealthMetric.date.asc()).all()
    
    return render_template('member/healthmetrics.html', health_metrics=health_metrics)


@app.route('/healthmetrics/<int:health_metric_id>', methods=['GET', 'POST'])
def edit_health_metric(health_metric_id=None):
    health_metric = HealthMetric.query.get_or_404(health_metric_id)

    if request.method == 'POST':
        health_metric.date = request.form['date']
        health_metric.weight = request.form['weight']
        health_metric.height = request.form['height']
        health_metric.muscle_percentage = request.form['muscle_percentage']
        health_metric.fat_percentage = request.form['fat_percentage']
        health_metric.blood_pressure_systolic = request.form['blood_pressure_systolic']
        health_metric.blood_pressure_diastolic = request.form['blood_pressure_diastolic']
        health_metric.resting_heart_rate = request.form['resting_heart_rate']
        health_metric.notes = request.form['notes']

        db.session.commit()

        flash('Health metric updated successfully!', 'success')

        return redirect(url_for('health_metrics'))

    return render_template('member/healthmetricsupdate.html', health_metric=health_metric)


@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    if request.method == 'POST':
        goal_type = request.form['goal_type']
        target_value = request.form['target_value']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        new_goal = Goals(
            member_id=current_user.user_id,
            goal_type=goal_type,
            target_value=target_value,
            start_date=start_date,
            end_date=end_date,
            progress=0
        )
        db.session.add(new_goal)
        db.session.commit()
        flash('Goal created successfully', 'success')
        return redirect(url_for('goals'))
    
    goals = Goals.query.filter_by(member_id=current_user.user_id).all()
    return render_template('member/goals.html', goals=goals)


@app.route('/goals/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def update_goal(goal_id):
    goal = Goals.query.get_or_404(goal_id)
    if request.method == 'POST':
        goal_type = request.form['goal_type']
        target_value = request.form['target_value']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        progress = request.form['progress']

        goal.goal_type = goal_type
        goal.target_value = target_value
        goal.start_date = start_date
        goal.end_date = end_date
        goal.progress = progress

        db.session.commit()
        flash('Goal updated successfully', 'success')
        return redirect(url_for('goals'))
    return render_template('member/goalsupdate.html', goal=goal)


@app.route('/schedules', methods=['GET', 'POST'])
@login_required
def schedules():
    if request.method == 'POST':
        day_of_week = request.form['day_of_week']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        
        new_schedule = TrainerSchedule(trainer_id=current_user.user_id, day_of_week=day_of_week,
                                       start_time=start_time, end_time=end_time)
        db.session.add(new_schedule)
        db.session.commit()
        flash('New schedule added successfully!', 'success')
        return redirect(url_for('schedules'))
    
    schedules = TrainerSchedule.query.filter_by(trainer_id=current_user.user_id).all()
    
    return render_template('trainer/scheduels.html', schedules=schedules)


@app.route('/schedules/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
def edit_schedule(schedule_id):
    schedule = TrainerSchedule.query.get_or_404(schedule_id)
    
    if request.method == 'POST':
        schedule.day_of_week = request.form['day_of_week']
        schedule.start_time = request.form['start_time']
        schedule.end_time = request.form['end_time']
        
        db.session.commit()
        flash('Schedule updated successfully!', 'success')
        return redirect(url_for('schedules'))
    
    return render_template('trainer/schedulesupdate.html', schedule=schedule)

@app.route('/schedules/<int:schedule_id>/delete', methods=['GET'])
@login_required
def delete_schedule(schedule_id):
    schedule = TrainerSchedule.query.get_or_404(schedule_id)
    
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        flash('Schedule deleted successfully!', 'success')
        return redirect(url_for('schedules'))
    else:
        flash("There was a problem in deleting the availability!", 'error')
        return redirect(url_for('schedules'))


@app.route('/member/sessions')
def member_sessions():
    member_id = current_user.user_id
    sessions = Session.query.filter_by(member_id=member_id).all()
    return render_template('trainer/sessions.html', sessions=sessions)


@app.route('/trainer/sessions')
def trainer_sessions():
    trainer_id = current_user.user_id
    sessions = Session.query.filter_by(trainer_id=trainer_id).all()
    return render_template('trainer/sessions.html', sessions=sessions)


@app.route('/cancel_session/<int:session_id>', methods=['POST'])
def cancel_session(session_id):
    session = Session.query.get(session_id)
    if session:
        session.status = 'Canceled'
        db.session.commit()
        flash('Session canceled successfully!', 'success')
    return redirect(url_for('trainer_sessions'))


@app.route('/trainer/classes')
def trainer_classes():
    trainer_id = current_user.user_id
    trainer_classes = Class.query.filter_by(trainer_id=trainer_id).all()
    return render_template('trainer/classes.html', classes=trainer_classes)


@app.route('/member/classes')
def member_classes():
    user = User.query.get(current_user.user_id)
    classes = [registration.corresponding_class for registration in user.registered_classes]

    return render_template('trainer/classes.html', classes=classes)


@app.route('/exercises', methods=['GET', 'POST'])
@login_required
def exercises():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        musclegroup = request.form['musclegroup']
        reps = request.form['reps']
        sets = request.form['sets']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        new_exercise = Exercise(
            member_id=current_user.user_id,
            name=name,
            category=category,
            musclegroup=musclegroup,
            reps=reps,
            sets=sets,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_exercise)
        db.session.commit()
        flash('Exercise created successfully', 'success')
        return redirect(url_for('exercises'))
    
    exercises = Exercise.query.filter_by(member_id=current_user.user_id).order_by(Exercise.start_date.asc()).all()
    return render_template('member/exercises.html', exercises=exercises)


@app.route('/exercises/<int:exercise_id>', methods=['GET', 'POST'])
@login_required
def update_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)

    if request.method == 'POST':
        exercise.name = request.form['name']
        exercise.category = request.form['category']
        exercise.musclegroup = request.form['musclegroup']
        exercise.reps = request.form['reps']
        exercise.sets = request.form['sets']
        exercise.start_date = request.form['start_date']
        exercise.end_date = request.form['end_date']

        db.session.commit()
        flash('Exercise updated successfully', 'success')
        return redirect(url_for('exercises'))
    
    return render_template('member/exerciseupdate.html', exercise=exercise)


@app.route('/book_session', methods=['GET', 'POST'])
@login_required
def create_session():
    if request.method == 'POST':
        session_date = request.form['session_date']
        session_time = request.form['session_time']
        duration = request.form['duration']
        trainer_id = request.form['trainer_id']

        # checks no one else has booked the trainer on this time
        session_start = datetime.strptime(session_date + ' ' + session_time, '%Y-%m-%d %H:%M')
        duration_hours, duration_minutes = map(int, duration.split(':'))
        session_end = session_start + timedelta(hours=duration_hours, minutes=duration_minutes)
        trainer_sessions = Session.query.filter_by(trainer_id=trainer_id, session_date=session_date).all()
        for session in trainer_sessions:
            start = datetime.combine(session.session_date, session.session_time)
            end = start + session.duration
            if session_start < end and session_end > start:
                flash('Selected time overlaps with existing session for the trainer.', 'error')
                return redirect(url_for('create_session'))

    
        # checks if the selected time is within the trainer's availability or not
        session_start = datetime.strptime(session_date + ' ' + session_time, '%Y-%m-%d %H:%M')
        day_of_week = session_start.strftime('%a')
        trainer_schedule = TrainerSchedule.query.filter_by(trainer_id=trainer_id, day_of_week=day_of_week).first()
        if trainer_schedule:
            start_time = trainer_schedule.start_time
            end_time = trainer_schedule.end_time
            session_start = datetime.strptime(session_date + ' ' + session_time, '%Y-%m-%d %H:%M')
            session_end = session_start + timedelta(hours=duration_hours, minutes=duration_minutes)

            if session_start.time() < start_time or session_end.time() > end_time:
                flash("Selected time is not within the trainer's availability.", 'error')
                return redirect(url_for('create_session'))
        else:
            flash("Selected time is not within the trainer's availability.", 'error')
            return redirect(url_for('create_session'))
            
        new_session = Session(session_date=session_date, session_time=session_time, 
                            duration=duration, member_id=current_user.user_id, trainer_id=trainer_id)
        db.session.add(new_session)
        db.session.commit()

        db.session.commit()
        
        return redirect(url_for('member_sessions'))
    
    return render_template('member/book_session.html', trainers = User.query.filter_by(role='trainer').all())


@app.route('/register_class', methods=['GET', 'POST'])
def register_class():
    if request.method == 'POST':
        class_id = request.form['class_id']
        member_id = current_user.user_id

        selected_class = Class.query.get(class_id)
        if selected_class.remaining_capacity <= 0:
            flash("The class is full!", "error")
            return redirect(url_for('register_class'))

        new_registration = ClassRegistration(class_id=class_id, member_id=member_id)
        db.session.add(new_registration)
        db.session.commit()

        db.session.commit()
        
        return redirect(url_for('member_classes')) 

    classes = Class.query.all()
    print(classes)
    user_id = current_user.user_id
    registered_class_ids = [reg.class_id for reg in ClassRegistration.query.filter_by(member_id=user_id).all()]
    unregistered_classes = [c for c in classes if c.class_id not in registered_class_ids]

    return render_template('member/register_class.html', classes=unregistered_classes)


@app.route('/bills', methods=['GET'])
@login_required
def list_bills():
    bills = []
    sorted_bills = sorted(bills, key=lambda x: x.bill_id)
    return render_template('member/bills.html', bills=sorted_bills)


@app.route('/pay_bill/<int:bill_id>', methods=['POST'])
@login_required
def pay_bill(bill_id):
    bill = Bill.query.get(bill_id)
    new_payment = Payment(bill_id=bill_id, method=request.form['method'], amount=bill.price, date=datetime.today(), time=datetime.now().time())
    db.session.add(new_payment)
    db.session.commit()
    flash("Payment successful!", "success")
    return redirect(url_for('list_bills'))


@app.route('/search_users', methods=['GET', 'POST'])
def search_users():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        first_name_users = User.query.filter_by(role="member").filter(User.first_name.ilike(f'%{search_query}%')).all()
        last_name_users = User.query.filter_by(role="member").filter(User.last_name.ilike(f'%{search_query}%')).all()
        users = first_name_users + last_name_users
        return render_template('trainer/search_users.html', users=users)
    return render_template('trainer/search_users.html', users=[])


@app.route('/user_info/<int:user_id>')
def user_info(user_id):
    user = User.query.get_or_404(user_id)
    health_metrics = HealthMetric.query.filter_by(member_id=user_id).all()
    goals = Goals.query.filter_by(member_id=user_id).all()
    exercise_routines = Exercise.query.filter_by(member_id=user_id).all()
    return render_template('trainer/memberprofile.html', user=user, health_metrics=health_metrics, goals=goals, exercises=exercise_routines)


@app.route('/assign_room', methods=['GET', 'POST'])
@login_required
def assign_room():
    if request.method == 'POST':
        class_id = request.form['class_id']
        room_id = request.form['room_id']

        selected_class = Class.query.get(class_id)
        selected_room = Room.query.get(room_id)

        if (selected_class.max_capacity > selected_room.capacity):
            flash("The capacity of the room is not enough!")
            return redirect(url_for('assign_room'))

        new_reservation = RoomReservation(class_id=class_id, room_id=room_id)
        db.session.add(new_reservation)
        db.session.commit()
        flash("room assigned to the class successfully!", "success")

        return redirect(url_for('assign_room'))

    classes_without_rooms = Class.query.filter(Class.room_reservation == None).all()
    available_rooms = Room.query.all()

    return render_template('admin/assign_room.html', classes=classes_without_rooms, rooms=available_rooms)


@app.route('/equipment_maintenance', methods=['GET', 'POST'])
def equipment_maintenance():
    if request.method == 'POST':
        equipment_id = request.form['equipment_id']
        date = request.form['date']
        report = request.form['report']

        new_maintenance = EquipmentMaintennance(admin_id=current_user.user_id, equipment_id=equipment_id, date=date, report=report)
        db.session.add(new_maintenance)
        db.session.commit()
        flash("The maintenance record has been saved successfully!", "success")

        return redirect(url_for('equipment_maintenance'))

    maintenances = EquipmentMaintennance.query.filter_by(admin_id=current_user.user_id).all()
    return render_template('admin/equipmentmaintenance.html', maintenances=maintenances, equipments=Equipment.query.all())


@app.route('/dashboard')
def dashboard():
    user = current_user
    if user.role == 'admin':
        return render_template('admin/dashboard.html')
    elif user.role == 'trainer':
        return render_template('trainer/dashboard.html')
    elif user.role == 'member':
        return render_template('member/dashboard.html')
    return render_template('index.html')


if __name__ == '__main__':
    
    from sqlalchemy.schema import CreateTable
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
