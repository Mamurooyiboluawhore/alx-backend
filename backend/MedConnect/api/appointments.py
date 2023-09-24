from api import db
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required
from api.models import Appointments, Doctors, Patients, TimeSlots
appt_bp = Blueprint('appt_bp', __name__)

# To Book an Appointment, The following must be done
# get the timeshedule of the doctors endpoint
# post a appointment
# Get convenient date and time for patients
# Determine the day and time
# Determine doctor that matches the day and time
# Filter to remove doctors with exception coinciding with the date
# Determine the number of appointment for a selected doctor
# Assign appointment to doctor with smallest appointment
    # If doctors have the same appointment
        # Assign appointments to doctors with highest duration
#Exception route with : id, doctors id, date

@appt_bp.route("/exception", methods=['POST'])
@jwt_required()
def exceptions():
    data = request.json
    doctor_id = data.get("doctor_id")
    date = data.get()



@appt_bp.route('/book-appointment', methods=['POST'])
#@jwt_required()
def book_appointment():
    data = request.json
    
    if 'patient_id' not in data or 'timeslots_id' not in data:
        return jsonify({'message': 'Please provide patient_id and timslots_id'}), 400

    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    timeslots_id = data.get('timeslots_id')
    day_of_the_week = data.get('day_of_the_week')

    current_datetime = datetime.now()
    day_of_the_week = current_datetime.strftime('%A')
    # Find all available time slots for the specified day_of_the_week and doctor
    time_slots = TimeSlots.query.filter_by(day_of_the_week=day_of_the_week).all()

    if not time_slots:
        return jsonify({'message': 'No available time slots for this doctor on the specified day'}), 400

    # Determine the number of appointments for each doctor on the specified day
    doctor_appointment_counts = {}
    for time_slot in time_slots:
        appointment_count = Appointments.query.filter_by(doctor_id=time_slot.doctor_id, date_of_appointment=current_datetime.date()).count()
        doctor_appointment_counts[time_slot] = appointment_count

    # Sort doctors by appointment count in ascending order
    sorted_doctors = sorted(doctor_appointment_counts.items(), key=lambda x: x[1])

    # Find doctors with the smallest appointment count
    smallest_appointment_count = sorted_doctors[0][1]
    available_doctors = [doctor for doctor, count in sorted_doctors if count == smallest_appointment_count]

    # If multiple doctors have the same smallest appointment count, choose the one with the highest duration (not implemented in your model)

    # Assign the appointment to the first available doctor
    chosen_doctor = available_doctors[0]

    # Create a new appointment
    appointment = Appointments(
        patient_id=patient_id,
        doctor_id_id=doctor_id,
        #date_of_appointment=current_datetime.date(),
        time=chosen_doctor.id
    )

    db.session.add(appointment) 
    db.session.commit()

    return jsonify({'message': 'Appointment booked successfully'}), 200



@appt_bp.route("/book_appointment", methods=["POST"])
def bookAppointment():
    data = request.get_json()
    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    dob_app = data.get('date_of_appointment')
    date_of_appointment = datetime.strptime(dob_app, '%Y-%m-%d').date()
    time_slot=data.get("TimeSlots").id

    '''check if doctor has reached max limit'''
    doctor = Doctors.query.get(doctor_id)
    week_start = date_of_appointment - timedelta(days=date_of_appointment.weekday())
    week_end = week_start + timedelta(days=6)
    weekly_appointment = Appointments.query.filter_by(doctor_id=doctor_id).filter(
        Appointments.date_of_appointment >= week_start,
        Appointments.date_of_appointment <= week_end
    ).count()

    if weekly_appointment >= 21:
        return jsonify({'message': 'Doctor has reached the maximum number of patients for this week'}), 400
    daily_appointments = Appointments.query.filter_by(doctor_id=doctor_id, date_of_appointment=date_of_appointment).count()

    if daily_appointments >= 3:
        return jsonify({'message': 'Doctor has reached the max number of patients for today'}), 400

    appointment = Appointments(patient_id=patient_id, doctor_id=doctor_id, date_of_appointment=date_of_appointment, status='Scheduled', time_slot_id=time_slot.id)
    db.session.add(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment booked successfully'}), 201


@appt_bp.route("/appointment/<int>: id", methods=["PUT"])
def update_appointment(appointment_id):
    appointment = Appointments.query.get(id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    data = request.get_json()
    appointment.time = data.get('time', appointment.time)
    appointment.doctor = data.get('doctor', appointment.doctor)


@appt_bp.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(post_id):
    appointment = Appointments.query.get(id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()

