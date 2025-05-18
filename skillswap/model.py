# models.py
class User:
    def __init__(self, user_id, name, email, role="learner"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

    def become_mentor(self):
        self.role = "mentor"

class Skill:
    def __init__(self, skill_id, title, description, mentor_id):
        self.skill_id = skill_id
        self.title = title
        self.description = description
        self.mentor_id = mentor_id

class Booking:
    def __init__(self, booking_id, mentor_id, learner_id, time_slot):
        self.booking_id = booking_id
        self.mentor_id = mentor_id
        self.learner_id = learner_id
        self.time_slot = time_slot
        self.status = "pending"

    def confirm(self):
        self.status = "confirmed"

class Payment:
    def __init__(self, session_id, amount=10.0):
        self.session_id = session_id
        self.amount = amount
        self.platform_fee = 1.0
        self.status = "unpaid"

    def process_payment(self):
        self.status = "paid"
