# payments.py
from database import session, PaymentDB

def create_payment(session_id):
    payment = PaymentDB(session_id=session_id, amount=10.0, platform_fee=1.0, status="paid")
    session.add(payment)
    session.commit()
    return payment
