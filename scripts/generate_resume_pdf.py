#!/usr/bin/env python3
"""
Generate a clean, professional single-column PDF resume for Ashok Pokharel
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import urllib.request

# Colors - Minimal, professional
ACCENT_RED = HexColor('#dc2626')  # Red accent for section headers
TEXT_BLACK = HexColor('#1a1a1a')
TEXT_GRAY = HexColor('#4b5563')
TEXT_LIGHT = HexColor('#6b7280')
BORDER_GRAY = HexColor('#e5e7eb')
LINK_BLUE = HexColor('#2563eb')

def draw_horizontal_line(c, x, y, width, color=BORDER_GRAY, thickness=0.5):
    """Draw a horizontal line"""
    c.setStrokeColor(color)
    c.setLineWidth(thickness)
    c.line(x, y, x + width, y)

def draw_section_header(c, title, x, y, width):
    """Draw a section header with red left border"""
    # Red accent bar
    c.setFillColor(ACCENT_RED)
    c.rect(x, y - 2, 3, 14, fill=True, stroke=False)

    # Section title
    c.setFillColor(TEXT_BLACK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 10, y, title)

    return y - 20

def draw_bullet(c, text, x, y, max_width, font="Helvetica", size=9):
    """Draw a bullet point with text wrapping"""
    c.setFillColor(TEXT_BLACK)
    c.setFont(font, size)

    # Bullet
    c.drawString(x, y, "•")

    # Text with wrapping
    words = text.split()
    lines = []
    current_line = []
    text_x = x + 12

    for word in words:
        test_line = ' '.join(current_line + [word])
        if c.stringWidth(test_line, font, size) <= max_width - 12:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    for i, line in enumerate(lines):
        c.drawString(text_x, y - (i * 12), line)

    return len(lines) * 12

def draw_skill_category(c, category, skills, x, y, width):
    """Draw a skill category with underlined category name"""
    c.setFillColor(TEXT_BLACK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, category)

    # Underline effect for category
    cat_width = c.stringWidth(category, "Helvetica-Bold", 9)
    c.setStrokeColor(TEXT_LIGHT)
    c.setLineWidth(0.5)
    c.line(x, y - 2, x + cat_width, y - 2)

    # Skills text
    c.setFont("Helvetica", 9)
    c.setFillColor(TEXT_GRAY)
    skills_text = skills
    c.drawString(x + cat_width + 8, y, skills_text)

    return 14

def create_resume():
    """Create the PDF resume"""
    output_path = "/Users/ashok/projects/personal/portfolio/public/Ashok_Pokharel_Resume.pdf"

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    margin_left = 45
    margin_right = 45
    content_width = width - margin_left - margin_right

    y = height - 45

    # === HEADER ===
    # Top red line
    c.setStrokeColor(ACCENT_RED)
    c.setLineWidth(2)
    c.line(margin_left, y + 10, width - margin_right, y + 10)

    # Name
    c.setFillColor(TEXT_BLACK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(margin_left, y - 15, "Ashok Pokharel")

    # Title
    c.setFillColor(TEXT_GRAY)
    c.setFont("Helvetica", 11)
    c.drawString(margin_left, y - 32, "Fractional CTO | DevOps | SRE | AI Solutions Architect")

    # Contact info on right side
    c.setFont("Helvetica", 9)
    c.setFillColor(LINK_BLUE)
    c.drawRightString(width - margin_right, y - 15, "ashokpokharel977@gmail.com")

    c.setFillColor(TEXT_GRAY)
    c.drawRightString(width - margin_right, y - 28, "linkedin.com/in/AshokPokharel | github.com/ashokpokharel977")
    c.drawRightString(width - margin_right, y - 41, "Kathmandu, Nepal")

    y -= 55

    # Summary paragraph
    c.setFillColor(TEXT_GRAY)
    c.setFont("Helvetica", 9)
    summary = "Over 10 years of experience as a DevOps engineer in designing and developing cloud-native solutions with CI/CD and security tools. Aiming to improve software delivery posture, increase agility and effectiveness, manage and collaborate with internal and external teams to contribute and achieve company goals. Currently seeking an opportunity to build and grow with a team to innovate for a better tomorrow."

    words = summary.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if c.stringWidth(test_line, "Helvetica", 9) <= content_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    for line in lines:
        c.drawString(margin_left, y, line)
        y -= 12

    y -= 10
    draw_horizontal_line(c, margin_left, y, content_width)
    y -= 15

    # === EXPERIENCE ===
    y = draw_section_header(c, "EXPERIENCE", margin_left, y, content_width)

    experiences = [
        {
            "title": "Technical Lead",
            "company": "Adex International Pvt. Ltd.",
            "location": "Nepal",
            "period": "Aug 2020 - Present",
            "bullets": [
                "Manage teams, measure outcomes, provide feedback and improve processes",
                "Identify customer needs, collaborating with teams to design, build and deploy cloud solutions",
                "Build tools, frameworks & products to enhance workflows, maintain security, and control cost",
                "Design and deploy highly and dynamically available, fault-tolerant, and secure cloud-native deployment architecture on AWS",
                "Provide training and mentorship to team members and clients",
                "Build and automate cloud-native solutions in ECS, Kubernetes, Serverless, and Data Lake with Glue, Athena, Lambda, and On-Prem to cloud migrations",
            ]
        },
        {
            "title": "Senior Solution Architect",
            "company": "Certegy",
            "location": "Australia (Contract)",
            "period": "2022 - 2024",
            "bullets": [
                "Led migration of 80+ applications from on-prem data center to AWS with zero downtime",
                "Designed hybrid network architecture handling 10K+ daily transactions securely",
                "Modernized legacy C and Java applications, reducing maintenance overhead by 60%",
                "Delivered $2M+ infrastructure project on schedule across 3 delivery phases",
                "Coordinated 4 cross-functional teams spanning development, QA, and operations",
            ]
        },
        {
            "title": "DevOps Engineer",
            "company": "Home Loan Experts",
            "location": "Australia (Remote)",
            "period": "Jun 2019 - Oct 2022",
            "bullets": [
                "Create custom build and deployment tools for Serverless, AWS SAM, Terraform & AWS CloudFormation",
                "Designing & Implementing scalable multi-environment IAC with Terraform and Terragrunt",
                "Research and implement tools for both DevOps and business needs fulfillment",
                "Centralize monitoring and alerting solution with DataDog & Serverless environment",
                "Architect serverless applications with best practices, improve user experience by shifting towards event-driven workflows",
            ]
        },
        {
            "title": "R&D Security Engineer",
            "company": "Genese Solutions",
            "location": "Nepal",
            "period": "Jun 2018 - Apr 2019",
            "bullets": [
                "Pentest web applications, APIs against web exploits to prevent unavailability, and security compromise with proven pentest frameworks",
                "Accomplish PCI, SOC, and HIPAA compliance assessments, analyze the compliance level of the business entity, make and regulate necessary changes, and complete a formal attestation",
                "Implement security pipeline on AWS Cloud using AWS tools Guard Duty, CloudTrail, Inspector, WAF, Security Hub, SSO, KMS, Detective",
                "Implement SIEM solutions using AWS-managed services",
                "Kubernetes deployment in the cloud and on self-hosted solutions, managing security in Kubernetes",
            ]
        }
    ]

    for exp in experiences:
        # Title and period on same line
        c.setFillColor(TEXT_BLACK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin_left, y, f"{exp['title']},")

        title_width = c.stringWidth(f"{exp['title']},", "Helvetica-Bold", 10)
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(margin_left + title_width + 5, y, f"{exp['company']}, {exp['location']}")

        c.setFillColor(TEXT_GRAY)
        c.setFont("Helvetica", 9)
        c.drawRightString(width - margin_right, y, exp['period'])

        y -= 14

        # Bullets
        for bullet in exp['bullets']:
            if y < 60:  # Check for page break
                c.showPage()
                y = height - 45
            height_used = draw_bullet(c, bullet, margin_left + 5, y, content_width - 10)
            y -= height_used + 2

        y -= 8

    # === EDUCATION ===
    y -= 5
    y = draw_section_header(c, "EDUCATION", margin_left, y, content_width)

    c.setFillColor(TEXT_BLACK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin_left, y, "Bachelor in Electronics and Communication Engineering,")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(margin_left + c.stringWidth("Bachelor in Electronics and Communication Engineering,", "Helvetica-Bold", 10) + 5, y, "Nepal Institute Of Engineering")

    c.setFillColor(TEXT_GRAY)
    c.setFont("Helvetica", 9)
    c.drawRightString(width - margin_right, y, "Sep 2014 - Oct 2018")

    y -= 25

    # === SKILLS ===
    y = draw_section_header(c, "SKILLS", margin_left, y, content_width)

    skills = [
        ("Security tools and frameworks", "Metasploit, Burp Suite, Nmap, Wireshark, Scripting, MITRE ATT&CK framework"),
        ("Programming", "Python, JS, Ruby, PHP"),
        ("DevOps", "Jenkins, Terraform, Ansible, Docker, Kubernetes, ArgoCD, Vault"),
        ("Data", "PySpark, Hadoop, AWS Glue, AWS EMR, GCP Big Data, AWS Glue, Redshift"),
        ("Others", "Project Management (Trello, Jira, Miro), Agile Development"),
        ("SoftSkills", "Effective Communication, Team Work, Creativity, Leadership"),
    ]

    for category, skill_list in skills:
        c.setFillColor(TEXT_BLACK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin_left, y, category)

        cat_width = c.stringWidth(category, "Helvetica-Bold", 9)

        # Underline
        c.setStrokeColor(TEXT_GRAY)
        c.setLineWidth(0.3)
        c.line(margin_left, y - 1, margin_left + cat_width, y - 1)

        c.setFillColor(TEXT_GRAY)
        c.setFont("Helvetica", 9)
        c.drawString(margin_left + cat_width + 8, y, skill_list)

        y -= 14

    # === PAGE 2 ===
    c.showPage()
    y = height - 45

    # === PROJECTS ===
    y = draw_section_header(c, "PROJECTS", margin_left, y, content_width)

    projects = [
        {
            "title": "Solution Architect Consultant | Digital Wallet Platform",
            "bullets": [
                "Design & develop overall system architecture combining multiple cloud vendors",
                "Identify use cases and implement Highly and dynamically available, fault-tolerant and secure record",
                "Automate app distribution of the Flutter application to both iOS and PlayStore",
                "Manage and deploy multiple microservices in ECS clusters",
            ]
        },
        {
            "title": "DevOps Engineer | FinOps Platform",
            "bullets": [
                "Architect a solution to connect to multiple payment gateways managing multiple VPN connectivity",
                "Enforce multi-layer security in the cloud and on applications protecting with cloud-native tools and third-party solutions. Automate disaster recovery process, DB migrations, and rollbacks",
                "Centralized logging and monitoring with AWS native CloudWatch Metrics, logs, alarms and alerts",
            ]
        },
        {
            "title": "Security Consultant | Financial Health Security",
            "bullets": [
                "Conduct assessment on security pipeline for deployed application in addition to infrastructure",
                "Container security assessment and vulnerability remediation",
                "Provide insights on best security practices for implementing microservice and serverless architectures",
                "Python-based AWS security auditing tool to identify possible security threats, take measures, and security implementations",
            ]
        },
    ]

    for proj in projects:
        c.setFillColor(TEXT_BLACK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin_left, y, proj['title'])
        y -= 14

        for bullet in proj['bullets']:
            height_used = draw_bullet(c, bullet, margin_left + 5, y, content_width - 10)
            y -= height_used + 2

        y -= 8

    # === ACHIEVEMENTS ===
    y -= 5
    y = draw_section_header(c, "ACHIEVEMENTS", margin_left, y, content_width)

    achievements = [
        "Improved Home Loan inquiry workflow system with a 30% reduction in overall latency by changing system architecture leveraging event-driven system and improving database performance",
        "Preventing 20+ high-severity security vulnerabilities threats in clouds by implementing Cloud monitoring, IDS, and IPS systems",
        "Empowered 50+ students to pursue their careers in technology through seminars, workshops, and mentorship",
    ]

    for achievement in achievements:
        height_used = draw_bullet(c, achievement, margin_left + 5, y, content_width - 10)
        y -= height_used + 4

    # === TRAINING ===
    y -= 10
    y = draw_section_header(c, "TRAINING", margin_left, y, content_width)

    trainings = [
        "CyberSecurity training - HackTheBox",
        "Cranberry training on pen-testing for web security assessment",
        "Cybrary CompTIA security training",
        "Cloud Security Engineer for Mitigating Vulnerability in Google Cloud",
        "Design Scalable architecture for AI and ML products",
        "Hybrid Infrastructure with Google Anthos (Kubernetes Solution)",
        '"Ways to become a better leader" - Leadership training at HLE',
    ]

    for training in trainings:
        height_used = draw_bullet(c, training, margin_left + 5, y, content_width - 10)
        y -= height_used + 2

    # === CERTIFICATIONS ===
    y -= 15
    y = draw_section_header(c, "CERTIFICATIONS", margin_left, y, content_width)

    # Draw certification boxes with logos
    cert_y = y - 10
    cert_box_width = 100
    cert_box_height = 70
    cert_spacing = 20

    certs = [
        {"name": "AWS Certified\nDevOps Engineer\nProfessional", "color": HexColor('#FF9900')},
        {"name": "AWS Certified\nDeveloper\nAssociate", "color": HexColor('#FF9900')},
        {"name": "Google Cloud\nProfessional\nCloud Architect", "color": HexColor('#4285F4')},
    ]

    cert_x = margin_left
    for cert in certs:
        # Box border
        c.setStrokeColor(BORDER_GRAY)
        c.setLineWidth(1)
        c.roundRect(cert_x, cert_y - cert_box_height, cert_box_width, cert_box_height, 5, fill=False, stroke=True)

        # Colored top bar
        c.setFillColor(cert['color'])
        c.rect(cert_x, cert_y - 8, cert_box_width, 8, fill=True, stroke=False)

        # AWS/GCP logo placeholder (text representation)
        c.setFillColor(cert['color'])
        c.setFont("Helvetica-Bold", 10)
        if "AWS" in cert['name']:
            c.drawCentredString(cert_x + cert_box_width/2, cert_y - 30, "AWS")
            c.setFillColor(HexColor('#232F3E'))
            c.setFont("Helvetica", 7)
            c.drawCentredString(cert_x + cert_box_width/2, cert_y - 40, "certified")
        else:
            c.drawCentredString(cert_x + cert_box_width/2, cert_y - 30, "Google Cloud")

        # Cert name
        c.setFillColor(TEXT_BLACK)
        c.setFont("Helvetica", 7)
        lines = cert['name'].split('\n')
        line_y = cert_y - 50
        for line in lines:
            c.drawCentredString(cert_x + cert_box_width/2, line_y, line)
            line_y -= 9

        cert_x += cert_box_width + cert_spacing

    y = cert_y - cert_box_height - 25

    # === FOOTER ===
    c.setFillColor(TEXT_GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 35, "Nationality: Nepali")
    c.drawCentredString(width/2, 25, "Linguistic Ability: Nepali, English, Hindi | Address: Kathmandu, Nepal")
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 15, "*References can be provided on request*")

    # Bottom red line
    c.setStrokeColor(ACCENT_RED)
    c.setLineWidth(2)
    c.line(margin_left, 45, width - margin_right, 45)

    c.save()
    print(f"Resume PDF created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_resume()
