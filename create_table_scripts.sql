DROP TABLE IF EXISTS equipments cascade ;
DROP TABLE IF EXISTS rooms  cascade;
DROP TABLE IF EXISTS users cascade;
DROP TABLE IF EXISTS classes cascade;
DROP TABLE IF EXISTS equipmentmaintenances cascade;
DROP TABLE IF EXISTS exercises cascade;
DROP TABLE IF EXISTS goals cascade;
DROP TABLE IF EXISTS healthmetrics cascade;
DROP TABLE IF EXISTS schedules cascade;
DROP TABLE IF EXISTS classregistrations cascade;
DROP TABLE IF EXISTS roomreservations cascade;
DROP TABLE IF EXISTS bills cascade;
DROP TABLE IF EXISTS payments cascade;
DROP TABLE IF EXISTS sessions cascade;



CREATE TABLE equipments (
	equipment_id SERIAL NOT NULL, 
	name VARCHAR(50), 
	condition VARCHAR(18), 
	PRIMARY KEY (equipment_id)
);



CREATE TABLE rooms (
	room_id SERIAL NOT NULL, 
	capacity INTEGER, 
	PRIMARY KEY (room_id)
);



CREATE TABLE users (
	user_id SERIAL NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	first_name VARCHAR(50), 
	last_name VARCHAR(50), 
	phone_number VARCHAR(10), 
	address VARCHAR(50), 
	role VARCHAR(7), 
	birthdate DATE, 
	registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (user_id), 
	UNIQUE (username), 
	UNIQUE (email)
);



CREATE TABLE classes (
	class_id SERIAL NOT NULL, 
	class_name VARCHAR(100), 
	description TEXT, 
	trainer_id SERIAL, 
	class_date DATE, 
	class_time TIME, 
	duration INTERVAL, 
	max_capacity INTEGER, 
	PRIMARY KEY (class_id), 
	FOREIGN KEY(trainer_id) REFERENCES users (user_id)
);



CREATE TABLE equipmentmaintenances (
	"equipmentMaintennance_id" SERIAL NOT NULL, 
	admin_id SERIAL, 
	equipment_id SERIAL, 
	date DATE, 
	report TEXT, 
	PRIMARY KEY ("equipmentMaintennance_id"), 
	FOREIGN KEY(admin_id) REFERENCES users (user_id), 
	FOREIGN KEY(equipment_id) REFERENCES equipments (equipment_id)
);



CREATE TABLE exercises (
	exercise_id SERIAL NOT NULL, 
	member_id SERIAL, 
	name VARCHAR(50), 
	category VARCHAR(50), 
	musclegroup VARCHAR(50), 
	reps INTEGER, 
	sets INTEGER, 
	start_date DATE, 
	end_date DATE, 
	PRIMARY KEY (exercise_id), 
	FOREIGN KEY(member_id) REFERENCES users (user_id)
);



CREATE TABLE goals (
	goal_id SERIAL NOT NULL, 
	member_id SERIAL, 
	goal_type VARCHAR(100), 
	target_value NUMERIC, 
	start_date DATE, 
	end_date DATE, 
	progress NUMERIC, 
	PRIMARY KEY (goal_id), 
	FOREIGN KEY(member_id) REFERENCES users (user_id)
);


CREATE TABLE healthmetrics (
	healthmetrics_id SERIAL NOT NULL, 
	member_id SERIAL, 
	weight INTEGER, 
	height INTEGER, 
	muscle_percentage INTEGER, 
	fat_percentage INTEGER, 
	blood_pressure_systolic INTEGER, 
	blood_pressure_diastolic INTEGER, 
	resting_heart_rate INTEGER, 
	notes VARCHAR(100), 
	date DATE, 
	PRIMARY KEY (healthmetrics_id), 
	FOREIGN KEY(member_id) REFERENCES users (user_id)
);



CREATE TABLE schedules (
	schedule_id SERIAL NOT NULL, 
	trainer_id SERIAL, 
	day_of_week VARCHAR(3), 
	start_time TIME, 
	end_time TIME, 
	PRIMARY KEY (schedule_id), 
	FOREIGN KEY(trainer_id) REFERENCES users (user_id)
);



CREATE TABLE sessions (
	session_id SERIAL, 
	member_id SERIAL, 
	trainer_id SERIAL, 
	session_date DATE, 
	session_time TIME, 
	duration INTERVAL, 
	status VARCHAR(8), 
	PRIMARY KEY (session_id), 
	FOREIGN KEY(member_id) REFERENCES users (user_id), 
	FOREIGN KEY(trainer_id) REFERENCES users (user_id)
);



CREATE TABLE classregistrations (
	id SERIAL NOT NULL, 
	class_id SERIAL, 
	member_id SERIAL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(class_id) REFERENCES classes (class_id), 
	FOREIGN KEY(member_id) REFERENCES users (user_id)
);



CREATE TABLE roomreservations (
	roomreservation_id SERIAL NOT NULL, 
	room_id SERIAL, 
	class_id SERIAL, 
	PRIMARY KEY (roomreservation_id), 
	FOREIGN KEY(room_id) REFERENCES rooms (room_id), 
	FOREIGN KEY(class_id) REFERENCES classes (class_id)
);



CREATE TABLE bills (
	bill_id SERIAL NOT NULL, 
	member_id SERIAL,
	price INTEGER,
	paid BOOL,
	PRIMARY KEY (bill_id), 
	FOREIGN KEY(member_id) REFERENCES users (user_id)
);