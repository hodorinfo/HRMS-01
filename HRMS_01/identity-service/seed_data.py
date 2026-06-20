"""Seed mock data into all HRMS databases."""
import asyncio
import bcrypt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://horilla:horilla@postgres:5432/horilla"

def hash_pw(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

async def seed():
    engine = create_async_engine(DATABASE_URL)
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as db:
        # Clean existing data first
        await db.execute(text("TRUNCATE employee_employeeworkinformation, employee_employeebankdetails, employee_employee, auth_user CASCADE"))
        await db.execute(text("TRUNCATE base_holidays, leave_leavetype CASCADE"))
        await db.execute(text("TRUNCATE base_jobposition, base_jobrole, base_department, base_company, base_worktype, base_employeetype, base_employeeshift CASCADE"))
        
        # Reset sequences
        for tbl in ['auth_user', 'employee_employee', 'base_company', 'base_department', 'base_jobposition', 'base_jobrole', 'base_worktype', 'base_employeetype', 'base_employeeshift', 'base_holidays', 'leave_leavetype', 'employee_employeeworkinformation']:
            await db.execute(text(f"ALTER SEQUENCE IF EXISTS {tbl}_id_seq RESTART WITH 1"))

        ah = hash_pw("admin123")
        mh = hash_pw("manager123")

        # 1. Users
        await db.execute(text("""
            INSERT INTO auth_user (id, username, email, password_hash, first_name, last_name, is_staff, is_superuser, is_active, is_new_employee) VALUES 
                (1, 'admin', 'admin@horilla.com', :ah, 'Super', 'Admin', true, true, true, false),
                (2, 'john.manager', 'john@horilla.com', :mh, 'John', 'Smith', true, false, true, false),
                (3, 'jane.employee', 'jane@horilla.com', :eh1, 'Jane', 'Doe', false, false, true, false),
                (4, 'bob.dev', 'bob@horilla.com', :eh2, 'Bob', 'Wilson', false, false, true, false),
                (5, 'alice.hr', 'alice@horilla.com', :eh3, 'Alice', 'Johnson', true, false, true, false)
        """), {"ah": ah, "mh": mh, "eh1": hash_pw("employee123"), "eh2": hash_pw("employee123"), "eh3": hash_pw("employee123")})
        await db.execute(text("SELECT setval('auth_user_id_seq', 5)"))

        # 2. Company
        await db.execute(text("INSERT INTO base_company (id, company, hq, address, country, state, city, zip, is_active) VALUES (1, 'Horilla Technologies', true, '123 Tech Park', 'India', 'Karnataka', 'Bangalore', '560100', true)"))

        # 3. Departments
        await db.execute(text("INSERT INTO base_department (id, department, is_active) VALUES (1,'Engineering',true),(2,'Human Resources',true),(3,'Marketing',true),(4,'Finance',true)"))

        # 4. Job Positions
        await db.execute(text("INSERT INTO base_jobposition (id, job_position, department_id, is_active) VALUES (1,'Software Engineer',1,true),(2,'HR Manager',2,true),(3,'Marketing Lead',3,true),(4,'DevOps Engineer',1,true)"))

        # 5. Work Types, Employee Types, Shifts
        await db.execute(text("INSERT INTO base_worktype (id, work_type, is_active) VALUES (1,'Office',true),(2,'Remote',true),(3,'Hybrid',true)"))
        await db.execute(text("INSERT INTO base_employeetype (id, employee_type, is_active) VALUES (1,'Full Time',true),(2,'Part Time',true),(3,'Contract',true)"))
        await db.execute(text("INSERT INTO base_employeeshift (id, employee_shift, weekly_full_time, full_time, is_active) VALUES (1,'Morning','40:00','200:00',true),(2,'General','45:00','200:00',true)"))

        # 6. Employees
        await db.execute(text("""
            INSERT INTO employee_employee (id, employee_user_id, badge_id, employee_first_name, employee_last_name, email, phone, gender, dob, country, state, city, is_active) VALUES
                (1, 1, 'PEP0001', 'Super', 'Admin', 'admin@horilla.com', '9876543210', 'male', '1985-01-15', 'India', 'Karnataka', 'Bangalore', true),
                (2, 2, 'PEP0002', 'John', 'Smith', 'john@horilla.com', '9876543211', 'male', '1988-06-20', 'India', 'Karnataka', 'Bangalore', true),
                (3, 3, 'PEP0003', 'Jane', 'Doe', 'jane@horilla.com', '9876543212', 'female', '1995-03-10', 'India', 'Karnataka', 'Bangalore', true),
                (4, 4, 'PEP0004', 'Bob', 'Wilson', 'bob@horilla.com', '9876543213', 'male', '1992-11-05', 'India', 'Karnataka', 'Bangalore', true),
                (5, 5, 'PEP0005', 'Alice', 'Johnson', 'alice@horilla.com', '9876543214', 'female', '1990-07-22', 'India', 'Karnataka', 'Bangalore', true)
        """))
        await db.execute(text("SELECT setval('employee_employee_id_seq', 5)"))

        # 7. Work Info
        await db.execute(text("""
            INSERT INTO employee_employeeworkinformation (employee_id, department_id, job_position_id, date_joining, basic_salary, company_id) VALUES
                (1, 1, 1, '2024-01-01', 150000, 1),
                (2, 1, 1, '2024-02-15', 120000, 1),
                (3, 2, 2, '2024-03-01', 80000, 1),
                (4, 1, 4, '2024-04-10', 90000, 1),
                (5, 2, 2, '2024-05-20', 85000, 1)
        """))

        # 8. Leave Types
        await db.execute(text("""
            INSERT INTO leave_leavetype (
                id, name, color, payment, count, period_in, limit_leave, reset, 
                is_encashable, require_approval, require_attachment, 
                exclude_company_leave, exclude_holiday, is_compensatory_leave, is_active
            ) VALUES 
                (1, 'Casual Leave', '#3498db', 'paid', 12, 'day', false, false, false, 'yes', 'no', 'no', 'no', false, true),
                (2, 'Sick Leave', '#e74c3c', 'paid', 10, 'day', false, false, false, 'yes', 'no', 'no', 'no', false, true),
                (3, 'Earned Leave', '#2ecc71', 'paid', 15, 'day', false, false, false, 'yes', 'no', 'no', 'no', false, true),
                (4, 'Unpaid Leave', '#95a5a6', 'unpaid', 0, 'day', false, false, false, 'yes', 'no', 'no', 'no', false, true)
        """))

        # 9. Holidays
        await db.execute(text("""
            INSERT INTO base_holidays (id, name, start_date, end_date, recurring, is_active) VALUES 
                (1, 'Republic Day', '2026-01-26', '2026-01-26', true, true),
                (2, 'Independence Day', '2026-08-15', '2026-08-15', true, true),
                (3, 'Diwali', '2026-10-20', '2026-10-21', false, true),
                (4, 'Christmas', '2026-12-25', '2026-12-25', true, true)
        """))

        await db.commit()
        print("\n✅ SEED COMPLETE!")
        print("\n📋 Login Credentials:")
        print("=" * 50)
        print("  Admin:    admin / admin123")
        print("  Manager:  john.manager / manager123")
        print("  Employee: jane.employee / employee123")
        print("  DevOps:   bob.dev / employee123")
        print("  HR Staff: alice.hr / employee123")
        print("=" * 50)

    await engine.dispose()

asyncio.run(seed())
