import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """
    kwargs: top, bottom, left, right, insideH, insideV
    values: {"sz": 4, "val": "single", "color": "000000"}
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', 'auto'))
            tcBorders.append(element)
    tcPr.append(tcBorders)

def setup_page_layout(s):
    # Instructions: A4 size, Left: 4 cm, Right: 2 cm, Top: 3 cm, Bottom: 3 cm
    s.page_width = Cm(21.0)
    s.page_height = Cm(29.7)
    s.left_margin = Cm(4.0)
    s.right_margin = Cm(2.0)
    s.top_margin = Cm(3.0)
    s.bottom_margin = Cm(3.0)
    s.header_distance = Cm(1.2)
    s.footer_distance = Cm(1.2)

    # Printable width: 21.0 - 4.0 - 2.0 = 15.0 cm
    # Tab stops: center at 7.5 cm, right at 15.0 cm
    hp = s.header.paragraphs[0]
    hp.text = ""
    hp.paragraph_format.tab_stops.add_tab_stop(Cm(7.5), WD_TAB_ALIGNMENT.CENTER)
    hp.paragraph_format.tab_stops.add_tab_stop(Cm(15.0), WD_TAB_ALIGNMENT.RIGHT)
    hrun = hp.add_run("Internship Report\tDepartment of CSE-AI&ML\t2026-27")
    hrun.font.name = 'Times New Roman'
    hrun.font.size = Pt(10)
    hrun.font.color.rgb = RGBColor(90, 90, 90)

    fp = s.footer.paragraphs[0]
    fp.text = ""
    fp.paragraph_format.tab_stops.add_tab_stop(Cm(7.5), WD_TAB_ALIGNMENT.CENTER)
    fp.paragraph_format.tab_stops.add_tab_stop(Cm(15.0), WD_TAB_ALIGNMENT.RIGHT)
    frun = fp.add_run("Internship Report\tDepartment of CSE-AI&ML\t2026-27")
    frun.font.name = 'Times New Roman'
    frun.font.size = Pt(10)
    frun.font.color.rgb = RGBColor(90, 90, 90)

def add_p(doc, text="", space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, font_size=12, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.italic = italic
        if color:
            r.font.color.rgb = color
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

doc = Document()
setup_page_layout(doc.sections[0])

# Set base normal style
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.font.color.rgb = RGBColor(0, 0, 0)

logo_path = 'presentation_assets/extracted_p1_img1.jpeg'
cert_img_path = 'presentation_assets/katuri_keerthi_internship_certificate.png'
arch_diagram_path = 'presentation_assets/certchain_architecture_diagram.png'
dataflow_diagram_path = 'presentation_assets/certchain_dataflow_diagram.png'

# ==========================================
# PAGE 1: COVER PAGE
# ==========================================
p_top = add_p(doc, "An\nInternship Report on\n", space_before=10, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13)

p_title = add_p(doc, "Blockchain — CertChain: Decentralized Academic Credential Verification Platform", space_before=6, space_after=14, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16)

p_sub = add_p(doc, "Submitted\nin partial fulfillment of the requirements for the award of the degree of\n", space_before=10, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, font_size=11)
r_deg = p_sub.add_run("BACHELOR OF TECHNOLOGY\nin\nCSE-Artificial Intelligence and Machine Learning")
r_deg.font.size = Pt(13)
r_deg.font.bold = True
r_deg.font.color.rgb = RGBColor(0, 102, 102)

p_by = add_p(doc, "By\n", space_before=10, space_after=12, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER, font_size=12)
r_name = p_by.add_run("KATURI KEERTHI\n")
r_name.font.size = Pt(15)
r_name.font.bold = True
r_roll = p_by.add_run("24R11A66N9")
r_roll.font.size = Pt(13)
r_roll.font.bold = True

if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(8)
    p_logo.paragraph_format.space_after = Pt(8)
    p_logo.add_run().add_picture(logo_path, width=Cm(3.8))

p_col = add_p(doc, "", space_before=4, space_after=2, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
r_dept = p_col.add_run("Department of CSE-Artificial Intelligence and Machine Learning\n")
r_dept.font.size = Pt(12)
r_dept.font.bold = True
r_dept.font.color.rgb = RGBColor(0, 128, 128)

r_cname = p_col.add_run("Geethanjali College of Engineering and Technology\n")
r_cname.font.size = Pt(13)
r_cname.font.bold = True
r_cname.font.color.rgb = RGBColor(180, 20, 20)

r_cinfo = p_col.add_run("(UGC AUTONOMOUS INSTITUTION)\n(Affiliated to J.N.T.U.H, Approved by AICTE, New Delhi)\nCheeryal (V), Keesara (M), Medchal.Dist.-501 301.\n\n")
r_cinfo.font.size = Pt(10)

r_date = p_col.add_run("August -2026")
r_date.font.size = Pt(12)
r_date.font.bold = True

doc.add_page_break()

# ==========================================
# PAGE 2: CERTIFICATE (COLLEGE)
# ==========================================
p_ch = add_p(doc, "", space_before=6, space_after=2, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
r_ch1 = p_ch.add_run("Geethanjali College of Engineering & Technology\n")
r_ch1.font.size = Pt(15)
r_ch1.font.bold = True
r_ch1.font.color.rgb = RGBColor(180, 20, 20)

r_ch2 = p_ch.add_run("(UGC Autonomous)\n(Affiliated to JNTUH, Approved by AICTE, New Delhi)\nCheeryal (V), Keesara(M), Medchal Dist.-501 301.\n\n")
r_ch2.font.size = Pt(10)

r_ch3 = p_ch.add_run("Department of CSE-Artificial Intelligence and Machine Learning")
r_ch3.font.size = Pt(12.5)
r_ch3.font.bold = True
r_ch3.font.color.rgb = RGBColor(0, 102, 153)

if os.path.exists(logo_path):
    p_clogo = doc.add_paragraph()
    p_clogo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_clogo.paragraph_format.space_before = Pt(6)
    p_clogo.paragraph_format.space_after = Pt(2)
    p_clogo.add_run().add_picture(logo_path, width=Cm(3.2))

p_clabel = add_p(doc, "Geethanjali\n", space_before=2, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11)

p_ctitle = add_p(doc, "CERTIFICATE", space_before=6, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=16, color=RGBColor(180, 120, 0))

p_cbody = add_p(doc, "", space_before=6, space_after=20, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
p_cbody.add_run("This is to certify that the internship report titled ")
r_t = p_cbody.add_run("Blockchain — CertChain: Decentralized Academic Credential Verification Platform")
r_t.font.bold = True
p_cbody.add_run(" being submitted by ")
r_n = p_cbody.add_run("KATURI KEERTHI")
r_n.font.bold = True
p_cbody.add_run(", bearing roll number ")
r_r = p_cbody.add_run("24R11A66N9")
r_r.font.bold = True
p_cbody.add_run(", in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology ")
r_b = p_cbody.add_run("“CSE-Artificial Intelligence and Machine Learning”")
r_b.font.bold = True
p_cbody.add_run(" from Jawaharlal Nehru Technological University, Hyderabad during the year 2026-2027.")

tbl_sig = doc.add_table(rows=1, cols=2)
tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_sig.autofit = False
tbl_sig.columns[0].width = Inches(2.9)
tbl_sig.columns[1].width = Inches(2.9)

c0 = tbl_sig.cell(0, 0)
p0 = c0.paragraphs[0]
p0.paragraph_format.line_spacing = 1.15
r_s1 = p0.add_run("Internship Supervisor\nMr. G. Raju\n(Asst.Prof, CSE-AI&ML)")
r_s1.font.bold = True
r_s1.font.size = Pt(10.5)

c1 = tbl_sig.cell(0, 1)
p1 = c1.paragraphs[0]
p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p1.paragraph_format.line_spacing = 1.15
r_s2 = p1.add_run("Internship Coordinator\nMr. Vedavyas Gurla\n(Assoc.Prof CSE-AI&ML)")
r_s2.font.bold = True
r_s2.font.size = Pt(10.5)

p_hod = add_p(doc, "Dr. L. Venkateswarlu\n(Professor & HoD, CSE-AI&ML)", space_before=24, space_after=24, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11)

p_ex = add_p(doc, "Examiner\nSignature:\nName:\nDesignation:", space_before=6, space_after=0, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=10.5)

doc.add_page_break()

# ==========================================
# PAGE 3: INTERNSHIP CERTIFICATE FROM ORGANIZATION WITH LETTER HEAD
# ==========================================
# Look at template page 5: "3rd page: Internship Certificate from Organization with Letter Head"
# Look at friend's report page 3: Landscape certificate image embedded directly filling page
if os.path.exists(cert_img_path):
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert.paragraph_format.space_before = Pt(40)
    p_cert.paragraph_format.space_after = Pt(20)
    # Printable width is 15.0 cm (~5.9 inches)
    p_cert.add_run().add_picture(cert_img_path, width=Cm(15.0))

doc.add_page_break()

# ==========================================
# PAGE 4: DECLARATION BY THE CANDIDATE
# ==========================================
p_dh = add_p(doc, "", space_before=6, space_after=2, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
r_dh1 = p_dh.add_run("Geethanjali College of Engineering & Technology\n")
r_dh1.font.size = Pt(15)
r_dh1.font.bold = True
r_dh1.font.color.rgb = RGBColor(180, 20, 20)

r_dh2 = p_dh.add_run("(UGC Autonomous)\n(Affiliated to JNTUH Approved by AICTE, New Delhi)\nCheeryal (V), Keesara(M), Medchal Dist.-501 301.\n\n")
r_dh2.font.size = Pt(10)

r_dh3 = p_dh.add_run("Department of CSE-Artificial Intelligence and Machine Learning")
r_dh3.font.size = Pt(12.5)
r_dh3.font.bold = True
r_dh3.font.color.rgb = RGBColor(0, 102, 153)

if os.path.exists(logo_path):
    p_dlogo = doc.add_paragraph()
    p_dlogo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dlogo.paragraph_format.space_before = Pt(6)
    p_dlogo.paragraph_format.space_after = Pt(2)
    p_dlogo.add_run().add_picture(logo_path, width=Cm(3.2))

p_dlabel = add_p(doc, "Geethanjali\n", space_before=2, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11)

p_dtitle = add_p(doc, "DECLARATION BY THE CANDIDATE", space_before=6, space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=15, color=RGBColor(180, 120, 0))

p_dbody = add_p(doc, "", space_before=6, space_after=16, line_spacing=1.35, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
p_dbody.add_run("I, ")
r_dn = p_dbody.add_run("KATURI KEERTHI")
r_dn.font.bold = True
p_dbody.add_run(" , bearing Roll No. ")
r_dr = p_dbody.add_run("24R11A66N9")
r_dr.font.bold = True
p_dbody.add_run(" , hereby declare that the Internship Report entitled ")
r_dt = p_dbody.add_run("“Blockchain — CertChain: Decentralized Academic Credential Verification Platform”")
r_dt.font.bold = True
p_dbody.add_run(" is submitted in partial fulfillment of the requirements for the award of the degree of ")
r_dd = p_dbody.add_run("Bachelor of Technology in CSE-Artificial Intelligence and Machine Learning.\n\n")
r_dd.font.bold = True

p_dbody.add_run("This is a record of bonafide work carried out by me in ")
r_dc = p_dbody.add_run("Centurion University of Technology and Management (School of Future Nexus)")
r_dc.font.bold = True
p_dbody.add_run(" and the results embodied in this internship have not been reproduced or copied from any source. The results embodied in this Internship Report have not been submitted to any other University or Institute.")

p_dsig = add_p(doc, "Signature of Student\n(KATURI KEERTHI, 24R11A66N9)", space_before=36, space_after=0, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, font_size=11)

doc.add_page_break()

# ==========================================
# PAGE 5: ACKNOWLEDGEMENT
# ==========================================
add_heading_1(doc, "ACKNOWLEDGEMENT")

p_a1 = add_p(doc, "", space_before=6, space_after=14, line_spacing=1.35)
p_a1.add_run("     I would like to express my heartfelt gratitude to everyone who played a role in the successful completion of this project. My deepest thanks go to our Director, ")
p_a1.add_run("Dr. Uday Kumar Susarla").font.bold = True
p_a1.add_run(", and our college Principal, ")
p_a1.add_run("Dr. K. Sagar").font.bold = True
p_a1.add_run(", for providing the essential resources and unwavering support for this endeavor. I am profoundly grateful to the Professor & Dean - School of CS and Informatics ")
p_a1.add_run("Dr. V. Madhusudan Rao").font.bold = True
p_a1.add_run(" and our Head of the Department. ")
p_a1.add_run("Dr. L. Venkateswarlu").font.bold = True
p_a1.add_run(" for his invaluable guidance and encouragement throughout the internship project.")

p_a2 = add_p(doc, "", space_before=6, space_after=14, line_spacing=1.35)
p_a2.add_run("     I would like to extend my heartfelt gratitude to our beloved faculty as Internship supervisor ")
p_a2.add_run("Mr. G. Raju").font.bold = True
p_a2.add_run(" whose invaluable expertise and guidance were instrumental to our success. I am also sincerely appreciative of our Internship Coordinator, ")
p_a2.add_run("Mr. Vedavyas Gurla").font.bold = True
p_a2.add_run(", for the unwavering support and encouragement throughout this period. Additionally, I am deeply grateful to ")
p_a2.add_run("Centurion University of Technology and Management (School of Future Nexus)").font.bold = True
p_a2.add_run(" and my internship guide ")
p_a2.add_run("Prof. Anil Kumar").font.bold = True
p_a2.add_run(" (Dean, Extension, Skills, and Incubation) for this incredible opportunity, continuous training, and invaluable guidance throughout my journey. Thank you all for your significant contributions to my learning and growth.")

doc.add_page_break()

# ==========================================
# PAGE 6: INTRODUCTION ABOUT INTERNSHIP ORGANIZATION
# ==========================================
add_heading_1(doc, "Introduction about Internship Organization")

p_io1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_io1.add_run("     ")
p_io1.add_run("Centurion University of Technology and Management (CUTM)").font.bold = True
p_io1.add_run(" is a pioneering state-enacted private university recognized by UGC and accredited by NAAC with 'A+' Grade. Through its ")
p_io1.add_run("School of Future Nexus").font.bold = True
p_io1.add_run(", the university provides high-impact practical exposure, experiential incubation, and advanced skill development in emerging technology domains including Blockchain Engineering, Smart Contract Development, Decentralized Applications (dApps), and Cryptographic Systems. The organization emphasizes hands-on learning and encourages students to apply theoretical computer science concepts to real-world industrial challenges through structured internship programs and project-based training.")

p_io2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_io2.add_run("     The School of Future Nexus conducts specialized technical programs designed to help students master modern decentralized architectures. The training curriculum encompasses Solidity smart contract programming, Ethereum Virtual Machine (EVM) internals, asymmetric public-key cryptography, document fingerprinting, decentralized storage, gas optimization strategies, and automated testing with the Foundry toolkit. Students gain practical experience in industry-standard software engineering workflows, including Git version control, GitHub team collaboration, and cloud-based CI/CD deployment pipelines.")

p_io3 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_io3.add_run("     As part of my intensive internship program on ")
p_io3.add_run("Blockchain").font.bold = True
p_io3.add_run(" (Certificate ID: ")
p_io3.add_run("CUTM/AP/26/907367077873").font.bold = True
p_io3.add_run(", issued on 06-08-2026 under the mentorship of Prof. Anil Kumar), I received comprehensive practical instruction in EVM mechanics, OpenZeppelin security standards, Ethers.js integration, and Web3 security paradigms. The training introduced me to decentralized ledgers, cryptographic hashing, and zero-trust verification systems.")

p_io4 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_io4.add_run("     The knowledge and practical experience gained during the internship were directly applied to the end-to-end development of ")
p_io4.add_run("CertChain").font.bold = True
p_io4.add_run(", a decentralized academic credential verification platform anchored live on the Ethereum Sepolia blockchain network. The project eliminates credential fraud by anchoring SHA-256 document digests on-chain and providing instant, zero-trust verification via camera QR scanning and direct JSON-RPC node querying.")

p_io5 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_io5.add_run("     Overall, the internship at Centurion University of Technology and Management provided exceptional exposure to frontier Web3 technologies and enterprise-grade software development. It successfully bridged the gap between academic learning and industry-oriented decentralized software engineering while strengthening my analytical, problem-solving, and system implementation skills.")

doc.add_page_break()

# ==========================================
# PAGE 7: TRAINING SCHEDULE
# ==========================================
add_heading_1(doc, "Training Schedule")

tbl_ts = doc.add_table(rows=5, cols=2)
tbl_ts.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_ts.autofit = False
tbl_ts.columns[0].width = Inches(1.3)
tbl_ts.columns[1].width = Inches(4.6)

sched_data = [
    ("Week", "Training Schedule"),
    ("WEEK\n1", "Introduction to Blockchain Fundamentals and Cryptography: Principles of Distributed Ledger Technology (DLT), consensus algorithms (Proof of Work vs. Proof of Stake), SHA-256 cryptographic hashing, Merkle trees, asymmetric public-private key cryptography, digital signatures, and Ethereum address derivation."),
    ("WEEK\n2", "Ethereum Virtual Machine (EVM) and Solidity Smart Contracts: Solidity 0.8.24 programming, state variables, mappings, structs, modifiers, events, OpenZeppelin Ownable security patterns, Foundry development environment (forge, cast, test), gas optimization techniques, and deployment to Ethereum Sepolia Testnet."),
    ("WEEK\n3", "Full-Stack Web3 Integration and Document Fingerprinting: Ethers.js v6 library integration, MetaMask provider connectivity, JSON-RPC Sepolia network interaction, deterministic PDF generation using jsPDF, client-side SHA-256 binary hashing via Web Cryptography API, and real-time in-browser camera/image QR barcode decoding using html5-qrcode."),
    ("WEEK\n4", "Project Development – CertChain: End-to-end engineering of CertChain, implementation of dual-mode issuance (gasless institutional relayer vs. MetaMask Web3 signing), tamper detection pipeline, SQLite native backend storage, and live production CI/CD cloud deployment on Netlify Edge CDN and Cloudflare.")
]

for row_idx, (col0, col1) in enumerate(sched_data):
    cell0 = tbl_ts.cell(row_idx, 0)
    cell1 = tbl_ts.cell(row_idx, 1)
    cell0.paragraphs[0].text = col0
    cell1.paragraphs[0].text = col1
    cell0.paragraphs[0].paragraph_format.line_spacing = 1.15
    cell1.paragraphs[0].paragraph_format.line_spacing = 1.15
    set_cell_margins(cell0, top=100, bottom=100, left=120, right=120)
    set_cell_margins(cell1, top=100, bottom=100, left=120, right=120)
    b_args = {"top": {"val": "single", "sz": 6, "color": "000000"},
              "bottom": {"val": "single", "sz": 6, "color": "000000"},
              "left": {"val": "single", "sz": 6, "color": "000000"},
              "right": {"val": "single", "sz": 6, "color": "000000"}}
    set_cell_border(cell0, **b_args)
    set_cell_border(cell1, **b_args)
    if row_idx == 0:
        cell0.paragraphs[0].runs[0].font.bold = True
        cell1.paragraphs[0].runs[0].font.bold = True
        cell0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell0._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))
        cell1._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))
    else:
        cell0.paragraphs[0].runs[0].font.bold = True
        cell0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# ==========================================
# PAGE 8: TABLE OF CONTENTS
# ==========================================
add_heading_1(doc, "TABLE OF CONTENTS")

tbl_toc = doc.add_table(rows=12, cols=3)
tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_toc.autofit = False
tbl_toc.columns[0].width = Inches(0.9)
tbl_toc.columns[1].width = Inches(4.0)
tbl_toc.columns[2].width = Inches(1.0)

toc_data = [
    ("S. No", "Contents", "Page No"),
    ("", "Abstract", "i"),
    ("", "List of Figures", "ii"),
    ("", "List of Tables", "iii"),
    ("", "List of Screenshots", "iv"),
    ("", "List of Symbols & Abbreviations", "v"),
    ("1", "Introduction", "1"),
    ("2", "Related work/ Technologies used", "2.."),
    ("3", "Work done/ Observation/ Duties performed", "3.."),
    ("4", "Learning after Internship", ""),
    ("5", "Summary / Conclusion", ""),
    ("6", "Bibliography", "")
]

for row_idx, (c0_t, c1_t, c2_t) in enumerate(toc_data):
    c0 = tbl_toc.cell(row_idx, 0)
    c1 = tbl_toc.cell(row_idx, 1)
    c2 = tbl_toc.cell(row_idx, 2)
    c0.paragraphs[0].text = c0_t
    c1.paragraphs[0].text = c1_t
    c2.paragraphs[0].text = c2_t
    set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
    set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
    set_cell_margins(c2, top=70, bottom=70, left=100, right=100)
    b_k = {"top": {"val": "single", "sz": 4, "color": "000000"},
           "bottom": {"val": "single", "sz": 4, "color": "000000"},
           "left": {"val": "single", "sz": 4, "color": "000000"},
           "right": {"val": "single", "sz": 4, "color": "000000"}}
    set_cell_border(c0, **b_k); set_cell_border(c1, **b_k); set_cell_border(c2, **b_k)
    if row_idx == 0:
        c0.paragraphs[0].runs[0].font.bold = True
        c1.paragraphs[0].runs[0].font.bold = True
        c2.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c0._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))
        c1._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))
        c2._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))
    else:
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# ==========================================
# PAGE 9: PRELIMINARY PAGES LIST & IMPORTANT NOTE
# ==========================================
add_heading_2(doc, "List of Figures/Diagrams/Graphs")
doc.add_paragraph("Fig 5.1: System Architecture of CertChain", style='List Bullet')
doc.add_paragraph("Fig 5.2: Cryptographic Data Flow and Issuance Lifecycle", style='List Bullet')

add_heading_2(doc, "List of Tables")
doc.add_paragraph("Table 2.1: Comparison of Core Technologies and Libraries in CertChain", style='List Bullet')
doc.add_paragraph("Table 3.1: Smart Contract Key Functions in CertChain.sol", style='List Bullet')
doc.add_paragraph("Table 1: Correlation between Internship Project and Program Outcomes (POs/PSOs)", style='List Bullet')
doc.add_paragraph("Table 2: Project Correlation with Appropriate Level (H/M/L)", style='List Bullet')
doc.add_paragraph("Table 3: Nature of Internship Work", style='List Bullet')
doc.add_paragraph("Table 4: Nature of Internship Project Domain Classification", style='List Bullet')

add_heading_2(doc, "List of Screenshots")
doc.add_paragraph("5.4.1 Home Page (CertChain Public Landing Interface)", style='List Bullet')
doc.add_paragraph("5.4.2 Dashboard (Public Zero-Trust Verification Portal)", style='List Bullet')
doc.add_paragraph("5.4.3 Real-Time QR Camera Scanner Viewfinder", style='List Bullet')
doc.add_paragraph("5.4.4 Cryptographically Verified On-Chain Output Card", style='List Bullet')
doc.add_paragraph("5.4.5 Institutional Admin Telemetry Dashboard", style='List Bullet')
doc.add_paragraph("5.4.6 Credential Issuance Engine with Live Vector Preview", style='List Bullet')
doc.add_paragraph("5.4.7 Certificate Registry and Revocation Management Table", style='List Bullet')
doc.add_paragraph("5.4.8 Live Production Deployment on Netlify Edge CDN", style='List Bullet')

add_heading_2(doc, "List of Abbreviations")
doc.add_paragraph("EVM: Ethereum Virtual Machine", style='List Bullet')
doc.add_paragraph("DLT: Distributed Ledger Technology", style='List Bullet')
doc.add_paragraph("SHA-256: Secure Hash Algorithm 256-bit", style='List Bullet')
doc.add_paragraph("ECDSA: Elliptic Curve Digital Signature Algorithm", style='List Bullet')
doc.add_paragraph("RPC: Remote Procedure Call", style='List Bullet')
doc.add_paragraph("API: Application Programming Interface", style='List Bullet')
doc.add_paragraph("QR: Quick Response (Optical 2D Matrix Barcode)", style='List Bullet')
doc.add_paragraph("URI: Uniform Resource Identifier", style='List Bullet')

add_heading_2(doc, "Important Note")
p_in1 = add_p(doc, "▪ All the above pages are to be numbered in Roman numerals of lower case. Ex. i, ii, iii, iv,…\n▪ The Table of contents must be numbered using numbers i.e. 1, 2, 3……", space_before=4, space_after=6, line_spacing=1.3)
p_in1.runs[0].font.bold = True

doc.add_page_break()

# ==========================================
# PAGE 10: ABSTRACT
# ==========================================
add_heading_1(doc, "ABSTRACT")

p_ab1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_ab1.add_run("     Academic credential fraud is an escalating global challenge, with counterfeit diplomas and falsified degree certificates undermining trust in educational institutions and employer hiring pipelines. Traditional academic verification methods rely heavily on centralized registrar databases or expensive third-party background screening agencies, resulting in turnaround delays of several weeks, substantial financial overhead, and vulnerability to single points of failure, unauthorized tampering, and privacy breaches. During the internship at Centurion University of Technology and Management (School of Future Nexus), practical knowledge was gained in Blockchain Engineering, Ethereum Virtual Machine (EVM) architecture, Solidity smart contract programming, and cryptographic data integrity. This knowledge was applied to develop ")
p_ab1.add_run("CertChain").font.bold = True
p_ab1.add_run(", an intelligent, decentralized academic and professional credential verification platform designed to provide instant, tamper-proof, zero-trust verification on the Ethereum blockchain.")

p_ab2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_ab2.add_run("     CertChain uses cryptographic document fingerprinting techniques to guarantee data authenticity without compromising recipient privacy. Digital certificates are rendered deterministically using client-side vector compilation (jsPDF), and a mathematical 256-bit binary digest is generated using SHA-256 via the Web Cryptography API. Only this cryptographic fingerprint, along with institutional issuer metadata, is anchored immutably onto the Ethereum Sepolia smart contract. Consequently, sensitive personal student data is never exposed directly on public ledgers, ensuring 100% compliance with contemporary data privacy regulations.")

p_ab3 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_ab3.add_run("     The project features a dual-mode issuance mechanism supporting both gasless institutional relayer transactions (sponsored through institutional ECDSA key management) and direct Web3 wallet signing via MetaMask. For verifiers and employers, the platform incorporates real-time in-browser optical QR code barcode scanning powered by html5-qrcode, allowing immediate camera-based or image-upload authentication that directly interrogates the Ethereum Sepolia network via JSON-RPC. A resilient client-side architecture guarantees uninterrupted availability even on serverless Edge CDNs.")

p_ab4 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_ab4.add_run("     Overall, CertChain demonstrates the practical, transformative application of Blockchain and Web3 technologies in higher education administration. The project provides an accessible, high-performance platform that reduces credential verification latency from weeks to milliseconds while eliminating third-party intermediaries. The internship experience bridged theoretical computer science principles with enterprise-grade decentralized software engineering.")

doc.add_page_break()

# ==========================================
# PAGE 11: CHAPTER 1 - INTRODUCTION
# ==========================================
add_heading_1(doc, "INTRODUCTION")

p_in_1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_in_1.add_run("     ")
p_in_1.add_run("CertChain").font.bold = True
p_in_1.add_run(" is a decentralized academic credential verification platform engineered to eliminate diploma fraud and restore uncompromised mathematical trust to educational records. The system combines Blockchain Engineering, Distributed Ledger Technology, cryptographic hashing, and optical computer vision to provide features such as immutable credential registration, on-chain revocation management, instant QR-based verification, and gasless institutional issuance.")

p_in_2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_in_2.add_run("     The application follows a modern four-tier architecture consisting of an Ethereum Sepolia Smart Contract layer, a Node.js institutional relayer service, an SQLite query cache, and a responsive React single-page frontend. The backend manages institutional authorization, relayer transaction broadcast, and PDF persistence, while the client interface enables employers and public verifiers to authenticate credentials instantly without intermediaries.")

p_in_3 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_in_3.add_run("     A key feature of CertChain is its zero-trust cryptographic verification pipeline. Instead of trusting centralized database entries that can be altered by database administrators or corrupted by malicious intrusions, the platform calculates the SHA-256 binary hash of the presented certificate and verifies its existence, issuer authority, and revocation status directly on the Ethereum blockchain. If even a single character in the student's name, grade, or certificate ID is altered, the cryptographic digest changes completely (avalanche effect), immediately flagging the certificate as counterfeit.")

p_in_4 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_in_4.add_run("     The system also incorporates in-browser optical barcode decoding using html5-qrcode. Verifiers can scan physical or digital QR codes using webcams, mobile device cameras, or uploaded screenshot images. The QR code points directly to the immutable record on Ethereum Sepolia, providing verifiers with cryptographic proof of issuance, including transaction hashes, block numbers, and timestamped issuer signatures.")

p_in_5 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_in_5.add_run("     The primary objective of this project is to demonstrate how distributed ledgers, smart contracts, cryptographic hashing, and modern web technologies can work harmoniously within a unified credential verification platform. The application is intended to serve universities, accreditation councils, and recruitment enterprises as a scalable, tamper-proof alternative to legacy verification workflows.")

doc.add_page_break()

# ==========================================
# PAGES 12 - 15: CHAPTER 2 - RELATED WORK / TECHNOLOGIES USED
# ==========================================
add_heading_1(doc, "RELATED WORK / TECHNOLOGIES USED")

p_rw1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_rw1.add_run("     Higher education institutions increasingly rely on digital technologies to issue academic degrees, diplomas, transcripts, and certificates. Traditional credential management systems primarily focus on storing records in centralized relational databases (such as MySQL or PostgreSQL) and transmitting digitized PDF copies over email. Modern Web3 applications extend these capabilities by incorporating decentralized consensus, immutable distributed ledgers, cryptographic proofs of existence, and zero-knowledge privacy guarantees.")

p_rw2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_rw2.add_run("     Blockchain technology enables independent, decentralized nodes to maintain a synchronized, append-only transaction ledger without relying on a centralized clearinghouse. Smart contracts execute self-enforcing business logic directly within the Ethereum Virtual Machine (EVM), guaranteeing that credential state transitions (such as certificate issuance or administrative revocation) are cryptographically signed, timestamped, and audited publicly.")

p_rw3 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_rw3.add_run("     CertChain — Decentralized Academic Credential Verification Platform integrates these technologies into a unified, high-performance web application. It uses React 18 and Vite for the frontend, Node.js and Express for the institutional backend relayer, and Solidity 0.8.24 on Ethereum Sepolia for on-chain state anchoring. Its core capabilities include gasless relayer issuance, Web3 wallet signing, live SVG/canvas certificate preview, deterministic PDF compilation, and optical QR barcode scanning.")

add_heading_2(doc, "Development Approach")
p_da1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_da1.add_run("     CertChain follows a decoupled, modular development approach separating smart contract execution from client-side cryptographic rendering and backend relayer services. The frontend provides a dark-mode glassmorphic interface that allows administrators to input certificate metadata and preview certificates in real time before on-chain commitment.")

p_da2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_da2.add_run("     The backend institutional relayer provides REST API endpoints for authentication, sequential ID reservation, database querying, and transaction relaying. The relayer holds the institution's authorized Ethereum private key, allowing university staff to issue certificates with a single click without requiring staff members to manage personal crypto wallets or acquire testnet ETH.")

p_da3 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_da3.add_run("     The smart contract is developed using Solidity 0.8.24 and compiled and tested using the Foundry toolkit (forge). It enforces role-based access control (RBAC), ensuring that only authorized institutional wallets can execute the issuance function, while public verifiers can query certificate validity through gasless read-only view calls.")

add_heading_2(doc, "Technologies and Tools Used")
p_tt = add_p(doc, "The project utilizes a robust stack spanning frontend, backend, smart contract, cryptographic, and cloud hosting technologies:", space_before=4, space_after=8, line_spacing=1.35)

add_heading_2(doc, "Frontend and Backend Technologies")
p_fe1 = add_p(doc, "React 18 & Vite: React powers the single-page application interface, providing modular component composition, responsive state management, and real-time UI feedback. Vite provides fast HMR development and optimized production bundling.", space_before=4, space_after=8, line_spacing=1.35)
p_fe2 = add_p(doc, "Vanilla CSS & Glassmorphism: Custom CSS styling with HSL color tokens, backdrop-filter blurs, sleek dark modes, and dynamic micro-animations to deliver a state-of-the-art user experience without bloat.", space_before=4, space_after=8, line_spacing=1.35)
p_fe3 = add_p(doc, "Node.js & Express: A lightweight backend managing institutional admin authentication, PDF file persistence, and automated transaction relaying to the Ethereum Sepolia network.", space_before=4, space_after=12, line_spacing=1.35)

add_heading_2(doc, "Database and Smart Contract Technologies")
p_db1 = add_p(doc, "Solidity 0.8.24: The smart contract language used to implement CertChain.sol. Employs OpenZeppelin Ownable access control, struct mappings, custom events, and reentrancy protections.", space_before=4, space_after=8, line_spacing=1.35)
p_db2 = add_p(doc, "Ethereum Sepolia Testnet: An Ethereum proof-of-stake test network replicating mainnet execution, providing immutable transaction confirmation, block explorer auditability on Etherscan, and real EVM gas dynamics.", space_before=4, space_after=8, line_spacing=1.35)
p_db3 = add_p(doc, "SQLite Database: An embedded relational database used by the institutional server to cache certificate records, sequential counters, and query logs for low-latency operational dashboards.", space_before=4, space_after=12, line_spacing=1.35)

add_heading_2(doc, "Document Processing & Cryptography")
p_dp1 = add_p(doc, "jsPDF & QRCode: jsPDF renders deterministic A4 landscape certificate documents. QRCode dynamically generates high-density QR matrices encoding verification URIs embedded directly onto certificate vector layouts.", space_before=4, space_after=8, line_spacing=1.35)
p_dp2 = add_p(doc, "Web Cryptography API (SHA-256): Native browser cryptographic primitives generate deterministic 256-bit hashes from PDF binary array buffers, establishing mathematical proof of content authenticity.", space_before=4, space_after=8, line_spacing=1.35)
p_dp3 = add_p(doc, "html5-qrcode: An optical barcode scanning library enabling verifiers to scan physical diplomas or digital screens using live device cameras with automatic frame capture and QR decoding.", space_before=4, space_after=12, line_spacing=1.35)

doc.add_page_break()

# ==========================================
# PAGES 16 - 20: CHAPTER 3 - WORK DONE / OBSERVATION / DUTIES PERFORMED
# ==========================================
add_heading_1(doc, "WORK DONE / OBSERVATION / DUTIES PERFORMED")

add_heading_2(doc, "System Architecture of Proposed System")
p_sa1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_sa1.add_run("     ")
p_sa1.add_run("CertChain — Decentralized Academic Credential Verification Platform").font.bold = True
p_sa1.add_run(" follows a modular architecture consisting of a frontend web application, an institutional backend relayer server, an embedded SQLite database, a client-side cryptographic engine, and a smart contract deployed on the Ethereum Sepolia network. These components work together to register certificates securely, sponsor gas fees, and enable instant verification through a unified interface.")

p_sa2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_sa2.add_run("     The frontend provides administrative workflows for credential generation, batch presets, and live preview rendering. Verifiers can query certificates either by entering the unique Certificate ID (e.g., CERT-2026-0001) or by scanning the embedded QR code using a webcam or mobile camera. The interface features custom glassmorphic aesthetics, network health badges, and real-time verification indicators.")

p_sa3 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_sa3.add_run("     The backend server is implemented using Node.js and Express. It manages institutional administrator authentication using JWT tokens, maintains sequential certificate counters, and stores generated PDF copies in an encrypted filesystem directory. REST API endpoints facilitate communication between the frontend and backend and support data synchronization.")

add_heading_2(doc, "System Architecture of CertChain")
if os.path.exists(arch_diagram_path):
    p_arch = doc.add_paragraph()
    p_arch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_arch.paragraph_format.space_before = Pt(8)
    p_arch.paragraph_format.space_after = Pt(4)
    p_arch.add_run().add_picture(arch_diagram_path, width=Cm(15.0))
    p_arch_cap = add_p(doc, "Fig. 5.1: System Architecture of CertChain", space_before=2, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, font_size=9.5)

add_heading_2(doc, "Data Flow")
p_df1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_df1.add_run("     The data flow of CertChain describes how credential information moves between the administrator interface, the cryptographic engine, backend relayer services, the SQLite database, and the Ethereum blockchain. The workflow begins when an institutional user accesses the issuance portal and specifies recipient details, course title, and honors.")

p_df2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_df2.add_run("     When the administrator triggers certificate generation, the client-side vector engine renders the certificate PDF. A SHA-256 cryptographic digest is calculated from the exact binary bytes of the PDF. If relayer issuance is selected, the frontend sends the certificate ID and hash to the Node.js backend, which constructs, signs, and broadcasts an Ethereum transaction using the university's relayer key. The transaction receipt (txHash and block number) is returned to the client and recorded in SQLite.")

add_heading_2(doc, "Data Flow of CertChain")
if os.path.exists(dataflow_diagram_path):
    p_df = doc.add_paragraph()
    p_df.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_df.paragraph_format.space_before = Pt(8)
    p_df.paragraph_format.space_after = Pt(4)
    p_df.add_run().add_picture(dataflow_diagram_path, width=Cm(15.0))
    p_df_cap = add_p(doc, "Fig. 5.2: Cryptographic Data Flow and Issuance Lifecycle of CertChain", space_before=2, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, font_size=9.5)

add_heading_2(doc, "Data Sets and Verification Pipeline")
p_ds1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_ds1.add_run("     CertChain maintains structured certificate records containing certificate IDs, recipient names, course titles, achievement honors, issuance timestamps, SHA-256 hashes, issuer Ethereum addresses, transaction hashes, and on-chain validity flags. The SQLite database provides high-speed query indexing for institutional telemetry and administrative management.")

add_heading_2(doc, "Key Features Extracted for Functionality")
doc.add_paragraph("• Certificate Registry: Recipient identity, course completion, timestamped issuance metadata, and transaction hashes.", style='List Bullet')
doc.add_paragraph("• Cryptographic Fingerprint: SHA-256 binary hash derived from deterministic vector PDF bytes.", style='List Bullet')
doc.add_paragraph("• Smart Contract State: Immutable on-chain mapping associating certificate IDs with document hashes, issuer addresses, and revocation booleans.", style='List Bullet')
doc.add_paragraph("• Optical Verification: Encoded QR matrix containing direct verification URIs for instant camera decoding.", style='List Bullet')
doc.add_paragraph("• Zero-Trust Validation: Direct JSON-RPC Sepolia queries comparing client-side presented documents against immutable on-chain anchors.", style='List Bullet')

doc.add_page_break()

# ==========================================
# PAGES 21 - 24: SCREENS (SCREENSHOTS 5.4.1 TO 5.4.8)
# Matching friend's report Pages 21-24: 2 screenshots per page with 5.4.x titles!
# ==========================================
add_heading_1(doc, "Screens")

# Screen 5.4.1 & 5.4.2
add_heading_2(doc, "5.4.1 Home Page")
if os.path.exists("presentation_assets/01_Landing_Hero.png"):
    p_s1 = doc.add_paragraph()
    p_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s1.paragraph_format.space_before = Pt(4)
    p_s1.paragraph_format.space_after = Pt(8)
    p_s1.add_run().add_picture("presentation_assets/01_Landing_Hero.png", width=Cm(14.5))

add_heading_2(doc, "5.4.2 Dashboard")
if os.path.exists("presentation_assets/02_Public_Verify_Interface.png"):
    p_s2 = doc.add_paragraph()
    p_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s2.paragraph_format.space_before = Pt(4)
    p_s2.paragraph_format.space_after = Pt(8)
    p_s2.add_run().add_picture("presentation_assets/02_Public_Verify_Interface.png", width=Cm(14.5))

doc.add_page_break()

# Screen 5.4.3 & 5.4.4
add_heading_2(doc, "5.4.3 QR Code Scanner")
if os.path.exists("presentation_assets/03_QR_Camera_Scanner.png"):
    p_s3 = doc.add_paragraph()
    p_s3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s3.paragraph_format.space_before = Pt(4)
    p_s3.paragraph_format.space_after = Pt(8)
    p_s3.add_run().add_picture("presentation_assets/03_QR_Camera_Scanner.png", width=Cm(14.5))

add_heading_2(doc, "5.4.4 Verified Result Card")
if os.path.exists("presentation_assets/05_Verified_Certificate_Result.png"):
    p_s4 = doc.add_paragraph()
    p_s4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s4.paragraph_format.space_before = Pt(4)
    p_s4.paragraph_format.space_after = Pt(8)
    p_s4.add_run().add_picture("presentation_assets/05_Verified_Certificate_Result.png", width=Cm(14.5))

doc.add_page_break()

# Screen 5.4.5 & 5.4.6
add_heading_2(doc, "5.4.5 Admin Telemetry Portal")
if os.path.exists("presentation_assets/07_Admin_Dashboard_Telemetry.png"):
    p_s5 = doc.add_paragraph()
    p_s5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s5.paragraph_format.space_before = Pt(4)
    p_s5.paragraph_format.space_after = Pt(8)
    p_s5.add_run().add_picture("presentation_assets/07_Admin_Dashboard_Telemetry.png", width=Cm(14.5))

add_heading_2(doc, "5.4.6 Certificate Issuance Portal")
if os.path.exists("presentation_assets/08_Issue_Credential_Live_Preview.png"):
    p_s6 = doc.add_paragraph()
    p_s6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s6.paragraph_format.space_before = Pt(4)
    p_s6.paragraph_format.space_after = Pt(8)
    p_s6.add_run().add_picture("presentation_assets/08_Issue_Credential_Live_Preview.png", width=Cm(14.5))

doc.add_page_break()

# Screen 5.4.7 & 5.4.8
add_heading_2(doc, "5.4.7 Certificate Registry and Revocation Management")
if os.path.exists("presentation_assets/09_Certificates_Registry_Table.png"):
    p_s7 = doc.add_paragraph()
    p_s7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s7.paragraph_format.space_before = Pt(4)
    p_s7.paragraph_format.space_after = Pt(8)
    p_s7.add_run().add_picture("presentation_assets/09_Certificates_Registry_Table.png", width=Cm(14.5))

add_heading_2(doc, "5.4.8 Cloud Production Deployment")
if os.path.exists("presentation_assets/11_Netlify_Public_Deployment.png"):
    p_s8 = doc.add_paragraph()
    p_s8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s8.paragraph_format.space_before = Pt(4)
    p_s8.paragraph_format.space_after = Pt(8)
    p_s8.add_run().add_picture("presentation_assets/11_Netlify_Public_Deployment.png", width=Cm(14.5))

doc.add_page_break()

# ==========================================
# PAGES 25 - 26: CHAPTER 4 - LEARNING AFTER INTERNSHIP
# ==========================================
add_heading_1(doc, "LEARNING AFTER INTERNSHIP")

p_l1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_l1.add_run("     The internship provided valuable practical exposure to Blockchain Engineering, Smart Contract Architecture, and Web3 application development. It helped me understand how theoretical cryptographic principles can be applied to develop a tamper-proof decentralized software system. Working on ")
p_l1.add_run("CertChain — Decentralized Academic Credential Verification Platform").font.bold = True
p_l1.add_run(" improved my understanding of frontend development, backend functionality, database management, smart contract execution, document fingerprinting, and decentralized state coordination.")

p_l2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_l2.add_run("     I gained practical knowledge of Solidity programming and learned how smart contracts execute within the Ethereum Virtual Machine (EVM). I understood how to manage persistent blockchain storage, use struct mappings for certificate tracking, implement role-based access control with OpenZeppelin Ownable, and optimize gas consumption during batch transaction execution. I also learned how to use the Foundry development toolkit (forge, cast, test) for rigorous automated smart contract unit testing and testnet deployment.")

p_l3 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_l3.add_run("     The internship improved my understanding of backend development through Node.js and Express. I learned how backend services manage institutional administrator authentication using JWT tokens, handle sequential ID generation, and maintain persistent SQLite databases. I also gained practical knowledge of transaction relaying, understanding how institutional key custody allows organizations to sponsor gas fees on behalf of non-technical administrators.")

p_l4 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_l4.add_run("     I gained practical understanding of database management through SQLite and learned how structured records can be indexed for high-performance administrative dashboards. The project helped me understand how databases support certificate query caching, event logging, and status tracking while maintaining synchronization with on-chain Ethereum state.")

p_l5 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_l5.add_run("     Another important area of learning was document processing and optical computer vision. I gained knowledge of how jsPDF can compile deterministic vector PDFs and how html5-qrcode can capture live video frames from webcams or smartphone cameras to decode embedded QR barcode matrices in real time. I also learned how the Web Cryptography API generates SHA-256 hashes directly in the browser, ensuring mathematical data integrity.")

p_l6 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_l6.add_run("     Apart from technical skills, the internship improved my problem-solving, debugging, integration, and documentation skills. Working on CertChain helped me understand how frontend interfaces, backend services, databases, cryptographic engines, and smart contracts can be combined into a seamless, enterprise-grade application.")

p_l7 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_l7.add_run("     Overall, the internship strengthened my technical knowledge and provided practical experience in developing a production-ready Web3 application. It helped me apply concepts learned during my academic studies to a practical project and improved my understanding of how Blockchain and decentralized architectures can solve real-world integrity challenges.")

doc.add_page_break()

# ==========================================
# PAGES 27 - 28: CHAPTER 5 - SUMMARY / CONCLUSION & FUTURE SCOPE
# ==========================================
add_heading_1(doc, "SUMMARY / CONCLUSION")

p_sc1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_sc1.add_run("     ")
p_sc1.add_run("CertChain — Decentralized Academic Credential Verification Platform").font.bold = True
p_sc1.add_run(" was developed as a production-grade Web3 application designed to eliminate credential forgery and provide instant, decentralized verification of educational records. The system integrates smart contracts on Ethereum Sepolia, institutional relayer services, SQLite query caching, deterministic vector PDF generation, client-side SHA-256 document fingerprinting, and real-time optical QR barcode scanning within a unified platform.")

p_sc2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_sc2.add_run("     The application combines modern frontend and backend technologies to provide an integrated software solution. React 18 is used to develop the interactive user interface with glassmorphic styling, while Node.js and Express handle backend operations, sequential ID tracking, and transaction relaying. SQLite is used to store structured certificate records, administrator credentials, and audit logs.")

p_sc3 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_sc3.add_run("     A key feature of the system is its decentralized verification model. By anchoring immutable SHA-256 document digests on Ethereum Sepolia, CertChain enables employers and verification agencies to validate credentials directly against blockchain consensus. This eliminates costly intermediaries, reduces verification latency from weeks to milliseconds, and protects student privacy by avoiding the exposure of personally identifiable information on public ledgers.")

p_sc4 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_sc4.add_run("     The development of CertChain provided practical experience in Solidity smart contract engineering, EVM architecture, frontend development, backend services, database management, REST API integration, client-side cryptography, and cloud DevOps. The project demonstrated how these technologies can be integrated to develop an enterprise-ready system that restores mathematical integrity to academic credentials.")

p_sc5 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_sc5.add_run("     Overall, CertChain demonstrates the practical application of Blockchain technology in higher education administration. It provides a foundation for further improvements in digital identity and decentralized accreditation. The application successfully bridges academic computer science theory with enterprise-grade decentralized software engineering.")

add_heading_2(doc, "Future Scope")
p_fs1 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_fs1.add_run("     CertChain can be enhanced by introducing additional capabilities such as Soulbound Tokens (ERC-5192) tied to decentralized student identity wallets, Zero-Knowledge Proofs (zk-SNARKs) for selective attribute disclosure without revealing full academic transcripts, and Layer-2 scaling (Arbitrum, Optimism, Polygon) for sub-cent transaction fees at institutional scale.")

p_fs2 = add_p(doc, "", space_before=6, space_after=12, line_spacing=1.35)
p_fs2.add_run("     Future versions could also establish multi-university consortium networks, enabling federated decentralized identity verification across international university alliances, automated diploma NFT minting upon registrar grade submission, and mobile wallet integrations supporting Apple Wallet and Google Wallet digital identity credentials.")

doc.add_page_break()

# ==========================================
# PAGE 29: CHAPTER 6 - BIBLIOGRAPHY
# ==========================================
add_heading_1(doc, "BIBLIOGRAPHY")

bib_items = [
    ("Nakamoto, S.", "Bitcoin: A Peer-to-Peer Electronic Cash System. Cryptography Mailing List, 2008."),
    ("Wood, G.", "Ethereum: A Secure Decentralised Generalised Transaction Ledger. Ethereum Project Yellow Paper, 2014."),
    ("Ethereum Foundation", "Solidity Documentation. Official documentation for the Solidity smart contract programming language, 2024. https://docs.soliditylang.org/"),
    ("OpenZeppelin", "OpenZeppelin Contracts Documentation. Standard for secure blockchain applications, 2024. https://docs.openzeppelin.com/contracts/"),
    ("Foundry Development Team", "Foundry Book: Modular EVM Application Development Toolkit, 2024. https://book.getfoundry.sh/"),
    ("Ethers.js Contributors", "Ethers.js Documentation: Complete Ethereum Library and Wallet Implementation in TypeScript and JavaScript, 2024. https://docs.ethers.org/v6/"),
    ("National Institute of Standards and Technology (NIST)", "FIPS PUB 180-4: Secure Hash Standard (SHS), 2015. https://csrc.nist.gov/publications/detail/fips/180/4/final"),
    ("World Wide Web Consortium (W3C)", "Decentralized Identifiers (DIDs) v1.0: Core Architecture, Data Model, and Representations, 2022. https://www.w3.org/TR/did-core/"),
    ("Netlify Inc.", "Netlify Edge Platform Documentation: Modern Hosting Architecture for Serverless and JAMstack Applications, 2024. https://docs.netlify.com/"),
    ("Parashar, N.", "jsPDF: Client-side JavaScript PDF Generator Documentation, 2024. https://github.com/parallax/jsPDF"),
    ("Mecheve, M.", "html5-qrcode: An End-to-End In-Browser Optical QR and Barcode Scanning Library, 2024. https://github.com/mebjas/html5-qrcode"),
    ("SQLite Development Team", "SQLite Database Architecture and SQL Engine Documentation, 2024. https://www.sqlite.org/docs.html"),
    ("React Core Team", "React Documentation: The Library for Web and Native User Interfaces, 2024. https://react.dev/"),
    ("Express.js Foundation", "Express.js REST API Framework Documentation, 2024. https://expressjs.com/"),
    ("CertChain Project Repository", "CertChain Source Code Repository and Technical Verification Specifications, 2026. https://github.com/Keerthi1316/certchain")
]

for idx, (authors, title) in enumerate(bib_items, 1):
    p_b = add_p(doc, "", space_before=4, space_after=6, line_spacing=1.35)
    r_idx = p_b.add_run(f"{idx}. {authors}, ")
    r_idx.font.bold = True
    r_t = p_b.add_run(title)
    r_t.font.italic = True if "http" not in title else False

doc.add_page_break()

# ==========================================
# PAGES 30 - 31: PROGRAM OUTCOMES (POs & PSOs)
# Matching friend's Pages 30-31 word for word
# ==========================================
add_heading_2(doc, "PROGRAM OUTCOMES (POs)")

p_po_intro = add_p(doc, "Program Outcomes (POs) describe what students are expected to know and be able to do by the time of graduation to accomplish Program Educational Objectives (PEOs). The Program Outcomes for CSE-Artificial Intelligence and Machine Learning graduates are:\nEngineering Graduates would be able to:", space_before=6, space_after=10, line_spacing=1.35)

add_heading_2(doc, "PROGRAM OUTCOMES")

pos = [
    ("1. Engineering Knowledge: ", "Apply knowledge of mathematics, natural science, computing, engineering fundamentals and an engineering specialization as specified in WK1 to WK4 respectively to develop to the solution of complex engineering problems."),
    ("2. Problem analysis: ", "Identify, formulate, review research literature and analyze complex engineering problems reaching substantiated conclusions with consideration for sustainable development."),
    ("3. Design/development of solutions: ", "Design creative solutions for complex engineering problems and design/develop systems/components/processes to meet identified needs with consideration for the public health and safety, whole-life cost, net zero carbon, culture, society and environment as required."),
    ("4. Conduct investigations of complex problems: ", "Conduct investigations of complex engineering problems using research-based knowledge including design of experiments, modelling, analysis & interpretation of data to provide valid conclusions."),
    ("5. Engineering tool usage: ", "Create, select and apply appropriate techniques, resources and modern engineering & IT tools, including prediction and modelling recognizing their limitations to solve complex engineering problems."),
    ("6. The engineer and the world: ", "Analyze and evaluate societal and environmental aspects while solving complex engineering problems for its impact on sustainability with reference to economy, health, safety, legal framework, culture and environment."),
    ("7. Ethics: ", "Apply ethical principles and commit to professional ethics, human values, diversity and inclusion; adhere to national & international laws."),
    ("8. Individual and Collaborative team work: ", "Function effectively as an individual, and as a member or leader in diverse/multi-disciplinary teams."),
    ("9. Communication: ", "Communicate effectively and inclusively within the engineering community and society at large, such as being able to comprehend and write effective reports and design documentation, make effective presentations considering cultural, language, and learning differences"),
    ("10. Project management and finance: ", "Apply knowledge and understanding of engineering management principles and economic decision-making and apply these to one’s own work, as a member and leader in a team, and to manage projects and in multidisciplinary environments."),
    ("11. Life-long learning: ", "Recognize the need for, and have the preparation and ability for i) independent and life-long learning ii) adaptability to new and emerging technologies and iii) critical thinking in the broadest context of technological change.")
]

for po_title, po_desc in pos:
    p_po = add_p(doc, "", space_before=3, space_after=6, line_spacing=1.3)
    r_pot = p_po.add_run(po_title)
    r_pot.font.bold = True
    p_po.add_run(po_desc)

add_heading_2(doc, "PROGRAM SPECIFIC OUTCOMES:")

psos = [
    ("PSO 1: ", "Demonstrate competency in Programming and problem-solving skills and apply those skills in solving computing problems"),
    ("PSO 2: ", "Select appropriate programming languages, Data structures and algorithms in combination with modern technologies and apply them in developing innovative solutions"),
    ("PSO 3: ", "Demonstrate adequate knowledge in the concepts and techniques of artificial intelligence and machine learning, apply them in developing intelligent systems to solve real world problems.")
]

for pso_title, pso_desc in psos:
    p_pso = add_p(doc, "", space_before=3, space_after=6, line_spacing=1.3)
    r_psot = p_pso.add_run(pso_title)
    r_psot.font.bold = True
    p_pso.add_run(pso_desc)

doc.add_page_break()

# ==========================================
# PAGE 32: DEPARTMENT WORK TABLES (TABLES 1, 2, 3, 4)
# Matching friend's Page 32 and Template Page 17
# ==========================================
p_last_banner = add_p(doc, "The following pages print on end of the report, i.e. last three pages for department work.", space_before=4, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11, color=RGBColor(180, 20, 20))

# Table 1: Correlation between Project and POs/PSOs
p_t1 = add_p(doc, "Table1: Correlation between the Internship Project and Program Outcomes (POs), Program Specific Outcomes (PSOs).", space_before=4, space_after=6, bold=True, font_size=11)

tbl_1 = doc.add_table(rows=2, cols=3)
tbl_1.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_1.autofit = False
tbl_1.columns[0].width = Inches(1.8)
tbl_1.columns[1].width = Inches(2.0)
tbl_1.columns[2].width = Inches(2.1)

t1_headers = ["Roll No", "Name", "Title"]
t1_vals = ["24R11A66N9", "Katuri Keerthi", "CertChain"]

for c in range(3):
    c0 = tbl_1.cell(0, c)
    c1 = tbl_1.cell(1, c)
    c0.paragraphs[0].text = t1_headers[c]
    c1.paragraphs[0].text = t1_vals[c]
    set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
    set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
    b_def = {"top": {"val": "single", "sz": 4, "color": "000000"},
             "bottom": {"val": "single", "sz": 4, "color": "000000"},
             "left": {"val": "single", "sz": 4, "color": "000000"},
             "right": {"val": "single", "sz": 4, "color": "000000"}}
    set_cell_border(c0, **b_def); set_cell_border(c1, **b_def)
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))

# Table 2: PO/PSO Correlation Level
p_t2 = add_p(doc, "Table2: Project correlation with appropriate POs/PSOs (Please specify level of correlation H, M, L against POs/PSOs).", space_before=10, space_after=4, bold=True, font_size=11)

p_hml = add_p(doc, "H   High        M   Medium        L   Low", space_before=2, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=10)

p_t2_sub = add_p(doc, "Internship Project correlation with appropriate POs/PSOs", space_before=2, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=10.5)

tbl_2 = doc.add_table(rows=2, cols=14)
tbl_2.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_2.autofit = False

t2_cols = ["PO1", "PO2", "PO3", "PO4", "PO5", "PO6", "PO7", "PO8", "PO9", "PO10", "PO11", "PSO1", "PSO2", "PSO3"]
t2_ratings = ["H", "H", "H", "H", "H", "M", "H", "M", "H", "M", "H", "H", "H", "H"]

for c in range(14):
    tbl_2.columns[c].width = Inches(0.42)
    c0 = tbl_2.cell(0, c)
    c1 = tbl_2.cell(1, c)
    c0.paragraphs[0].text = t2_cols[c]
    c1.paragraphs[0].text = t2_ratings[c]
    set_cell_margins(c0, top=40, bottom=40, left=30, right=30)
    set_cell_margins(c1, top=40, bottom=40, left=30, right=30)
    set_cell_border(c0, **b_def); set_cell_border(c1, **b_def)
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(8.5)
    c1.paragraphs[0].runs[0].font.size = Pt(9)
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))

# Table 3: Nature of Project
p_t3 = add_p(doc, "Table3: Nature of Internship work (Please tick ✓ appropriate for your Project)", space_before=10, space_after=4, bold=True, font_size=11)

tbl_3 = doc.add_table(rows=2, cols=6)
tbl_3.alignment = WD_TABLE_ALIGNMENT.CENTER
t3_headers = ["Roll Number", "Title", "Product", "Application", "Research", "Others (Please Specify)"]
t3_vals = ["24R11A66N9", "CertChain", "✓", "✓", "", ""]

for c in range(6):
    c0 = tbl_3.cell(0, c)
    c1 = tbl_3.cell(1, c)
    c0.paragraphs[0].text = t3_headers[c]
    c1.paragraphs[0].text = t3_vals[c]
    set_cell_margins(c0, top=50, bottom=50, left=50, right=50)
    set_cell_margins(c1, top=50, bottom=50, left=50, right=50)
    set_cell_border(c0, **b_def); set_cell_border(c1, **b_def)
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(9.5)
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))

# Table 4: Project Domain
p_t4 = add_p(doc, "Table4: Nature of Internship Project work (Please tick ✓ appropriate for your Project)", space_before=10, space_after=4, bold=True, font_size=11)

tbl_4 = doc.add_table(rows=2, cols=6)
tbl_4.alignment = WD_TABLE_ALIGNMENT.CENTER
t4_headers = ["Roll Number", "AI", "ML/DL", "Web Applications/Mern Stack", "Network Security", "IoT"]
t4_vals = ["24R11A66N9", "", "", "✓", "✓ (Blockchain Security)", ""]

for c in range(6):
    c0 = tbl_4.cell(0, c)
    c1 = tbl_4.cell(1, c)
    c0.paragraphs[0].text = t4_headers[c]
    c1.paragraphs[0].text = t4_vals[c]
    set_cell_margins(c0, top=50, bottom=50, left=40, right=40)
    set_cell_margins(c1, top=50, bottom=50, left=40, right=40)
    set_cell_border(c0, **b_def); set_cell_border(c1, **b_def)
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(9)
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))

output_doc = "Katuri_Keerthi_24R11A66N9_Internship_Report.docx"
doc.save(output_doc)
print(f"SUCCESS: Report saved as {output_doc} (Size: {os.path.getsize(output_doc)} bytes)")
