"""Seed mock data into all HRMS databases."""
import asyncio
from datetime import date, datetime
import bcrypt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://horilla:horilla@postgres:5432/horilla"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

async def seed():
    engine = create_async_engine(DATABASE_URL)
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as db:
        # 1. Create Users
        admin_hash = hash_password("admin123")
        manager_hash = hash_password("manager123")
        emp_hash = hash_password("employee123")

        await db.execute(text("""
            INSERT INTO auth_user (username, email, password_hash, first_name, last_name, is_staff, is_superuser, is_active, is_new_employee)
            VALUES 
                ('admin', 'admin@horilla.com', :admin_hash, 'Super', 'Admin', true, true, true, false),
                ('john.manager', 'john@horilla.com', :manager_hash, 'John', 'Smith', true, false, true, false),
                ('jane.employee', 'jane@horilla.com', :emp_hash, 'Jane', 'Doe', false, false, true, false),
                ('bob.dev', 'bob@horilla.com', :emp_hash, 'Bob', 'Wilson', false, false, true, false),
                ('alice.hr', 'alice@horilla.com', :emp_hash, 'Alice', 'Johnson', true, false, true, false)
            ON CONFLICT (username) DO NOTHING
        """), {"admin_hash": admin_hash, "manager_hash": manager_hash, "emp_hash": emp_hash})

        # 2. Create Company
        await db.execute(text("""
            INSERT INTO base_company (company, hq, address, country, state, city, zip, is_active)
            VALUES ('Horilla Technologies', true, '123 Tech Park, Electronic City', 'India', 'Karnataka', 'Bangalore', '560100', true)
            ON CONFLICT DO NOTHING
        """))

        # 3. Create Departments
        await db.execute(text("""
            INSERT INTO base_department (department, is_active) VALUES 
                ('Engineering', true), ('Human Resources', true), ('Marketing', true), ('Finance', true), ('Operations', true)
            ON CONFLICT DO NOTHING
        """))

        # 4. Create Job Positions
        await db.execute(text("""
            INSERT INTO base_jobposition (job_position, department_id, is_active)
            SELECT jp.job_position, d.id, true
            FROM (VALUES ('Software Engineer', 'Engineering'), ('HR Manager', 'Human Resources'), ('Marketing Lead', 'Marketing'), ('Accountant', 'Finance'), ('DevOps Engineer', 'Engineering')) AS jp(job_position, dept)
            JOIN base_department d ON d.department = jp.dept
            ON CONFLICT DO NOTHING
        """))

        # 5. Create Job Roles
        await db.execute(text("""
            INSERT INTO base_jobrole (job_position_id, job_role, is_active)
            SELECT jp.id, r.role_name, true
            FROM (VALUES ('Software Engineer', 'Backend Developer'), ('Software Engineer', 'Frontend Developer'), ('HR Manager', 'Recruiter'), ('DevOps Engineer', 'Cloud Engineer')) AS r(pos, role_name)
            JOIN base_jobposition jp ON jp.job_position = r.pos
            ON CONFLICT DO NOTHING
        """))

        # 6. Work Types & Employee Types
        await db.execute(text("""
            INSERT INTO base_worktype (work_type, is_active) VALUES ('Work From Office', true), ('Work From Home', true), ('Hybrid', true)
            ON CONFLICT DO NOTHING
        """))
        await db.execute(text("""
            INSERT INTO base_employeetype (employee_type, is_active) VALUES ('Full Time', true), ('Part Time', true), ('Contract', true), ('Intern', true)
            ON CONFLICT DO NOTHING
        """))

        # 7. Shifts
        await db.execute(text("""
            INSERT INTO base_employeeshift (employee_shift, weekly_full_time, full_time, is_active) VALUES 
                ('Morning Shift', '40:00', '200:00', true), ('Evening Shift', '40:00', '200:00', true), ('General Shift', '45:00', '200:00', true)
            ON CONFLICT DO NOTHING
        """))

        # 8. Employees
        await db.execute(text("""
            INSERT INTO employee_employee (employee_user_id, badge_id, employee_first_name, employee_last_name, email, phone, gender, dob, country, state, city, is_active)
            SELECT u.id, 'PEP' || LPAD(u.id::text, 4, '0'), u.first_name, u.last_name, u.email, 
                CASE u.username WHEN 'admin' THEN '9876543210' WHEN 'john.manager' THEN '9876543211' WHEN 'jane.employee' THEN '9876543212' WHEN 'bob.dev' THEN '9876543213' WHEN 'alice.hr' THEN '9876543214' END,
                CASE WHEN u.username IN ('jane.employee','alice.hr') THEN 'female' ELSE 'male' END,
                CASE u.username WHEN 'admin' THEN '1985-01-15' WHEN 'john.manager' THEN '1988-06-20' WHEN 'jane.employee' THEN '1995-03-10' WHEN 'bob.dev' THEN '1992-11-05' WHEN 'alice.hr' THEN '1990-07-22' END ::date,
                'India', 'Karnataka', 'Bangalore', true
            FROM auth_user u WHERE u.username IN ('admin','john.manager','jane.employee','bob.dev','alice.hr')
            ON CONFLICT (email) DO NOTHING
        """))

        # 9. Employee Work Information
        await db.execute(text("""
            INSERT INTO employee_employeeworkinformation (employee_id, department_id, job_position_id, date_joining, basic_salary, company_id)
            SELECT e.id, d.id, jp.id, '2024-01-15'::date, sal.salary, 1
            FROM employee_employee e
            JOIN auth_user u ON u.id = e.employee_user_id
            JOIN (VALUES ('admin', 'Engineering', 'Software Engineer', 150000), ('john.manager', 'Engineering', 'Software Engineer', 120000), ('jane.employee', 'Human Resources', 'HR Manager', 80000), ('bob.dev', 'Engineering', 'DevOps Engineer', 90000), ('alice.hr', 'Human Resources', 'HR Manager', 85000)) AS sal(uname, dept, pos, salary)
                ON u.username = sal.uname
            JOIN base_department d ON d.department = sal.dept
            JOIN base_jobposition jp ON jp.job_position = sal.pos
            ON CONFLICT DO NOTHING
        """))

        # 10. Leave Types
        await db.execute(text("""
            INSERT INTO leave_leavetype (name, color, payment, count, period_in, is_active, limit_leave, reset, is_encashable, require_approval, require_attachment, exclude_company_leave, exclude_holiday, is_compensatory_leave) VALUES 
                ('Casual Leave', '#3498db', 'paid', 12, 'day', true, false, false, false, 'yes', 'no', 'no', 'no', false),
                ('Sick Leave', '#e74c3c', 'paid', 10, 'day', true, false, false, false, 'yes', 'no', 'no', 'no', false),
                ('Earned Leave', '#2ecc71', 'paid', 15, 'day', true, false, false, false, 'yes', 'no', 'no', 'no', false),
                ('Unpaid Leave', '#95a5a6', 'unpaid', 0, 'day', true, false, false, false, 'yes', 'no', 'no', 'no', false),
                ('Maternity Leave', '#9b59b6', 'paid', 180, 'day', true, false, false, false, 'yes', 'no', 'no', 'no', false)
            ON CONFLICT DO NOTHING
        """))

        # 11. Holidays
        await db.execute(text("""
            INSERT INTO base_holidays (name, start_date, end_date, recurring, is_active) VALUES 
                ('Republic Day', '2026-01-26', '2026-01-26', true, true),
                ('Holi', '2026-03-14', '2026-03-14', false, true),
                ('Independence Day', '2026-08-15', '2026-08-15', true, true),
                ('Diwali', '2026-10-20', '2026-10-21', false, true),
                ('Christmas', '2026-12-25', '2026-12-25', true, true)
            ON CONFLICT DO NOTHING
        """))

        await db.commit()
        print("=== SEED COMPLETE ===")
        print("Login Credentials:")
        print("  Admin:    username=admin          password=admin123")
        print("  Manager:  username=john.manager   password=manager123")
        print("  Employee: username=jane.employee  password=employee123")
        print("  Employee: username=bob.dev         password=employee123")
        print("  HR Staff: username=alice.hr        password=employee123")

    await engine.dispose()

asyncio.run(seed())
