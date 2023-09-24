"""
This file contains routes that concerns Users as listed below
1. Doctors
2. Patients
3. Healthcares
4. Admins
"""

from api import db
from flask import Blueprint, jsonify, abort, request
from api.main import is_user
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import Patients, Doctors, Healthcares, TimeSlots
from flask_jwt_extended import jwt_required

users_bp = Blueprint('users', __name__)

@users_bp.route("/patient", methods=["POST"], strict_slashes=False)
def register_patient():
    """
    Register a new patient
    """
    try:
        data = request.get_json()
        email_address = data['email_address']
        hashed_password = data['hashed_password']
        first_name = data['first_name']
        last_name = data['last_name']
        other_name = data['other_name']
        dob_str = data['date_of_birth']
        date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        gender = data['gender']
        phone_number = data['phone_number']
        
        
        if not is_user(email_address):
            hash_password = generate_password_hash(hashed_password)
            patient = Patients(
                    first_name=first_name,
                    last_name=last_name,
                    other_name=other_name,
                    email_address=email_address,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    phone_number=phone_number,
                    hashed_password=hash_password
                    )
            from api import db
            db.session.add(patient)
            db.session.commit()
            return jsonify({'status' : 'Patient successfully added'}), 200

        return jsonify({'message': 'User already exists'})
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown error"}) 


@users_bp.route("/patients/<int:id>", strict_slashes=False)
@jwt_required()
def get_patient(id):
    """
    Get a patient from the database
    """
    patient = Patients.query.get(id)
    if patient:
        return jsonify({
            'id': patient.id,
            'first_name' : patient.first_name,
            'last_name' : patient.last_name,
            'other_name' : patient.other_name,
            'email_address' : patient.email_address,
            'phone_number' : patient.phone_number,
            'date_of_birth' : patient.date_of_birth,
            'gender' : patient.gender
            }), 200
    return jsonify({'error': 'User not found'})


@users_bp.route("/patients", strict_slashes=False)
@jwt_required()
def all_patients():
    patients = Patients.query.all()
    all_patients = []
    if patients:
        for patient in patients:
            pat = {
            'id': patient.id,
            'first_name' : patient.first_name,
            'last_name' : patient.last_name,
            'other_name' : patient.other_name,
            'email_address' : patient.email_address,
            'phone_number' : patient.phone_number,
            'date_of_birth' : patient.date_of_birth,
            'gender' : patient.gender
            }
            all_patients.append(pat)
    return jsonify({'patients': all_patients}), 200

@users_bp.route("/patients/<int:id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_patient(id):
    patient = Patients.query.get(id)
    if not patient:
        return jsonify({'msg': 'User does not exist'})
    try:
        data = request.get_json()
        print(data)
        patient.email_address = data.get('email_address', patient.email_address)
        #password = data.get('hashed_password')
        patient.first_name = data.get('first_name', patient.first_name)
        patient.last_name = data.get('last_name', patient.last_name)
        patient.other_name = data.get('other_name', patient.other_name)
        #dob_str = data.get('date_of_birth', patient.date_of_birth)
        patient.gender = data.get('gender', patient.gender)
        patient.phone_number = data.get('phone_number', patient.phone_number)
        #if password:
        #patient.hashed_password = generate_password_hash(password)
        #if dob_str:
        #patient.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()

        db.session.commit()
        return jsonify({'status' : 'Patient successfully updated'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred'}), 500


@users_bp.route("/doctors/<int:id>", methods=["GET"])
def get_doctor(id):
    doctor = Doctors.query.get(id)
    if doctor:
        return (
            jsonify({
                "id": doctor.id,
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "other_name": doctor.other_name,
                "date_of_birth": doctor.date_of_birth,
                "gender": doctor.gender,
                "phone_number": doctor.phone_number,
                "email_address": doctor.email_address,
                "hashed_password": doctor.hashed_password,
                "specialty": doctor.specialty
                }),
            200
        )
    return jsonify({"message": "Doctor not found"}), 404


@users_bp.route("/doctors", methods=["POST"])
def add_doctor():
    data = request.get_json()
    print(data)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    other_name = data.get("other_name")
    gender = data.get("gender")
    phone_number = data.get("phone_number")
    email_address = data.get("email_address")
    password = data.get("password")
    specialty = data.get("specialty")
    healthcare = data.get("healthcare_id")
    
    if "@" not in email_address:
            return jsonify({"error": "Invalid email address format"}), 400
    
    hashed_password = generate_password_hash(password)

    new_doctor = Doctors(first_name=first_name,
                          last_name= last_name, email_address=email_address,
                            other_name=other_name, gender=gender, 
                            phone_number=phone_number, specialty=specialty, 
                            hashed_password=hashed_password, healthcare_id=healthcare)

    try:
        db.session.add(new_doctor)
        db.session.commit()
        return jsonify({"message": "Doctor successfully added"}), 201
    except Exception as err:
        print(str(err))
        return jsonify({"message": "Failed to create doctor"}), 500


@users_bp.route("/doctors/<int:id>", methods=["PUT"])
@jwt_required()
def update_doctors(id): 
    doctor = Doctors.query.get(id)
    if not doctor:
        return jsonify({"message": "Doctor not found"}), 
    try:
        data = request.get_json()
        doctor.first_name = data.get("first_name", doctor.first_name)
        doctor.last_name = data.get("last_name", doctor.last_name)
        doctor.other_name = data.get("other_name", doctor.last_name)
        doctor.gender = data.get("gender", doctor.gender)
        doctor.phone_number = data.get("phone_number", doctor.phone_number)
        doctor.email_address = data.get("email_address", doctor.email_address)
        doctor.specialty = data.get("specialty", doctor.specialty)
        

        db.session.commit()
        return jsonify({"message": "Doctor updated successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": " an error occured"}), 500


@users_bp.route("/doctors/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_doctor(id):
    doctor = Doctors.query.get(id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"message": "Doctor removed successfully"}), 200
    else:
        return jsonify({"message": "Doctor not found"}), 404


@users_bp.route('/doctors', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_doctors():
    try:
        doctors = Doctors.query.all()
        all_doctors = []

        for doctor in doctors:
            doc = {
                    'first_name': doctor.first_name,
                    'last_name' : doctor.last_name,
                    'other_name': doctor.other_name,
                    'gender' : doctor.gender,
                    'phone_number' : doctor.phone_number,
                    'email_address' : doctor.email_address,
                    'specialty': doctor.specialty,
                    'healthcare_id' : doctor.healthcare_id
            }

            all_doctors.append(doc)

        return jsonify({'doctors' : all_doctors}), 200
    except Exception as e :
        print(e)
        abort(500)


@users_bp.route("/healthcares", methods=["POST"], strict_slashes=False)
def add_health():
    """
    Register a new patient
    """
    try:
        data = request.get_json()
        name = data.get("name")
        address = data.get('address')
        contact_number = data.get('contact_number')

        existing_healthcare = Healthcares.query.filter_by(name=name).first()
        if existing_healthcare:
            return jsonify({"error": "Healthcare entity with the same name already exists"}), 409  # 409 Conflict status

        new_healthcare = Healthcares(name=name, address=address, contact_number=contact_number)
                             
        db.session.add(new_healthcare)
        db.session.commit()

        return jsonify({'status' : 'Healthcare successfully added'}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "an error occured"}), 500

@users_bp.route("/healthcares/<int:id>", methods=['GET'], strict_slashes=False)
@jwt_required()
def get_healthcare(id):
    """
    Get a patient from the database
    """
    healthcare = Healthcares.query.get(id)
    if healthcare:
        return jsonify({
            'id': healthcare.id,
            'name' : healthcare.name,
            'address' : healthcare.address,
            'contact_number' : healthcare.contact_number,
            }), 200
    return jsonify({'error': 'Healthcare not found'})


@users_bp.route("/healthcares", methods=['GET'], strict_slashes=False)
@jwt_required()
def all_healthcares():
    healthcares = Healthcares.query.all()
    all_healthcares = []
    if healthcares:
        for healthcare in healthcares:
            health = {
            'name' : healthcare.name,
            'address' : healthcare.address,
            'contact_number' : healthcare.contact_number,
            }
            all_healthcares.append(health)
    return jsonify({'healthcare': all_healthcares}), 200

@users_bp.route("/healthcares/<int:id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_healthcare(id):
    healthcare = Healthcares.query.get(id)
    if not healthcare:
        return jsonify({'message': 'healthcare does not exist'})
    try:
        data = request.get_json()
        healthcare.name = data.get('name', healthcare.name)
        healthcare.address = data.get('address', healthcare.address)
        healthcare.contact_number = data.get('contact_number', healthcare.contact_number)

        db.session.commit()
        return jsonify({'status' : 'Healthcare successfully added'}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "an error occured"})


@users_bp.route("/healthcares/<int:id>", methods=["DELETE"])
@jwt_required()
def healthcare(id):
    healthcare = Healthcares.query.get(id)
    if healthcare:
        db.session.delete(healthcare)
        db.session.commit()
        return jsonify({"message": "Healthcare removed successfully"}), 200
    else:
        return jsonify({"message": "Healthcare not found"}), 404


@users_bp.route('/time-slots', methods=['GET'])
@jwt_required()
def get_time_slots():
    time_slots = TimeSlots.query.all()
    time_slots_data = [{
        'id': slot.id,
        'doctor_id': slot.doctor_id,
        'start_time': slot.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': slot.end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'day_of_the_week': slot.day_of_the_week,
    } for slot in time_slots]
    return jsonify(time_slots_data), 200


@users_bp.route("/time-slots", methods=["POST"])
@jwt_required()
def create_time_slot():
    data = request.get_json()
    
    # Parse start_time and end_time into datetime objects
    start_time_str = data.get("start_time")
    end_time_str = data.get("end_time")
    
    try:
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        return jsonify({"error": "Invalid datetime format"}), 400
    
    # Validate day_of_the_week
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_the_week = data.get("day_of_the_week")
    
    if day_of_the_week not in valid_days:
        return jsonify({"error": "Invalid day_of_the_week"}), 400
    
    doctor_id = data.get("doctor_id")
    
    try:
        time_slot = TimeSlots(doctor_id=doctor_id, start_time=start_time, end_time=end_time, day_of_the_week=day_of_the_week)
        db.session.add(time_slot)
        db.session.commit()
        return jsonify({"message": "Time slot created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create time slot"}), 500


@users_bp.route('/time-slots/<int:id>', methods=['PUT'])
@jwt_required()
def update_time_slot(id):
    data = request.get_json()
    
    # Parse start_time and end_time into datetime objects
    start_time_str = data.get("start_time")
    end_time_str = data.get("end_time")
    
    try:
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        return jsonify({"error": "Invalid datetime format"}), 400
    
    # Validate day_of_the_week
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_the_week = data.get("day_of_the_week")
    
    if day_of_the_week not in valid_days:
        return jsonify({"error": "Invalid day_of_the_week"}), 400
    
    doctor_id = data.get("doctor_id")
    
    try:
        time_slot = TimeSlots.query.get(id)
        if not time_slot:
            return jsonify({"error": "Time slot not found"}), 404
        
        time_slot.doctor_id = doctor_id
        time_slot.start_time = start_time
        time_slot.end_time = end_time
        time_slot.day_of_the_week = day_of_the_week
        
        db.session.commit()
        
        return jsonify({"message": "Time slot updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update time slot"}), 500


@users_bp.route('/time-slots/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_time_slot(id):
    time_slot = TimeSlots.query.get(id)
    if not time_slot:
        return jsonify({'message': 'Time slot not found'}), 404

    try:
        db.session.delete(time_slot)
        db.session.commit()
        return jsonify({'message': 'Time slot deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete time slot'}), 500
