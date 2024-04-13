
INSERT INTO users (username, password, email, first_name, last_name, phone_number, address, role, birthdate)
VALUES
('user1', 'p1', 'user1@example.com', 'John', 'Doe', '1234567890', '123 Main St', 'member', '1990-01-01'),
('user2', 'p2', 'user2@example.com', 'Jane', 'Smith', '0987654321', '456 Elm St', 'trainer', '1985-05-05'),
('user3', 'p3', 'user3@example.com', 'jack', 'Parson', '3437779999', '2343 sdf sd', 'admin', '1990-05-05');

INSERT INTO schedules (trainer_id, day_of_week, start_time, end_time)
VALUES
(2, 'Mon', '09:00:00', '12:00:00'),
(2, 'Tue', '14:00:00', '17:00:00');

INSERT INTO sessions (member_id, trainer_id, session_date, session_time, duration, status)
VALUES
(1, 2, CURRENT_DATE, '10:00:00', '01:00:00', 'Active');

INSERT INTO exercises (member_id, name, category, musclegroup, reps, sets, start_date, end_date)
VALUES 
    (1, 'Squats', 'Strength', 'Legs', 12, 3, '2024-04-01', '2024-04-30'),
    (1, 'Pull-ups', 'Strength', 'Back', 8, 3, '2024-05-01', '2024-05-30'),
    (1, 'Plank', 'Core', 'Abs', 60, 1, '2024-06-01', '2024-06-30');

INSERT INTO classes (class_name, description, trainer_id, class_date, class_time, duration, max_capacity)
VALUES
('Yoga Class', 'Relaxing yoga session for all levels.', 2, '2024-04-01', '09:00:00', INTERVAL '1 hour', 20),
('Bootcamp', 'High-intensity interval training for fitness enthusiasts.', 2, '2024-04-02', '18:00:00', INTERVAL '1.5 hours', 15),
('Advanced Yoga Class', 'Intense yoga session for experts.', 2, '2024-04-02', '09:00:00', INTERVAL '1 hour', 10),
('Boxing Class', 'Relaxing yoga session for all levels.', 2, '2024-04-01', '09:00:00', INTERVAL '1 hour', 20),
('Fencing', 'High-intensity interval training for fitness enthusiasts.', 2, '2024-04-02', '18:00:00', INTERVAL '1.5 hours', 15),
('Advanced Soccer Class', 'Intense yoga session for experts.', 2, '2024-04-02', '09:00:00', INTERVAL '1 hour', 10);

INSERT INTO classregistrations (class_id, member_id)
VALUES
(1, 1);





INSERT INTO goals (member_id, goal_type, target_value, start_date, end_date, progress)
VALUES
(1, 'Weight Loss', 10, '2024-04-01', '2024-05-01', 10),
(1, 'Muscle Gain', 5, '2024-05-01', '2024-06-01', 3);

INSERT INTO healthmetrics (member_id, weight, height, muscle_percentage, fat_percentage, blood_pressure_systolic, blood_pressure_diastolic, resting_heart_rate, notes, date)
VALUES
(1, 70, 170, 20, 15, 120, 80, 60, 'Healthy', '2024-04-01'),
(1, 80, 180, 25, 20, 130, 85, 65, 'Normal', '2024-04-10');

INSERT INTO rooms (capacity)
VALUES
(20),
(15),
(5);

INSERT INTO roomreservations (room_id, class_id)
VALUES
(1, 1),
(2, 2);

INSERT INTO equipments (name, condition)
VALUES
('Treadmill', 'good'),
('Dumbbells', 'maintenance_needed');

INSERT INTO equipmentmaintennances (admin_id, equipment_id, date, report)
VALUES
(3, 1, '2024-04-01', 'Performed routine maintenance.'),
(3, 2, '2024-04-02', 'Scheduled maintenance for expert repairs.');

