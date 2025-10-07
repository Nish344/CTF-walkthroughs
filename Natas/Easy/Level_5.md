# 🏴󠁡󠁦󠁷󠁡󠁲󠁿Natas Challenge - Level 5

Prepared by: Nishanth Antony  
Date: October 08, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 5, a beginner-level web security challenge designed to demonstrate client-side cookie manipulation vulnerabilities. The objective was to retrieve the password for Level 6 by altering a cookie value. The assessment identified a critical vulnerability where the application relied on a client-controlled cookie ("logIn") to determine access, allowing unauthorized privilege escalation. This finding highlights the risks of trusting client-side data for authentication and the need for robust server-side validation. No advanced tools or exploitation were required, and the vulnerability was rated as **High Severity** due to the direct exposure of authentication credentials.

Key Findings:
- Cookie "logIn" with value 0 indicates logged-out state, manipulable via browser tools.
- Changing the value to 1 bypasses access controls, revealing the password.
- No server-side validation of cookie data.

Recommendations:
- Implement server-side session management with secure tokens.
- Use HttpOnly and Secure flags on cookies to limit client-side tampering.
- Conduct regular security reviews of authentication mechanisms.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 6 by identifying and exploiting a cookie manipulation vulnerability to bypass client-side access controls.

### Scope
- Target: Natas Level 5 web page (assumed URL: http://natas5.natas.labs.overthewire.org, accessible with credentials from Level 4).
- Assessment Type: White-box (source code and cookie inspection allowed).
- Exclusions: No network scanning, brute-forcing, or server-side exploitation was performed, as the challenge focuses on client-side manipulation.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included standard browser developer tools for cookie inspection and modification. The process was non-destructive and focused on reconnaissance, cookie analysis, and manipulation.

### Step 1: Initial Reconnaissance
- Accessed the target web page using a standard web browser.
- Reviewed the page content, which displayed a message indicating restricted access without login.

### Step 2: Cookie Inspection
- Opened browser developer tools (e.g., F12 or right-click > Inspect) and navigated to the "Application" or "Storage" tab.
- Identified a cookie named "logIn" with a value of "0", indicating a logged-out state.

### Step 3: Cookie Manipulation and Vulnerability Identification
- Modified the "logIn" cookie value to "1" using the developer tools (e.g., edit value directly or via console command: document.cookie = "logIn=1;").
- Refreshed the page to observe the change, which displayed the password for Level 6.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- Developer Tools: Built-in Application/Storage tab and JavaScript console.
- No additional scripts or external tools were required.

## Findings
### Vulnerability Details
- **Vulnerability Type**: Improper Access Control (CWE-284: Improper Access Control) via Client-Side Cookie Manipulation (CWE-602: Client-Side Enforcement of Server-Side Security).
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The application uses a client-side cookie ("logIn") to control access, with a value of "0" indicating logged-out and "1" indicating logged-in. Without server-side validation, an attacker can modify the cookie value to bypass restrictions and access sensitive data, such as the password for the next level.
- **Proof of Concept**:
  1. Navigate to the Natas Level 5 page and open developer tools.
  2. Locate the "logIn" cookie with value "0".
  3. Change the value to "1" and refresh the page.
  4. Observe the revealed password for natas6.
- **Impact**: An attacker can manipulate cookies to gain unauthorized access to restricted content, leading to credential theft and progression to higher levels. In real-world scenarios, this could enable session hijacking or privilege escalation.

### Affected Components
- Client-side cookie management.
- No server-side vulnerabilities were tested in this level.

## Solution and Exploitation
The password for Natas Level 6 was successfully retrieved by changing the "logIn" cookie value to "1" without any modifications to the application. In a real pentest, this would be reported as a finding rather than exploited further without authorization.

- **Extracted Artifact**: Password for Level 6 (redacted for this report).
- **Remediation Steps**:
  1. Remove reliance on client-side cookies for access control.
  2. Implement server-side session management with cryptographically secure tokens.
  3. Set HttpOnly and Secure flags on cookies to prevent JavaScript access and enforce HTTPS.
  4. Validate all session data server-side before granting access.

## Learnings and Recommendations
### Key Learnings
- **Cookie Security**: Client-side cookies can be manipulated, highlighting the need for server-side validation of session data to prevent unauthorized access.
- **Secure Session Management**: Relying on client-controlled values for authentication is insecure; secure, server-side session tokens should be used instead.
- **Broader Implications**: This vulnerability underscores the importance of defense-in-depth, including input validation, secure cookie attributes, and regular security testing.

### Recommendations
- **Short-Term**: Audit cookie usage and implement server-side session validation.
- **Long-Term**: 
  - Adopt OWASP best practices for session management and cookie security.
  - Integrate automated tools (e.g., Burp Suite or OWASP ZAP) to test for cookie vulnerabilities in CI/CD pipelines.
  - Train developers on secure authentication practices to prevent client-side control issues.
- **Mitigation Controls**: Use CSRF tokens, enforce HTTPS, and monitor for abnormal cookie modifications.

## Conclusion
This walkthrough for Natas Level 5 demonstrates how client-side cookie manipulation can bypass weak access controls, leading to information disclosure. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: never trust client-side data for security. For real-world applications, regular VAPT assessments are essential to mitigate such risks.
