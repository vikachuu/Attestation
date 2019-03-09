from web import db


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

    personnel_number = db.Column(db.Integer, db.ForeignKey('teacher.personnel_number', onupdate="CASCADE",
                                                           ondelete="NO ACTION"), nullable=False)
    teacher = db.relationship("Teacher", back_populates="attestation")
