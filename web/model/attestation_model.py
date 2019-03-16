from datetime import datetime

from web import db
from web.model.teacher_model import CATEGORY, RANK
from web.service.teacher_utils import TeacherUtils


class Attestation(db.Model):
    __tablename__ = "attestation"

    attestation_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attestation_date = db.Column(db.Date, nullable=False)
    attestation_letter = db.Column(db.String(1000), nullable=False)  # url to file
    characteristic = db.Column(db.String(1000), nullable=False)  # url to file

    category_conclusion = db.Column(db.String(250), nullable=False)
    rank_conclusion = db.Column(db.String(250), nullable=True)
    on_category = db.Column(db.String(250), nullable=False)
    on_rank = db.Column(db.String(250), nullable=True)
    previous_category = db.Column(db.String(250), nullable=False)
    previous_rank = db.Column(db.String(250), nullable=True)

    personnel_number = db.Column(db.Integer, db.ForeignKey('teacher.personnel_number', onupdate="CASCADE",
                                                           ondelete="NO ACTION"), nullable=False)
    teacher = db.relationship("Teacher", back_populates="attestation")

    def __init__(self, attestation_date, attestation_letter, characteristic, category_conclusion,
                 rank_conclusion, on_category, on_rank, personnel_number):
        self.attestation_date = datetime.strptime(attestation_date, '%Y-%m-%d').date()
        self.attestation_letter = attestation_letter
        self.characteristic = characteristic

        self.category_conclusion = CATEGORY[category_conclusion].value
        self.rank_conclusion = RANK[rank_conclusion].value if rank_conclusion else None
        self.on_category = CATEGORY[on_category].value
        self.on_rank = RANK[on_rank].value if on_rank else None
        self.previous_category = TeacherUtils.get_category_by_personnel_number(self.personnel_number)
        self.previous_rank = TeacherUtils.get_rank_by_personnel_number(self.personnel_number)

        self.personnel_number = personnel_number
