from app.database import SessionLocal
from app.models import User
from sqlalchemy import select
from rag.generation.llm_client import generate_answer_with_tools

db = SessionLocal()
user = db.execute(select(User).where(User.id == 1)).scalar_one()

question = "What EMIs do I currently have?"
answer = generate_answer_with_tools(question, db, user)
print(answer)

db.close()