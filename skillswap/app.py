import streamlit as st
from auth import register_user, login_user
from database import session, UserDB, SkillDB, BookingDB
from payments import create_payment

# 🎨 Custom CSS Styling
st.markdown("""
    <style>
    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Buttons */
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
    /* Skill box with hover */
    .skill-box {
        background: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: box-shadow 0.3s ease;
    }
    .skill-box:hover {
        box-shadow: 4px 4px 12px rgba(0,0,0,0.2);
    }
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px 0;
        font-size: 16px;
        color: #4A90E2;
        font-weight: bold;
        border-top: 1px solid #ddd;
        margin-top: 40px;
    }
    /* Sidebar dark styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E2F;
        color: #ddd;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        color: #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# 🎉 Animated Header
st.markdown('<div class="main-title">💡 SkillTrade — Learn & Earn </div>', unsafe_allow_html=True)
st.balloons()  # Animation when app starts

menu = ["Login", "Register", "Add Skill", "Book Skill", "Manage Skills"]
choice = st.sidebar.selectbox("📋 Select Option", menu)

# ✍️ Register
if choice == "Register":
    st.subheader("📝 Register as a User")
    name = st.text_input("👤 Name")
    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")
    if st.button("Register"):
        user = register_user(name, email, password)
        st.success("🎉 Registered successfully!")
        st.snow()  # Show snow animation

# 🔐 Login
elif choice == "Login":
    st.subheader("🔐 Login to Your Account")
    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success(f"✅ Welcome {user.name} ({user.role})")
        else:
            st.error("❌ Invalid credentials")

# ➕ Add Skill
elif choice == "Add Skill":
    st.subheader("🛠️ Post a New Skill")
    email = st.text_input("📧 Your Email")
    user = session.query(UserDB).filter_by(email=email).first()
    if user:
        title = st.text_input("🎯 Skill Title")
        desc = st.text_area("📝 Skill Description")
        if st.button("Add Skill"):
            new_skill = SkillDB(title=title, description=desc, mentor=user)
            session.add(new_skill)
            session.commit()
            st.success("✅ Skill posted successfully!")
    else:
        st.warning("⚠️ Please login first")

# 📚 Book Skill
elif choice == "Book Skill":
    st.subheader("📚 Book a Mentor")
    skills = session.query(SkillDB).all()
    for skill in skills:
        st.markdown(f"""
            <div class="skill-box">
                <h4>🔹 {skill.title} — <span style='color:#357ABD;'>{skill.mentor.name}</span></h4>
                <p>{skill.description}</p>
        """, unsafe_allow_html=True)

        # Learner email input shown *before* button
        learner_email = st.text_input("📧 Your Email", key=f"email_{skill.id}")
        
        if st.button(f"📅 Book '{skill.title}' with {skill.mentor.name}", key=f"book_{skill.id}"):
            learner = session.query(UserDB).filter_by(email=learner_email).first()
            if learner:
                booking = BookingDB(mentor_id=skill.mentor.id, learner_id=learner.id)
                session.add(booking)
                session.commit()
                create_payment(booking.id)
                st.success("✅ Booked and paid $10 successfully!")
            else:
                st.error("❌ Email not found. Please register or check your login.")

        st.markdown("</div>", unsafe_allow_html=True)

# 🗑️ Manage Skills (delete your skills)
elif choice == "Manage Skills":
    st.subheader("🗑️ Manage Your Skills")
    email = st.text_input("📧 Your Email to load skills")
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
                    session.delete(skill)
                    session.commit()
                    st.success(f"✅ Skill '{skill.title}' deleted successfully!")
                    st.experimental_rerun()  # Refresh page to update list
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("ℹ️ You have not added any skills yet.")
    else:
        st.warning("⚠️ Please enter a valid email to load your skills.")

# Footer
st.markdown("""
    <div class="footer">
        Made with ❤️ by Kanwal Rafiqe
    </div>
""", unsafe_allow_html=True)
