from datetime import datetime
from database import SessionLocal
from models import Student, Tutor, Module, Grade
import random
import string   
from sqlalchemy import inspect
from database import engine, Base

def generate_student_id():
    """Generate a student ID matching 6 digits + 1 letter (e.g., 123456A)"""
    return f"{random.randint(100000, 999999)}{random.choice(string.ascii_uppercase)}"

def create_sample_data():
    db = SessionLocal()

    try:
        # Check if tables exist and delete all records
        inspector = inspect(db.get_bind())
        if "grades" in inspector.get_table_names():
            db.query(Grade).delete()
        if "students" in inspector.get_table_names():
            db.query(Student).delete()
        if "modules" in inspector.get_table_names():
            db.query(Module).delete()
        if "tutors" in inspector.get_table_names():
            db.query(Tutor).delete()
        db.commit()

        Base.metadata.create_all(bind=engine)

        # 1. Create Tutors
        tutors = [
            Tutor(title = "Dr", first_name="John", last_name="Smith", email="john.smith@university.ac.uk"),
            Tutor(title="Prof", first_name="Brown", last_name="Johnson", email="brown.johnson@university.ac.uk"),
            Tutor(title="Dr", first_name="Lee", last_name="Jones", email="lee.jones@university.ac.uk")
        ]
        db.add_all(tutors)
        db.commit()  # Flush to get tutor IDs

        # 2. Create Modules
        modules = [
            Module(title="Mathematics", module_tutor_id=tutors[0].id),
            Module(title="Literature", module_tutor_id=tutors[1].id),
            Module(title="Computer Science", module_tutor_id=tutors[2].id)
        ]
        db.add_all(modules)
        db.commit()  # Flush to get module IDs

        # 3. Create Students with Personal Tutors
        students = [
            Student(
                student_id=generate_student_id(),
                first_name="Alice",
                last_name="Brown",
                dob=datetime(2000, 5, 15),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            Student(
                student_id=generate_student_id(),
                first_name="Bob",
                last_name="Wilson",
                dob=datetime(2001, 8, 22),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            Student(
                student_id=generate_student_id(),
                first_name="Charlie",
                last_name="Davis",
                dob=datetime(2000, 3, 10),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            Student(
                student_id=generate_student_id(),
                first_name="David",
                last_name="Evans",
                dob=datetime(2001, 11, 30),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            Student(
                student_id=generate_student_id(),
                first_name="Frank",
                last_name="Garcia",
                dob=datetime(2000, 7, 15),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            Student(
                student_id=generate_student_id(),
                first_name="Grace",
                last_name="Hernandez",
                dob=datetime(2002, 2, 28),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            Student(
                student_id=generate_student_id(),
                first_name="Henry",
                last_name="Ibarra",
                dob=datetime(2001, 9, 12),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            Student(
                student_id=generate_student_id(),
                first_name="Ivy",
                last_name="Johnson",
                dob=datetime(2001, 4, 25),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            Student(
                student_id=generate_student_id(),
                first_name="Jack",
                last_name="Kim",
                dob=datetime(2001, 1, 18),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            Student(
                student_id=generate_student_id(),
                first_name="Liam",
                last_name="Lopez",
                dob=datetime(2001, 10, 14),
                personal_tutor_id=tutors[random.randint(0, 2)].id
            ),
            
        ]
        db.add_all(students)
        db.commit()

        # 4. Create Grades (linking students to modules)
        grade_records = []
        for student in students:
            for module in modules:
                grade_records.append(
                    Grade(
                        student_id=student.student_id,
                        module_id=module.id,
                        score=round(random.uniform(0.4, 1.0), 2) 
                    )
                )
        
        db.add_all(grade_records)
        db.commit()

        print("Sample data created successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()