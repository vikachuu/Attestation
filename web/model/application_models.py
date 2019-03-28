import enum
from datetime import datetime
from web import db


class STATUS(enum.Enum):  # TODO: change enum
    IN_PROGRESS = "на розгляді"
    CONFIRMED = "підтверджено"
    REJECTED = "відхилено"


class ExtraApplication(db.Model):
    __tablename__ = "extra_application"

    extra_application_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    extra_application_date = db.Column(db.Date, nullable=False)
    extra_application_reason = db.Column(db.String(1500), nullable=False)
    extra_application_status = db.Column(db.String(50), nullable=False)

    teacher_position = db.Column(db.String(100), nullable=False)
    teacher_pib = db.Column(db.String(100), nullable=False)

    personnel_number = db.Column(db.Integer, db.ForeignKey('teacher.personnel_number', onupdate="CASCADE",
                                                           ondelete="CASCADE"), nullable=False)
    teacher = db.relationship("Teacher", back_populates="extra_application")

    def __init__(self, extra_application_reason, extra_application_date, extra_application_status, teacher_position,
                 teacher_pib, personnel_number):
        self.extra_application_date = datetime.strptime(extra_application_date, '%Y-%m-%d').date()
        self.extra_application_reason = extra_application_reason
        self.extra_application_status = STATUS[extra_application_status].value

        self.teacher_position = teacher_position
        self.teacher_pib = teacher_pib

        self.personnel_number = personnel_number


class DefermentApplication(db.Model):
    __tablename__ = "deferment_application"

    deferment_application_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deferment_application_date = db.Column(db.Date, nullable=False)
    deferment_application_reason = db.Column(db.String(1500), nullable=False)
    deferment_application_years = db.Column(db.Integer, nullable=False)
    deferment_application_status = db.Column(db.String(50), nullable=False)

    teacher_position = db.Column(db.String(100), nullable=False)
    teacher_pib = db.Column(db.String(100), nullable=False)

    personnel_number = db.Column(db.Integer, db.ForeignKey('teacher.personnel_number', onupdate="CASCADE",
                                                           ondelete="CASCADE"), nullable=False)
    teacher = db.relationship("Teacher", back_populates="deferment_application")

    def __init__(self, deferment_application_date, deferment_application_reason, deferment_application_years,
                 deferment_application_status,  teacher_position, teacher_pib,  personnel_number):
        self.deferment_application_date = datetime.strptime(deferment_application_date, '%Y-%m-%d').date()
        self.deferment_application_reason = deferment_application_reason
        self.deferment_application_years = deferment_application_years
        self.deferment_application_status = STATUS[deferment_application_status].value

        self.teacher_position = teacher_position
        self.teacher_pib = teacher_pib

        self.personnel_number = personnel_number
