import streamlit as st
from auth import register_user, login_user
from database import session, UserDB, SkillDB, BookingDB
from payments import create_payment

# 🎨 Custom CSS Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton > button {
        background-color: #4A90E2;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #357ABD;
        color: #f0f0f0;
    }
    .skill-box {
        background: #e6f2ff;
        color: #000000;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: box-shadow 0.3s ease;
    }
    .skill-box:hover {
        box-shadow: 4px 4px 12px rgba(0,0,0,0.2);
    }
    .footer {
        text-align: center;
        padding: 20px 0;
        font-size: 16px;
        color: #4A90E2;
        font-weight: bold;
        border-top: 1px solid #ddd;
        margin-top: 40px;
    }
    [data-testid="stSidebar"] {
        background-color: #1E1E2F;
        color: #ddd;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💡 SkillTrade — Learn & Earn </div>', unsafe_allow_html=True)
st.balloons()

menu = ["Login", "Register", "Add Skill", "Book Skill", "Manage Skills"]
choice = st.sidebar.selectbox("📋 Select Option", menu)

# ✍️ Register
if choice == "Register":
    st.subheader("📝 Register as a User")
    name = st.text_input("👤 Name")
    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Register"):
        try:
            user = register_user(name, email, password)
            st.success("🎉 Registered successfully!")
            st.snow()
        except Exception as e:
            session.rollback()
            st.error("❌ Registration failed.")
            st.exception(e)

# 🔐 Login
elif choice == "Login":
    st.subheader("🔐 Login to Your Account")
    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        try:
            user = login_user(email, password)
            if user:
                st.success(f"✅ Welcome {user.name} ({user.role})")
            else:
                st.error("❌ Invalid credentials")
        except Exception as e:
            session.rollback()
            st.error("❌ Login failed.")
            st.exception(e)

# ➕ Add Skill
elif choice == "Add Skill":
    st.subheader("🛠️ Post a New Skill")
    email = st.text_input("📧 Your Email")

    try:
        user = session.query(UserDB).filter_by(email=email).first()
        if user:
            title = st.text_input("🎯 Skill Title")
            desc = st.text_area("📝 Skill Description")

            if st.button("Add Skill"):
                if title.strip() == "" or desc.strip() == "":
                    st.warning("⚠️ Title and description cannot be empty.")
                else:
                    new_skill = SkillDB(title=title, description=desc, mentor_id=user.id)
                    session.add(new_skill)
                    session.commit()
                    st.success("✅ Skill posted successfully!")
        else:
            st.warning("⚠️ Please login first.")
    except Exception as e:
        session.rollback()
        st.error("❌ Error while adding skill.")
        st.exception(e)

# 📚 Book Skill
elif choice == "Book Skill":
    st.subheader("📚 Book a Mentor")
    try:
        skills = session.query(SkillDB).all()

        for skill in skills:
            st.markdown(f"""
                <div class="skill-box">
                    <h4>🔹 {skill.title} — <span style='color:#357ABD;'>{skill.mentor.name}</span></h4>
                    <p>{skill.description}</p>
            """, unsafe_allow_html=True)

            learner_email = st.text_input("📧 Your Email", key=f"email_{skill.id}")

            if st.button(f"📅 Book '{skill.title}' with {skill.mentor.name}", key=f"book_{skill.id}"):
                try:
                    if learner_email.strip() == "":
                        st.warning("⚠️ Please enter your email.")
                    else:
                        learner = session.query(UserDB).filter_by(email=learner_email).first()
                        if learner:
                            booking = BookingDB(mentor_id=skill.mentor.id, learner_id=learner.id)
                            session.add(booking)
                            session.commit()
                            create_payment(booking.id)
                            st.success("✅ Booked and paid $10 successfully!")
                        else:
                            st.error("❌ Email not found. Please register first.")
                except Exception as e:
                    session.rollback()
                    st.error("❌ Booking failed.")
                    st.exception(e)

            st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        session.rollback()
        st.error("❌ Failed to load skills.")
        st.exception(e)

# 🗑️ Manage Skills
elif choice == "Manage Skills":
    st.subheader("🗑️ Manage Your Skills")
    email = st.text_input("📧 Your Email to load skills")

    try:
        user = session.query(UserDB).filter_by(email=email).first()
        if user:
            user_skills = session.query(SkillDB).filter_by(mentor_id=user.id).all()
            if user_skills:
                for skill in user_skills:
                    st.markdown(f"""
                        <div class="skill-box">
                            <h4>🔹 {skill.title}</h4>
                            <p>{skill.description}</p>
                    """, unsafe_allow_html=True)

                    if st.button(f"🗑️ Delete '{skill.title}'", key=f"del_{skill.id}"):
                        try:
                            session.delete(skill)
                            session.commit()
                            st.success(f"✅ Skill '{skill.title}' deleted.")
                            st.experimental_rerun()
                        except Exception as e:
                            session.rollback()
                            st.error("❌ Failed to delete skill.")
                            st.exception(e)

                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("ℹ️ You have not added any skills yet.")
        else:
            st.warning("⚠️ Please enter a valid email.")
    except Exception as e:
        session.rollback()
        st.error("❌ Error while loading your skills.")
        st.exception(e)

# Footer
st.markdown("""
    <div class="footer">
        Made with ❤️ by Kanwal Rafiqe
    </div>
""", unsafe_allow_html=True)
