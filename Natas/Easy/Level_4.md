# Natas Challenge - Level 4

Prepared by: Nishanth Antony  
Date: September 23, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 4, a beginner-level web security challenge designed to demonstrate access control bypass through HTTP header manipulation. The objective was to obtain the password for Level 5 by altering the Referer header. The assessment identified a critical vulnerability where access was restricted based on the Referer header without proper server-side validation, allowing easy bypass via request modification. This finding highlights the unreliability of client-controlled headers for security enforcement and the risks of improper access controls. No advanced exploitation was required, and the vulnerability was rated as **High Severity** due to the direct exposure of authentication credentials.

Key Findings:
- Access control reliant on the HTTP Referer header, which is user-controllable.
- Hint on the page reveals the required Referer value for bypass.
- No additional authentication or tools beyond browser developer tools needed.

Recommendations:
- Implement robust server-side validation for all headers and access controls.
- Avoid relying on Referer or other client-side headers for security decisions.
- Use secure tokens or session-based checks for origin verification.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 5 by identifying and exploiting weak access controls through manipulation of the HTTP Referer header.

### Scope
- Target: Natas Level 4 web page (assumed URL: http://natas4.natas.labs.overthewire.org, accessible with credentials from Level 3).
- Assessment Type: White-box (header inspection and modification allowed).
- Exclusions: No network scanning, brute-forcing, or server-side exploitation was performed, as the challenge focuses on client-side request manipulation.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included browser developer tools for request interception and modification. The process was non-destructive and focused on reconnaissance, header analysis, and bypass techniques.

### Step 1: Initial Reconnaissance
- Accessed the target web page using a standard web browser.
- Observed an "Access disallowed" message with a hint: "You are visiting from 'http://natas4.natas.labs.overthewire.org/index.php' while authorized users should come only from 'http://natas5.natas.labs.overthewire.org/'".

### Step 2: HTTP Request Analysis
- Opened the browser developer tools (e.g., Chrome DevTools) and navigated to the Network tab.
- Enabled request interception or used the "Preserve log" option to monitor outgoing requests.
- Identified that the page load or refresh sends a GET request without a specific Referer, triggering the denial.

### Step 3: Header Manipulation and Vulnerability Identification
- Used the developer tools to edit and resend the request, or configured a proxy like Burp Suite for header modification.
- Set the HTTP Referer header to the hinted value: http://natas5.natas.labs.overthewire.org/.
- Forwarded the modified request, which granted access and displayed the password for Level 5.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- Developer Tools: Network tab for request inspection and modification.
- Optional: Proxy tools like Burp Suite for advanced header editing (not required here).

## Findings
### Vulnerability Details
- **Vulnerability Type**: Improper Access Control (CWE-284: Improper Access Control) via Unvalidated HTTP Header (CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers).
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The application enforces access based solely on the HTTP Referer header, which is fully controllable by the client. The page provides a direct hint on the required Referer value, making bypass trivial through request tampering.
- **Proof of Concept**:
  1. Navigate to the Natas Level 4 page and note the "Access disallowed" message with the Referer hint.
  2. Open developer tools, refresh the page, and intercept the request.
  3. Modify the Referer header to "http://natas5.natas.labs.overthewire.org/".
  4. Resend the request to receive the "Access granted" response containing the password: "The password for natas5 is [REDACTED]".
- **Impact**: An attacker can bypass access controls to obtain sensitive credentials, enabling unauthorized progression. In real-world scenarios, this could allow access to restricted areas, data leakage, or session hijacking.

### Affected Components
- Server-side logic validating the Referer header.
- No client-side vulnerabilities were tested in this level.

### Screenshots of Exploitation
The following screenshots capture the before-and-after states of the exploitation:

[Image Description 1: The initial "Access disallowed" page displayed when accessing without the correct Referer. The message reads: "Access disallowed. You are visiting from 'http://natas4.natas.labs.overthewire.org/index.php' while authorized users should come only from 'http://natas5.natas.labs.overthewire.org/'". A "Refresh page" link is present.]

[Image Description 2: The "Access granted" page after modifying the Referer header. The message reads: "Access granted. The password for natas5 is On35Pkg gAPm2ZbEpOU802c0x0Msn1ToK". A "Refresh page" link is present. (Password redacted in report).]

## Solution and Exploitation
The password for Natas Level 5 was successfully obtained by setting the correct Referer header in the request. In a real pentest, this would be reported as a finding rather than exploited further without authorization.

- **Extracted Artifact**: Password for Level 5 (redacted for this report).
- **Remediation Steps**:
  1. Remove reliance on the Referer header for access control.
  2. Implement server-side validation using secure mechanisms like CSRF tokens or origin checks.
  3. Validate all user-controlled inputs, including headers, against expected values.
  4. Log and monitor suspicious header values for anomaly detection.

## Learnings and Recommendations
### Key Learnings
- **HTTP Header Vulnerabilities**: Improper validation of headers like Referer can allow unauthorized access, as they are easily forged by attackers.
- **Server-Side Validation**: Always validate HTTP headers server-side to ensure they originate from trusted sources, and never trust client-provided data for security decisions.
- **Broader Implications**: This vulnerability emphasizes the need for multi-layered security, including proper access controls, header sanitization, and tools like proxies for testing.

### Recommendations
- **Short-Term**: Patch the application to ignore or properly validate the Referer; add authentication layers.
- **Long-Term**: 
  - Adopt OWASP best practices for access control and header security.
  - Integrate automated tools (e.g., Burp Suite Scanner) in testing pipelines to detect header-based flaws.
  - Train developers on the risks of client-controlled data and secure header handling.
- **Mitigation Controls**: Use Content-Security-Policy (CSP) headers, enable strict Referrer-Policy, and enforce HTTPS to reduce tampering risks.

## Conclusion
This walkthrough for Natas Level 4 demonstrates how weak reliance on manipulable HTTP headers can lead to access control bypass. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: validate everything server-side. For real-world applications, regular VAPT assessments are essential to mitigate such risks.
