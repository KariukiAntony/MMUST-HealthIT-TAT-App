from flask import Blueprint, request, jsonify, make_response
from .models import Result
from .utils import add_result, all_results
from . import db
from .sms import send_sms
import re


main = Blueprint('main', __name__)


@main.route('/hae')
def index():
    return "<p>Hello World<p/>"


@main.route('/tests', methods=['POST', 'GET'])
def tests():
    if request.method == "POST":
        data = request.json
        required_fields = ['patient_name', 'patient_phone']


        if all(field in data for field in required_fields):
            patient_name = data.get('patient_name')
            patient_phone = data.get('patient_phone')
            # Validate result params
            if not re.match("^\w+$", patient_name):
                return "Invalid value on name parameter", 400
            if not re.match("^(07|01)\d{8}$", patient_phone):
                return "Invalid phone number", 400
            # TODO: Implement data persistency to db
            add_result(patient_phone, patient_name)

            # add_result(patient_phone, patient_name)
            message = f"Hello {patient_name} your test results are available input 1 to confirm collection"
            send_sms("+254798589847", message)
            return "Data successfully stored in database", 201
        else:
            # Required fields are missing, return an error response
            return "Missing required fields: {}".format(", ".join(set(required_fields) - set(data))), 400

    if request.method == "GET":
        results = all_results()

        serialized = []
        for result in results:
            serialized.append({
                'id': result.id,
                'name': result.patient_name,
                'description': result.patient_phone
            })
        return jsonify(serialized)



