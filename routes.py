from app import app
from flask import render_template, request, session, make_response
from scanner.modules import scan_sqli, scan_xss, check_headers
from fpdf import FPDF

# Secret key is needed to use sessions
app.secret_key = 'your_super_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target_url = request.form.get('url')
    if not target_url:
        return "Error: No URL provided.", 400

    urls_to_scan = [target_url]
    all_findings = []
    for url in urls_to_scan:
        all_findings.extend(scan_sqli(url))
        all_findings.extend(scan_xss(url))
        all_findings.extend(check_headers(url))

    # Store findings in the user's session
    session['findings'] = all_findings
    session['target'] = target_url

    return render_template('results.html', findings=all_findings, target=target_url)

@app.route('/report')
def report():
    findings = session.get('findings', [])
    target = session.get('target', 'N/A')

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'Security Scan Report for {target}', 0, 1, 'C')
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(60, 10, 'Type', 1)
    pdf.cell(100, 10, 'Details', 1)
    pdf.cell(30, 10, 'Severity', 1)
    pdf.ln()

    pdf.set_font('Arial', '', 10)
    for finding in findings:
        pdf.cell(60, 10, finding['type'], 1)
        details = finding.get('url') or finding.get('details', 'N/A')
        pdf.cell(100, 10, details[:60], 1)
        pdf.cell(30, 10, finding['severity'], 1)
        pdf.ln()

    response = make_response(pdf.output())

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response