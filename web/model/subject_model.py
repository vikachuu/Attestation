from web import db


class Subject(db.Model):
    __tablename__ = "subject"

    subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)

    teacher_subject = db.relationship("TeacherSubject", back_populates="subject")

    def __init__(self, subject_name, department):
        self.subject_name = subject_name
        self.department = department


class TeacherSubject(db.Model):
    __tablename__ = "teacher_subject"

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id ', onupdate="CASCADE",
                                                     ondelete="NO ACTION"), primary_key=True)
    personnel_number = db.Column(db.Integer, db.ForeignKey('teacher.personnel_number', onupdate="CASCADE",
                                                           ondelete="CASCADE"), primary_key=True)

    teacher = db.relationship("Teacher", back_populates="teacher_subject")
    subject = db.relationship("Subject", back_populates="teacher_subject")

    def __init__(self, subject_id, personnel_number):
        self.subject_id = subject_id
        self.personnel_number = personnel_number
