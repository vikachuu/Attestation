from web import db
from web.model.attestation_model import Attestation
from web.service.teacher_utils import TeacherUtils
from web.service.utils import requires_access_level


class AttestationUtils:

    @staticmethod
    @requires_access_level(2)
    def create_attestation(data, token):
        attestation = Attestation.query.filter_by(attestation_number=data.get('attestation_number')).first()
        if not attestation:
            personnel_number = data.get('personnel_number')
            if personnel_number and TeacherUtils.if_teacher_exists(personnel_number):
                attestation = Attestation(
                    attestation_number=data.get('attestation_number'),
                    attestation_date=data.get('attestation_date'),
                    attestation_letter=data.get('attestation_letter'),
                    characteristic=data.get('characteristic'),

                    category_conclusion=data.get('category_conclusion'),
                    rank_conclusion=data.get('rank_conclusion'),
                    on_category=data.get('on_category'),
                    on_rank=data.get('on_rank'),

                    personnel_number=data.get('personnel_number')
                )
                db.session.add(attestation)
                db.session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully created attestation'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'No such teacher for attestation exists',
                }
                return response_object, 400
        else:
            response_object = {
                'status': 'fail',
                'message': 'Attestation already exists.',
            }
            return response_object, 400
