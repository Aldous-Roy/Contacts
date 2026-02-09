from flask import request, jsonify
from config import app, db
from model import Contact
from sqlalchemy.exc import IntegrityError

def validate_contact_data(data):
    required_fields = ("firstName", "lastName", "email")
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400
    return True


@app.route("/", methods=["GET"])
def test_server():
    return jsonify({"message": "Server is running on port 8000"}), 200


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "GET":
        contacts = Contact.query.all()
        return jsonify([contact.to_json() for contact in contacts]), 200

    # POST
    data = request.get_json()
    if not validate_contact_data(data):
        return jsonify({"message": "Invalid JSON body"}), 400

    contact = Contact(
        first_name=data["firstName"],
        last_name=data["lastName"],
        email=data["email"]
    )

    try:
        db.session.add(contact)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email already exists"}), 409

    return jsonify(contact.to_json()), 201


@app.route("/contacts/<int:id>", methods=["GET", "PUT", "DELETE"])
def contact_by_id(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    if request.method == "GET":
        return jsonify(contact.to_json()), 200

    if request.method == "PUT":
        data = request.get_json()
        if not  validate_contact_data(data):
            return jsonify({"message": "Invalid JSON body"}), 400

        contact.first_name = data.get("firstName", contact.first_name)
        contact.last_name = data.get("lastName", contact.last_name)
        contact.email = data.get("email", contact.email)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Email already exists"}), 409

        return jsonify(contact.to_json()), 200

    # DELETE
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=8000, debug=False)