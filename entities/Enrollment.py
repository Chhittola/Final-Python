from sqlalchemy import ForeignKey
from sqlalchemy.orm import lazyload, joinedload

from configuretion import *


class Enrollment(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    student_id = db.Column(db.INTEGER, ForeignKey("student.id"))
    course_id = db.Column(db.INTEGER, ForeignKey("course.id"))
    payment = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.INTEGER, ForeignKey("users.id"))

    @app.route("/enrollment", methods=["POST"])
    def create_enrollment():
        request_data = request.get_json()
        enrollment = Enrollment()
        enrollment.student_id = request_data['student_id']
        enrollment.course_id = request_data['course_id']
        enrollment.payment = request_data['payment']
        enrollment.created_at = datetime.now()
        enrollment.user_id = request_data['user_id']
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({"message": "Created successfully"}), 200

    @app.route("/enrollment", methods=["GET"])
    def get_all_enrollment():
        results = Enrollment.query.all()
        for col in results:
            print(col)
        return jsonify({"message": "ok"})
