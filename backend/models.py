from sqlalchemy import Column, String, Date, Float, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Tutor(Base):
    __tablename__ = "tutors"
    id = Column(Integer, primary_key=True)
    title = Column(String(10))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)

    # Relationships
    taught_modules = relationship("Module", back_populates="module_tutor")
    personal_students = relationship("Student", back_populates="personal_tutor")

    def __repr__(self):
        name = f"{self.first_name} {self.last_name}"
        return (
            f"<Tutor(id={self.id}, title='{self.title}', "
            f"name='{name}', email='{self.email}')>"
        )

class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    module_tutor_id = Column(Integer, ForeignKey("tutors.id"))
    module_tutor = relationship("Tutor", back_populates="taught_modules")
    grades = relationship("Grade", back_populates="module")

    def __repr__(self):
        return (
            f"<Module(id={self.id}, title='{self.title}', "
            f"tutor_id={self.module_tutor_id})>"
        )

class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)
    personal_tutor_id = Column(Integer, ForeignKey("tutors.id"))
    personal_tutor = relationship("Tutor", back_populates="personal_students")
    grades = relationship("Grade", back_populates="student")

    def __repr__(self):
        name = f"{self.first_name} {self.last_name}"
        return (
            f"<Student(id='{self.student_id}', name='{name}', "
            f"dob={self.dob}, tutor_id={self.personal_tutor_id})>"
        )

class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = (
        CheckConstraint("score BETWEEN 0 AND 1", name="check_score_range"),
    )

    student_id = Column(String, ForeignKey("students.student_id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), primary_key=True)
    score = Column(Float)
    student = relationship("Student", back_populates="grades")
    module = relationship("Module", back_populates="grades")

    def __repr__(self):
        return (
            f"<Grade(student='{self.student_id}', module={self.module_id}, "
            f"score={self.score})>"
        )
