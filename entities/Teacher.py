import bdb

from sqlalchemy import ForeignKey

from configuretion import *


class Teacher(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.INTEGER, ForeignKey("users.id"))

    @app.route("/teacher", methods=["POST"])
    def create_teacher():
        request_data = request.get_json()
        teacher = Teacher()
        teacher.first_name = request_data['first_name']
        teacher.last_name = request_data['last_name']
        teacher.address = request_data['address']
        teacher.contact = request_data['contact']
        teacher.email = request_data['email']
        teacher.created_at = datetime.now()
        teacher.user_id = request_data['user_id']
        db.session.add(teacher)
        db.session.commit()
        return jsonify({"message": "Teacher created successfully"}), 200

    @app.route("/teacher", methods=["GET"])
    def get_all_teacher():
        teachers = Teacher.query.all()
        results = []
        for col in teachers:
            user = {
                'id': col.id,
                'first_name': col.first_name,
                'last_name': col.last_name,
                'address': col.address,
                'contact': col.contact,
                'email': col.email,
                'createdAt': col.created_at
            }
            results.append(user)
        return jsonify(results)

    @app.route("/teacher/<id>", methods=["PUT"])
    def update_teacher(id):
        request_data = request.get_json()
        teacher = Teacher.query.filter_by(id=id).first()
        if not teacher:
            return jsonify({"message": f"id {id} not found"}), 401
        teacher.first_name = request_data['first_name']
        teacher.last_name = request_data['last_name']
        teacher.address = request_data['address']
        teacher.contact = request_data['contact']
        teacher.email = request_data['email']
        db.session.add(teacher)
        db.session.commit()
        return jsonify({"message": "updated successfully"}), 202

    @app.route("/teacher/<id>", methods=["DELETE"])
    def delete_teacher(id):
        teacher = Teacher.query.filter_by(id=id).first()
        if not teacher:
            return jsonify({"message": f"id {id} not found"}), 401
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({"message": "deleted successfully"}), 202

    @staticmethod
    @app.route("/teacher/<id>", methods=["GET"])
    def find_by_id(id):
        teacher = Teacher.query.filter_by(id=id)
        if not teacher:
            return jsonify({"message": f"id {id} not found"}), 401
        result = []
        for col in teacher:
            teacher_dict = {}
            teacher_dict["id"] = col.id,
            teacher_dict["first_name"] = col.first_name,
            teacher_dict["last_name"] = col.last_name,
            teacher_dict["address"] = col.address,
            teacher_dict["contact"] = col.contact,
            teacher_dict["email"] = col.email,
            teacher_dict["createdAt"] = col.created_at
            result.append(teacher_dict)
        return json.dumps(result), 200
