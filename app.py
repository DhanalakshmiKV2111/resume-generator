import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="Resume Parser", layout="centered")

st.title("📄 Resume Generator from LinkedIn PDF")

uploaded_file = st.file_uploader("Upload your LinkedIn resume PDF", type=["pdf"])

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if text.strip():
        st.success("✅ Resume text extracted successfully!")

        # Extracting Name (Assume name is in the first line)
        lines = text.splitlines()
        name = lines[0].strip() if lines else "Not found"

        # Email extraction
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        email = email_match.group(0) if email_match else "Not found"

        # Phone number extraction (Indian format)
        phone_match = re.search(r'(\+91[\s-]?)?[789]\d{9}', text)
        phone = phone_match.group(0) if phone_match else "Not found"

        # Extract skills (basic match from a list)
        skill_keywords = ['Python', 'Java', 'C++', 'C', 'SQL', 'AI', 'Machine Learning',
                          'Data Science', 'NLP', 'Flask', 'Django', 'IoT']
        found_skills = [skill for skill in skill_keywords if skill.lower() in text.lower()]
        skills = ', '.join(found_skills) if found_skills else "Not found"

        # Display extracted fields
        st.subheader("🔍 Extracted Resume Info")
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Phone:** {phone}")
        st.write(f"**Skills:** {skills}")

        # Show entire text
        with st.expander("📄 View Full Extracted Text"):
            st.text_area("Resume Text", text, height=300)

    else:
        st.warning("❌ Could not extract any text from the uploaded PDF.")
