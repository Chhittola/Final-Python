from sqlalchemy import ForeignKey

from configuretion import *


class Student(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    email = db.Column(db.String(100))
    dob = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.INTEGER, ForeignKey("users.id"))

    @app.route("/student", methods=["POST"])
    def create_student():
        request_data = request.get_json()
        student = Student()
        student.first_name = request_data['first_name']
        student.last_name = request_data['last_name']
        student.address = request_data['address']
        student.contact = request_data['contact']
        student.email = request_data['email']
        student.dob = request_data['dob']
        student.user_id = request_data['user_id']
        student.created_at = datetime.now()
        db.session.add(student)
        db.session.commit()
        return jsonify({"message": "Student Create Successfully"}), 200

    @app.route("/student", methods=["PUT"])
    def edit_student():
        request_data = request.get_json()
        student_id = request_data['id']
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return jsonify({"message": f"Student id {student_id} not found"}), 404
        student.first_name = request_data['first_name']
        student.last_name = request_data['last_name']
        student.address = request_data['address']
        student.contact = request_data['contact']
        student.email = request_data['email']
        student.dob = request_data['dob']
        db.session.add(student)
        db.session.commit()
        return jsonify({"message": "Student Create Successfully"}), 200

    @app.route("/student", methods=["GET"])
    def get_all_student():
        students = Student.query.all()
        results = []
        for col in students:
            student = {
                'id': col.id,
                'first_name': col.first_name,
                'last_name': col.last_name,
                'address': col.address,
                'contact': col.contact,
                'email': col.email,
                'dob': col.dob.strftime('%d-%m-%Y'),
                'create_at': col.created_at
            }
            results.append(student)
        return jsonify(results), 200

    @app.route("/student/<id>", methods=["DELETE"])
    def delete_student(id):
        student = Student.query.filter_by(id=id).first()
        if not student:
            return jsonify({"message": f"Student id {id} not found"}), 404
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"Delete successfully"}), 200
