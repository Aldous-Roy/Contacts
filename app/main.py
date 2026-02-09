from flask import request,jsonify
from config import app,db
from model import Contact

@app.route("/",methods=["GET"])
def test_server():
    return("server is running in port 8000")

@app.route("/contacts",methods=["GET"])
def get_contacts():
    contacts=Contact.query.all()
    return jsonify([contact.to_json() for contact in contacts])

@app.route("/contacts",methods=["POST"])
def create_contact():
    first_name=request.json.get("firstName")
    last_name=request.json.get("lastName")
    email=request.json.get("email")
    contact=Contact(first_name=first_name,last_name=last_name,email=email)
    db.session.add(contact)
    db.session.commit()
    return jsonify(contact.to_json()),201

@app.route("/contacts/<int:id>",methods=["PUT"])
def update_contact(id):
    contact=Contact.query.get(id)
    if not contact:
        return jsonify({"message":"Contact not found"}),404
    contact.first_name=request.json.get("firstName")
    contact.last_name=request.json.get("lastName")
    contact.email=request.json.get("email")
    db.session.commit()
    return jsonify(contact.to_json()),200

@app.route("/contacts/<int:id>",methods=["DELETE"])
def delete_contact(id):
    contact=Contact.query.get(id)
    if not contact:
        return jsonify({"message":"Contact not found"}),404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message":"Contact deleted"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000, debug=False)