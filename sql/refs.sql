INSERT INTO roles_ref (code, name, sys_name) VALUES (1, 'Администратор', 'admin') ON CONFLICT DO NOTHING;
INSERT INTO roles_ref (code, name, sys_name) VALUES (2, 'Сотрудник', 'employee') ON CONFLICT DO NOTHING;
INSERT INTO roles_ref (code, name, sys_name) VALUES (3, 'Менеджер', 'manager') ON CONFLICT DO NOTHING;
INSERT INTO roles_ref (code, name, sys_name) VALUES (4, 'Рекрутер', 'recruiter') ON CONFLICT DO NOTHING;