from web import db
from datetime import datetime


class ReferralToCourses(db.Model):
    __tablename__ = "referral_to_courses"

    referral_number = db.Column(db.Integer, primary_key=True)
    proff_course_start_date = db.Column(db.Date, nullable=False)
    proff_course_end_date = db.Column(db.Date, nullable=False)
    sertificate = db.Column(db.Boolean, nullable=False)

    personnel_number = db.Column(db.Integer, db.ForeignKey('teacher.personnel_number', onupdate="CASCADE",
                                                           ondelete="CASCADE"), nullable=False)
    teacher = db.relationship("Teacher", back_populates="referral_to_courses")

    selective_course_date = db.relationship("SelectiveCourseDate", back_populates="referral_to_courses")

    def __init__(self, referral_number, proff_course_start_date, proff_course_end_date, sertificate,
                 personnel_number):
        self.referral_number = referral_number
        self.proff_course_start_date = datetime.strptime(proff_course_start_date, '%Y-%m-%d').date()
        self.proff_course_end_date = datetime.strptime(proff_course_end_date, '%Y-%m-%d').date()
        self.sertificate = sertificate if sertificate else False

        self.personnel_number = personnel_number


class SelectiveCourseDate(db.Model):
    __tablename__ = "selective_course_date"

    date_of_course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_of_course = db.Column(db.Date, nullable=False)

    referral_number = db.Column(db.Integer, db.ForeignKey('referral_to_courses.referral_number', onupdate="CASCADE",
                                                          ondelete="CASCADE"), nullable=False)
    referral_to_courses = db.relationship("ReferralToCourses", back_populates="selective_course_date")

    def __init__(self, date_of_course, referral_number):
        self.date_of_course = datetime.strptime(date_of_course, '%Y-%m-%d').date()
        self.referral_number = referral_number
