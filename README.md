# SkillTrade — Learn & Earn

SkillTrade is a web application built with Streamlit that allows users to register, post skills, book mentors, and manage their skills. It integrates a simple payment flow for booking skills. This app is designed to connect learners with mentors for skill-sharing and earning opportunities.

---

## Features

- **User Registration & Login:** Users can create accounts and log in securely.
- **Post Skills:** Registered users can post new skills they want to teach.
- **Book Skills:** Learners can browse skills and book sessions with mentors.
- **Payment Integration:** Upon booking a skill, a payment process is triggered.
- **Manage Skills:** Mentors can view and delete their posted skills.
- **Responsive UI:** Clean, custom styled interface with animations.

---

## Tech Stack

- **Python** with **Streamlit** for the frontend and UI.
- **SQLAlchemy** for database ORM.
- **SQLite/PostgreSQL** (or any SQL database supported by SQLAlchemy) for data storage.
- **Custom modules** for authentication (`auth.py`), payments (`payments.py`), and database models (`database.py`).

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/skilltrade.git
   cd skilltrade
