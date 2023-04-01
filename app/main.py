from flask import Blueprint, request, jsonify
from .models import Result
from . import db
import re


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return "<p>Hello World</>"


@main.route('/tests', methods=['POST'])
def tests():
    data = request.json
    required_fields = ['patient_name', 'patient_phone']

    if all(field in data for field in required_fields):
        patient_name = data.get('patient_name')
        patient_phone = data.get('patient_phone')
        result_status = 0
        # Validate result params
        if not re.match("^\w+$", patient_name):
            return "Invalid value on name parameter", 400
        if not re.match("^(07|01)\d{8}$", patient_phone):
            return "Invalid phone number", 400
        # TODO: Implement data persistency to db
        # new_result = Result(patient_name=patient_name, patient_phone=patient_phone, result_status=result_status)
        # db.add(new_result)
        # db.commit()
        return "success", 201
    else:
        # Required fields are missing, return an error response
        return "Missing required fields: {}".format(", ".join(set(required_fields) - set(data))), 400
