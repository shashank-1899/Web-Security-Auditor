import requests

def scan_sqli(url):
    """Scans for basic Error-Based SQL Injection vulnerabilities."""
    payloads = ["'", "\"", "' OR 1=1 --", "\" OR 1=1 --", "' OR 'a'='a"]
    error_messages = [
        "you have an error in your sql syntax",
        "warning: mysql",
        "unclosed quotation mark",
        "sql syntax"
    ]
    findings = []
    for payload in payloads:
        try:
            test_url = f"{url}?id={payload}"
            response = requests.get(test_url, timeout=5)
            for error in error_messages:
                if error in response.text.lower():
                    finding = {
                        "type": "SQL Injection",
                        "url": test_url,
                        "payload": payload,
                        "severity": "High"
                    }
                    findings.append(finding)
                    break 
        except requests.RequestException as e:
            print(f"SQLi Scan Error: {e}")
            pass
    return findings

def scan_xss(url):
    """Scans for basic Reflected XSS vulnerabilities."""
    payload = "<script>alert('xss-test')</script>"
    findings = []
    try:
        test_url = f"{url}?query={payload}"
        response = requests.get(test_url, timeout=5, allow_redirects=True)
        if payload in response.text:
            finding = {
                "type": "Cross-Site Scripting (XSS)",
                "url": test_url,
                "payload": payload,
                "severity": "Medium"
            }
            findings.append(finding)
    except requests.RequestException as e:
        print(f"XSS Scan Error: {e}")
        pass
    return findings

def check_headers(url):
    """Checks for missing security headers."""
    required_headers = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Content-Type-Options"
    ]
    findings = []
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        for header in required_headers:
            if header not in headers:
                finding = {
                    "type": "Missing Security Header",
                    "url": url,
                    "details": f"Header '{header}' is missing.",
                    "severity": "Low"
                }
                findings.append(finding)
    except requests.RequestException as e:
        print(f"Header Scan Error: {e}")
        pass
    return findings