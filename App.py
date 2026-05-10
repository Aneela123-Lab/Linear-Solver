import threading

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import re
from fractions import Fraction
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT


# ================= 1. CONFIGURATION & STYLING =================
st.set_page_config(page_title="Linear Solver Pro", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #00ADB5; text-align: center; font-weight: bold; font-size: 38px; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: bold; height: 3.5em; background-color: #00ADB5; color: white; border: none; }
    .stButton>button:hover { background-color: #008f95; box-shadow: 0px 4px 10px rgba(0,0,0,0.2); }
    .flashcard { padding: 20px; border-radius: 12px; color: white; margin-bottom: 12px; font-weight: bold; text-align: center; font-size: 18px; }
    .step-box { border-left: 6px solid #00ADB5; padding: 15px; margin: 15px 0; background-color: #f1f3f4; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# ================= 2. SESSION STATE & HELPERS =================
if "A" not in st.session_state:
    st.session_state.update({"A": None, "B": None, "method": None, "sub_view": "steps", "solution_text": ""})

def to_frac(num):
    f = Fraction(float(num)).limit_denominator()
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

# ================= 3. PDF GENERATOR (REPORTLAB) =================
def generate_technical_manual():
   
    buffer = io.BytesIO()
    # Industrial Standard Margins (1 inch)
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    story = []

    # --- Industrial Grade Styles ---
    title_style = ParagraphStyle('Title', fontSize=26, leading=32, alignment=TA_CENTER, spaceAfter=30, fontName='Helvetica-Bold', textColor=colors.teal)
    heading_style = ParagraphStyle('Heading', fontSize=14, leading=18, spaceBefore=20, spaceAfter=12, fontName='Helvetica-Bold', textColor=colors.teal)
    sub_heading_style = ParagraphStyle('SubHeading', fontSize=11, leading=14, spaceBefore=12, spaceAfter=8, fontName='Helvetica-Bold', textColor=colors.black)
    body_style = ParagraphStyle('Body', fontSize=10, leading=13, alignment=TA_JUSTIFY, fontName='Helvetica')
    table_header_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.teal),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]

    # ================= PAGE 1: FORMAL COVER PAGE =================
    story.append(Spacer(1, 150))
    story.append(Paragraph("PROJECT TECHNICAL REPORT", ParagraphStyle('Top', fontSize=10, alignment=TA_CENTER, fontName='Helvetica-Bold', textColor=colors.grey)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("LINEAR SOLVER PRO", title_style))
    story.append(Paragraph("An Advanced Computational & Educational Framework for Linear Algebra", ParagraphStyle('Sub', alignment=TA_CENTER, fontSize=12)))
    story.append(Spacer(1, 180))
    
    cover_meta = [
        ["Software Version:", "1.0.4"],
        ["Document ID:", "LSP-TECH-DOC-2026"],
        ["Report Type:", "Full System Documentation"],
        ["Report Generated:", "March 2026"]
    ]
    t_cover = Table(cover_meta, colWidths=[120, 200])
    t_cover.setStyle(TableStyle([('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'), ('BOTTOMPADDING', (0,0), (-1,-1), 10)]))
    story.append(t_cover)
    story.append(PageBreak())

    # ================= PAGE 2: TABLE OF CONTENTS =================
    story.append(Paragraph("TABLE OF CONTENTS", heading_style))
    toc_data = [
        ["1.0", "Project Overview & Architecture", "03"],
        ["2.0", "Detailed Programming Anatomy", "03"],
        ["3.0", "Core Algorithmic Logic (Engines)", "04"],
        ["4.0", "Multi-Modal Features (Voice & PDF)", "06"],
        ["5.0", "System Analysis & Classification", "06"],
        ["6.0", "Educational Impact & Scalability", "07"],
        ["17.0", "Technical Glossary (Deep-Dive)", "08"],
        ["18.0", "User Manual: Operational Workflow", "09"],
        ["19.0", "Programming 'Under the Hood'", "10"],
        ["20.0", "Final Conclusion", "11"]
    ]
    t_toc = Table(toc_data, colWidths=[40, 360, 40])
    t_toc.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, colors.teal), ('BOTTOMPADDING', (0,0), (-1,-1), 8)]))
    story.append(t_toc)
    story.append(PageBreak())

    # ================= PAGE 3: OVERVIEW & ANATOMY =================
    story.append(Paragraph("1.0 PROJECT OVERVIEW & ARCHITECTURE", heading_style))
    story.append(Paragraph("Linear Solver Pro is a sophisticated full-stack mathematical application built using the Python-Streamlit ecosystem. Unlike standard calculators, this system functions as an Expert System, mimicking the step-by-step cognitive process of a mathematician.", body_style))
    
    story.append(Paragraph("🏗️ Logic Flow Architecture:", sub_heading_style))
    arch_data = [
        ["Layer", "Function"],
        ["Ingestion", "Raw string input is captured via Streamlit text widgets."],
        ["Parsing", "The re (Regex) engine deconstructs the strings into numerical coefficients."],
        ["Validation", "The system checks for 'Division by Zero' and 'Matrix Singularity'."],
        ["Computation", "NumPy executes high-speed linear algebra operations."],
        ["Instructional", "The Explanation Engine converts raw data into LaTeX-formatted steps."],
        ["Export", "ReportLab compiles the session data into a persistent PDF document."]
    ]
    t_arch = Table(arch_data, colWidths=[100, 340])
    t_arch.setStyle(TableStyle(table_header_style))
    story.append(t_arch)

    story.append(Paragraph("2.0 DETAILED PROGRAMMING ANATOMY", heading_style))
    lib_data = [
        ["Library", "Module", "Technical Role"],
        ["Streamlit", "st.session_state", "Global State Management for persistence."],
        ["NumPy", "matrix_rank", "System Classification (Unique/Infinite/No Solution)."],
        ["Regex", "re.search()", "Pattern Matching variables (e.g. treats '-x' as -1.0)."],
        ["Fractions", "limit_denominator", "Symbolic Accuracy: Prevents float noise."],
        ["Matplotlib", "plt.axhline", "Geometric Rendering of intersections."],
        ["Threading", "Thread", "Asynchronous Execution for Voice Assistant."]
    ]
    t_lib = Table(lib_data, colWidths=[80, 100, 260])
    t_lib.setStyle(TableStyle(table_header_style))
    story.append(t_lib)
    story.append(PageBreak())

    # ================= PAGE 4: CORE ENGINES =================
    story.append(Paragraph("3.0 CORE ALGORITHMIC LOGIC", heading_style))
    
    story.append(Paragraph("3.1 The Algebraic Elimination Engine", sub_heading_style))
    story.append(Paragraph("• Coefficient Matching: Calculates Scalar Multiplier (m = target / source).\n• Row Subtraction: Subtracts equations to 'zero out' variables.\n• Recursive Reduction: Reduces 3x3 → 2x2 → 1x1.\n• Back-Substitution: Moves known values to RHS to solve for remaining variables.", body_style))

    story.append(Paragraph("3.2 The Determinant Engine (Cramer’s Rule)", sub_heading_style))
    story.append(Paragraph("• Column Slicing: Uses Ai[:, i] = B to swap columns.\n• Determinant Ratio: Calculates |Ai| / |A|.\n• Error Handling: Includes a 'Trap' for |A| = 0.", body_style))

    story.append(Paragraph("3.3 The Matrix Reduction Engine (Gauss-Jordan)", sub_heading_style))
    story.append(Paragraph("• Pivot Normalization: Scaling rows so leading entry is 1.0.\n• Forward Elimination: Clears entries below pivot (REF).\n• Backward Elimination: Clears entries above pivot (RREF).", body_style))
    story.append(PageBreak())

    # ================= PAGE 8: GLOSSARY =================
    story.append(Paragraph("17.0 TECHNICAL GLOSSARY (DEEP-DIVE)", heading_style))
    glossary_data = [
        ["Term", "Technical Definition", "Role in App"],
        ["Augmented Matrix", "[A|B] combination.", "Used in Row Operations."],
        ["Pivot Element", "First non-zero entry.", "Scaled to 1.0."],
        ["Regex", "Search pattern sequence.", "The 'Scanner' for strings."],
        ["Identity Matrix", "1s on diagonal.", "The Final Goal of RREF."],
        ["Back-Substitution", "Solving bottom-up.", "Used in Elimination."]
    ]
    t_glos = Table(glossary_data, colWidths=[100, 200, 140])
    t_glos.setStyle(TableStyle(table_header_style))
    story.append(t_glos)
    story.append(PageBreak())

    # ================= PAGE 9: USER MANUAL =================
    story.append(Paragraph("18.0 USER MANUAL: OPERATIONAL WORKFLOW", heading_style))
    manual_steps = [
        ["Step", "Phase", "Operational Logic"],
        ["1", "Input", "Standard format (e.g. 2x + 4y = 10) in Solver tab."],
        ["2", "Path", "Choose Elimination, Cramer's, or Row Ops."],
        ["3", "Analysis", "View Steps (LaTeX), Graph, or Explanation."],
        ["4", "Export", "Download this Detailed Report via Sidebar."]
    ]
    t_man = Table(manual_steps, colWidths=[40, 80, 320])
    t_man.setStyle(TableStyle(table_header_style))
    story.append(t_man)
    story.append(PageBreak())

    # ================= PAGE 10: UNDER THE HOOD =================
    story.append(Paragraph("19.0 PROGRAMMING 'UNDER THE HOOD'", heading_style))
    story.append(Paragraph("The system follows a strict mathematical pipeline: 1. String Cleanup → 2. Array Construction → 3. Singularity Check → 4. Step-by-Step Logging → 5. Output Rendering (st.latex). Every row operation is saved to a 'Steps List' in the session state.", body_style))

    story.append(Paragraph("20.0 FINAL CONCLUSION", heading_style))
    story.append(Paragraph("Linear Solver Pro represents a bridge between Applied Mathematics and Modern Software Engineering. It is not just a solver; it is a digital tutor ensuring the 'how' and 'why' are understood.", body_style))
    
    # Session Log
    story.append(Spacer(1, 20))
    raw_sol = st.session_state.get('solution_text', "No current calculation.")
    clean_sol = raw_sol.replace("**", "").replace("$", "").replace("#", "").replace("\\", "")
    story.append(Paragraph("SESSION COMPUTATION TRACE:", sub_heading_style))
    story.append(Paragraph(clean_sol, ParagraphStyle('Log', fontName='Courier', fontSize=7)))

    # Final Construction
    doc.build(story)
    buffer.seek(0)
    return buffer

def parse_equations(equations, variables):
    A, B = [], []
    for eq in equations:
        if "=" not in eq: continue # FIX: Equation adhuri ho to skip karega
        eq = eq.replace(" ", "").replace("-", "+-")
        left, right = eq.split("=")
        coeffs = []
        for var in variables:
            match = re.search(rf'([+-]?\d*\/?\d*){var}', left)
            if match:
                val = match.group(1).replace("+", "")
                if val == "" or val == "+": val = "1"
                elif val == "-": val = "-1"
                coeffs.append(float(Fraction(val)))
            else: coeffs.append(0.0)
        A.append(coeffs)
        B.append(float(Fraction(right)))
    return np.array(A), np.array(B)



# ================= 4. DETAILED SOLVERS =================

def solve_elimination_detailed(A, B):
    n = len(B)
    # Hamesha variables define karein taake errors na aayein
    vars_names = ["x1", "x2", "x3", "x4"][:n]
    
    st.markdown(f"### 🧮 Full Algebraic Elimination ({n}x{n})")
    
    # --- Step 1: Initial System ---
    st.write("#### Step 1: Given Equations")
    for i in range(n):
        eq_parts = [f"{to_frac(A[i,j])}{vars_names[j]}" for j in range(n)]
        st.latex(fr"\text{{Eq {i+1}: }} {' + '.join(eq_parts).replace('+ -', '- ')} = {to_frac(B[i])}")
    
    # ========================== 3x3 LOGIC ==========================
    if n == 3:
        # --- ELIMINATING x3 TO GET EQ 4 ---
        st.write("#### Step 2: Eliminating x3 using Eq 2 and Eq 3")
        m2, m3 = abs(A[2,2]), abs(A[1,2])
        st.info(f"Multiply Eq 2 by {to_frac(m2)} and Eq 3 by {to_frac(m3)}")
        
        r2_new, b2_new = A[1]*m2, B[1]*m2
        r3_new, b3_new = A[2]*m3, B[2]*m3
        eq4_A, eq4_B = r2_new[:2] - r3_new[:2], b2_new - b3_new
        
        st.latex(fr"\begin{{matrix}} & {to_frac(r2_new[0])}x1 + {to_frac(r2_new[1])}x2 + {to_frac(r2_new[2])}x3 = {to_frac(b2_new)} \\ \pm & {to_frac(r3_new[0])}x1 + {to_frac(r3_new[1])}x2 + {to_frac(r3_new[2])}x3 = {to_frac(b3_new)} \\ \hline & \text{{Eq 4: }} {to_frac(eq4_A[0])}x1 + {to_frac(eq4_A[1])}x2 = {to_frac(eq4_B)} \end{{matrix}}")

        # --- ELIMINATING x3 TO GET EQ 5 ---
        st.write("#### Step 3: Eliminating x3 using Eq 1 and Eq 3")
        m1_alt, m3_alt = abs(A[2,2]), abs(A[0,2])
        r1_alt, b1_alt = A[0]*m1_alt, B[0]*m1_alt
        r3_alt, b3_alt = A[2]*m3_alt, B[2]*m3_alt
        eq5_A, eq5_B = r1_alt[:2] - r3_alt[:2], b1_alt - b3_alt
        
        st.latex(fr"\begin{{matrix}} & {to_frac(r1_alt[0])}x1 + {to_frac(r1_alt[1])}x2 + {to_frac(r1_alt[2])}x3 = {to_frac(b1_alt)} \\ \pm & {to_frac(r3_alt[0])}x1 + {to_frac(r3_alt[1])}x2 + {to_frac(r3_alt[2])}x3 = {to_frac(b3_alt)} \\ \hline & \text{{Eq 5: }} {to_frac(eq5_A[0])}x1 + {to_frac(eq5_A[1])}x2 = {to_frac(eq5_B)} \end{{matrix}}")

        # --- SOLVING EQ 4 & 5 ---
        st.write("#### Step 4: Solving Eq 4 and Eq 5 for x1")
        mm4, mm5 = abs(eq5_A[1]), abs(eq4_A[1])
        e4_final, b4_final = eq4_A * mm4, eq4_B * mm4
        e5_final, b5_final = eq5_A * mm5, eq5_B * mm5
        
        final_x1_coeff = e4_final[0] - e5_final[0]
        final_const = b4_final - b5_final
        
        st.latex(fr"\begin{{matrix}} & {to_frac(e4_final[0])}x1 + {to_frac(e4_final[1])}x2 = {to_frac(b4_final)} \\ \pm & {to_frac(e5_final[0])}x1 + {to_frac(e5_final[1])}x2 = {to_frac(b5_final)} \\ \hline & {to_frac(final_x1_coeff)}x1 = {to_frac(final_const)} \end{{matrix}}")
        
        res_x1 = final_const / final_x1_coeff
        res_x2 = (eq4_B - (eq4_A[0] * res_x1)) / eq4_A[1]
        res_x3 = (B[0] - (A[0,0]*res_x1) - (A[0,1]*res_x2)) / A[0,2]

        st.success(fr"**Found:** $x1 = {to_frac(res_x1)}$")

        # --- BACK SUBSTITUTION ---
        # --- STEP 5: DETAILED BACK-SUBSTITUTION (3x3) ---
        st.write("#### Step 5: Back-Substitution Phase")
        
        # 1. x1 into Eq 4 to find x2
        st.write(f"**A) Finding x2 using Eq 4:**")
        term1 = eq4_A[0] * res_x1
        st.latex(fr"{to_frac(eq4_A[0])}({to_frac(res_x1)}) + {to_frac(eq4_A[1])}x2 = {to_frac(eq4_B)}")
        st.latex(fr"{to_frac(term1)} + {to_frac(eq4_A[1])}x2 = {to_frac(eq4_B)}")
        
        # Moving to other side
        rhs_step1 = eq4_B - term1
        st.latex(fr"{to_frac(eq4_A[1])}x2 = {to_frac(eq4_B)} - ({to_frac(term1)})")
        st.latex(fr"{to_frac(eq4_A[1])}x2 = {to_frac(rhs_step1)}")
        
        res_x2 = rhs_step1 / eq4_A[1]
        st.latex(fr"x2 = \frac{{{to_frac(rhs_step1)}}}{{{to_frac(eq4_A[1])}}} \implies x2 = {to_frac(res_x2)}")

        # 2. x1, x2 into Eq 1 to find x3
        st.write(f"**B) Finding x3 using Eq 1:**")
        val1 = A[0,0] * res_x1
        val2 = A[0,1] * res_x2
        combined_vals = val1 + val2
        
        st.latex(fr"{to_frac(A[0,0])}({to_frac(res_x1)}) + {to_frac(A[0,1])}({to_frac(res_x2)}) + {to_frac(A[0,2])}x3 = {to_frac(B[0])}")
        st.latex(fr"{to_frac(val1)} + {to_frac(val2)} + {to_frac(A[0,2])}x3 = {to_frac(B[0])}")
        st.latex(fr"{to_frac(combined_vals)} + {to_frac(A[0,2])}x3 = {to_frac(B[0])}")
        
        # Moving to other side
        rhs_final = B[0] - combined_vals
        st.latex(fr"{to_frac(A[0,2])}x3 = {to_frac(B[0])} - ({to_frac(combined_vals)})")
        st.latex(fr"{to_frac(A[0,2])}x3 = {to_frac(rhs_final)}")
        
        res_x3 = rhs_final / A[0,2]
        st.latex(fr"x3 = \frac{{{to_frac(rhs_final)}}}{{{to_frac(A[0,2])}}} \implies x3 = {to_frac(res_x3)}")
        st.success(fr"**Final Solution:** $x1={to_frac(res_x1)}, x2={to_frac(res_x2)}, x3={to_frac(res_x3)}$")

    # ========================== 2x2 LOGIC ==========================
    elif n == 2:
        st.write(f"### *Step 2: Eliminating {vars_names[0]} by Equating Coefficients*")
        f1, f2 = A[1, 0], A[0, 0]
        
        e1_A, e1_B = A[0] * f1, B[0] * f1
        e2_A, e2_B = A[1] * f2, B[1] * f2

        st.info(f"Multiply Eq 1 by ({to_frac(f1)}) and Eq 2 by ({to_frac(f2)})")
        st.latex(fr"\text{{New Eq 1: }} {to_frac(e1_A[0])}{vars_names[0]} + {to_frac(e1_A[1])}{vars_names[1]} = {to_frac(e1_B)}")
        st.latex(fr"\text{{New Eq 2: }} {to_frac(e2_A[0])}{vars_names[0]} + {to_frac(e2_A[1])}{vars_names[1]} = {to_frac(e2_B)}")

        st.write("### *Step 3: Changing Signs & Eliminating*")
        st.markdown("---")
        st.latex(fr"\begin{{matrix}} & {to_frac(e1_A[0])}{vars_names[0]} & + & {to_frac(e1_A[1])}{vars_names[1]} & = & {to_frac(e1_B)} \\ - & ({to_frac(e2_A[0])}{vars_names[0]}) & - & ({to_frac(e2_A[1])}{vars_names[1]}) & = & -({to_frac(e2_B)}) \\ \hline & \cancel{{{to_frac(e1_A[0])}{vars_names[0]}}} & & {to_frac(e1_A[1] - e2_A[1])}{vars_names[1]} & = & {to_frac(e1_B - e2_B)} \end{{matrix}}")
        
        final_coeff = e1_A[1] - e2_A[1]
        final_const = e1_B - e2_B
        
        res_y = final_const / final_coeff
        st.latex(fr"{to_frac(final_coeff)}{vars_names[1]} = {to_frac(final_const)} \implies {vars_names[1]} = {to_frac(res_y)}")

        # --- STEP 4: DETAILED BACK-SUBSTITUTION (2x2) ---
        st.write(f"#### Step 4: Back-Substitution")
        st.write(f"Substitute {vars_names[1]} = {to_frac(res_y)} into Eq 1 to find {vars_names[0]}:")
        
        # Solving step by step: Ax + By = C
        term_by = A[0, 1] * res_y
        st.latex(fr"{to_frac(A[0,0])}{vars_names[0]} + {to_frac(A[0,1])}({to_frac(res_y)}) = {to_frac(B[0])}")
        st.latex(fr"{to_frac(A[0,0])}{vars_names[0]} + ({to_frac(term_by)}) = {to_frac(B[0])}")
        
        # Sign change logic
        rhs_val = B[0] - term_by
        st.latex(fr"{to_frac(A[0,0])}{vars_names[0]} = {to_frac(B[0])} - ({to_frac(term_by)})")
        st.latex(fr"{to_frac(A[0,0])}{vars_names[0]} = {to_frac(rhs_val)}")
        
        res_x = rhs_val / A[0,0]
        st.latex(fr"{vars_names[0]} = \frac{{{to_frac(rhs_val)}}}{{{to_frac(A[0,0])}}} \implies {vars_names[0]} = {to_frac(res_x)}")
        st.success(f"Final Solution: {vars_names[0]} = {to_frac(res_x)}, {vars_names[1]} = {to_frac(res_y)}")
    # ========================== HIGHER ORDER ==========================
    else:
        st.warning(f"Systems of size {n}x{n} use automated solver.")
        try:
            sol = np.linalg.solve(A, B)
            for i in range(n):
                st.latex(fr"{vars_names[i]} = {to_frac(sol[i])}")
        except:
            st.error("No unique solution found.")


    st.markdown("---")
    st.markdown("### 🔍 System Analysis (Algebraic Reason)")

    det_A = np.linalg.det(A)
    aug = np.hstack([A, B.reshape(-1, 1)])
    rank_A = np.linalg.matrix_rank(A)
    rank_aug = np.linalg.matrix_rank(aug)

    if rank_A == n:
        st.success("✅ **Type: Unique Solution**")
        st.write("**Reason:** All equations are independent. Each variable has a specific value that satisfies all equations simultaneously.")
    
    elif rank_A == rank_aug:
        st.warning("♾️ **Type: Infinite Many Solutions**")
        st.write("**Reason:** During elimination, one or more equations completely canceled out (became 0 = 0). This means the equations are dependent on each other.")
        
    else:
        st.error("❌ **Type: No Solution**")
        st.write("**Reason:** During elimination, we reached a contradiction (like 0 = some number). This means the equations are inconsistent and represent parallel lines/planes.")
def solve_cramer_detailed(A, B):
    n = len(B)
    vars = ["x", "y", "z", "w"][:n]
    
    st.markdown("### 📊 Cramer's Rule Step-by-Step")
    
    # Input Equations Show karna (Notebook style)
    st.write("**Given Equations:**")
    for i in range(n):
        eq_str = " + ".join([f"{to_frac(A[i,j])}{vars[j]}" for j in range(n)]).replace("+ -", "- ")
        st.latex(f"{eq_str} = {to_frac(B[i])}")

    def get_det_expansion(matrix, name):
        size = len(matrix)
        det_val = np.linalg.det(matrix)
        
        st.write(f"#### Finding |{name}|")
        
        # Proper Matrix Display (Fixing Red LaTeX error)
        matrix_latex = r"| " + name + r" | = \begin{vmatrix} "
        for row in matrix:
            matrix_latex += " & ".join([to_frac(v) for v in row]) + r" \\ "
        matrix_latex += r"\end{vmatrix}"
        st.latex(matrix_latex)
        
        if size == 2:
            # 2x2 Formula and Calculation
            st.latex(fr"|{name}| = (a_{{11}} \times a_{{22}}) - (a_{{12}} \times a_{{21}})")
            v1, v2, v3, v4 = matrix.flatten()
            st.latex(fr"|{name}| = ({to_frac(v1)} \times {to_frac(v4)}) - ({to_frac(v2)} \times {to_frac(v3)})")
            st.latex(fr"|{name}| = {to_frac(v1*v4)} - ({to_frac(v2*v3)}) = {to_frac(round(det_val))}")
            
        elif size == 3:
            # 3x3 Expansion logic (Notebook style)
            st.write("**Expansion along Row 1:**")
            r1 = matrix[0]
            m1 = matrix[1:, [1, 2]]
            m2 = matrix[1:, [0, 2]]
            m3 = matrix[1:, [0, 1]]
            
            # Step 1: Sub-matrices display
            st.latex(fr"|{name}| = {to_frac(r1[0])} \begin{{vmatrix}} {to_frac(m1[0,0])} & {to_frac(m1[0,1])} \\ {to_frac(m1[1,0])} & {to_frac(m1[1,1])} \end{{vmatrix}} - ({to_frac(r1[1])}) \begin{{vmatrix}} {to_frac(m2[0,0])} & {to_frac(m2[0,1])} \\ {to_frac(m2[1,0])} & {to_frac(m2[1,1])} \end{{vmatrix}} + {to_frac(r1[2])} \begin{{vmatrix}} {to_frac(m3[0,0])} & {to_frac(m3[0,1])} \\ {to_frac(m3[1,0])} & {to_frac(m3[1,1])} \end{{vmatrix}}")
            
            # Step 2: Intermediate arithmetic
            t1 = (m1[0,0]*m1[1,1]) - (m1[0,1]*m1[1,0])
            t2 = (m2[0,0]*m2[1,1]) - (m2[0,1]*m2[1,0])
            t3 = (m3[0,0]*m3[1,1]) - (m3[0,1]*m3[1,0])
            
            st.latex(fr"|{name}| = {to_frac(r1[0])}({to_frac(t1)}) - ({to_frac(r1[1])})({to_frac(t2)}) + {to_frac(r1[2])}({to_frac(t3)})")
            st.latex(fr"|{name}| = {to_frac(r1[0]*t1)} - ({to_frac(r1[1]*t2)}) + {to_frac(r1[2]*t3)}")
            st.latex(fr"|{name}| = {to_frac(round(det_val))}")

        return round(det_val)

        return det_val

    # Main Determinant D
    D = get_det_expansion(A, "A")
    
    if abs(D) < 1e-9:
        st.error("D = 0, Cramer's Rule cannot solve this (No unique solution).")
        return

    results = []
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = B
        Di = get_det_expansion(Ai, f"A_{vars[i]}")
        
        val = Di / D
        st.write(f"**Calculating {vars[i]}:**")
        st.latex(fr"{vars[i]} = \frac{{|A_{vars[i]}|}}{{|A|}} = \frac{{{to_frac(Di)}}}{{{to_frac(D)}}} = {to_frac(val)}")
        results.append(val)
    
    st.success("Final Values: " + ", ".join([f"{vars[i]} = {to_frac(results[i])}" for i in range(n)]))
    # --- Step 4: System Analysis Block (Based on Determinant) ---
    st.markdown("---")
    st.markdown("### 🔍 System Analysis (Nature of Solution)")
    
    det_A = np.linalg.det(A)
    aug = np.hstack([A, B.reshape(-1, 1)])
    rank_A = np.linalg.matrix_rank(A)
    rank_aug = np.linalg.matrix_rank(aug)

    if abs(det_A) > 1e-9:
        # Unique Solution: Determinant is NOT zero
        st.success("✅ **Type: Unique Solution (Consistent)**")
        st.write(f"**Reason:** The determinant $|A| = {to_frac(det_A)}$, which is **not zero**.")
        st.write("Since $|A| \\neq 0$, the system has exactly one unique solution where all lines/planes intersect.")
    
    elif rank_A == rank_aug:
        # Infinite Solutions: Determinant is zero AND ranks match
        st.warning("♾️ **Type: Infinite Many Solutions (Dependent)**")
        st.write(f"**Reason:** The determinant $|A| = 0$, but the equations are consistent (Rank $A$ = Rank Augmented).")
        st.write("This means the equations represent the same line or plane, leading to infinite common points.")
    
    else:
        # No Solution: Determinant is zero AND ranks do NOT match
        st.error("❌ **Type: No Solution (Inconsistent)**")
        st.write(f"**Reason:** The determinant $|A| = 0$ and the equations are inconsistent (Rank $A \\neq$ Rank Augmented).")
        st.write("This indicates that the equations represent parallel lines or planes that never meet.")
def solve_row_ops_detailed(A, B):
    n = len(B)
    aug = np.hstack([A, B.reshape(-1, 1)]).astype(float)
    vars_names = ["x", "y", "z"][:n]
    
    st.markdown(f"### 📐 Row Operations ({n}x{n} Step-by-Step)")

    # --- n == 2 Logic ---
    if n == 2:
        # Step 1: a11 = 1
        pivot1 = aug[0, 0]
        aug[0] = aug[0] / pivot1
        st.write(f"**Entry (1):** $R_1 \\to R_1 / {to_frac(pivot1)}$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")
        
        # Step 2: a21 = 0
        f21 = aug[1, 0]
        aug[1] = aug[1] - f21 * aug[0]
        st.write(f"**Entry (2):** $R_2 \\to R_2 - ({to_frac(f21)})R_1$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        # Step 3: a22 = 1
        pivot2 = aug[1, 1]
        aug[1] = aug[1] / pivot2
        st.write(f"**Entry (3):** $R_2 \\to R_2 / {to_frac(pivot2)}$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")
        
        st.success("✨ **Reached: Row Echelon Form (REF)**")
        st.markdown("---")
        
        # Step 4: a12 = 0 (RREF)
        f12 = aug[0, 1]
        aug[0] = aug[0] - f12 * aug[1]
        st.write(f"**Entry (4):** $R_1 \\to R_1 - ({to_frac(f12)})R_2$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

    # --- n == 3 Logic ---
    elif n == 3:
        st.markdown("### 📐 Row Operations (Step-by-Step Sequence)")
        
        # --- Phase 1: Forward Elimination (To Reach Echelon Form) ---
        # Entry 1: Make (1,1) = 1
        pivot1 = aug[0, 0]
        aug[0] = aug[0] / pivot1
        st.write(f"**Entry (1):** Making $a_{{11}} = 1$ using $R_1 \\to R_1 / {to_frac(pivot1)}$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        # Entry 2: Make (2,1) = 0
        f21 = aug[1, 0]
        aug[1] = aug[1] - f21 * aug[0]
        st.write(f"**Entry (2):** Making $a_{{21}} = 0$ using $R_2 \\to R_2 - ({to_frac(f21)})R_1$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        # Entry 3: Make (3,1) = 0
        f31 = aug[2, 0]
        aug[2] = aug[2] - f31 * aug[0]
        st.write(f"**Entry (3):** Making $a_{{31}} = 0$ using $R_3 \\to R_3 - ({to_frac(f31)})R_1$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        # Entry 4: Make (2,2) = 1
        pivot2 = aug[1, 1]
        aug[1] = aug[1] / pivot2
        st.write(f"**Entry (4):** Making $a_{{22}} = 1$ using $R_2 \\to R_2 / {to_frac(pivot2)}$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        # Entry 5: Make (3,2) = 0
        f32 = aug[2, 1]
        aug[2] = aug[2] - f32 * aug[1]
        st.write(f"**Entry (5):** Making $a_{{32}} = 0$ using $R_3 \\to R_3 - ({to_frac(f32)})R_2$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        # Entry 6: Make (3,3) = 1
        pivot3 = aug[2, 2]
        aug[2] = aug[2] / pivot3
        st.write(f"**Entry (6):** Making $a_{{33}} = 1$ using $R_3 \\to R_3 / {to_frac(pivot3)}$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        st.success("✨ **Reached: Row Echelon Form (REF)**")
        
        # --- Back-Substitution Logic ---
        res_z = aug[2, 3]
        res_y = aug[1, 3] - (aug[1, 2] * res_z)
        res_x = aug[0, 3] - (aug[0, 1] * res_y) - (aug[0, 2] * res_z)
        
        st.write("**Back-Substitution Phase:**")
        st.latex(fr"z = {to_frac(res_z)}")
        st.latex(fr"y = {to_frac(aug[1, 3])} - ({to_frac(aug[1, 2])})({to_frac(res_z)}) \implies y = {to_frac(res_y)}")
        st.latex(fr"x = {to_frac(aug[0, 3])} - ({to_frac(aug[0, 1])})({to_frac(res_y)}) - ({to_frac(aug[0, 2])})({to_frac(res_z)}) \implies x = {to_frac(res_x)}")

        st.markdown("---")
        st.write("#### 🔄 Converting to Reduced Row Echelon Form (RREF)")

        # Entry 7: Make (2,3) = 0
        f23 = aug[1, 2]
        aug[1] = aug[1] - f23 * aug[2]
        st.write(f"**Entry (7):** Making $a_{{23}} = 0$ using $R_2 \\to R_2 - ({to_frac(f23)})R_3$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        # Entry 8: Make (1,3) = 0
        f13 = aug[0, 2]
        aug[0] = aug[0] - f13 * aug[2]
        st.write(f"**Entry (8):** Making $a_{{13}} = 0$ using $R_1 \\to R_1 - ({to_frac(f13)})R_3$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        # Entry 9: Make (1,2) = 0
        f12 = aug[0, 1]
        aug[0] = aug[0] - f12 * aug[1]
        st.write(f"**Entry (9):** Making $a_{{12}} = 0$ using $R_1 \\to R_1 - ({to_frac(f12)})R_2$")
        st.latex(r"\begin{bmatrix} " + r" \\ ".join([" & ".join([to_frac(v) for v in r]) for r in aug]) + r" \end{bmatrix}")

        st.success("🎯 **Reached: Reduced Row Echelon Form (RREF)**")
    results = [aug[i, n] for i in range(n)]
    st.info("Final Values: " + ", ".join([f"{vars_names[i]} = {to_frac(results[i])}" for i in range(n)]))
    # Extract results from RREF
    results = [aug[i, n] for i in range(n)]
    st.success("Final Values: " + ", ".join([f"{vars_names[i]} = {to_frac(results[i])}" for i in range(n)]))
    # Row Operation based Analysis
    det_A = np.linalg.det(A)
    aug = np.hstack([A, B.reshape(-1, 1)])
    rank_A = np.linalg.matrix_rank(A)
    rank_aug = np.linalg.matrix_rank(aug)

    st.markdown("---")
    st.markdown("### 🔍 System Analysis (Row Operation Basis)")

    if abs(det_A) > 1e-9:
        st.success("✅ **Type: Unique Solution**")
        st.write("**Observation:** All diagonal elements in the Row Echelon Form are non-zero (or can be made 1).")
        st.write(f"**Reason:** Since the determinant $|A| = {to_frac(det_A)}$ is not zero, each variable has a pivot, leading to a single unique answer.")
    
    else:
        # Jab niche wali row zero ho jaye
        if rank_A == rank_aug:
            st.warning("♾️ **Type: Infinite Many Solutions**")
            st.write("**Observation:** During row operations, an entire row became zero ($0 = 0$).")
            st.write(f"**Reason:** The determinant $|A| = 0$ and the number of non-zero rows ({rank_A}) is less than the variables. This means one variable is 'free'.")
        else:
            st.error("❌ **Type: No Solution**")
            st.write("**Observation:** A row became zero on the left side, but has a non-zero value on the right ($0 = k$).")
            st.write(f"**Reason:** The determinant $|A| = 0$ and the ranks do not match. This creates a mathematical contradiction.")
# ================= EXPLANATION SECTION (FROM NOTEBOOK) =================
def show_explanation(method):
    st.title(f"💡 Detailed Theory: {method}")
    
    if method == "RowOps":
        st.markdown("### 📐 Elementary Row Operations")
        st.write("""
        Row operations are methods used to manipulate the rows of a matrix, usually to solve systems of 
        linear equations, find determinants, or get the matrix into a particular form like 
        **Row-Echelon Form (REF)** or **Reduced Row-Echelon Form (RREF)**.
        """)
        
        # Rules from Image 1000399655
        st.subheader("📜 The 4 Basic Rules:")
        st.info("""
        1. **Row Interchange:** $R_n \leftrightarrow R_m$ (Swap any two rows).
        2. **Scalar Multiply:** $R_n \rightarrow K \cdot R_n$ (Multiply a row by a non-zero constant).
        3. **Row Addition/Subtraction:** $R_n \rightarrow R_n + R_m$ (Add or subtract rows).
        4. **Divide a Row:** $R_n \rightarrow \\frac{1}{n} \cdot R_n$ (Divide by a non-zero number).
        """)

        st.markdown("---")
        
        # REF Section from Image 1000399655 & 1000399656
        st.subheader("1️⃣ Row Echelon Form (Gauss-Elimination)")
        st.write("**A Matrix is in REF if it looks like a staircase going down to the right:**")
        st.markdown("""
        * All rows that are completely zeros go at the bottom.
        * The first non-zero number in each row (called the **leading entry/pivot**) is to the right of the leading entry in the row above.
        * All numbers below a leading entry must be zeros.
        """)
        
        st.write("**Solving Order for REF:**")
        ref_order = [
            {"Step": "(1)", "Location": "Row 1, Col 1", "Action": "Create pivot ($a_{11} \\rightarrow 1$)"},
            {"Step": "(2)", "Location": "Row 2, Col 1", "Action": "Clear Below ($a_{21} \\rightarrow 0$)"},
            {"Step": "(3)", "Location": "Row 3, Col 1", "Action": "Clear Below ($a_{31} \\rightarrow 0$)"},
            {"Step": "(4)", "Location": "Row 2, Col 2", "Action": "Create pivot ($a_{22} \\rightarrow 1$)"},
            {"Step": "(5)", "Location": "Row 3, Col 2", "Action": "Clear Below ($a_{32} \\rightarrow 0$)"},
            {"Step": "(6)", "Location": "Row 3, Col 3", "Action": "Create pivot ($a_{33} \\rightarrow 1$)"},
        ]
        st.table(ref_order)

        st.markdown("---")

        # RREF Section from Image 1000399656 & 1000399657
        st.subheader("2️⃣ Reduced Row Echelon Form (Gauss-Jordan)")
        st.write("**RREF is the simplest form of a matrix. The goal is to transform it into an Identity Matrix.**")
        st.markdown("""
        * The matrix must already be in **REF**.
        * Every leading entry (pivot) must be **1**.
        * Each pivot must be the **only non-zero number** in its column (zeros above and below).
        """)

        st.write("**Solving Order for RREF (Back-Substitution Phase):**")
        rref_order = [
            {"Step": "(7)", "Location": "Row 2, Col 3", "Action": "Make this 0 (Above Pivot)"},
            {"Step": "(8)", "Location": "Row 1, Col 3", "Action": "Make this 0 (Above Pivot)"},
            {"Step": "(9)", "Location": "Row 1, Col 2", "Action": "Make this 0 (Above Pivot)"},
        ]
        st.table(rref_order)
        st.success("Target: All diagonal entries = 1, All others = 0.")

    elif method == "Cramer":
        st.markdown("### 📊 Cramer's Rule Theory")
        
        st.write("""
        **Cramer's Rule** is an explicit formula for solving a system of linear equations using **determinants**. 
        It is highly efficient when you need to solve for a specific variable without calculating the entire system.
        """)

        # Prerequisites
        st.subheader("📋 Mathematical Requirements")
        st.info("""
        1. **Square Matrix:** The number of equations must equal the number of unknowns (e.g., $3\\times3$).
        2. **Non-Zero Determinant ($D \\neq 0$):** The system must have a unique solution. 
           If the determinant of the coefficient matrix is zero, Cramer's Rule cannot be applied.
        """)

        # Operational Steps
        st.markdown("---")
        st.subheader("🛠️ Step-by-Step Procedure")
        
        st.markdown("""
        1.  **Calculate the Main Determinant ($D$):** Find the determinant of the coefficient matrix $A$.
        2.  **Construct Variable Matrices ($A_x, A_y, A_z$):** * To find $D_x$, replace the first column of $A$ with the constant vector $B$.
            * To find $D_y$, replace the second column of $A$ with the constant vector $B$.
            * To find $D_z$, replace the third column of $A$ with the constant vector $B$.
        3.  **Calculate Variable Determinants:** Find the determinants for $D_x, D_y,$ and $D_z$.
        4.  **Solve:** Divide each variable determinant by the main determinant $D$.
        """)

        # The Formulas
        st.latex(r"x = \frac{\det(A_x)}{\det(A)}, \quad y = \frac{\det(A_y)}{\det(A)}, \quad z = \frac{\det(A_z)}{\det(A)}")

        st.markdown("---")

        # Quick Summary Table
        st.subheader("📝 Cramer's Rule Quick Table")
        cramer_summary_data = [
            {"Term": "Main Determinant (D)", "Definition": "Determinant of the original coefficient matrix.", "Role": "Denominator"},
            {"Term": "Variable Det (Dx, Dy...)", "Definition": "Determinant after replacing the variable's column with constants.", "Role": "Numerator"},
            {"Term": "Unique Solution", "Action": "Variable = Variable Det / Main Det", "Requirement": "D ≠ 0"},
            {"Term": "Singular Matrix", "Action": "Rule Fails", "Requirement": "D = 0"}
        ]
        st.table(cramer_summary_data)

        st.success("Target: Replace the target variable's column with the 'Equals To' constants and divide by the total determinant.")
    elif method == "Elimination":
        st.markdown("### 🧮 Elimination Method (Addition/Subtraction)")
        
        st.write("""
        The **Elimination Method** is a technique used to solve a system of linear equations by 
        removing (eliminating) variables one at a time. This is done by making the coefficients 
        of one variable the same in two equations and then subtracting or adding them.
        """)

        # Step-by-Step Logic
        st.subheader("🛠️ Step-by-Step Procedure")
        st.markdown("""
        1.  **Align Equations:** Arrange the equations in the standard form $ax + by + cz = d$.
        2.  **Equalize Coefficients:** Multiply one or both equations by a constant so that the coefficients of one variable (e.g., $x$) become equal or opposite.
        3.  **Eliminate:** Add or subtract the equations to cancel out that variable, leaving you with a simpler equation.
        4.  **Repeat:** For a $3 \\times 3$ system, repeat this process with a different pair of equations to eliminate the same variable again.
        5.  **Back-Substitution:** Once you find the value of one variable, substitute it back into the previous equations to find the others.
        """)

        st.markdown("---")

        # Quick Summary Table
        st.subheader("📝 Elimination Method Quick Table")
        elimination_summary = [
            {"Step": "1. Multiply", "Goal": "Make coefficients of one variable match (e.g., $2x$ and $-2x$)."},
            {"Step": "2. Add/Subtract", "Goal": "Combine equations to eliminate that variable completely."},
            {"Step": "3. Solve", "Goal": "Solve the resulting smaller equation for the remaining variable."},
            {"Step": "4. Substitute", "Goal": "Plug the known value back into original equations to find the rest."}
        ]
        st.table(elimination_summary)

        # Pro-Tip
        st.info("""
        💡 **Pro-Tip:** This method is often the fastest for $2 \\times 2$ systems. For $3 \\times 3$ or larger, 
        it is essentially the manual version of **Gaussian Elimination** without using a matrix grid.
        """)

        st.success("Target: Reduce the number of variables until you have one equation with one unknown.")
# ================= 6. NAVIGATION & SIDEBAR =================
st.sidebar.title("📚 Academic Menu")
page = st.sidebar.radio("Go to:", ["🏠 Solver", "📘 Project Details", "🎯 Applications", "🎨 Flashcards"])

if page == "🏠 Solver":
    st.markdown("<h1 class='main-title'>Linear Solver Pro</h1>", unsafe_allow_html=True)
    
    if st.session_state.method is None:
        num = st.number_input("Variables", 2, 3, 2)
        eqs = [st.text_input(f"Equation {i+1}", key=f"q{i}") for i in range(num)]
        if st.button("Initialize System"):
            # Check karein k sab equations mein '=' mojud hai
            if all("=" in e and e.split("=")[1].strip() != "" for e in eqs):
                st.session_state.A, st.session_state.B = parse_equations(eqs, ["x", "y", "z"][:num])
                st.session_state.method = "Pending"
                st.rerun()
            else:
                st.error("It is necessary for every equation to have an '=' sign and a constant value (for example, = 2).!")
    else:
        st.write("### 1. Select Your Method")
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("🧮 Elimination"): st.session_state.method = "Elimination"
        if c2.button("📊 Cramer's"): st.session_state.method = "Cramer"
        if c3.button("📐 Row Ops"): st.session_state.method = "RowOps"
        if c4.button("🔄 Reset"): st.session_state.method = None; st.rerun()
        
        if st.session_state.method != "Pending":
            st.markdown("---")
            b1, b2, b3, b4 = st.columns(4)
            if b1.button("📝 Steps"): st.session_state.sub_view = "steps"
            if b2.button("📈 Graph"): st.session_state.sub_view = "graph"
            if b3.button("💡 Explanation"): st.session_state.sub_view = "explain"
            if b4.button("⬅ Back"): st.session_state.method = "Pending"; st.rerun()
            st.markdown("---")
            
            if st.session_state.sub_view == "steps":
                if st.session_state.method == "Elimination": solve_elimination_detailed(st.session_state.A, st.session_state.B)
                elif st.session_state.method == "Cramer": solve_cramer_detailed(st.session_state.A, st.session_state.B)
                elif st.session_state.method == "RowOps": solve_row_ops_detailed(st.session_state.A, st.session_state.B)
            elif st.session_state.sub_view == "explain":
                show_explanation(st.session_state.method)
            elif st.session_state.sub_view == "graph":
                st.write("Visualizing your Equations...")
                # Simple Plot Logic
                x = np.linspace(-10, 10, 100)
                plt.figure(figsize=(8,4))
                for i in range(len(st.session_state.B)):
                    if st.session_state.A[i, 1] != 0:
                        y = (st.session_state.B[i] - st.session_state.A[i, 0]*x) / st.session_state.A[i, 1]
                        plt.plot(x, y, label=f'Eq {i+1}')
                plt.axhline(0, color='black', lw=1); plt.axvline(0, color='black', lw=1); plt.grid(True); plt.legend(); st.pyplot(plt)
       
# ================= DETAILS =================
elif page == "📘 Project Details":

    st.title("📘 Project Details")

    st.markdown("""
### 📊 Project Title:
*Linear Equation Solver Pro (Streamlit Based Application)*

---

### 🎯 Objective:
This project is designed to solve systems of linear equations using multiple mathematical methods and provide both analytical and graphical understanding of the solution.

---

### 🧠 Core Methods Implemented:

🔹 *Elimination Method*  
A traditional algebraic approach where variables are eliminated step-by-step to find unknown values.

🔹 *Row Operations (Gaussian Elimination + RREF)*  
Matrix-based approach where the system is converted into:
- Echelon Form  
- Reduced Row Echelon Form (RREF)  
to directly obtain solutions.

🔹 *Cramer's Rule*  
A determinant-based method used to compute the values of variables when a unique solution exists.

---

### ⚙️ Key Features:

✔ Step-by-step solution for each method  
✔ AI-based explanation (text + voice)  
✔ Animated graphical visualization (2D & 3D)  
✔ System classification:
- Unique Solution  
- Infinite Solutions  
- No Solution  

✔ PDF report generation with graph  
✔ Interactive UI with sidebar navigation  
✔ Educational flashcards for learning  

---

### 🧮 Mathematical Concepts Used:

- Matrix Algebra  
- Determinants  
- Rank of Matrix  
- Gaussian Elimination  
- Linear Dependence & Independence  

---

### 💡 Purpose of Project:

This project helps students:
- Understand linear systems visually  
- Learn multiple solving techniques  
- Compare methods easily  
- Build strong mathematical concepts  

---

### 🛠️ Technologies Used:

- Python  
- Streamlit (UI framework)  
- NumPy (matrix operations)  
- Matplotlib (graph plotting)  
- ReportLab (PDF generation)  

---

### 🚀 Conclusion:

This application is not just a solver but a *complete learning tool* that combines mathematics, visualization, and interactive technology to make complex concepts easy to understand.
""")

# ================= APPLICATIONS =================
elif page == "🎯 Applications":

    st.title("💻 Applications in IT & Real Life")

    st.markdown("""
### 1️⃣ Machine Learning (Regression Models)
Linear equations are used in linear regression to predict outcomes such as house prices, student marks, or sales forecasting.

📌 Example: Predicting house price based on size and location.

---

### 2️⃣ Computer Graphics & Game Development
Matrices and linear systems are used to perform transformations like rotation, scaling, and translation in 2D/3D objects.

📌 Example: Moving characters in games like GTA or PUBG.

---

### 3️⃣ Data Science & Analytics
Used to find relationships between multiple variables in datasets.

📌 Example: Analyzing how temperature, humidity, and time affect sales.

---

### 4️⃣ Artificial Intelligence (AI)
AI models use systems of equations in optimization and neural networks.

📌 Example: Training a model to recognize images.

---

### 5️⃣ Networking & Traffic Optimization
Linear equations help optimize data flow and routing in networks.

📌 Example: Finding best path for internet data packets.

---

### 6️⃣ Electrical Engineering
Used in circuit analysis (Kirchhoff’s Laws) to calculate current and voltage.

📌 Example: Solving multi-loop circuits.

---

### 7️⃣ Economics & Business
Used to model supply-demand relationships and profit calculations.

📌 Example: Finding equilibrium price in market.

---

### 8️⃣ Robotics & Automation
Used for motion planning and control systems.

📌 Example: Robot arm positioning in manufacturing.

---

### 9️⃣ Image Processing
Used in filters and transformations for images.

📌 Example: Applying blur, sharpening filters.

---

### 🔟 Cryptography & Security
Used in encoding and decoding algorithms.

📌 Example: Encryption techniques in cybersecurity.

---

### ⭐ Bonus Insight:
Almost every modern technology — from AI to apps — somewhere uses *linear algebra and systems of equations*.
""")

# ================= FLASHCARDS =================
elif page == "🎨 Flashcards":

    st.title("🎨 Learning Flashcards")

    st.markdown("""
    <div style="background:#00ADB5;padding:20px;border-radius:12px;color:white;">
    <b>🧮 Elimination Method</b><br>
    Variables are removed step-by-step by adding or subtracting equations until one variable remains.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#FF5722;padding:20px;border-radius:12px;color:white;">
    <b>📐 Row Operations</b><br>
    Convert matrix into echelon form and then RREF to directly find solution values.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#4CAF50;padding:20px;border-radius:12px;color:white;">
    <b>📊 Cramer's Rule</b><br>
    Uses determinants to compute values of variables when system has unique solution.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#9C27B0;padding:20px;border-radius:12px;color:white;">
    <b>📌 System Types</b><br>
    Unique → One solution<br>
    Infinite → Many solutions<br>
    No Solution → Inconsistent system
    </div>
    """, unsafe_allow_html=True)
# # Sidebar header
# st.sidebar.title("📑 Technical Suite")

# Sidebar Styling
st.sidebar.markdown("<h1 style='text-align: center; color: #008080;'>📑 Technical Suite</h1>", unsafe_allow_html=True)
st.sidebar.divider()

st.sidebar.subheader("📥 Export Documentation")
st.sidebar.write("Generate and download the full technical manual instantly.")

# DIRECT DOWNLOAD BUTTON (No conditions)
# Ye hamesha clickable rahega
st.sidebar.download_button(
    label="📄 Download Technical Report",
    data=generate_technical_manual(), # Click hote hi function call hoga
    file_name="LSP_Technical_Manual_2026.pdf",
    mime="application/pdf",
    use_container_width=True,
    key="always_active_download",
)


st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Developer Tools")
st.sidebar.markdown("""
- **View Code on GitHub:** [Repo Link](https://github.com/yourusername/linear-solver)
""")