from app.database import SessionLocal
from app.models import User
from sqlalchemy import select
from rag.tools.db_tools import get_subscriptions, get_emis, get_payment_history, get_subscription_by_id

db = SessionLocal()

user = db.execute(select(User).where(User.id == 1)).scalar_one()  # use a real user_id from your data

print(get_subscriptions(db, user))
print(get_emis(db, user))
print(get_payment_history(db, user))
print(get_subscription_by_id(db, user, subscription_id=9999))  # deliberately bad ID, should give status: error

db.close()