import streamlit as st
import re
import random

# 🚫 Common weak passwords to block
blacklist = ['password', '123456', 'admin', 'qwerty', 'abc123', 'password123']

# 🔐 Strong password generator
def suggest_strong_password(length=12):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# ✅ Strength Checker
def check_password_strength(password):
    score = 0
    feedback = []
    criteria = {
        "📏 At least 8 characters": len(password) >= 8,
        "🔡 Upper & lowercase letters": re.search(r"[A-Z]", password) and re.search(r"[a-z]", password),
        "🔢 Includes a number": re.search(r"\d", password),
        "🔒 Special character (!@#$%^&*)": re.search(r"[!@#$%^&*]", password),
        "🚫 Not a common/blacklisted password": password.lower() not in blacklist
    }

    # Score Calculation
    for passed in criteria.values():
        if passed:
            score += 1
    for rule, passed in criteria.items():
        if not passed:
            feedback.append(f"❌ {rule}")

    return score, feedback, criteria

# 🖥️ Streamlit UI
st.set_page_config("🔐 Password Strength Meter", page_icon="🔐")
st.title("🔐 Secure Password Strength Meter")
st.caption("Analyze your password strength in real time and get security tips 🛡️")

# 🔑 Input Password
password = st.text_input("🔑 Enter your password", type="password", placeholder="Type here...")

# 📊 Evaluation
if password:
    score, feedback, criteria = check_password_strength(password)

    # Strength Message
    if score == 5:
        st.success("✅ Strong Password! Well done 🔐")
    elif score >= 3:
        st.warning("⚠️ Moderate Password – Consider improving it 🔧")
    else:
        st.error("❌ Weak Password – Needs major improvements 🚨")

    # Score bar
    st.markdown(f"**Score:** `{score}/5`")
    st.progress(score / 5)

    # Rule Checklist
    st.subheader("📋 Password Criteria")
    for rule, passed in criteria.items():
        icon = "✅" if passed else "❌"
        st.write(f"{icon} {rule}")

    # Suggestions
    if feedback:
        st.subheader("💡 Suggestions to Improve")
        for tip in feedback:
            st.write("• " + tip)

    # Strong Password Generator
    if score < 5:
        st.subheader("🔑 Suggested Strong Password")
        suggestion = suggest_strong_password()
        st.code(suggestion)
        st.download_button("📥 Download Strong Password", suggestion, file_name="strong_password.txt")
