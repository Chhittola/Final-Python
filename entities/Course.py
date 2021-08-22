from sqlalchemy import ForeignKey
from sqlalchemy.orm import join

from configuretion import *
from entities.Teacher import Teacher


class Course(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    limit_student = db.Column(db.INTEGER)
    teacher_id = db.Column(db.INTEGER, ForeignKey("teacher.id"))
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.INTEGER, ForeignKey("users.id"))

    @app.route("/course", methods=["POST"])
    def create_course():
        request_data = request.get_json()
        teacher_id = request_data['teacher_id']
        teacher = Teacher.find_by_id(teacher_id)
        if not teacher:
            return json.jsonify({"message": f"Teacher id {teacher_id} not found"}), 401
        course = Course()
        course.name = request_data['name']
        course.start_date = request_data['start_date']
        course.end_date = request_data['end_date']
        course.price = request_data['price']
        course.limit_student = request_data['limit_student']
        course.teacher_id = teacher_id
        course.created_at = datetime.now()
        course.user_id = request_data['user_id']
        db.session.add(course)
        db.session.commit()
        return json.jsonify({"message": f"Course {course.name} has been created successfully"}), 200

    @app.route("/course", methods=["GET"])
    def get_all_course():
        courses = Course.query.all()
        results = []
        for col in courses:
            course = {
                'id': col.id,
                'name': col.name,
                'start_date': col.start_date.strftime('%Y-%m-%d'),
                'end_date': col.end_date.strftime('%Y-%m-%d'),
                'price': col.price,
                'limit_student': col.limit_student,
                'teacher_id': col.teacher_id,
                'created_at': col.created_at
            }
            results.append(course)
        return jsonify(results), 200

    @app.route("/course", methods=["PUT"])
    def update_course():
        request_data = request.get_json()
        course_id = request_data['id']
        teacher_id = request_data['teacher_id']
        courses = Course.query.filter_by(id=course_id).first()
        if not courses:
            return json.jsonify({"message": f"Course id {course_id} not found"}), 401
        courses.name = request_data['name']
        courses.start_date = request_data['start_date']
        courses.end_date = request_data['end_date']
        courses.price = request_data['price']
        courses.limit_student = request_data['limit_student']
        courses.teacher_id = teacher_id
        db.session.add(courses)
        db.session.commit()
        return jsonify({"message": "Updated"}), 200

    @app.route("/course/<id>", methods=["DELETE"])
    def delete_course(id):
        courses = Course.query.filter_by(id=id).first()
        if not courses:
            return json.jsonify({"message": f"Course id {id} not found"}), 401
        db.session.delete(courses)
        db.session.commit()
        return jsonify({"message": "deleted"}), 200
