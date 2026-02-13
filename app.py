import streamlit as st
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
import tempfile
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="GenAI Curriculum Generator", layout="wide")

st.title("🎓 GenAI Curriculum Generator")
st.markdown("AI-Powered Curriculum Design using Google Gemini")

# -----------------------------
# SIDEBAR - AIzaSyBHd6m9W8ea-_naP_HoWB_sYAq8ALNCn9Q
# -----------------------------
st.sidebar.header("AIzaSyBHd6m9W8ea-_naP_HoWB_sYAq8ALNCn9Q" \
"" \
"")
api_key = st.sidebar.text_input("Enter API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.warning("Please enter your Google AI Studio API key in sidebar.")
    st.stop()

# -----------------------------
# USER INPUT SECTION
# -----------------------------
st.header("📚 Curriculum Inputs")

col1, col2 = st.columns(2)

with col1:
    skill = st.text_input("Skill / Domain", "Machine Learning")
    level = st.selectbox("Education Level", ["Diploma", "BTech", "Masters", "Certification"])
    semesters = st.number_input("Number of Semesters", 1, 8, 4)

with col2:
    weekly_hours = st.text_input("Weekly Hours", "20-25")
    industry_focus = st.text_input("Industry Focus", "AI")

generate = st.button("🚀 Generate Curriculum")

# -----------------------------
# GENERATION LOGIC
# -----------------------------
if generate:

    prompt = f"""
    Design a complete academic curriculum.

    Skill: {skill}
    Level: {level}
    Semesters: {semesters}
    Weekly Hours: {weekly_hours}
    Industry Focus: {industry_focus}

    Generate:
    - Semester wise course structure
    - 4-6 subjects per semester
    - Each subject should include 5-7 topics
    - Learning outcomes
    - Capstone project suggestion
    - Credits per subject
    """

    with st.spinner("Generating curriculum using Gemini..."):
        response = model.generate_content(prompt)
        curriculum_text = response.text

    st.success("Curriculum Generated Successfully!")

    st.subheader("📖 Generated Curriculum")
    st.write(curriculum_text)

    # -----------------------------
    # PDF GENERATION
    # -----------------------------
    def generate_pdf(text):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = SimpleDocTemplate(temp_file.name)
        elements = []

        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]

        for line in text.split("\n"):
            elements.append(Paragraph(line, normal_style))
            elements.append(Spacer(1, 0.2 * inch))

        doc.build(elements)
        return temp_file.name

    pdf_path = generate_pdf(curriculum_text)

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Download PDF",
            data=f,
            file_name="Curriculum.pdf",
            mime="application/pdf"
        )

    os.remove(pdf_path)