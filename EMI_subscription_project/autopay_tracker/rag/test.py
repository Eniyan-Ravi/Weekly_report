from app.database import SessionLocal
from app.models import User
from sqlalchemy import select
from rag.pipeline import answer_question

db = SessionLocal()
user = db.execute(select(User).where(User.id == 2)).scalar_one()

print(answer_question("tell me my subscription details", db, user))

db.close()