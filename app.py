import hashlib
import io
import random
import re
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from xml.sax.saxutils import escape

st.set_page_config(page_title="FDM Print Quality Learning App", page_icon="🖨️", layout="wide")

st.title("FDM 3D Printing: Parameter Settings and Print Quality")
st.write("Explore the parameter effects, complete your assigned practical task, write conclusions, and attempt the MCQ assessment.")

st.header("Student details")
c1, c2 = st.columns(2)
with c1:
    student_name = st.text_input("Student name", placeholder="Enter your full name")
with c2:
    roll_number = st.text_input("Roll number", placeholder="Enter your roll number")

identity_ready = bool(student_name.strip() and roll_number.strip())
if identity_ready:
    seed_text = f"{student_name.strip().casefold()}|{roll_number.strip().casefold()}"
    seed_value = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:16], 16)
    rng = random.Random(seed_value)
else:
    seed_value = 0
    rng = random.Random(2026)

st.header("1. Set the printing parameters")
st.caption("Use the assigned ranges in Section 3. Adjust one parameter at a time and observe the effect in Section 2.")
left, right = st.columns(2)
with left:
    layer_height = st.select_slider(
        "Layer height (mm)", options=[0.08, 0.10, 0.12, 0.16, 0.20, 0.24, 0.28, 0.32], value=0.20
    )
    print_speed = st.slider("Print speed (mm/s)", min_value=20, max_value=100, value=50, step=5)
    nozzle_temp = st.slider("Nozzle temperature (°C) — PLA example", min_value=180, max_value=230, value=205, step=5)
with right:
    infill = st.slider("Infill (%)", min_value=0, max_value=100, value=20, step=5)
    cooling = st.select_slider("Part cooling fan (%)", options=[0, 25, 50, 75, 100], value=100)
    retraction = st.select_slider("Retraction", options=["Off", "On"], value="On")

st.header("2. Parameter effects")
cards = st.columns(3)
with cards[0]:
    st.metric("Layer height", f"{layer_height:.2f} mm")
    if layer_height <= 0.12:
        st.success("Fine layer detail; usually slower printing.")
    elif layer_height <= 0.20:
        st.info("Balanced detail and printing time.")
    else:
        st.warning("Faster printing; layer lines may be more visible.")
with cards[1]:
    st.metric("Print speed", f"{print_speed} mm/s")
    if print_speed <= 40:
        st.info("Slower speed can help detail, depending on the printer.")
    elif print_speed <= 60:
        st.success("Moderate speed; a useful starting range.")
    else:
        st.warning("Higher speed may cause ringing, weak details, or under-extrusion.")
with cards[2]:
    st.metric("Infill", f"{infill}%")
    if infill < 15:
        st.warning("Low internal support; the part may be less stiff.")
    elif infill <= 40:
        st.success("Moderate infill; balances material use and stiffness.")
    else:
        st.info("More internal material; usually increases mass and print time.")

st.subheader("Temperature, cooling and stringing")
t1, t2, t3 = st.columns(3)
with t1:
    if nozzle_temp < 195:
        st.warning("PLA temperature may be too low for some filaments, risking poor layer bonding.")
    elif nozzle_temp <= 215:
        st.success("Common PLA starting range; follow filament manufacturer guidance.")
    else:
        st.warning("Higher PLA temperature may increase stringing or ooze.")
with t2:
    if cooling >= 75:
        st.success("Higher cooling often helps small PLA features and bridges.")
    elif cooling >= 40:
        st.info("Moderate cooling; suitability depends on material and part.")
    else:
        st.warning("Low cooling can cause sagging on PLA overhangs.")
with t3:
    if retraction == "On":
        st.success("Retraction can reduce stringing during travel moves when tuned correctly.")
    else:
        st.warning("Retraction off may increase stringing.")
st.info("These are general learning guidelines. Actual results depend on the printer, material, geometry, and slicer settings.")

# Individualized task assignment. Student gets two parameter comparisons.
all_tasks = [
    {"parameter":"Layer height", "setting_a":"0.12 mm", "setting_b":"0.28 mm",
     "task":"Compare a low and a high layer height. Set each value in Section 1 separately and observe Section 2.",
     "focus":"surface finish, visible layer lines, and printing time"},
    {"parameter":"Print speed", "setting_a":"30 mm/s", "setting_b":"80 mm/s",
     "task":"Compare a low and a high print speed. Set each value in Section 1 separately and observe Section 2.",
     "focus":"detail, ringing risk, extrusion reliability, and printing time"},
    {"parameter":"Nozzle temperature (PLA)", "setting_a":"190 °C", "setting_b":"220 °C",
     "task":"Compare a lower and a higher PLA nozzle temperature. Set each value in Section 1 separately and observe Section 2.",
     "focus":"layer bonding, stringing, and material flow"},
    {"parameter":"Infill", "setting_a":"10%", "setting_b":"60%",
     "task":"Compare a low and a high infill percentage. Set each value in Section 1 separately and observe Section 2.",
     "focus":"material use, internal support, stiffness, and print time"},
    {"parameter":"Part cooling fan", "setting_a":"25%", "setting_b":"100%",
     "task":"Compare low and high part cooling. Set each value in Section 1 separately and observe Section 2.",
     "focus":"small features, bridges, and overhang shape"},
    {"parameter":"Retraction", "setting_a":"Off", "setting_b":"On",
     "task":"Compare retraction off and on. Set each value in Section 1 separately and observe Section 2.",
     "focus":"stringing and ooze during travel moves"},
]
if identity_ready:
    task_rng = random.Random(seed_value ^ 0xF0D)
    # Assign five different practical tasks to each student from the task bank.
    assigned_tasks = task_rng.sample(all_tasks, 5)
else:
    assigned_tasks = all_tasks[:5]

st.header("3. Individual practical assignment and conclusions")
if not identity_ready:
    st.warning("Enter your name and roll number above to receive your individual parameter assignment.")
else:
    st.write("Complete all five assigned comparisons. For each task, adjust the parameter in Section 1 to Setting A, read Section 2, then adjust it to Setting B. Compare the effects and write a short conclusion.")
    conclusion_values = []
    for i, task in enumerate(assigned_tasks, start=1):
        with st.container(border=True):
            st.subheader(f"Task {i}: {task['parameter']}")
            st.markdown(f"**Assignment:** {task['task']}")
            st.markdown(f"**Setting A:** {task['setting_a']}  |  **Setting B:** {task['setting_b']}")
            st.markdown(f"**Compare:** {task['focus']}.")
            st.caption("Remember: set the values one at a time in Section 1. Section 2 updates automatically when the app reruns.")
            conclusion = st.text_area(
                f"Write your short conclusion for Task {i}",
                key=f"conclusion_{seed_value}_{i}",
                placeholder="Compare Setting A with Setting B. Explain how the parameter may affect print quality and why.",
                height=100
            )
            conclusion_values.append(conclusion)

st.header("4. Assessment — 15 MCQs")
st.write("Answer all 15 questions and submit to calculate your score. Your PDF report will include your answers and results.")

mcq_bank = [
    ("Which layer height generally gives finer visible detail?", ["0.32 mm", "0.28 mm", "0.08 mm", "0.30 mm"], 2, "Smaller layer heights generally produce finer vertical detail."),
    ("What can happen when print speed is set too high?", ["Ringing or under-extrusion", "Automatic calibration", "No material use", "Guaranteed stronger bonding"], 0, "High speed can exceed the printer's motion or extrusion capability."),
    ("What is a possible result of PLA nozzle temperature being too low?", ["Weak layer bonding", "Increased infill automatically", "No visible layers", "The part becomes metallic"], 0, "Too-low temperature can reduce material flow and layer adhesion."),
    ("Which setting controls the proportion of the part's internal fill?", ["Retraction", "Nozzle temperature", "Infill percentage", "Fan speed"], 2, "Infill percentage controls the amount of internal fill."),
    ("Why is part cooling commonly used for PLA?", ["To help features and bridges solidify", "To heat the nozzle", "To increase layer height", "To change the CAD model"], 0, "Cooling helps PLA retain shape on small features and bridges."),
    ("What is one purpose of retraction?", ["Reduce stringing during travel moves", "Increase infill", "Change nozzle diameter", "Level the bed"], 0, "Retraction can reduce ooze while the nozzle travels between regions."),
    ("Which is the best starting point for choosing nozzle temperature?", ["Always use 230 °C", "Use the filament manufacturer's recommended range", "Choose the lowest possible temperature", "Temperature never matters"], 1, "Temperature requirements vary by filament type and formulation."),
    ("Reducing layer height while keeping part height the same usually means:", ["Fewer layers", "More layers", "No layers", "Larger nozzle diameter"], 1, "A smaller layer height means more layers for the same part height."),
    ("What is a likely effect of increasing infill?", ["More material use and often greater stiffness", "Always less material use", "No effect on the interior", "Automatic surface smoothing"], 0, "More infill generally increases material use and may increase stiffness."),
    ("What can very low cooling cause on PLA overhangs?", ["Sagging", "Higher infill", "Lower nozzle temperature automatically", "Fewer layers"], 0, "Insufficient cooling can make overhangs sag before the material solidifies."),
    ("A high layer height can make layer lines more:", ["Visible", "Invisible in all cases", "Strongly bonded in every case", "Cool"], 0, "Larger layer steps are often more visible on the surface."),
    ("Which parameter has the most direct relationship with internal fill amount?", ["Infill", "Retraction", "Cooling", "Nozzle temperature"], 0, "Infill is the direct setting for internal fill percentage."),
    ("Why might very high nozzle temperature increase stringing?", ["It can increase ooze", "It removes all filament", "It disables extrusion", "It always lowers flow"], 0, "Hotter material can ooze more during travel moves, depending on the filament."),
    ("What is a sensible way to study one parameter's effect?", ["Change several settings at once", "Change one setting at a time", "Ignore the settings", "Use random values without recording"], 1, "Changing one variable at a time makes its effect easier to identify."),
    ("Why are the app's quality statements general guidelines?", ["Real results depend on printer, material, and geometry", "All printers behave identically", "The app uses a physical test printer for every setting", "Quality never changes"], 0, "Real print quality depends on multiple interacting factors.")
]
if identity_ready:
    mcq_rng = random.Random(seed_value ^ 0x15C0)
    selected_mcqs = mcq_rng.sample(mcq_bank, 15)
else:
    selected_mcqs = mcq_bank[:15]

mcq_answers = []
if identity_ready:
    with st.form("mcq_form"):
        for i, (question, options, correct, explanation) in enumerate(selected_mcqs, start=1):
            shuffled_options = list(enumerate(options))
            random.Random(seed_value + i * 71).shuffle(shuffled_options)
            option_labels = [opt for original_idx, opt in shuffled_options]
            correct_text = options[correct]
            chosen = st.radio(f"Q{i}. {question}", option_labels, index=None, key=f"mcq_answer_{seed_value}_{i}")
            mcq_answers.append({"question": question, "options": options, "correct": correct, "correct_text": correct_text, "explanation": explanation, "chosen": chosen})
        submitted = st.form_submit_button("Submit MCQs and Generate Report")
else:
    st.info("Enter your name and roll number to unlock the personalized assignment and MCQ assessment.")
    submitted = False

if identity_ready and submitted:
    missing = any(not a["chosen"] for a in mcq_answers)
    if missing:
        st.warning("Please answer all 15 MCQs before submitting.")
    elif any(not x.strip() for x in conclusion_values):
        st.warning("Please write a short conclusion for both assigned tasks before submitting.")
    else:
        score = sum(a["chosen"] == a["correct_text"] for a in mcq_answers)
        st.session_state["assessment_result"] = {
            "name": student_name.strip(),
            "roll": roll_number.strip(),
            "settings": {
                "Layer height": f"{layer_height:.2f} mm",
                "Print speed": f"{print_speed} mm/s",
                "Nozzle temperature (PLA example)": f"{nozzle_temp} °C",
                "Infill": f"{infill}%",
                "Part cooling fan": f"{cooling}%",
                "Retraction": retraction,
            },
            "tasks": [
                {"parameter": t["parameter"], "setting_a": t["setting_a"], "setting_b": t["setting_b"],
                 "focus": t["focus"], "conclusion": conclusion_values[i]}
                for i, t in enumerate(assigned_tasks)
            ],
            "score": score,
            "mcqs": mcq_answers,
        }

result = st.session_state.get("assessment_result")
if result and result["name"].casefold() == student_name.strip().casefold() and result["roll"].casefold() == roll_number.strip().casefold():
    st.subheader(f"MCQ score: {result['score']}/15")
    st.progress(result["score"] / 15)
    if result["score"] >= 12:
        st.success("Excellent understanding of FDM parameter settings.")
    elif result["score"] >= 8:
        st.info("Good attempt. Review the answer explanations in your report.")
    else:
        st.warning("Review Sections 1 and 2 and try again.")

    def make_pdf(data):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=14*mm, leftMargin=14*mm,
                                topMargin=14*mm, bottomMargin=14*mm)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("FDM 3D Printing — Practical Assignment and Assessment Report", styles["Title"]),
            Spacer(1, 8),
            Paragraph(f"<b>Student name:</b> {escape(data['name'])}", styles["Normal"]),
            Paragraph(f"<b>Roll number:</b> {escape(data['roll'])}", styles["Normal"]),
            Paragraph(f"<b>MCQ score:</b> {data['score']}/15", styles["Normal"]),
            Spacer(1, 10),
            Paragraph("Section 1 — Selected parameter settings", styles["Heading2"]),
        ]
        settings_data = [["Parameter", "Selected value"]] + [[k, v] for k, v in data["settings"].items()]
        settings_table = Table(settings_data, colWidths=[78*mm, 75*mm], repeatRows=1)
        settings_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey), ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("VALIGN", (0,0), (-1,-1), "TOP"), ("FONTSIZE", (0,0), (-1,-1), 9), ("PADDING", (0,0), (-1,-1), 5)
        ]))
        story += [settings_table, Spacer(1, 10), Paragraph("Section 3 — Assigned parameter comparisons and conclusions", styles["Heading2"])]
        for idx, task in enumerate(data["tasks"], 1):
            story.append(Paragraph(f"<b>Task {idx}: {escape(task['parameter'])}</b>", styles["Heading3"]))
            story.append(Paragraph(f"Setting A: {escape(task['setting_a'])} &nbsp;&nbsp; Setting B: {escape(task['setting_b'])}", styles["Normal"]))
            story.append(Paragraph(f"Focus: {escape(task['focus'])}", styles["Normal"]))
            story.append(Paragraph(f"<b>Student conclusion:</b> {escape(task['conclusion'])}", styles["BodyText"]))
            story.append(Spacer(1, 7))
        story.append(Paragraph("Section 4 — MCQ assessment", styles["Heading2"]))
        mcq_data = [["No.", "Question", "Student answer", "Correct answer", "Result"]]
        for idx, item in enumerate(data["mcqs"], 1):
            mcq_data.append([
                str(idx), Paragraph(escape(item["question"]), styles["BodyText"]),
                Paragraph(escape(item["chosen"] or "Not answered"), styles["BodyText"]),
                Paragraph(escape(item["correct_text"]), styles["BodyText"]),
                "Correct" if item["chosen"] == item["correct_text"] else "Incorrect"
            ])
        mcq_table = Table(mcq_data, colWidths=[8*mm, 58*mm, 32*mm, 32*mm, 20*mm], repeatRows=1)
        mcq_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey), ("GRID", (0,0), (-1,-1), 0.35, colors.grey),
            ("VALIGN", (0,0), (-1,-1), "TOP"), ("FONTSIZE", (0,0), (-1,-1), 7),
            ("LEFTPADDING", (0,0), (-1,-1), 3), ("RIGHTPADDING", (0,0), (-1,-1), 3),
            ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4)
        ]))
        story += [mcq_table, Spacer(1, 8), Paragraph("Answer explanations", styles["Heading2"])]
        for idx, item in enumerate(data["mcqs"], 1):
            story.append(Paragraph(f"<b>Q{idx}.</b> {escape(item['explanation'])}", styles["BodyText"]))
        story += [Spacer(1, 8), Paragraph("Note: FDM quality guidance is general. Real results depend on printer calibration, filament, geometry, cooling, and slicer settings.", styles["Italic"])]
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    pdf_data = make_pdf(result)
    safe_roll = re.sub(r"[^A-Za-z0-9_-]", "_", result["roll"])
    st.download_button(
        "Print / Download Student Report (PDF)",
        data=pdf_data,
        file_name=f"FDM_Print_Quality_Report_{safe_roll}.pdf",
        mime="application/pdf",
        type="primary"
    )

st.caption("Educational use only. Follow the printer manual and filament manufacturer's recommended settings.")

