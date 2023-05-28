import uuid
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.types.password import PasswordType


Base = declarative_base()


class VacancyPriorityRef(Base):
    __tablename__ = 'vacancy_priorities_ref'
    
    code = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String, nullable=False)
    is_archive = sa.Column(sa.Boolean, default=False, nullable=False)
    
    
class AdressRef(Base):
    __tablename__ = 'adresses_ref'

    code = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String, nullable=False)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey('adresses_ref.code'))
    is_archive = sa.Column(sa.Boolean, default=False, nullable=False)
    
    parent = relationship('AdressRef',)
    
    
class CountryRef(Base):
    __tablename__ = 'countries_ref'
    
    code = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String, nullable=False)
    is_archive = sa.Column(sa.Boolean, default=False, nullable=False)
    
    
class FamilyStatusRef(Base):
    __tablename__ = 'family_stats_ref'
    
    code = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String, nullable=False)
    is_archive = sa.Column(sa.Boolean, default=False, nullable=False)
    

class ContactTypeRef(Base):
    __tablename__ = 'contact_types_ref'
    
    code = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String, nullable=False)
    is_archive = sa.Column(sa.Boolean, default=False, nullable=False)


class LanguageRef(Base):
    __tablename__ = 'languages_ref'
    
    code = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String, nullable=False)
    is_archive = sa.Column(sa.Boolean, default=False, nullable=False)


class LanguageLevelRef(Base):
    __tablename__ = 'language_levels_ref'
    
    code = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String, nullable=False)
    level_code = sa.Column(sa.String, nullable=False)
    is_archive = sa.Column(sa.Boolean, default=False, nullable=False)
    
    
class InterviewStageRef(Base):
    __tablename__ = 'interview_stages_ref'

    code = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String, nullable=False)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey('interview_stages_ref.code'))
    is_archive = sa.Column(sa.Boolean, default=False, nullable=False)
    
    parent = relationship('InterviewStageRef',)


class RoleRef(Base):
    __tablename__ = 'roles_ref'
    
    code = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    sys_name = sa.Column(sa.String, nullable=False)
    
    # users = relationship('User', backref='role')


class VacansyStatusRef(Base):
    __tablename__ = 'vacancy_stats_ref'
    
    code = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.String, nullable=False)
    is_archive = sa.Column(sa.Boolean, default=False, nullable=False)


# Tables ------------------------------------------------------


class Company(Base):
    __tablename__ = 'companies'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    full_name = sa.Column(sa.String, nullable=False)
    short_name = sa.Column(sa.String, nullable=False)
    ogrn = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)


class Department(Base):
    __tablename__ = 'departments'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    name = sa.Column(sa.String, nullable=False)
    company_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=False)
    
    company = relationship('Company', lazy='selectin')
    

class Position(Base):
    __tablename__ = 'positions'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    name = sa.Column(sa.String, nullable=False)
    company_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=False)
    
    company = relationship('Company', lazy='selectin')    

    
class Grade(Base):
    __tablename__ = 'grades'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    name = sa.Column(sa.String, nullable=False)
    company_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=False)
    
    company = relationship('Company', lazy='selectin')
    
    
class User(Base):
    __tablename__ = 'users'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    username = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    role_code = sa.Column(sa.Integer, sa.ForeignKey('roles_ref.code'), nullable=False)
    company_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=False)
    department_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('departments.id'))
    position_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('positions.id'))
    grade_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('grades.id'))
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    middle_name = sa.Column(sa.String)
    email = sa.Column(sa.String, nullable=False)
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    logged_in_at = sa.Column(sa.DateTime)
    
    role = relationship('RoleRef', lazy='selectin')
    company = relationship('Company', lazy='selectin')
    department = relationship('Department', lazy='selectin')
    position = relationship('Position', lazy='selectin')
    grade = relationship('Grade', lazy='selectin')
    creator = relationship('User', lazy='selectin')
    
    
class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    
    token = sa.Column(UUID(as_uuid=True), primary_key=True)
    expires_at = sa.Column(sa.DateTime, nullable=False)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    
    user = relationship('User', lazy='selectin')
    
    
class Skill(Base):
    __tablename__ = 'skills'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    name = sa.Column(sa.String, nullable=False)
    normalized_name = sa.Column(sa.String, nullable=False, unique=True)
    company_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=False)
    
    company = relationship('Company', lazy='selectin')
    
    
class DepartmentSkill(Base):
    __tablename__ = 'department_skills'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    skill_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('skills.id'), nullable=False)
    department_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('departments.id'), nullable=False)
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    skill = relationship('Skill', lazy='selectin')
    department = relationship('Department', lazy='selectin')
    creator = relationship('User', lazy='selectin')
    
    
class Vacancy(Base):
    __tablename__ = 'vacancies'
    __table_args__ = (
        sa.CheckConstraint("salary_from > 0 AND salary_from <= salary_to"),
        sa.CheckConstraint("employee_count >= 0 AND employee_count <= 1000"),
        )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    position_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('positions.id'), nullable=False)
    department_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('departments.id'), nullable=False)
    grade_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('grades.id'))
    salary_from = sa.Column(sa.Integer)
    salary_to = sa.Column(sa.Integer)
    employee_count = sa.Column(sa.Integer)
    priority_code = sa.Column(sa.Integer, sa.ForeignKey('vacancy_priorities_ref.code'), nullable=False)
    deadline = sa.Column(sa.Date)
    company_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=False)
    recruiter_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    status_code = sa.Column(sa.Integer, sa.ForeignKey('vacancy_stats_ref.code'))
    adress_code = sa.Column(sa.Integer, sa.ForeignKey('adresses_ref.code'))
    project = sa.Column(sa.String)
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    department = relationship('Department', lazy='selectin')
    position = relationship('Position', lazy='selectin')
    grade = relationship('Grade', lazy='selectin')
    priority = relationship('VacancyPriorityRef', lazy='selectin')
    adress = relationship('AdressRef', lazy='selectin')
    status = relationship('VacansyStatusRef', lazy='selectin')
    skills = relationship('VacancySkill', lazy='selectin')
    # recruiter = relationship('User', primaryjoin = 'Vacancy.recruiter_id == User.id')
    creator = relationship('User', primaryjoin = 'Vacancy.creator_id == User.id')
    
    
class VacancySkill(Base):
    __tablename__ = 'vacancy_skills'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    skill_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('skills.id'), nullable=False)
    vacancy_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('vacancies.id'), nullable=False)
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    skill = relationship('Skill', lazy='selectin')
    creator = relationship('User', lazy='selectin')
    
    
class File(Base):
    __tablename__ = 'files'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    name = sa.Column(sa.String, nullable=False)
    size = sa.Column(sa.Float(6, 2), nullable=False)
    entity_name = sa.Column(sa.String, nullable=False)
    entity_id = sa.Column(UUID(as_uuid=True), nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)


class Candidate(Base):
    __tablename__ = 'candidates'
    __table_args__ = (
        sa.CheckConstraint("first_name ~ '^([А-я]|-)*$'"),
        sa.CheckConstraint("last_name ~ '^([А-я]|-)*$'"),
        sa.CheckConstraint("middle_name ~ '^([А-я]|-)*$'"),
        sa.CheckConstraint("min_salary > 0"),
        )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    position_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('positions.id'), nullable=False)
    grade_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('grades.id'), nullable=False)
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    middle_name = sa.Column(sa.String)
    birth_date = sa.Column(sa.Date)
    min_salary = sa.Column(sa.Integer)
    adress_code = sa.Column(sa.Integer, sa.ForeignKey('adresses_ref.code'))
    citizenship_code = sa.Column(sa.Integer, sa.ForeignKey('countries_ref.code'))
    family_status_code = sa.Column(sa.Integer, sa.ForeignKey('family_stats_ref.code'))
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    position = relationship('Position', lazy='selectin')
    grade = relationship('Grade', lazy='selectin')
    adress = relationship('AdressRef', lazy='selectin')
    citizenship = relationship('CountryRef', lazy='selectin')
    family_status = relationship('FamilyStatusRef', lazy='selectin')
    contacts = relationship('CandidateContact', lazy='selectin')
    languages = relationship('CandidateLanguageAbility', lazy='selectin')
    notes = relationship('CandidateNote', lazy='selectin')
    skills = relationship('CandidateSkill', lazy='selectin')
    work_places = relationship('CandidateWorkPlace', lazy='selectin')
    creator = relationship('User', lazy='selectin')
    
    
class CandidateContact(Base):
    __tablename__ = 'candidate_contacts'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    candidate_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('candidates.id'), nullable=False)
    type_code = sa.Column(sa.Integer, sa.ForeignKey('contact_types_ref.code'), nullable=False)
    value = sa.Column(sa.String)
    is_priority = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)    
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    type = relationship('ContactTypeRef', lazy='selectin')
    creator = relationship('User', lazy='selectin')


class CandidateWorkPlace(Base):
    __tablename__ = 'candidate_work_places'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    candidate_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('candidates.id'), nullable=False)
    position = sa.Column(sa.String, nullable=False)
    company = sa.Column(sa.String, nullable=False)
    work_from = sa.Column(sa.Date, nullable=False)
    work_to = sa.Column(sa.Date)
    is_actual = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)    
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    creator = relationship('User', lazy='selectin')


class CandidateLanguageAbility(Base):
    __tablename__ = 'candidate_language_ability'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    candidate_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('candidates.id'), nullable=False)
    language_code = sa.Column(sa.Integer, sa.ForeignKey('languages_ref.code'), nullable=False)
    language_level_code = sa.Column(sa.Integer, sa.ForeignKey('language_levels_ref.code'), nullable=False)    
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    language = relationship('LanguageRef', lazy="selectin")
    language_level = relationship('LanguageLevelRef', lazy="selectin")
    creator = relationship('User', lazy='selectin')


class CandidateNote(Base):
    __tablename__ = 'candidate_notes'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    candidate_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('candidates.id'), nullable=False)
    note = sa.Column(sa.String, nullable=False)
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    creator = relationship('User', lazy='selectin')


class CandidateSkill(Base):
    __tablename__ = 'candidate_skills'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    candidate_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('candidates.id'), nullable=False)
    skill_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('skills.id'), nullable=False)
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    skill = relationship('Skill', lazy='selectin')
    creator = relationship('User', lazy='selectin')


class Interview(Base):
    __tablename__ = 'interviews'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    candidate_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('candidates.id'), nullable=False)
    vacancy_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('vacancies.id'), nullable=False)
    stage_code = sa.Column(sa.Integer, sa.ForeignKey('interview_stages_ref.code'), nullable=False)    
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)

    candidate = relationship('Candidate', lazy='joined')
    vacancy = relationship('Vacancy', lazy='joined')
    stage = relationship('InterviewStageRef', lazy='joined')
    creator = relationship('User', lazy='joined')


class InterviewStageResult(Base):
    __tablename__ = 'interview_stage_results'
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=sa.text("gen_random_uuid()"))
    interview_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('interviews.id'), nullable=False)
    interview_stage_code_old = sa.Column(sa.Integer, sa.ForeignKey('interview_stages_ref.code'), nullable=False)
    interview_stage_code_new = sa.Column(sa.Integer, sa.ForeignKey('interview_stages_ref.code'), nullable=False)
    note = sa.Column(sa.String, nullable=False)
    creator_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.sql.func.now(), onupdate=sa.sql.func.now())
    is_deleted = sa.Column(sa.Boolean, server_default=sa.text('False'), nullable=False)
    
    interview = relationship('Interview', lazy='selectin')
    interview_stage_old = relationship('InterviewStageRef', primaryjoin = 'InterviewStageResult.interview_stage_code_old == InterviewStageRef.code', lazy='selectin')
    interview_stage_new = relationship('InterviewStageRef', primaryjoin = 'InterviewStageResult.interview_stage_code_new == InterviewStageRef.code', lazy='selectin')
    creator = relationship('User', lazy='selectin')
