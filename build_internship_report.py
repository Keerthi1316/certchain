import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
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
    kwargs: top, bottom, left, right
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

def add_header_footer(doc):
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.9)
        
        # Header
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Internship Report          Department of CSE-AI&ML          2026-27")
        hrun.font.name = 'Times New Roman'
        hrun.font.size = Pt(9)
        hrun.font.color.rgb = RGBColor(100, 100, 100)
        
        # Footer
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun = fp.add_run("Internship Report          Department of CSE-AI&ML          2026-27")
        frun.font.name = 'Times New Roman'
        frun.font.size = Pt(9)
        frun.font.color.rgb = RGBColor(100, 100, 100)

doc = Document()
add_header_footer(doc)

# Set base normal style font
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.font.color.rgb = RGBColor(0, 0, 0)

logo_path = 'presentation_assets/extracted_p1_img1.jpeg'
cert_img_path = 'presentation_assets/katuri_keerthi_internship_certificate.png'

# ==========================================
# PAGE 1: COVER PAGE
# ==========================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
p.paragraph_format.space_after = Pt(4)
r = p.add_run("An\nInternship Report on\n\n")
r.font.size = Pt(14)
r.font.bold = True

r2 = p.add_run("Blockchain — CertChain:\nDecentralized Academic Credential Verification Platform")
r2.font.size = Pt(18)
r2.font.bold = True
r2.font.color.rgb = RGBColor(20, 40, 120)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(16)
p_sub.paragraph_format.space_after = Pt(16)
r_sub = p_sub.add_run("Submitted\nin partial fulfillment of the requirements for the award of the degree of\n")
r_sub.font.size = Pt(11)
r_sub.font.italic = True

r_deg = p_sub.add_run("BACHELOR OF TECHNOLOGY\nin\nCSE-Artificial Intelligence and Machine Learning")
r_deg.font.size = Pt(14)
r_deg.font.bold = True
r_deg.font.color.rgb = RGBColor(0, 102, 102)

p_by = doc.add_paragraph()
p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_by.paragraph_format.space_before = Pt(12)
p_by.paragraph_format.space_after = Pt(16)
r_by = p_by.add_run("By\n")
r_by.font.size = Pt(12)
r_name = p_by.add_run("KATURI KEERTHI\n")
r_name.font.size = Pt(16)
r_name.font.bold = True
r_roll = p_by.add_run("24R11A66N9")
r_roll.font.size = Pt(14)
r_roll.font.bold = True

if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_after = Pt(8)
    p_logo.add_run().add_picture(logo_path, width=Inches(1.5))

p_col = doc.add_paragraph()
p_col.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_col.paragraph_format.space_after = Pt(2)
r_dept = p_col.add_run("Department of CSE-Artificial Intelligence and Machine Learning\n")
r_dept.font.size = Pt(12)
r_dept.font.bold = True
r_dept.font.color.rgb = RGBColor(0, 128, 128)

r_cname = p_col.add_run("Geethanjali College of Engineering and Technology\n")
r_cname.font.size = Pt(14)
r_cname.font.bold = True
r_cname.font.color.rgb = RGBColor(180, 20, 20)

r_cinfo = p_col.add_run("(UGC AUTONOMOUS INSTITUTION)\n(Affiliated to J.N.T.U.H, Approved by AICTE, New Delhi)\nCheeryal (V), Keesara (M), Medchal Dist.-501 301.\n")
r_cinfo.font.size = Pt(10)

r_date = p_col.add_run("August - 2026")
r_date.font.size = Pt(12)
r_date.font.bold = True

doc.add_page_break()

# ==========================================
# PAGE 2: CERTIFICATE (COLLEGE)
# ==========================================
p_ch = doc.add_paragraph()
p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ch.paragraph_format.space_after = Pt(2)
r_ch1 = p_ch.add_run("Geethanjali College of Engineering & Technology\n")
r_ch1.font.size = Pt(16)
r_ch1.font.bold = True
r_ch1.font.color.rgb = RGBColor(180, 20, 20)

r_ch2 = p_ch.add_run("(UGC Autonomous)\n(Affiliated to JNTUH, Approved by AICTE, New Delhi)\nCheeryal (V), Keesara(M), Medchal Dist.-501 301.\n\n")
r_ch2.font.size = Pt(10)

r_ch3 = p_ch.add_run("Department of CSE-Artificial Intelligence and Machine Learning")
r_ch3.font.size = Pt(13)
r_ch3.font.bold = True
r_ch3.font.color.rgb = RGBColor(0, 102, 153)

if os.path.exists(logo_path):
    p_clogo = doc.add_paragraph()
    p_clogo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_clogo.paragraph_format.space_after = Pt(6)
    p_clogo.add_run().add_picture(logo_path, width=Inches(1.3))

p_ctitle = doc.add_paragraph()
p_ctitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ctitle.paragraph_format.space_after = Pt(14)
r_ct = p_ctitle.add_run("CERTIFICATE")
r_ct.font.size = Pt(18)
r_ct.font.bold = True
r_ct.font.color.rgb = RGBColor(180, 120, 0)

p_cbody = doc.add_paragraph()
p_cbody.paragraph_format.line_spacing = 1.3
p_cbody.paragraph_format.space_after = Pt(24)
p_cbody.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r_cb = p_cbody.add_run("This is to certify that the internship report titled ")
r_cb.font.size = Pt(11)

r_cb_t = p_cbody.add_run("“Blockchain — CertChain: Decentralized Academic Credential Verification Platform”")
r_cb_t.font.size = Pt(11)
r_cb_t.font.bold = True

r_cb_2 = p_cbody.add_run(" being submitted by ")
r_cb_2.font.size = Pt(11)

r_cb_n = p_cbody.add_run("KATURI KEERTHI")
r_cb_n.font.size = Pt(11)
r_cb_n.font.bold = True

r_cb_3 = p_cbody.add_run(", bearing roll number ")
r_cb_3.font.size = Pt(11)

r_cb_r = p_cbody.add_run("24R11A66N9")
r_cb_r.font.size = Pt(11)
r_cb_r.font.bold = True

r_cb_4 = p_cbody.add_run(", in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology in ")
r_cb_4.font.size = Pt(11)

r_cb_b = p_cbody.add_run("“CSE-Artificial Intelligence and Machine Learning”")
r_cb_b.font.size = Pt(11)
r_cb_b.font.bold = True

r_cb_5 = p_cbody.add_run(" from Jawaharlal Nehru Technological University, Hyderabad during the academic year 2026-2027.")
r_cb_5.font.size = Pt(11)

# Signatures Table
tbl_sig = doc.add_table(rows=1, cols=2)
tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_sig.autofit = False
tbl_sig.columns[0].width = Inches(3.3)
tbl_sig.columns[1].width = Inches(3.3)

c0 = tbl_sig.cell(0, 0)
p0 = c0.paragraphs[0]
p0.paragraph_format.line_spacing = 1.15
r_s1 = p0.add_run("Internship Supervisor\nMr. G. Raju\n(Asst. Prof, CSE-AI&ML)")
r_s1.font.bold = True
r_s1.font.size = Pt(11)

c1 = tbl_sig.cell(0, 1)
p1 = c1.paragraphs[0]
p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p1.paragraph_format.line_spacing = 1.15
r_s2 = p1.add_run("Internship Coordinator\nMr. Vedavyas Gurla\n(Assoc. Prof, CSE-AI&ML)")
r_s2.font.bold = True
r_s2.font.size = Pt(11)

p_hod = doc.add_paragraph()
p_hod.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_hod.paragraph_format.space_before = Pt(28)
p_hod.paragraph_format.space_after = Pt(28)
r_hod = p_hod.add_run("Dr. L. Venkateswarlu\n(Professor & HoD, CSE-AI&ML)")
r_hod.font.bold = True
r_hod.font.size = Pt(11)

p_ex = doc.add_paragraph()
p_ex.paragraph_format.line_spacing = 1.2
r_ex = p_ex.add_run("Examiner\nSignature: ___________________________\nName: ______________________________\nDesignation: _________________________")
r_ex.font.size = Pt(10.5)

doc.add_page_break()

# ==========================================
# PAGE 3: CERTIFICATE OF INTERNSHIP (ATTACHED CERTIFICATE IMAGE)
# ==========================================
p_ic_h = doc.add_paragraph()
p_ic_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ic_h.paragraph_format.space_after = Pt(10)
r_ic_h = p_ic_h.add_run("INTERNSHIP COMPLETION CERTIFICATE")
r_ic_h.font.size = Pt(15)
r_ic_h.font.bold = True
r_ic_h.font.color.rgb = RGBColor(20, 40, 120)

if os.path.exists(cert_img_path):
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert.paragraph_format.space_after = Pt(10)
    p_cert.add_run().add_picture(cert_img_path, width=Inches(6.4))

p_ic_c = doc.add_paragraph()
p_ic_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_ic_c = p_ic_c.add_run("Fig: Certificate of Internship awarded to KATURI KEERTHI (CUTM/AP/26/907367077873)\nCenturion University of Technology and Management — School of Future Nexus")
r_ic_c.font.size = Pt(9.5)
r_ic_c.font.italic = True

doc.add_page_break()

# ==========================================
# PAGE 4: DECLARATION BY THE CANDIDATE
# ==========================================
p_dh = doc.add_paragraph()
p_dh.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dh.paragraph_format.space_after = Pt(2)
r_dh1 = p_dh.add_run("Geethanjali College of Engineering & Technology\n")
r_dh1.font.size = Pt(16)
r_dh1.font.bold = True
r_dh1.font.color.rgb = RGBColor(180, 20, 20)

r_dh2 = p_dh.add_run("(UGC Autonomous)\n(Affiliated to JNTUH, Approved by AICTE, New Delhi)\nCheeryal (V), Keesara(M), Medchal Dist.-501 301.\n\n")
r_dh2.font.size = Pt(10)

r_dh3 = p_dh.add_run("Department of CSE-Artificial Intelligence and Machine Learning")
r_dh3.font.size = Pt(13)
r_dh3.font.bold = True
r_dh3.font.color.rgb = RGBColor(0, 102, 153)

if os.path.exists(logo_path):
    p_dlogo = doc.add_paragraph()
    p_dlogo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dlogo.paragraph_format.space_after = Pt(6)
    p_dlogo.add_run().add_picture(logo_path, width=Inches(1.2))

p_dtitle = doc.add_paragraph()
p_dtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dtitle.paragraph_format.space_after = Pt(18)
r_dt = p_dtitle.add_run("DECLARATION BY THE CANDIDATE")
r_dt.font.size = Pt(16)
r_dt.font.bold = True
r_dt.font.color.rgb = RGBColor(180, 120, 0)

p_dbody = doc.add_paragraph()
p_dbody.paragraph_format.line_spacing = 1.3
p_dbody.paragraph_format.space_after = Pt(20)
p_dbody.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r_db1 = p_dbody.add_run("I, ")
r_db2 = p_dbody.add_run("KATURI KEERTHI")
r_db2.font.bold = True
r_db3 = p_dbody.add_run(", bearing Roll No. ")
r_db4 = p_dbody.add_run("24R11A66N9")
r_db4.font.bold = True
r_db5 = p_dbody.add_run(", hereby declare that the Internship Report entitled ")
r_db6 = p_dbody.add_run("“Blockchain — CertChain: Decentralized Academic Credential Verification Platform”")
r_db6.font.bold = True
r_db7 = p_dbody.add_run(" is submitted in partial fulfillment of the requirements for the award of the degree of ")
r_db8 = p_dbody.add_run("Bachelor of Technology in CSE-Artificial Intelligence and Machine Learning.\n\n")
r_db8.font.bold = True

r_db9 = p_dbody.add_run("This is a record of bonafide work carried out by me during the internship program at ")
r_db10 = p_dbody.add_run("Centurion University of Technology and Management (School of Future Nexus)")
r_db10.font.bold = True
r_db11 = p_dbody.add_run(" on Blockchain technology, and the results embodied in this internship report have not been reproduced or copied from any source. The results embodied in this Internship Report have not been submitted to any other University or Institute for the award of any degree or diploma.")

p_dsig = doc.add_paragraph()
p_dsig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_dsig.paragraph_format.space_before = Pt(40)
r_ds = p_dsig.add_run("Signature of Student\n")
r_ds.font.bold = True
r_ds_name = p_dsig.add_run("KATURI KEERTHI\n(24R11A66N9)")
r_ds_name.font.size = Pt(11)

doc.add_page_break()

# ==========================================
# PAGE 5: ACKNOWLEDGEMENT
# ==========================================
p_ah = doc.add_paragraph()
p_ah.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ah.paragraph_format.space_after = Pt(20)
r_ah = p_ah.add_run("ACKNOWLEDGEMENT")
r_ah.font.size = Pt(16)
r_ah.font.bold = True

p_ab = doc.add_paragraph()
p_ab.paragraph_format.line_spacing = 1.3
p_ab.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_ab.paragraph_format.space_after = Pt(14)
p_ab.add_run("I would like to express my heartfelt gratitude to everyone who played a role in the successful completion of this internship project. My deepest thanks go to our Director, ")
p_ab.add_run("Dr. Uday Kumar Susarla").font.bold = True
p_ab.add_run(", and our college Principal, ")
p_ab.add_run("Dr. K. Sagar").font.bold = True
p_ab.add_run(", for providing the essential resources, advanced computing infrastructure, and unwavering support throughout this endeavor.")

p_ab2 = doc.add_paragraph()
p_ab2.paragraph_format.line_spacing = 1.3
p_ab2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_ab2.paragraph_format.space_after = Pt(14)
p_ab2.add_run("I am profoundly grateful to the Professor & Dean - School of CS and Informatics, ")
p_ab2.add_run("Dr. V. Madhusudan Rao").font.bold = True
p_ab2.add_run(", and our Head of Department, ")
p_ab2.add_run("Dr. L. Venkateswarlu").font.bold = True
p_ab2.add_run(", for their invaluable guidance, encouragement, and technical advice throughout the duration of this internship project.")

p_ab3 = doc.add_paragraph()
p_ab3.paragraph_format.line_spacing = 1.3
p_ab3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_ab3.paragraph_format.space_after = Pt(14)
p_ab3.add_run("I would like to extend my heartfelt gratitude to our beloved faculty and Internship Supervisor, ")
p_ab3.add_run("Mr. G. Raju").font.bold = True
p_ab3.add_run(" (Asst. Prof, CSE-AI&ML), whose invaluable expertise, constant feedback, and guidance were instrumental to our success. I am also sincerely appreciative of our Internship Coordinator, ")
p_ab3.add_run("Mr. Vedavyas Gurla").font.bold = True
p_ab3.add_run(" (Assoc. Prof, CSE-AI&ML), for his unwavering support and coordination.")

p_ab4 = doc.add_paragraph()
p_ab4.paragraph_format.line_spacing = 1.3
p_ab4.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_ab4.add_run("Additionally, I express my sincere gratitude to ")
p_ab4.add_run("Centurion University of Technology and Management (School of Future Nexus)").font.bold = True
p_ab4.add_run(", especially ")
p_ab4.add_run("Prof. Anil Kumar").font.bold = True
p_ab4.add_run(" (Dean, Extension, Skills, and Incubation), for this incredible training opportunity in Blockchain technology, hands-on exposure to decentralized applications, and professional mentorship. Thank you all for your significant contributions to my learning and professional growth.")

doc.add_page_break()

# ==========================================
# PAGE 6: INTRODUCTION ABOUT INTERNSHIP ORGANIZATION
# ==========================================
p_io_h = doc.add_paragraph()
p_io_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_io_h.paragraph_format.space_after = Pt(16)
r_io_h = p_io_h.add_run("Introduction about Internship Organization")
r_io_h.font.size = Pt(15)
r_io_h.font.bold = True

p_io1 = doc.add_paragraph()
p_io1.paragraph_format.line_spacing = 1.25
p_io1.paragraph_format.space_after = Pt(12)
p_io1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_io1.add_run("Centurion University of Technology and Management (CUTM)").font.bold = True
p_io1.add_run(" is a premier multi-sector state-enacted private university recognized by UGC and accredited by NAAC with 'A+' Grade. Through its ")
p_io1.add_run("School of Future Nexus").font.bold = True
p_io1.add_run(", the university focuses on hands-on skill development, experiential learning, and advanced technical incubation in frontier technologies including Blockchain Engineering, Distributed Ledger Systems, Web3 architectures, and Artificial Intelligence.")

p_io2 = doc.add_paragraph()
p_io2.paragraph_format.line_spacing = 1.25
p_io2.paragraph_format.space_after = Pt(12)
p_io2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_io2.add_run("The institution emphasizes industry-aligned practical exposure, bridging the gap between theoretical classroom computer science concepts and enterprise-grade decentralized software engineering. The School of Future Nexus conducts rigorous hands-on internship programs that train students on smart contract deployment, cryptographic protocols, decentralized storage, zero-knowledge proofs, and full-stack dApp engineering.")

p_io3 = doc.add_paragraph()
p_io3.paragraph_format.line_spacing = 1.25
p_io3.paragraph_format.space_after = Pt(12)
p_io3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_io3.add_run("As part of the specialized Internship Program on ")
p_io3.add_run("Blockchain").font.bold = True
p_io3.add_run(" (Certificate ID: CUTM/AP/26/907367077873), I received in-depth training on Ethereum Virtual Machine (EVM) mechanics, Solidity smart contract development, cryptographic document fingerprinting (SHA-256), gas optimization strategies, Ethers.js integration, and Web3 cloud deployments.")

p_io4 = doc.add_paragraph()
p_io4.paragraph_format.line_spacing = 1.25
p_io4.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_io4.add_run("The practical knowledge gained during the internship was directly applied to conceptualize, design, develop, deploy, and verify ")
p_io4.add_run("CertChain").font.bold = True
p_io4.add_run(" — a decentralized, tamper-proof academic and professional credential verification system anchored live on the Ethereum Sepolia blockchain network. The internship provided invaluable exposure to real-world Web3 development practices, Git version control, and production CI/CD deployment.")

doc.add_page_break()

# ==========================================
# PAGE 7: TRAINING SCHEDULE
# ==========================================
p_ts_h = doc.add_paragraph()
p_ts_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ts_h.paragraph_format.space_after = Pt(16)
r_ts_h = p_ts_h.add_run("Training Schedule")
r_ts_h.font.size = Pt(15)
r_ts_h.font.bold = True

tbl_ts = doc.add_table(rows=5, cols=2)
tbl_ts.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_ts.autofit = False
tbl_ts.columns[0].width = Inches(1.4)
tbl_ts.columns[1].width = Inches(5.2)

sched_data = [
    ("Week", "Training Schedule & Curriculum"),
    ("WEEK 1", "Introduction to Blockchain Fundamentals & Cryptography:\nPrinciples of Distributed Ledger Technology (DLT), consensus algorithms (Proof of Work vs. Proof of Stake), SHA-256 cryptographic hashing, Merkle trees, asymmetric public-private key cryptography, digital signatures, and Ethereum address derivation."),
    ("WEEK 2", "Ethereum Virtual Machine (EVM) & Solidity Smart Contracts:\nSolidity 0.8.24 programming, contract state variables, mappings, structs, modifiers, events, OpenZeppelin Ownable security patterns, Foundry development environment (forge, cast, test), gas optimization techniques, and deployment to Ethereum Sepolia Testnet."),
    ("WEEK 3", "Full-Stack Web3 Integration & Document Fingerprinting:\nEthers.js v6 library integration, MetaMask provider connectivity, JSON-RPC Sepolia network interaction, deterministic PDF generation using jsPDF, client-side SHA-256 binary hashing via Web Cryptography API, and real-time in-browser camera/image QR barcode decoding using html5-qrcode."),
    ("WEEK 4", "Project Development — CertChain & Production Cloud Deployment:\nEnd-to-end engineering of CertChain, implementation of dual-mode issuance (gasless institutional relayer vs. MetaMask Web3 signing), tamper detection pipeline, SQLite native backend storage, and live production CI/CD cloud deployment on Netlify Edge CDN and Cloudflare.")
]

for row_idx, (col0, col1) in enumerate(sched_data):
    cell0 = tbl_ts.cell(row_idx, 0)
    cell1 = tbl_ts.cell(row_idx, 1)
    
    cell0.paragraphs[0].text = col0
    cell1.paragraphs[0].text = col1
    
    cell0.paragraphs[0].paragraph_format.line_spacing = 1.15
    cell1.paragraphs[0].paragraph_format.line_spacing = 1.15
    
    set_cell_margins(cell0, top=120, bottom=120, left=150, right=150)
    set_cell_margins(cell1, top=120, bottom=120, left=150, right=150)
    
    border_kwargs = {"top": {"val": "single", "sz": 6, "color": "000000"},
                     "bottom": {"val": "single", "sz": 6, "color": "000000"},
                     "left": {"val": "single", "sz": 6, "color": "000000"},
                     "right": {"val": "single", "sz": 6, "color": "000000"}}
    set_cell_border(cell0, **border_kwargs)
    set_cell_border(cell1, **border_kwargs)
    
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
p_toc_h = doc.add_paragraph()
p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_toc_h.paragraph_format.space_after = Pt(16)
r_toc_h = p_toc_h.add_run("TABLE OF CONTENTS")
r_toc_h.font.size = Pt(15)
r_toc_h.font.bold = True

tbl_toc = doc.add_table(rows=12, cols=3)
tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_toc.autofit = False
tbl_toc.columns[0].width = Inches(1.0)
tbl_toc.columns[1].width = Inches(4.5)
tbl_toc.columns[2].width = Inches(1.1)

toc_data = [
    ("S. No", "Contents", "Page No"),
    ("", "Abstract", "i"),
    ("", "List of Figures / Diagrams", "ii"),
    ("", "List of Tables", "iii"),
    ("", "List of Screenshots", "iv"),
    ("", "List of Symbols & Abbreviations", "v"),
    ("1", "Introduction", "1"),
    ("2", "Related Work / Technologies Used", "3"),
    ("3", "Work Done / Duties Performed / System Architecture", "7"),
    ("4", "Learning After Internship", "14"),
    ("5", "Summary / Conclusion & Future Scope", "17"),
    ("6", "Bibliography", "19")
]

for row_idx, (c0_t, c1_t, c2_t) in enumerate(toc_data):
    c0 = tbl_toc.cell(row_idx, 0)
    c1 = tbl_toc.cell(row_idx, 1)
    c2 = tbl_toc.cell(row_idx, 2)
    
    c0.paragraphs[0].text = c0_t
    c1.paragraphs[0].text = c1_t
    c2.paragraphs[0].text = c2_t
    
    set_cell_margins(c0, top=80, bottom=80, left=120, right=120)
    set_cell_margins(c1, top=80, bottom=80, left=120, right=120)
    set_cell_margins(c2, top=80, bottom=80, left=120, right=120)
    
    b_k = {"top": {"val": "single", "sz": 4, "color": "000000"},
           "bottom": {"val": "single", "sz": 4, "color": "000000"},
           "left": {"val": "single", "sz": 4, "color": "000000"},
           "right": {"val": "single", "sz": 4, "color": "000000"}}
    set_cell_border(c0, **b_k)
    set_cell_border(c1, **b_k)
    set_cell_border(c2, **b_k)
    
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
# PAGE 9: PRELIMINARY LISTS
# ==========================================
doc.add_heading("List of Figures", level=2)
lf_items = [
    "Fig 1.1: Traditional Centralized vs. Decentralized Blockchain Verification Paradigm",
    "Fig 2.1: Ethereum Sepolia EVM Execution and Smart Contract Architecture",
    "Fig 3.1: High-Level System Architecture of CertChain Platform",
    "Fig 3.2: End-to-End Cryptographic Document Lifecycle and Verification Flow",
    "Fig 3.3: SHA-256 Mathematical Document Fingerprinting Pipeline"
]
for item in lf_items:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading("List of Tables", level=2)
lt_items = [
    "Table 2.1: Comparison of Core Technologies and Libraries in CertChain",
    "Table 3.1: Smart Contract Key Functions in CertChain.sol",
    "Table 1: Correlation between the Internship Project and Program Outcomes (POs/PSOs)",
    "Table 2: Project Correlation with Appropriate Level (H/M/L)",
    "Table 3: Nature of Internship Work",
    "Table 4: Nature of Internship Project Domain Classification"
]
for item in lt_items:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading("List of Screenshots", level=2)
ls_items = [
    "Screenshot 1: CertChain Public Landing Page with Hero Showcase",
    "Screenshot 2: Public Zero-Trust Verification Portal with Sample Test Chips",
    "Screenshot 3: Fast-Track In-Browser Camera QR Code Scanner Modal",
    "Screenshot 4: Cryptographically Verified On-Chain Result Card for Katuri Keerthi",
    "Screenshot 5: Institutional Administration Telemetry Dashboard",
    "Screenshot 6: Certificate Issuance Portal with Real-Time Vector Preview",
    "Screenshot 7: Institutional Certificate Registry and Revocation Management Table",
    "Screenshot 8: Live Production Deployment on Netlify Edge CDN"
]
for item in ls_items:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading("List of Symbols & Abbreviations", level=2)
la_items = [
    "API — Application Programming Interface",
    "CLI — Command Line Interface",
    "dApp — Decentralized Application",
    "DLT — Distributed Ledger Technology",
    "ECDSA — Elliptic Curve Digital Signature Algorithm",
    "EVM — Ethereum Virtual Machine",
    "JWT — JSON Web Token",
    "PO — Program Outcome",
    "PSO — Program Specific Outcome",
    "QR — Quick Response Code",
    "RPC — Remote Procedure Call",
    "SHA-256 — Secure Hash Algorithm 256-bit",
    "SPA — Single Page Application",
    "UGC — University Grants Commission"
]
for item in la_items:
    doc.add_paragraph(item, style='List Bullet')

doc.add_page_break()

# ==========================================
# PAGE 10: ABSTRACT
# ==========================================
p_abs_h = doc.add_paragraph()
p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_abs_h.paragraph_format.space_after = Pt(16)
r_abs_h = p_abs_h.add_run("ABSTRACT")
r_abs_h.font.size = Pt(16)
r_abs_h.font.bold = True

p_abs1 = doc.add_paragraph()
p_abs1.paragraph_format.line_spacing = 1.3
p_abs1.paragraph_format.space_after = Pt(12)
p_abs1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_abs1.add_run("Credential fraud, counterfeit academic certificates, and unverified resume inflation present severe security and trust challenges across academic institutions, government bodies, and international employers. Traditional certificate validation processes rely on slow, manual email exchanges, physical registrar visits, or centralized databases vulnerable to single-point failures, internal corruption, and server outages. During the internship program on ")
p_abs1.add_run("Blockchain").font.bold = True
p_abs1.add_run(" organized by ")
p_abs1.add_run("Centurion University of Technology and Management (School of Future Nexus)").font.bold = True
p_abs1.add_run(", practical knowledge was acquired in Ethereum smart contract engineering, cryptographic hashing, decentralized application development, and modern cloud deployment.")

p_abs2 = doc.add_paragraph()
p_abs2.paragraph_format.line_spacing = 1.3
p_abs2.paragraph_format.space_after = Pt(12)
p_abs2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_abs2.add_run("Applying these core competencies, ")
p_abs2.add_run("CertChain").font.bold = True
p_abs2.add_run(" was developed as a state-of-the-art decentralized credential issuance and verification ecosystem. The platform anchors mathematical proofs of certificate authenticity directly onto the public ")
p_abs2.add_run("Ethereum Sepolia blockchain").font.bold = True
p_abs2.add_run(" (Contract Address: 0xba0553a92F82F62E62d38496398637f9CB11B37C). Instead of storing sensitive student personally identifiable information (PII) on-chain, CertChain computes a unique 256-bit cryptographic digest (SHA-256) of the deterministic vector PDF certificate, ensuring complete GDPR privacy compliance while guaranteeing mathematical tamper-resistance.")

p_abs3 = doc.add_paragraph()
p_abs3.paragraph_format.line_spacing = 1.3
p_abs3.paragraph_format.space_after = Pt(12)
p_abs3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_abs3.add_run("The platform features a dual-issuance architecture: institutional administrators can issue credentials either through a sponsored gasless institutional relayer or via direct Web3 wallet signatures (MetaMask). Verifiers, recruiters, and embassies can authenticate credentials globally in under two seconds through three distinct channels: manual Certificate ID lookup, client-side PDF drag-and-drop byte comparison, and real-time in-browser camera or screenshot QR code scanning.")

p_abs4 = doc.add_paragraph()
p_abs4.paragraph_format.line_spacing = 1.3
p_abs4.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_abs4.add_run("CertChain was deployed globally on Netlify's Edge CDN network with automated CI/CD synchronization from GitHub. The project demonstrates how blockchain technology, asymmetric cryptography, and modern web frameworks can eliminate credential fraud, establish absolute institutional trust, and provide decentralized mathematical validation at zero operational cost.")

doc.add_page_break()

# ==========================================
# CHAPTER 1: INTRODUCTION
# ==========================================
p_c1_h = doc.add_paragraph()
p_c1_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c1_h.paragraph_format.space_after = Pt(16)
r_c1_h = p_c1_h.add_run("CHAPTER 1\nINTRODUCTION")
r_c1_h.font.size = Pt(16)
r_c1_h.font.bold = True

p_i1 = doc.add_paragraph()
p_i1.paragraph_format.line_spacing = 1.3
p_i1.paragraph_format.space_after = Pt(12)
p_i1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_i1.add_run("1.1 Background\n").font.bold = True
p_i1.add_run("In the modern knowledge economy, academic degrees, professional certifications, and technical diplomas serve as the primary currency for employment, university admissions, and international licensing. However, the prevalence of counterfeit documents and 'diploma mills' has escalated dramatically. Recent industry studies estimate that over 40% of resumes contain exaggerated or forged academic claims, and fraudulent certificates represent a multi-billion dollar illicit market worldwide.")

p_i2 = doc.add_paragraph()
p_i2.paragraph_format.line_spacing = 1.3
p_i2.paragraph_format.space_after = Pt(12)
p_i2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_i2.add_run("Traditional certificate verification mechanisms suffer from fundamental limitations:\n")
p_i2.add_run("• High Latency: Verifying a credential often requires direct correspondence with university registrar offices, taking several days to weeks.\n")
p_i2.add_run("• Intermediary Costs: Background check organizations charge high verification fees per document.\n")
p_i2.add_run("• Centralized Vulnerabilities: University databases are susceptible to cyberattacks, internal administrative corruption, record loss, and institutional closure.\n")
p_i2.add_run("• Easy Document Manipulation: Digital image editing software allows bad actors to alter student names, grades, and graduation dates on PDF documents without visible trace.")

p_i3 = doc.add_paragraph()
p_i3.paragraph_format.line_spacing = 1.3
p_i3.paragraph_format.space_after = Pt(12)
p_i3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_i3.add_run("1.2 The Blockchain Solution\n").font.bold = True
p_i3.add_run("Blockchain technology provides a decentralized, append-only, immutable ledger governed by cryptographic consensus. By committing cryptographic certificate fingerprints (hashes) into an Ethereum smart contract, academic institutions can establish an unalterable proof-of-issuance. Because blockchain records cannot be modified or deleted once mined into a block, fraudulent alteration is mathematically impossible.")

p_i4 = doc.add_paragraph()
p_i4.paragraph_format.line_spacing = 1.3
p_i4.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_i4.add_run("1.3 Objectives of CertChain\n").font.bold = True
p_i4.add_run("1. Develop an immutable smart contract on Ethereum Sepolia for recording certificate hashes.\n")
p_i4.add_run("2. Implement client-side deterministic PDF rendering and SHA-256 hashing to preserve student privacy.\n")
p_i4.add_run("3. Build a dual-mode issuance portal supporting both gasless institutional relayers and MetaMask signatures.\n")
p_i4.add_run("4. Engineer an in-browser camera and screenshot QR scanner for fast-track verification.\n")
p_i4.add_run("5. Deploy the application publicly with automated CI/CD pipelines to Netlify Edge CDN.")

doc.add_page_break()

# ==========================================
# CHAPTER 2: TECHNOLOGIES USED
# ==========================================
p_c2_h = doc.add_paragraph()
p_c2_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c2_h.paragraph_format.space_after = Pt(16)
r_c2_h = p_c2_h.add_run("CHAPTER 2\nRELATED WORK & TECHNOLOGIES USED")
r_c2_h.font.size = Pt(16)
r_c2_h.font.bold = True

tech_sections = [
    ("2.1 Ethereum Sepolia Testnet & Smart Contract Architecture",
     "The foundational settlement layer of CertChain is the Ethereum Sepolia Testnet (Chain ID: 11155111). Ethereum is a Turing-complete decentralized computing platform executing smart contracts inside the Ethereum Virtual Machine (EVM). The custom CertChain.sol contract was authored in Solidity 0.8.24, leveraging OpenZeppelin Ownable access control. The contract maintains two persistent mappings: registered certificates by ID and authorized institutional issuer addresses. It was deployed at address 0xba0553a92F82F62E62d38496398637f9CB11B37C."),
    
    ("2.2 Foundry Smart Contract Tooling",
     "Smart contract compilation, testing, and deployment scripts were engineered using Foundry, a blazing-fast, Rust-based EVM development framework. Foundry's 'forge' compiler provides native Solidity unit testing and gas usage profiling, while 'cast' facilitates RPC interactions and deployment scripts."),
    
    ("2.3 Cryptographic Document Hashing (SHA-256)",
     "To respect international privacy frameworks such as GDPR and avoid storing sensitive personally identifiable information (PII) on a public distributed ledger, CertChain employs SHA-256 hashing. The exact binary byte stream of the generated certificate is passed to the browser's native crypto.subtle.digest API, producing an unforgeable 32-byte digest (e.g., 0x5e96...fee9). Even a 1-bit alteration in the certificate alters the entire resulting hash."),
    
    ("2.4 Backend Services & node:sqlite",
     "The backend API server is built on Node.js v24 and Express.js. Rather than relying on external C++ native compilation modules, the database layer uses Node's native 'node:sqlite' (DatabaseSync) module. The backend provides institutional relayer transaction signing, JWT authentication for registrars, and certificate metadata queries."),
    
    ("2.5 Frontend SPA (React 18 & Vite)",
     "The user interface is developed as a high-performance Single Page Application using React 18 and Vite. The design incorporates a dark glassmorphic design system using pure Vanilla CSS, HSL neon glows, fluid typography, particle stars animation, and responsive viewports."),
    
    ("2.6 Document & Barcode Processing (jsPDF & html5-qrcode)",
     "PDF certificates are rendered deterministically using jsPDF. Real-time QR code barcode detection is powered by html5-qrcode, allowing verifiers to scan QR codes using webcams, phone cameras, or uploaded screenshot images."),
    
    ("2.7 Netlify Edge CDN Deployment",
     "The application is deployed publicly on Netlify's global edge network (wondrous-smakager-fab5a3.netlify.app), utilizing automated git pushes and '_redirects' SPA rewrites.")
]

for title, desc in tech_sections:
    p_t = doc.add_paragraph()
    p_t.paragraph_format.line_spacing = 1.3
    p_t.paragraph_format.space_after = Pt(10)
    p_t.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_t.add_run(f"{title}\n").font.bold = True
    p_t.add_run(desc)

doc.add_page_break()

# ==========================================
# CHAPTER 3: WORK DONE & SYSTEM ARCHITECTURE
# ==========================================
p_c3_h = doc.add_paragraph()
p_c3_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c3_h.paragraph_format.space_after = Pt(16)
r_c3_h = p_c3_h.add_run("CHAPTER 3\nWORK DONE & SYSTEM ARCHITECTURE")
r_c3_h.font.size = Pt(16)
r_c3_h.font.bold = True

p_w1 = doc.add_paragraph()
p_w1.paragraph_format.line_spacing = 1.3
p_w1.paragraph_format.space_after = Pt(10)
p_w1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_w1.add_run("3.1 System Architecture of CertChain\n").font.bold = True
p_w1.add_run("CertChain follows a modern, modular Web3 architecture comprising four primary tiers:\n")
p_w1.add_run("1. Smart Contract Tier: Deployed on Ethereum Sepolia, managing the immutable certificate registry, authorization mappings, and on-chain revocation records.\n")
p_w1.add_run("2. Institutional Relayer Tier: A Node.js backend with ECDSA key management that sponsors gas fees for university administrators, enabling one-click gasless certificate issuance.\n")
p_w1.add_run("3. Client-Side Cryptographic Engine: In-browser vector PDF compilation, SHA-256 byte-level hashing, and optical QR code decoding.\n")
p_w1.add_run("4. Public Verification Engine: A decentralized client interface querying Ethereum Sepolia RPC directly to authenticate credentials without intermediaries.")

# Embed Screenshots into Chapter 3
screenshots_to_embed = [
    ("presentation_assets/01_Landing_Hero.png", "Fig 3.1: CertChain Public Landing Page with Hero Showcase & Sepolia Status"),
    ("presentation_assets/02_Public_Verify_Interface.png", "Fig 3.2: Public Zero-Trust Verification Portal with Sample Test Chips"),
    ("presentation_assets/03_QR_Camera_Scanner.png", "Fig 3.3: Real-Time In-Browser Camera QR Code Scanner Viewfinder"),
    ("presentation_assets/05_Verified_Certificate_Result.png", "Fig 3.4: Cryptographically Verified On-Chain Output for Katuri Keerthi"),
    ("presentation_assets/07_Admin_Dashboard_Telemetry.png", "Fig 3.5: Institutional Administration Telemetry Dashboard"),
    ("presentation_assets/08_Issue_Credential_Live_Preview.png", "Fig 3.6: Credential Issuance Engine with Dynamic Real-Time Vector Preview"),
    ("presentation_assets/09_Certificates_Registry_Table.png", "Fig 3.7: Institutional Certificate Registry and Revocation Management Table"),
    ("presentation_assets/11_Netlify_Public_Deployment.png", "Fig 3.8: Live Production Deployment on Netlify Edge CDN")
]

for img_path, caption in screenshots_to_embed:
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(img_path, width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(14)
        r_cap = p_cap.add_run(caption)
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.bold = True

doc.add_page_break()

# ==========================================
# CHAPTER 4: LEARNING AFTER INTERNSHIP
# ==========================================
p_c4_h = doc.add_paragraph()
p_c4_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c4_h.paragraph_format.space_after = Pt(16)
r_c4_h = p_c4_h.add_run("CHAPTER 4\nLEARNING AFTER INTERNSHIP")
r_c4_h.font.size = Pt(16)
r_c4_h.font.bold = True

learnings = [
    ("4.1 Blockchain & Smart Contract Engineering",
     "The internship provided comprehensive practical exposure to EVM architecture, Solidity memory/storage models, access control patterns, and gas optimization. I gained hands-on experience writing and deploying production contracts to the Ethereum Sepolia network and auditing transactions on Etherscan."),
    
    ("4.2 Asymmetric Cryptography & Data Integrity",
     "I gained practical mastery over cryptographic hashing algorithms (SHA-256), Elliptic Curve Digital Signature Algorithm (ECDSA), public-private key derivation, and client-side binary digest generation. Understanding how cryptographic hashing guarantees tamper-evidence was a pivotal learning milestone."),
    
    ("4.3 Web3 Full-Stack Integration",
     "Integrating Ethers.js v6 with React 18 taught me how decentralized applications communicate with remote blockchain nodes via JSON-RPC. I learned to handle wallet connection events, network switching between Ethereum mainnet and testnets, and contract transaction lifecycles."),
    
    ("4.4 Computer Vision & Optical Barcode Scanning",
     "Implementing the in-browser QR code scanner using html5-qrcode improved my skills in handling web media devices, browser camera permissions, video canvas streaming, and real-time image decoding."),
    
    ("4.5 Cloud DevOps & CI/CD Pipelines",
     "Deploying the project to Netlify Edge CDN and Cloudflare provided invaluable industry experience in production deployment, environment variable management, single-page application rewrite routing (_redirects), and automated Git synchronization.")
]

for l_title, l_desc in learnings:
    p_l = doc.add_paragraph()
    p_l.paragraph_format.line_spacing = 1.3
    p_l.paragraph_format.space_after = Pt(10)
    p_l.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_l.add_run(f"{l_title}\n").font.bold = True
    p_l.add_run(l_desc)

doc.add_page_break()

# ==========================================
# CHAPTER 5: SUMMARY & CONCLUSION
# ==========================================
p_c5_h = doc.add_paragraph()
p_c5_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c5_h.paragraph_format.space_after = Pt(16)
r_c5_h = p_c5_h.add_run("CHAPTER 5\nSUMMARY, CONCLUSION & FUTURE SCOPE")
r_c5_h.font.size = Pt(16)
r_c5_h.font.bold = True

p_sum = doc.add_paragraph()
p_sum.paragraph_format.line_spacing = 1.3
p_sum.paragraph_format.space_after = Pt(12)
p_sum.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_sum.add_run("5.1 Summary\n").font.bold = True
p_sum.add_run("CertChain was successfully designed, developed, deployed, and tested as a decentralized academic credential verification system on Ethereum Sepolia. By anchoring immutable SHA-256 document digests on-chain, the platform eliminates diploma forgery, reduces verification latency from weeks to milliseconds, and removes costly third-party verification middlemen while preserving 100% student privacy.")

p_con = doc.add_paragraph()
p_con.paragraph_format.line_spacing = 1.3
p_con.paragraph_format.space_after = Pt(12)
p_con.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_con.add_run("5.2 Conclusion\n").font.bold = True
p_con.add_run("The internship at Centurion University of Technology and Management provided an invaluable transition from academic theoretical computer science to hands-on Web3 engineering. CertChain demonstrates the practical, transformative impact of blockchain technology in higher education administration.")

p_fut = doc.add_paragraph()
p_fut.paragraph_format.line_spacing = 1.3
p_fut.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_fut.add_run("5.3 Future Scope\n").font.bold = True
p_fut.add_run("1. Soulbound Tokens (ERC-5192): Upgrading certificate anchors to non-transferable NFTs tied to a student's decentralized identity wallet.\n")
p_fut.add_run("2. Zero-Knowledge Proofs (zk-SNARKs): Enabling selective attribute disclosure (e.g., proving graduation or GPA > 3.5 without revealing the full transcript).\n")
p_fut.add_run("3. Layer-2 Scaling: Deploying on Ethereum Layer-2 networks (Arbitrum / Optimism / Polygon) for sub-cent transaction fees at institutional scale.\n")
p_fut.add_run("4. Multi-University Consortium: Establishing federated decentralized identity verification across international university alliances.")

doc.add_page_break()

# ==========================================
# CHAPTER 6: BIBLIOGRAPHY
# ==========================================
p_b_h = doc.add_paragraph()
p_b_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_b_h.paragraph_format.space_after = Pt(16)
r_b_h = p_b_h.add_run("CHAPTER 6\nBIBLIOGRAPHY")
r_b_h.font.size = Pt(16)
r_b_h.font.bold = True

bib_items = [
    "Nakamoto, S. (2008). Bitcoin: A Peer-to-Peer Electronic Cash System. Cryptography Mailing List.",
    "Wood, G. (2014). Ethereum: A Secure Decentralised Generalised Transaction Ledger. Ethereum Project Yellow Paper.",
    "Solidity Documentation. Ethereum Foundation (2024). https://docs.soliditylang.org/",
    "OpenZeppelin Contracts. Secure Smart Contract Development in Solidity (2024). https://docs.openzeppelin.com/contracts/",
    "Foundry Book. Fast, Portable and Modular EVM Toolkit (2024). https://book.getfoundry.sh/",
    "Ethers.js v6 Documentation. Complete Ethereum Library and Wallet Implementation (2024). https://docs.ethers.org/v6/",
    "National Institute of Standards and Technology (NIST). (2015). FIPS PUB 180-4: Secure Hash Standard (SHS).",
    "Netlify Edge Platform Documentation. Modern Hosting for Static Sites and Serverless APIs (2024). https://docs.netlify.com/",
    "CertChain Project Technical Documentation & Source Code Repository. https://github.com/Keerthi1316/certchain"
]

for idx, b_item in enumerate(bib_items, 1):
    p_b = doc.add_paragraph()
    p_b.paragraph_format.line_spacing = 1.25
    p_b.paragraph_format.space_after = Pt(6)
    p_b.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_b.add_run(f"[{idx}] {b_item}")

doc.add_page_break()

# ==========================================
# PROGRAM OUTCOMES (POs & PSOs) TABLES
# ==========================================
p_po_h = doc.add_paragraph()
p_po_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_po_h.paragraph_format.space_after = Pt(14)
r_po_h = p_po_h.add_run("PROGRAM OUTCOMES (POs) & PSOs MAPPING")
r_po_h.font.size = Pt(15)
r_po_h.font.bold = True

# Table 1: Correlation between Project and POs/PSOs
p_t1 = doc.add_paragraph()
p_t1.add_run("Table 1: Correlation between the Internship Project and Program Outcomes (POs), Program Specific Outcomes (PSOs).").font.bold = True

tbl_1 = doc.add_table(rows=2, cols=3)
tbl_1.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_1.columns[0].width = Inches(1.8)
tbl_1.columns[1].width = Inches(2.2)
tbl_1.columns[2].width = Inches(2.7)

tbl_1.cell(0, 0).paragraphs[0].text = "Roll No"
tbl_1.cell(0, 1).paragraphs[0].text = "Name"
tbl_1.cell(0, 2).paragraphs[0].text = "Title"

tbl_1.cell(1, 0).paragraphs[0].text = "24R11A66N9"
tbl_1.cell(1, 1).paragraphs[0].text = "Katuri Keerthi"
tbl_1.cell(1, 2).paragraphs[0].text = "Blockchain — CertChain"

for r in range(2):
    for c in range(3):
        cell = tbl_1.cell(r, c)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        set_cell_border(cell, top={"sz":4,"val":"single","color":"000000"}, bottom={"sz":4,"val":"single","color":"000000"}, left={"sz":4,"val":"single","color":"000000"}, right={"sz":4,"val":"single","color":"000000"})
        if r == 0:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))
        else:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

# Table 2: Project correlation
doc.add_paragraph()
p_t2 = doc.add_paragraph()
p_t2.add_run("Table 2: Project correlation with appropriate POs/PSOs (Specify level of correlation H, M, L against POs/PSOs).").font.bold = True
p_t2_leg = doc.add_paragraph("Legend:  H - High (3)    M - Medium (2)    L - Low (1)")
p_t2_leg.runs[0].font.italic = True

tbl_2 = doc.add_table(rows=2, cols=14)
tbl_2.alignment = WD_TABLE_ALIGNMENT.CENTER

po_headers = ["PO1", "PO2", "PO3", "PO4", "PO5", "PO6", "PO7", "PO8", "PO9", "PO10", "PO11", "PSO1", "PSO2", "PSO3"]
po_ratings = ["H", "H", "H", "M", "H", "M", "H", "H", "M", "M", "H", "H", "H", "H"]

for c in range(14):
    c0 = tbl_2.cell(0, c)
    c1 = tbl_2.cell(1, c)
    c0.paragraphs[0].text = po_headers[c]
    c1.paragraphs[0].text = po_ratings[c]
    
    set_cell_margins(c0, top=60, bottom=60, left=40, right=40)
    set_cell_margins(c1, top=60, bottom=60, left=40, right=40)
    
    set_cell_border(c0, top={"sz":4,"val":"single","color":"000000"}, bottom={"sz":4,"val":"single","color":"000000"}, left={"sz":4,"val":"single","color":"000000"}, right={"sz":4,"val":"single","color":"000000"})
    set_cell_border(c1, top={"sz":4,"val":"single","color":"000000"}, bottom={"sz":4,"val":"single","color":"000000"}, left={"sz":4,"val":"single","color":"000000"}, right={"sz":4,"val":"single","color":"000000"})
    
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(9.5)
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))
    
    c1.paragraphs[0].runs[0].font.bold = True
    c1.paragraphs[0].runs[0].font.size = Pt(10)
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

# Table 3: Nature of Project
doc.add_paragraph()
p_t3 = doc.add_paragraph()
p_t3.add_run("Table 3: Nature of Internship work (Please tick ✓ appropriate for your Project)").font.bold = True

tbl_3 = doc.add_table(rows=2, cols=6)
tbl_3.alignment = WD_TABLE_ALIGNMENT.CENTER
t3_headers = ["Roll Number", "Title", "Product", "Application", "Research", "Others"]
t3_vals = ["24R11A66N9", "CertChain", "✓", "✓", "", ""]

for c in range(6):
    c0 = tbl_3.cell(0, c)
    c1 = tbl_3.cell(1, c)
    c0.paragraphs[0].text = t3_headers[c]
    c1.paragraphs[0].text = t3_vals[c]
    
    set_cell_margins(c0, top=60, bottom=60, left=60, right=60)
    set_cell_margins(c1, top=60, bottom=60, left=60, right=60)
    
    set_cell_border(c0, top={"sz":4,"val":"single","color":"000000"}, bottom={"sz":4,"val":"single","color":"000000"}, left={"sz":4,"val":"single","color":"000000"}, right={"sz":4,"val":"single","color":"000000"})
    set_cell_border(c1, top={"sz":4,"val":"single","color":"000000"}, bottom={"sz":4,"val":"single","color":"000000"}, left={"sz":4,"val":"single","color":"000000"}, right={"sz":4,"val":"single","color":"000000"})
    
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(10)
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))
    
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

# Table 4: Project Domain
doc.add_paragraph()
p_t4 = doc.add_paragraph()
p_t4.add_run("Table 4: Nature of Internship Project work (Domain Classification)").font.bold = True

tbl_4 = doc.add_table(rows=2, cols=6)
tbl_4.alignment = WD_TABLE_ALIGNMENT.CENTER
t4_headers = ["Roll Number", "AI", "ML/DL", "Web Applications", "Network Security / Blockchain", "IoT"]
t4_vals = ["24R11A66N9", "", "", "✓", "✓ (Blockchain Security)", ""]

for c in range(6):
    c0 = tbl_4.cell(0, c)
    c1 = tbl_4.cell(1, c)
    c0.paragraphs[0].text = t4_headers[c]
    c1.paragraphs[0].text = t4_vals[c]
    
    set_cell_margins(c0, top=60, bottom=60, left=50, right=50)
    set_cell_margins(c1, top=60, bottom=60, left=50, right=50)
    
    set_cell_border(c0, top={"sz":4,"val":"single","color":"000000"}, bottom={"sz":4,"val":"single","color":"000000"}, left={"sz":4,"val":"single","color":"000000"}, right={"sz":4,"val":"single","color":"000000"})
    set_cell_border(c1, top={"sz":4,"val":"single","color":"000000"}, bottom={"sz":4,"val":"single","color":"000000"}, left={"sz":4,"val":"single","color":"000000"}, right={"sz":4,"val":"single","color":"000000"})
    
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(9.5)
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E0E0E0"/>'))
    
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

# Save Document
output_doc = "Katuri_Keerthi_24R11A66N9_Internship_Report.docx"
doc.save(output_doc)
print(f"SUCCESS: Report saved as {output_doc} (Size: {os.path.getsize(output_doc)} bytes)")
