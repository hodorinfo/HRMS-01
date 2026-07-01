"""Seed mock data into all HRMS databases using Microservices Architecture."""
import asyncio
import bcrypt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database URLs for each microservice
IDENTITY_DB_URL = "postgresql+asyncpg://horilla:horilla@postgres:5432/identity_db"
CORE_DB_URL = "postgresql+asyncpg://horilla:horilla@postgres:5432/core_db"
ATTENDANCE_DB_URL = "postgresql+asyncpg://horilla:horilla@postgres:5432/attendance_db"
PAYROLL_DB_URL = "postgresql+asyncpg://horilla:horilla@postgres:5432/payroll_db"
PERMISSION_DB_URL = "postgresql+asyncpg://horilla:horilla@postgres:5432/permission_db"
TALENT_DB_URL = "postgresql+asyncpg://horilla:horilla@postgres:5432/talent_db"


def hash_pw(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

async def get_db_session(url: str):
    engine = create_async_engine(url)
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return engine, Session

async def seed_core():
    print("Seeding core_db...")
    engine, Session = await get_db_session(CORE_DB_URL)
    async with Session() as db:
        await db.execute(text("TRUNCATE base_holidays, base_employeeshift CASCADE"))
        await db.execute(text("TRUNCATE base_jobrole, base_jobposition, base_department, base_company, base_worktype, base_employeetype CASCADE"))
        for tbl in ['base_company', 'base_department', 'base_jobposition', 'base_jobrole', 'base_worktype', 'base_employeetype', 'base_employeeshift', 'base_holidays']:
            await db.execute(text(f"ALTER SEQUENCE IF EXISTS {tbl}_id_seq RESTART WITH 1"))
        
        # Company
        await db.execute(text("INSERT INTO base_company (id, company, hq, address, country, state, city, zip, is_active) VALUES (1, 'Horilla Technologies', true, '123 Tech Park', 'India', 'Karnataka', 'Bangalore', '560100', true)"))
        # Departments
        await db.execute(text("INSERT INTO base_department (id, department, is_active) VALUES (1,'Engineering',true),(2,'Human Resources',true),(3,'Marketing',true),(4,'Finance',true)"))
        # Job Positions
        await db.execute(text("INSERT INTO base_jobposition (id, job_position, department_id, is_active) VALUES (1,'Software Engineer',1,true),(2,'HR Manager',2,true),(3,'Marketing Lead',3,true),(4,'DevOps Engineer',1,true)"))
        # Work Types, Employee Types, Shifts
        await db.execute(text("INSERT INTO base_worktype (id, work_type, is_active) VALUES (1,'Office',true),(2,'Remote',true),(3,'Hybrid',true)"))
        await db.execute(text("INSERT INTO base_employeetype (id, employee_type, is_active) VALUES (1,'Full Time',true),(2,'Part Time',true),(3,'Contract',true)"))
        await db.execute(text("INSERT INTO base_employeeshift (id, employee_shift, weekly_full_time, full_time, is_active) VALUES (1,'Morning','40:00','200:00',true),(2,'General','45:00','200:00',true)"))
        # Holidays
        await db.execute(text("""
            INSERT INTO base_holidays (id, name, start_date, end_date, recurring, is_active) VALUES 
                (1, 'Republic Day', '2026-01-26', '2026-01-26', true, true),
                (2, 'Independence Day', '2026-08-15', '2026-08-15', true, true),
                (3, 'Diwali', '2026-10-20', '2026-10-21', false, true),
                (4, 'Christmas', '2026-12-25', '2026-12-25', true, true)
        """))
        
        # Fix sequences
        await db.execute(text("SELECT setval('base_company_id_seq', (SELECT MAX(id) FROM base_company))"))
        await db.execute(text("SELECT setval('base_department_id_seq', (SELECT MAX(id) FROM base_department))"))
        await db.execute(text("SELECT setval('base_jobposition_id_seq', (SELECT MAX(id) FROM base_jobposition))"))
        await db.execute(text("SELECT setval('base_worktype_id_seq', (SELECT MAX(id) FROM base_worktype))"))
        await db.execute(text("SELECT setval('base_employeetype_id_seq', (SELECT MAX(id) FROM base_employeetype))"))
        await db.execute(text("SELECT setval('base_employeeshift_id_seq', (SELECT MAX(id) FROM base_employeeshift))"))
        await db.execute(text("SELECT setval('base_holidays_id_seq', (SELECT MAX(id) FROM base_holidays))"))

        await db.commit()
    await engine.dispose()

async def seed_identity():
    print("Seeding identity_db...")
    engine, Session = await get_db_session(IDENTITY_DB_URL)
    async with Session() as db:
        await db.execute(text("TRUNCATE employee_employeeworkinformation, employee_employeebankdetails, employee_employee, auth_user CASCADE"))
        for tbl in ['auth_user', 'employee_employee', 'employee_employeeworkinformation']:
            await db.execute(text(f"ALTER SEQUENCE IF EXISTS {tbl}_id_seq RESTART WITH 1"))

        ah = hash_pw("admin123")
        mh = hash_pw("manager123")

        # Users
        await db.execute(text("""
            INSERT INTO auth_user (id, username, email, password_hash, first_name, last_name, is_staff, is_superuser, is_active, is_new_employee) VALUES 
                (1, 'admin', 'admin@horilla.com', :ah, 'Super', 'Admin', true, true, true, false),
                (2, 'john.manager', 'john@horilla.com', :mh, 'John', 'Smith', true, false, true, false),
                (3, 'jane.employee', 'jane@horilla.com', :eh1, 'Jane', 'Doe', false, false, true, false),
                (4, 'bob.dev', 'bob@horilla.com', :eh2, 'Bob', 'Wilson', false, false, true, false),
                (5, 'alice.hr', 'alice@horilla.com', :eh3, 'Alice', 'Johnson', true, false, true, false)
        """), {"ah": ah, "mh": mh, "eh1": hash_pw("employee123"), "eh2": hash_pw("employee123"), "eh3": hash_pw("employee123")})
        
        # Employees
        await db.execute(text("""
            INSERT INTO employee_employee (id, employee_user_id, badge_id, employee_first_name, employee_last_name, email, phone, gender, dob, country, state, city, is_active) VALUES
                (1, 1, 'PEP0001', 'Super', 'Admin', 'admin@horilla.com', '9876543210', 'male', '1985-01-15', 'India', 'Karnataka', 'Bangalore', true),
                (2, 2, 'PEP0002', 'John', 'Smith', 'john@horilla.com', '9876543211', 'male', '1988-06-20', 'India', 'Karnataka', 'Bangalore', true),
                (3, 3, 'PEP0003', 'Jane', 'Doe', 'jane@horilla.com', '9876543212', 'female', '1995-03-10', 'India', 'Karnataka', 'Bangalore', true),
                (4, 4, 'PEP0004', 'Bob', 'Wilson', 'bob@horilla.com', '9876543213', 'male', '1992-11-05', 'India', 'Karnataka', 'Bangalore', true),
                (5, 5, 'PEP0005', 'Alice', 'Johnson', 'alice@horilla.com', '9876543214', 'female', '1990-07-22', 'India', 'Karnataka', 'Bangalore', true)
        """))
        
        # Work Info
        await db.execute(text("""
            INSERT INTO employee_employeeworkinformation (employee_id, department_id, job_position_id, date_joining, basic_salary, company_id) VALUES
                (1, 1, 1, '2024-01-01', 150000, 1),
                (2, 1, 1, '2024-02-15', 120000, 1),
                (3, 2, 2, '2024-03-01', 80000, 1),
                (4, 1, 4, '2024-04-10', 90000, 1),
                (5, 2, 2, '2024-05-20', 85000, 1)
        """))

        # Fix sequences
        await db.execute(text("SELECT setval('auth_user_id_seq', (SELECT MAX(id) FROM auth_user))"))
        await db.execute(text("SELECT setval('employee_employee_id_seq', (SELECT MAX(id) FROM employee_employee))"))
        
        await db.commit()
    await engine.dispose()

async def seed_attendance():
    print("Seeding attendance_db...")
    engine, Session = await get_db_session(ATTENDANCE_DB_URL)
    async with Session() as db:
        await db.execute(text("TRUNCATE leave_leavetype CASCADE"))
        await db.execute(text("ALTER SEQUENCE IF EXISTS leave_leavetype_id_seq RESTART WITH 1"))
        
        # Leave Types
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
        await db.execute(text("SELECT setval('leave_leavetype_id_seq', (SELECT MAX(id) FROM leave_leavetype))"))
        
        # General Settings
        await db.execute(text("TRUNCATE attendance_attendancegeneralsetting CASCADE"))
        await db.execute(text("""
            INSERT INTO attendance_attendancegeneralsetting (time_runner, enable_check_in, company_id, is_active) VALUES 
                (true, true, 1, true)
        """))
        
        # Available Leave for users
        await db.execute(text("TRUNCATE leave_availableleave CASCADE"))
        await db.execute(text("""
            INSERT INTO leave_availableleave (employee_id, leave_type_id, available_days, carryforward_days, total_leave_days, is_active) VALUES 
                (1, 1, 12, 0, 12, true),
                (1, 2, 10, 0, 10, true),
                (2, 1, 12, 0, 12, true),
                (3, 1, 12, 0, 12, true),
                (4, 1, 12, 0, 12, true),
                (5, 1, 12, 0, 12, true)
        """))

        # Attendance Timesheets (Work Records)
        await db.execute(text("TRUNCATE attendance_attendance CASCADE"))
        await db.execute(text("""
            INSERT INTO attendance_attendance (employee_id, attendance_date, minimum_hour, attendance_overtime, attendance_overtime_approve, attendance_validated, approved_overtime_second, is_validate_request, is_bulk_request, is_validate_request_approved, is_holiday, is_active) VALUES 
                (1, '2026-06-20', '08:00:00', '00:00:00', false, true, 0, false, false, false, false, true),
                (2, '2026-06-20', '08:00:00', '00:00:00', false, true, 0, false, false, false, false, true),
                (3, '2026-06-20', '08:00:00', '00:00:00', false, true, 0, false, false, false, false, true),
                (1, '2026-06-21', '08:00:00', '00:00:00', false, true, 0, false, false, false, false, true),
                (2, '2026-06-21', '08:00:00', '00:00:00', false, true, 0, false, false, false, false, true)
        """))
        
        # Leave Requests
        await db.execute(text("TRUNCATE leave_leaverequest CASCADE"))
        await db.execute(text("ALTER SEQUENCE IF EXISTS leave_leaverequest_id_seq RESTART WITH 1"))
        await db.execute(text("""
            INSERT INTO leave_leaverequest (employee_id, leave_type_id, start_date, end_date, start_date_breakdown, end_date_breakdown, requested_days, leave_clashes_count, description, status, requested_date, is_active) VALUES 
                (2, 1, '2026-06-25', '2026-06-26', 'full_day', 'full_day', 2.0, 0, 'Going out of station for personal work.', 'requested', '2026-06-20', true),
                (3, 2, '2026-07-01', '2026-07-01', 'full_day', 'full_day', 1.0, 0, 'Not feeling well.', 'approved', '2026-06-21', true),
                (4, 1, '2026-07-10', '2026-07-15', 'full_day', 'full_day', 5.0, 0, 'Family vacation.', 'rejected', '2026-06-22', true),
                (5, 3, '2026-08-01', '2026-08-02', 'full_day', 'full_day', 2.0, 0, 'Attending a conference.', 'requested', '2026-06-23', true)
        """))
        await db.execute(text("SELECT setval('leave_leaverequest_id_seq', (SELECT MAX(id) FROM leave_leaverequest))"))

        await db.commit()
    await engine.dispose()

async def seed_payroll():
    print("Seeding payroll_db...")
    engine, Session = await get_db_session(PAYROLL_DB_URL)
    async with Session() as db:
        await db.execute(text("TRUNCATE payroll_contract, payroll_filingstatus CASCADE"))
        for tbl in ['payroll_filingstatus', 'payroll_contract']:
            await db.execute(text(f"ALTER SEQUENCE IF EXISTS {tbl}_id_seq RESTART WITH 1"))
        
        # Filing Status
        await db.execute(text("""
            INSERT INTO payroll_filingstatus (id, filing_status, based_on, use_py, description, is_active) VALUES 
                (1, 'Single', 'amount', false, 'Single or married filing separately', true),
                (2, 'Married', 'amount', false, 'Married filing jointly', true)
        """))
        
        # Default contracts for seeded employees
        await db.execute(text("""
            INSERT INTO payroll_contract (contract_name, employee_id, contract_start_date, wage_type, pay_frequency, wage, filing_status_id, contract_status, deduct_leave_from_basic_pay, calculate_daily_leave_amount, deduction_for_one_leave_amount, is_active) VALUES 
                ('Contract for Admin', 1, '2024-01-01', 'Hourly', 'Monthly', 150000, 1, 'Active', false, false, 0, true),
                ('Contract for John', 2, '2024-02-15', 'Hourly', 'Monthly', 120000, 2, 'Active', false, false, 0, true),
                ('Contract for Jane', 3, '2024-03-01', 'Hourly', 'Monthly', 80000, 1, 'Active', false, false, 0, true),
                ('Contract for Bob', 4, '2024-04-10', 'Hourly', 'Monthly', 90000, 1, 'Active', false, false, 0, true),
                ('Contract for Alice', 5, '2024-05-20', 'Hourly', 'Monthly', 85000, 2, 'Active', false, false, 0, true)
        """))

        await db.execute(text("SELECT setval('payroll_filingstatus_id_seq', (SELECT MAX(id) FROM payroll_filingstatus))"))
        await db.execute(text("SELECT setval('payroll_contract_id_seq', (SELECT MAX(id) FROM payroll_contract))"))
        await db.commit()
    await engine.dispose()

async def seed_permission():
    print("Seeding permission_db...")
    engine, Session = await get_db_session(PERMISSION_DB_URL)
    async with Session() as db:
        await db.execute(text("TRUNCATE permission_user_roles, permission_role CASCADE"))
        for tbl in ['permission_role']:
            await db.execute(text(f"ALTER SEQUENCE IF EXISTS {tbl}_id_seq RESTART WITH 1"))
        
        # Roles
        await db.execute(text("""
            INSERT INTO permission_role (id, name, description, is_system, is_active) VALUES 
                (1, 'Admin', 'Super Administrator', true, true),
                (2, 'Manager', 'Department Manager', false, true),
                (3, 'Employee', 'Regular Employee', false, true)
        """))
        
        # Map roles to seeded auth_user IDs (from identity_db)
        await db.execute(text("""
            INSERT INTO permission_user_roles (user_id, role_id) VALUES 
                (1, 1), 
                (2, 2), 
                (3, 3), 
                (4, 3), 
                (5, 3)  
        """))

        await db.execute(text("SELECT setval('permission_role_id_seq', (SELECT MAX(id) FROM permission_role))"))
        await db.commit()
    await engine.dispose()

async def seed_talent():
    print("Seeding talent_db...")
    engine, Session = await get_db_session(TALENT_DB_URL)
    async with Session() as db:
        # Offboarding
        all_offboarding_tables = [
            'offboarding_employeetask', 'offboarding_exitreason', 'offboarding_offboardingnote',
            'offboarding_resignationletter', 'offboarding_offboardingemployee',
            'offboarding_offboardingtask', 'offboarding_offboardingstage',
            'offboarding_offboarding', 'offboarding_generalsetting', 'offboarding_offboardingstagefile'
        ]
        await db.execute(text(f"TRUNCATE {', '.join(all_offboarding_tables)} CASCADE"))
        for tbl in all_offboarding_tables:
            await db.execute(text(f"ALTER SEQUENCE IF EXISTS {tbl}_id_seq RESTART WITH 1"))

        # 1. Offboarding Pipeline
        await db.execute(text("""
            INSERT INTO offboarding_offboarding (id, title, description, managers, status, company_id, is_active) VALUES
                (1, 'Standard Exit', 'Standard company offboarding pipeline for all resignations', '[]', 'ongoing', 1, true),
                (2, 'Involuntary Exit', 'Offboarding pipeline for terminations', '[]', 'ongoing', 1, true)
        """))

        # 2. Offboarding Stages
        await db.execute(text("""
            INSERT INTO offboarding_offboardingstage (id, title, type, offboarding_id, managers, sequence, is_active) VALUES
                (1, 'Notice Period', 'notice_period', 1, '[]', 1, true),
                (2, 'Work Handover', 'handover', 1, '[]', 2, true),
                (3, 'Exit Interview', 'interview', 1, '[]', 3, true),
                (4, 'FnF Settlement', 'fnf', 1, '[]', 4, true),
                (5, 'Notice Period', 'notice_period', 2, '[]', 1, true),
                (6, 'Asset Return', 'other', 2, '[]', 2, true)
        """))

        # 3. Offboarding Tasks (template)
        await db.execute(text("""
            INSERT INTO offboarding_offboardingtask (id, title, managers, stage_id, is_active) VALUES
                (1, 'Submit Resignation', '[]', 1, true),
                (2, 'Handover Projects', '[]', 2, true),
                (3, 'Handover Documents', '[]', 2, true),
                (4, 'Schedule Interview', '[]', 3, true),
                (5, 'Complete FnF Form', '[]', 4, true),
                (6, 'Clear Dues & Advances', '[]', 4, true),
                (7, 'Return Laptop', '[]', 6, true),
                (8, 'Return Access Cards', '[]', 6, true)
        """))

        # 4. General Settings
        await db.execute(text("""
            INSERT INTO offboarding_generalsetting (id, resignation_request, company_id, is_active) VALUES
                (1, true, 1, true)
        """))

        # 5. Employee Offboarding records (employee_id=4 is Bob Wilson from identity seed)
        await db.execute(text("""
            INSERT INTO offboarding_offboardingemployee (id, employee_id, stage_id, notice_period, unit, notice_period_starts, notice_period_ends, is_active) VALUES
                (1, 4, 1, 30, 'day', '2026-06-25', '2026-07-25', true)
        """))

        # 6. Resignation Letter
        await db.execute(text("""
            INSERT INTO offboarding_resignationletter (id, employee_id, title, description, planned_to_leave_on, status, offboarding_employee_id, is_active) VALUES
                (1, 4, 'Resignation - Bob Wilson', 'I have decided to pursue new opportunities. Thank you for the experience.', '2026-07-25', 'approved', 1, true)
        """))

        # 7. Employee Tasks (assigned to Bob's offboarding)
        await db.execute(text("""
            INSERT INTO offboarding_employeetask (id, employee_id, task_id, status, description, is_active) VALUES
                (1, 1, 1, 'completed', 'Resignation letter submitted and approved.', true),
                (2, 1, 2, 'in_progress', 'Handing over the main product features.', true),
                (3, 1, 3, 'todo', NULL, true),
                (4, 1, 4, 'todo', NULL, true)
        """))

        # 8. Exit Reason
        await db.execute(text("""
            INSERT INTO offboarding_exitreason (id, title, description, offboarding_employee_id, attachments, is_active) VALUES
                (1, 'Better Opportunity', 'Received a better salary and role offer from another company.', 1, '[]', true)
        """))

        # 9. Offboarding Notes
        await db.execute(text("""
            INSERT INTO offboarding_offboardingnote (id, description, note_by, employee_id, stage_id, attachments, is_active) VALUES
                (1, 'Employee has been cooperative during notice period. No concerns.', 2, 1, 1, '[]', true),
                (2, 'Handover documentation pending for Project Alpha.', 2, 1, 2, '[]', true)
        """))

        # PMS
        await db.execute(text("TRUNCATE pms_period CASCADE"))
        await db.execute(text("ALTER SEQUENCE IF EXISTS pms_period_id_seq RESTART WITH 1"))
        await db.execute(text("""
            INSERT INTO pms_period (id, period_name, start_date, end_date, is_active) VALUES 
                (1, 'Q1 2026', '2026-01-01', '2026-03-31', true),
                (2, 'Q2 2026', '2026-04-01', '2026-06-30', true)
        """))

        # Recruitment (Rejection Reasons)
        await db.execute(text("TRUNCATE phm_rejection_reason CASCADE"))
        await db.execute(text("ALTER SEQUENCE IF EXISTS phm_rejection_reason_id_seq RESTART WITH 1"))
        await db.execute(text("""
            INSERT INTO phm_rejection_reason (id, reason_name) VALUES 
                (1, 'Culture Fit'),
                (2, 'Salary Expectations Too High'),
                (3, 'Failed Technical Round'),
                (4, 'Did Not Show Up')
        """))


        # Fix sequences
        for tbl in all_offboarding_tables:
            await db.execute(text(f"SELECT setval('{tbl}_id_seq', COALESCE((SELECT MAX(id) FROM {tbl}), 1))"))
        await db.execute(text("SELECT setval('pms_period_id_seq', (SELECT MAX(id) FROM pms_period))"))
        await db.execute(text("SELECT setval('phm_rejection_reason_id_seq', (SELECT MAX(id) FROM phm_rejection_reason))"))
        
        await db.commit()
    await engine.dispose()


async def main():
    print("Starting database seeding...")
    await seed_core()
    await seed_identity()
    await seed_attendance()
    await seed_payroll()
    await seed_permission()
    await seed_talent()
    print("\n✅ SEED COMPLETE!")
    print("\n📋 Login Credentials:")
    print("=" * 50)
    print("  Admin:    admin / admin123")
    print("  Manager:  john.manager / manager123")
    print("  Employee: jane.employee / employee123")
    print("  DevOps:   bob.dev / employee123")
    print("  HR Staff: alice.hr / employee123")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
