from models import *
from database import *

Base.metadata.create_all(bind=engine)

db = SessionLocal()

new_user = User(
    name="Valentino",
    age=30,
    height_cm=183,
    goal="bulk"
)

db.add(new_user)
db.commit()

user_id = new_user.id

weight = WeightLog(
    user_id=user_id,
    weight=205
)

db.add(weight)
db.commit()

print("User created")