from app import app
from flask import render_template, request
# Import your scanner functions
from scanner.modules import scan_sqli, scan_xss, check_headers
# Note: We will create the crawler function in a later step, so we comment it out for now.
# from scanner.crawler import discover_targets 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    # Get the URL from the form
    target_url = request.form.get('url')

    if not target_url:
        return "Error: No URL provided.", 400

    # For now, we will scan the single URL provided.
    # Later, we can use the crawler to find more URLs.
    urls_to_scan = [target_url]

    all_findings = []

    # Run each scanner on the target URL(s)
    for url in urls_to_scan:
        all_findings.extend(scan_sqli(url))
        all_findings.extend(scan_xss(url))
        all_findings.extend(check_headers(url))

    # Render a new page to display the results
    return render_template('results.html', findings=all_findings, target=target_url)