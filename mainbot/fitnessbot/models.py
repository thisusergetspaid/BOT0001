from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    age = Column(Integer)
    height_cm = Column(Float)

    goal = Column(String)

class WeightLog(Base):
    __tablename__ = "weight_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    weight = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    exercise = Column(String)

    sets = Column(Integer)
    reps = Column(Integer)

    weight = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    calories = Column(Integer)

    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )