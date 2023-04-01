from . import db
from .models import Result

def add_result(phone: str, name: str):
    new_result = Result(patient_name=name, patient_phone=phone, result_status=0)
    db.session.add(new_result)
    db.session.commit()


def all_results():
    return Result.query.all()