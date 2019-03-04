from web import db


class Teacher(db.Model):
    __tablename__ = "teacher"

    teacher_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(100))

    def __init__(self, teacher_id, last_name):
        self.teacher_id = teacher_id
        self.last_name = last_name
