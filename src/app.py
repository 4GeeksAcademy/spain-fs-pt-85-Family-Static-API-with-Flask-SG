"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    try:
        return jsonify(jackson_family.get_all_members()), 200
    except Exception:
        return jsonify({"Error": "Bad request"}), 400

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"Error": "Member not found"}), 404

@app.route('/member/', methods=['POST'])
def add_member():

    # this is how you can use the Family datastructure by calling its methods
    new_member = request.get_json()
    if not new_member.get("first_name") or not new_member.get("age") or not new_member.get("lucky_numbers"):
        return jsonify({"Error": "Missing required fields"}), 400
    
    jackson_family.add_member(new_member)
    return jsonify(new_member), 201

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    if jackson_family.delete_member(member_id):
        return jsonify({"Done": True}), 200
    return jsonify({"Error": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
