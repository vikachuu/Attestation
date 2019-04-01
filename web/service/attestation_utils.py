from flask import jsonify
from sqlalchemy import desc, asc
from datetime import datetime
from web import db
from web.model.attestation_model import Attestation
from web.service.teacher_utils import TeacherUtils
from web.service.utils import requires_access_level


class AttestationUtils:

    @staticmethod
    @requires_access_level(2)
    def create_attestation(data, token):
        attestation = Attestation.query.filter_by(personnel_number=data.get('personnel_number')).\
            order_by(asc(Attestation.attestation_date)).first()
        if not attestation or attestation.attestation_date.year != datetime.now().year:
            personnel_number = data.get('personnel_number')
            if personnel_number and TeacherUtils.if_teacher_exists(personnel_number):
                attestation = Attestation(
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
                'message': 'Attestation for this year already exists.',
            }
            return response_object, 400

    @staticmethod
    def get_all_attestations_with_teachers(year):
        sql = """
        SELECT A.attestation_number, A.attestation_date, A.attestation_letter, A.characteristic, A.category_conclusion, 
        A.rank_conclusion, A.on_category, A.on_rank, A.previous_category, A.previous_rank, A.personnel_number, 
        T.surname, T.name
        FROM attestation AS A 
        INNER JOIN teacher AS T ON T.personnel_number = A.personnel_number
        WHERE (%s IS NULL OR date_part('year', attestation_date) = %s)
        ORDER BY A.attestation_date DESC;
        """
        result = db.engine.execute(sql, (year, year))
        return jsonify([dict(row) for row in result])
