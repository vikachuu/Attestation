import enum
from datetime import datetime
from web import db


class CATEGORY(enum.Enum):  # TODO: change enum
    SPEC = "спеціаліст"
    SPEC_1 = "спеціаліст першої категорії"
    SPEC_2 = "спеціаліст другої категорії"
    SPEC_HIGH = "спеціаліст вищої категорії"


class RANK(enum.Enum):  # TODO: change enum
    RANK1 = "учитель-методист"
    RANK2 = "педагог-організатор-методист"
    RANK3 = "практичний психолог-методист"
    RANK4 = "керівник гуртка-методист"
    RANK5 = "старший учитель"


class Teacher(db.Model):
    __tablename__ = "teacher"

    personnel_number = db.Column(db.Integer, primary_key=True)
    employment_history = db.Column(db.Integer, nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    middle_name = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    educational_institution = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    accreditation_level = db.Column(db.String(50), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=True)
    position = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)

    qualification_category = db.Column(db.String(50), nullable=False)
    rank = db.Column(db.String(50), nullable=True)
    previous_attestation_date = db.Column(db.Integer, nullable=False)
    next_attestation_date = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String(100), nullable=True)
    avatar_url = db.Column(db.String(1000), nullable=True)

    user = db.relationship("User", back_populates="teacher", uselist=False)
    attestation = db.relationship("Attestation", back_populates="teacher")
    teacher_subject = db.relationship("TeacherSubject", back_populates="teacher")

    extra_application = db.relationship("ExtraApplication", back_populates="teacher")
    deferment_application = db.relationship("DefermentApplication", back_populates="teacher")

    # referral_to_courses = db.relationship("ReferralToCourses", back_populates="teacher")

    def __init__(self, personnel_number, employment_history, surname, name, middle_name, birth_date,
                 educational_institution, specialty, accreditation_level, graduation_year, position, experience,
                 qualification_category, rank, previous_attestation_date, next_attestation_date, degree, avatar_url):
        self.personnel_number = personnel_number
        self.employment_history = employment_history
        self.surname = surname
        self.name = name
        self.middle_name = middle_name
        self.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()

        self.educational_institution = educational_institution
        self.specialty = specialty
        self.accreditation_level = accreditation_level
        self.graduation_year = graduation_year
        self.position = position
        self.experience = experience

        self.qualification_category = CATEGORY[qualification_category].value if qualification_category else None
        self.rank = RANK[rank].value if rank else None
        self.previous_attestation_date = datetime.strptime(previous_attestation_date, '%Y').year
        self.next_attestation_date = datetime.strptime(next_attestation_date, '%Y').year
        self.degree = degree
        self.avatar_url = avatar_url
