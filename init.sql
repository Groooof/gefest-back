CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS refs;


-- Справочники *************************************************************

CREATE TABLE IF NOT EXISTS refs.vacancy_priorities (
    code INTEGER PRIMARY KEY NOT NULL,
    value TEXT NOT NULL,
    is_archive BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS refs.adresses (
    code INTEGER PRIMARY KEY NOT NULL,
    value TEXT NOT NULL,
    parent_id INTEGER,
    is_archive BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (parent_id) REFERENCES refs.adresses (code)
);

CREATE TABLE IF NOT EXISTS refs.countries (
    code INTEGER PRIMARY KEY NOT NULL,
    value TEXT NOT NULL,
    is_archive BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS refs.family_stats (
    code INTEGER PRIMARY KEY NOT NULL,
    value TEXT NOT NULL,
    is_archive BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS refs.contact_types (
    code INTEGER PRIMARY KEY NOT NULL,
    value TEXT NOT NULL,
    is_archive BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS refs.languages (
    code INTEGER PRIMARY KEY NOT NULL,
    value TEXT NOT NULL,
    is_archive BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS refs.language_levels (
    code INTEGER PRIMARY KEY NOT NULL,
    level_code TEXT NOT NULL,
    value TEXT NOT NULL,
    is_archive BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS refs.interview_stages (
    code INTEGER PRIMARY KEY NOT NULL,
    value TEXT NOT NULL,
    parent_id INTEGER,
    is_archive BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (parent_id) REFERENCES refs.interview_stages (code)
);

CREATE TABLE IF NOT EXISTS refs.roles (
    code INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    sys_name TEXT NOT NULL
);

-- Таблицы *****************************************************************

CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    short_name TEXT NOT NULL,
    ogrn TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    company_id UUID NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

CREATE TABLE IF NOT EXISTS positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    company_id UUID NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

CREATE TABLE IF NOT EXISTS grades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    company_id UUID NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL,
    hashed_password TEXT NOT NULL,
    role_code INTEGER NOT NULL,
    company_id UUID NOT NULL,
    department_id UUID,
    position_id UUID,
    grade_id UUID,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    email TEXT NOT NULL,
    creator_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    logged_in_at TIMESTAMP,
    UNIQUE (username),
    FOREIGN KEY (role_code) REFERENCES refs.roles (code),
    FOREIGN KEY (company_id) REFERENCES companies (id),
    FOREIGN KEY (department_id) REFERENCES departments (id),
    FOREIGN KEY (position_id) REFERENCES positions (id),
    FOREIGN KEY (grade_id) REFERENCES grades (id),
    FOREIGN KEY (creator_id) REFERENCES users (id),
    CONSTRAINT first_name_format CHECK (first_name ~ '^([А-я]|-)*$'),
    CONSTRAINT last_name_format CHECK (last_name ~ '^([А-я]|-)*$'),
    CONSTRAINT middle_name_format CHECK (middle_name ~ '^([А-я]|-)*$')
);

CREATE TABLE IF NOT EXISTS refresh_tokens (
    token UUID PRIMARY KEY,
    expires_at TIMESTAMP NOT NULL,
    user_id UUID NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    company_id UUID NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

CREATE TABLE IF NOT EXISTS department_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    department_id UUID NOT NULL,
    skill_id UUID NOT NULL,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (department_id) REFERENCES departments (id),
    FOREIGN KEY (skill_id) REFERENCES skills (id),
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS vacancies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    position_id UUID NOT NULL,
    department_id UUID NOT NULL,
    salary_from INTEGER NOT NULL,
    salary_to INTEGER NOT NULL,
    employee_count INTEGER NOT NULL,
    priority_code INTEGER NOT NULL,
    deadline TIMESTAMP,
    company_id UUID NOT NULL,
    recruiter_id UUID NOT NULL,
    adress_code INTEGER,
    project TEXT,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (position_id) REFERENCES positions (id),
    FOREIGN KEY (company_id) REFERENCES companies (id),
    FOREIGN KEY (recruiter_id) REFERENCES users (id),
    FOREIGN KEY (creator_id) REFERENCES users (id),
    FOREIGN KEY (adress_code) REFERENCES refs.adresses (code),
    FOREIGN KEY (priority_code) REFERENCES refs.vacancy_priorities (code),
    FOREIGN KEY (department_id) REFERENCES departments (id),
    CONSTRAINT salary CHECK (salary_from > 0 AND salary_from <= salary_to),
    CONSTRAINT employee_count CHECK (employee_count >= 0 AND employee_count <= 1000)
);

CREATE TABLE IF NOT EXISTS vacancy_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vacancy_id UUID NOT NULL,
    skill_id UUID NOT NULL,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies (id),
    FOREIGN KEY (skill_id) REFERENCES skills (id),
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    size NUMERIC(6,2) NOT NULL,
    entity_name TEXT NOT NULL,
    entity_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS candidates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    birth_date DATE,
    min_salary INTEGER,
    adress_code INTEGER,
    citizenship_code INTEGER,
    family_status_code INTEGER,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (creator_id) REFERENCES users (id),
    FOREIGN KEY (adress_code) REFERENCES refs.adresses (code),
    FOREIGN KEY (citizenship_code) REFERENCES refs.countries (code),
    FOREIGN KEY (family_status_code) REFERENCES refs.family_stats (code),
    CONSTRAINT first_name_format CHECK (first_name ~ '^([А-я]|-)*$'),
    CONSTRAINT last_name_format CHECK (last_name ~ '^([А-я]|-)*$'),
    CONSTRAINT middle_name_format CHECK (middle_name ~ '^([А-я]|-)*$'),
    CONSTRAINT min_salary CHECK (min_salary > 0)
);

CREATE TABLE IF NOT EXISTS candidate_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL,
    type_code INTEGER NOT NULL,
    value TEXT NOT NULL,
    is_priority BOOLEAN DEFAULT FALSE,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (candidate_id) REFERENCES candidates (id),
    FOREIGN KEY (creator_id) REFERENCES users (id),
    FOREIGN KEY (type_code) REFERENCES refs.contact_types (code)
);

CREATE TABLE IF NOT EXISTS candidate_work_expirience (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL,
    post TEXT NOT NULL,
    company TEXT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE,
    is_actual BOOLEAN DEFAULT FALSE,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (creator_id) REFERENCES users (id),
    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
);

CREATE TABLE IF NOT EXISTS candidate_language_ability (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL,
    language_code INTEGER NOT NULL,
    language_level_code INTEGER NOT NULL,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (creator_id) REFERENCES users (id),
    FOREIGN KEY (candidate_id) REFERENCES candidates (id),
    FOREIGN KEY (language_code) REFERENCES refs.languages (code),
    FOREIGN KEY (language_level_code) REFERENCES refs.language_levels (code)
);

CREATE TABLE IF NOT EXISTS candidate_notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL,
    note TEXT NOT NULL,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (creator_id) REFERENCES users (id),
    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
);

CREATE TABLE IF NOT EXISTS candidate_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL,
    skill_id UUID NOT NULL,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (creator_id) REFERENCES users (id),
    FOREIGN KEY (candidate_id) REFERENCES candidates (id),
    FOREIGN KEY (skill_id) REFERENCES skills (id)
);

CREATE TABLE IF NOT EXISTS interviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL,
    vacancy_id UUID NOT NULL,
    stage_code INTEGER NOT NULL,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies (id),
    FOREIGN KEY (creator_id) REFERENCES users (id),
    FOREIGN KEY (candidate_id) REFERENCES candidates (id),
    FOREIGN KEY (stage_code) REFERENCES refs.interview_stages (code)
);

CREATE TABLE IF NOT EXISTS interview_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interview_id UUID NOT NULL,
    -- event_code INTEGER NOT NULL, -- нет справочника
    planned_at TIMESTAMP NOT NULL,
    creator_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (interview_id) REFERENCES interviews (id),
    -- FOREIGN KEY (event_code) REFERENCES refs.interview_events (code),
    FOREIGN KEY (creator_id) REFERENCES users (id),
    CONSTRAINT planned_at CHECK (planned_at >= created_at)
);

-- Функции *****************************************************************

CREATE OR REPLACE FUNCTION set_users_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_vacancies_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_files_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_candidates_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_candidate_contacts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_candidate_work_expirience_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_candidate_language_ability_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_candidate_notes_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_interviews_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_interview_events_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_companies_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_skills_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_candidate_skills_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_vacancy_skills_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_department_skills_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггеры *****************************************************************

CREATE OR REPLACE TRIGGER set_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE PROCEDURE set_users_updated_at();

CREATE OR REPLACE TRIGGER set_vacancies_updated_at
AFTER UPDATE ON vacancies
FOR EACH ROW
EXECUTE PROCEDURE set_vacancies_updated_at();

CREATE OR REPLACE TRIGGER set_files_updated_at
AFTER UPDATE ON files
FOR EACH ROW
EXECUTE PROCEDURE set_files_updated_at();

CREATE OR REPLACE TRIGGER set_candidates_updated_at
AFTER UPDATE ON candidates
FOR EACH ROW
EXECUTE PROCEDURE set_candidates_updated_at();

CREATE OR REPLACE TRIGGER set_candidate_contacts_updated_at
AFTER UPDATE ON candidate_contacts
FOR EACH ROW
EXECUTE PROCEDURE set_candidate_contacts_updated_at();

CREATE OR REPLACE TRIGGER set_candidate_work_expirience_updated_at
AFTER UPDATE ON candidate_work_expirience
FOR EACH ROW
EXECUTE PROCEDURE set_candidate_work_expirience_updated_at();

CREATE OR REPLACE TRIGGER set_candidate_language_ability_updated_at
AFTER UPDATE ON candidate_language_ability
FOR EACH ROW
EXECUTE PROCEDURE set_candidate_language_ability_updated_at();

CREATE OR REPLACE TRIGGER set_candidate_notes_updated_at
AFTER UPDATE ON candidate_notes
FOR EACH ROW
EXECUTE PROCEDURE set_candidate_notes_updated_at();

CREATE OR REPLACE TRIGGER set_interviews_updated_at
AFTER UPDATE ON interviews
FOR EACH ROW
EXECUTE PROCEDURE set_interviews_updated_at();

CREATE OR REPLACE TRIGGER set_interview_events_updated_at
AFTER UPDATE ON interview_events
FOR EACH ROW
EXECUTE PROCEDURE set_interview_events_updated_at();

CREATE OR REPLACE TRIGGER set_companies_updated_at
AFTER UPDATE ON companies
FOR EACH ROW
EXECUTE PROCEDURE set_companies_updated_at();

CREATE OR REPLACE TRIGGER set_skills_updated_at
AFTER UPDATE ON skills
FOR EACH ROW
EXECUTE PROCEDURE set_skills_updated_at();

CREATE OR REPLACE TRIGGER set_candidate_skills_updated_at
AFTER UPDATE ON candidate_skills
FOR EACH ROW
EXECUTE PROCEDURE set_candidate_skills_updated_at();

CREATE OR REPLACE TRIGGER set_vacancy_skills_updated_at
AFTER UPDATE ON vacancy_skills
FOR EACH ROW
EXECUTE PROCEDURE set_vacancy_skills_updated_at();

CREATE OR REPLACE TRIGGER set_department_skills_updated_at
AFTER UPDATE ON department_skills
FOR EACH ROW
EXECUTE PROCEDURE set_department_skills_updated_at();

-- Моки *****************************************************************

INSERT INTO refs.roles (code, name, sys_name) VALUES (1, 'Администратор', 'admin') ON CONFLICT DO NOTHING;
INSERT INTO refs.roles (code, name, sys_name) VALUES (2, 'Сотрудник', 'employee') ON CONFLICT DO NOTHING;
INSERT INTO refs.roles (code, name, sys_name) VALUES (3, 'Менеджер', 'manager') ON CONFLICT DO NOTHING;
INSERT INTO refs.roles (code, name, sys_name) VALUES (4, 'Рекрутер', 'recruiter') ON CONFLICT DO NOTHING;

INSERT INTO companies (id, full_name, short_name, ogrn)
VALUES ('a35302aa-b092-4b30-a384-464ed29619e1', 'ООО "Пачки"', 'пу пу пу', '1234567890') ON CONFLICT DO NOTHING;

INSERT INTO users
(
    username,
    hashed_password,
    role_code,
    company_id,
    department_id,
    position_id,
    grade_id,
    first_name,
    last_name,
    middle_name,
    email,
    creator_id
)
VALUES
(
    'admin',
    crypt('admin', gen_salt('bf', 10)),
    1,
    'a35302aa-b092-4b30-a384-464ed29619e1',
    NULL,
    NULL,
    NULL,
    'Иван',
    'Иванов',
    'Иванович',
    'pochta@mail.ru',
    NULL
)
ON CONFLICT DO NOTHING;
