# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Time, TIMESTAMP, Interval, Numeric, Text, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask import render_template
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone_number = Column(String(10))
    address = Column(String(50))
    role = Column(Enum('member', 'trainer', 'admin', name='role'))
    birthdate = Column(Date)
    registration_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    is_active = Column(Boolean, default=True)

    registered_classes = relationship("ClassRegistration", backref="member_to_registrations")

    def is_active(self):
        return self.is_active
    
    def get_id(self):
        return str(self.user_id)
    
    @property
    def fullname(self):
        return str(self.first_name) + " " + str(self.last_name)


class TrainerSchedule(db.Model):
    __tablename__ = 'schedules'

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    trainer_id = Column(Integer, ForeignKey('users.user_id'))
    day_of_week = Column(Enum('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', name='day_of_week'))
    start_time = Column(Time)
    end_time = Column(Time)


class Session(db.Model):
    __tablename__ = 'sessions'

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('users.user_id'))
    trainer_id = Column(Integer, ForeignKey('users.user_id'))
    session_date = Column(Date)
    session_time = Column(Time)
    duration = Column(Interval)
    status = Column(Enum('Active', 'Canceled', name='status'), default='Active')

    member = relationship("User", foreign_keys=[member_id], backref="sessions_as_member")
    trainer = relationship("User", foreign_keys=[trainer_id], backref="sessions_as_trainer")



class Exercise(db.Model):
    __tablename__ = 'exercises'

    exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(50))
    category = Column(String(50))
    musclegroup = Column(String(50))
    reps = Column(Integer)
    sets = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)



class Class(db.Model):
    __tablename__ = 'classes'

    class_id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(100))
    description = Column(Text)
    trainer_id = Column(Integer, ForeignKey('users.user_id'))
    class_date = Column(Date)
    class_time = Column(Time)
    duration = Column(Interval)
    max_capacity = Column(Integer)

    trainer = relationship("User", foreign_keys=[trainer_id], backref="classes_as_trainer")
    registrations = relationship("ClassRegistration", backref="class_to_registrations")

    room_reservation = relationship("RoomReservation", uselist=False, backref="class_to_roomreservation")

    @property
    def remaining_capacity(self):
        registered_count = len(self.registrations)
        return self.max_capacity - registered_count if registered_count < self.max_capacity else 0



class ClassRegistration(db.Model):
    __tablename__ = 'classregistrations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey('classes.class_id'))
    member_id = Column(Integer, ForeignKey('users.user_id'))

    member = relationship("User", foreign_keys=[member_id], backref="classregistrations_as_member")
    corresponding_class = relationship("Class", foreign_keys=[class_id], backref="classregistrations_as_class")


class Bill(db.Model):
    __tablename__ = 'bills'

    bill_id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, default=100)

    payment = relationship("Payment", uselist=False, backref="bill_to_payment")


    @property
    def is_paid(self):
        return True if self.payment else False


class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey('bills.bill_id'))
    method = Column(Enum('Credit', 'Debit', 'Cash', name='method'))
    amount = Column(Integer)
    date = Column(Date)
    time = Column(Time)


class Goals(db.Model):
    __tablename__ = 'goals'

    goal_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('users.user_id'))
    goal_type = Column(String(100))
    target_value = Column(Numeric)
    start_date = Column(Date)
    end_date = Column(Date)
    progress = Column(Numeric)


class HealthMetric(db.Model):
    __tablename__ = 'healthmetrics'

    healthmetrics_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('users.user_id'))
    weight = Column(Integer)
    height = Column(Integer)
    muscle_percentage = Column(Integer)
    fat_percentage = Column(Integer)
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    resting_heart_rate = Column(Integer)
    notes = Column(String(100))
    date = Column(Date)


class Room(db.Model):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    capacity = Column(Integer)

class RoomReservation(db.Model):
    __tablename__ = "roomreservations"

    roomreservation_id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('rooms.room_id'))
    class_id = Column(Integer, ForeignKey('classes.class_id'))

class Equipment(db.Model):
    __tablename__ = 'equipments'

    equipment_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    condition = Column(Enum('good', 'maintenance_needed', 'non_functional', name='condition'))


class EquipmentMaintennance(db.Model):
    __tablename__ = 'equipmentmaintennances'

    equipmentMaintennance_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('users.user_id'))
    equipment_id = Column(Integer, ForeignKey('equipments.equipment_id'))
    date = Column(Date)
    report = Column(Text)

    admin = relationship("User", foreign_keys=[admin_id], backref="equipmentmaintenance_to_admin")
    equipment = relationship("Equipment", foreign_keys=[equipment_id], backref="equipmentmaintenance_to_equipment")
