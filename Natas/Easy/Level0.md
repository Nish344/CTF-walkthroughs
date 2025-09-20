# 🏴󠁡󠁦󠁷󠁡󠁲󠁿Natas Challenge - Level 0

Prepared by: Nishanth Antony  
Date: July 17, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 0, a beginner-level web security challenge designed to demonstrate basic information disclosure vulnerabilities. The objective was to retrieve the password for Level 1 through non-intrusive inspection techniques. The assessment identified a critical vulnerability where sensitive credentials were exposed in the client-side HTML source code. This finding highlights the risks associated with improper handling of sensitive data in web applications. No exploitation beyond source code review was required, and the vulnerability was rated as **High Severity** due to the direct exposure of authentication credentials.

Key Findings:
- Sensitive information (password) embedded in HTML comments, accessible via browser tools.
- No authentication or advanced tools needed for extraction.

Recommendations:
- Implement server-side storage for sensitive data.
- Conduct regular code reviews to eliminate client-side exposures.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 1 by identifying and exploiting basic information disclosure issues in the web application.

### Scope
- Target: Natas Level 0 web page (assumed URL: http://natas0.natas.labs.overthewire.org, accessible with provided credentials for Level 0).
- Assessment Type: White-box (source code inspection allowed).
- Exclusions: No network scanning, brute-forcing, or server-side exploitation was performed, as the challenge focuses on client-side analysis.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included standard browser developer tools (e.g., Chrome DevTools). The process was non-destructive and focused on reconnaissance and information gathering.

### Step 1: Initial Reconnaissance
- Accessed the target web page using a standard web browser.
- Reviewed the page content for any visible indicators of sensitive information.

### Step 2: Source Code Inspection
- Right-clicked on the webpage and selected "View Page Source" or "Inspect" to open the browser's developer tools.
- Navigated to the "Elements" tab to examine the full HTML structure.
- Searched for comments, hidden elements, or inline text that might contain sensitive data (e.g., using Ctrl+F for keywords like "password" or scanning for HTML comments <!-- -->).

### Step 3: Vulnerability Identification
- Identified that the password for Level 1 was embedded directly within an HTML comment or a non-rendered element, making it trivially accessible without authentication bypass or advanced techniques.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- Developer Tools: Built-in Inspect Element feature.
- No additional scripts or external tools were required.

## Findings
### Vulnerability Details
- **Vulnerability Type**: Information Disclosure (CWE-200: Exposure of Sensitive Information to an Unauthorized Actor).
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The web application exposes the password for the next level directly in the client-side HTML source code. This is a common misconfiguration where developers inadvertently leave sensitive data in comments or elements that are sent to the client browser.
- **Proof of Concept**:
  1. Navigate to the Natas Level 0 page.
  2. View the source code.
  3. Locate the comment or element containing the string: "The password for natas1 is [REDACTED]".
- **Impact**: An attacker could easily obtain credentials for subsequent levels or, in a real-world scenario, gain unauthorized access to protected resources. This vulnerability bypasses any server-side protections and requires no special privileges.

### Affected Components
- Client-side HTML rendering.
- No server-side vulnerabilities were tested in this level.

## Solution and Exploitation
The password for Natas Level 1 was successfully extracted from the HTML source code without any modifications to the application. In a real pentest, this would be reported as a finding rather than exploited further without authorization.

- **Extracted Artifact**: Password for Level 1 (redacted for this report).
- **Remediation Steps**:
  1. Remove all sensitive information from client-side code.
  2. Store credentials securely on the server (e.g., in a database with proper access controls).
  3. Use environment variables or secure vaults for configuration secrets.

## Learnings and Recommendations
### Key Learnings
- **Basic Web Inspection Techniques**: Browser developer tools are powerful for initial reconnaissance. Many web applications leak sensitive data through source code, JavaScript files, or metadata, which can be accessed without advanced skills.
- **Importance of Secure Coding Practices**: Developers should never embed secrets like passwords, API keys, or tokens in client-side code, as it is transmitted to users and can be inspected easily.
- **Broader Implications**: This vulnerability underscores the need for defense-in-depth, including code reviews, static analysis tools (e.g., SAST), and secure development lifecycle (SDLC) integration.

### Recommendations
- **Short-Term**: Conduct a full source code audit of the application to identify and remove any exposed secrets.
- **Long-Term**: 
  - Adopt OWASP best practices for handling sensitive data.
  - Implement automated scanning tools (e.g., GitHub Secrets Scanning) in CI/CD pipelines.
  - Train developers on secure coding to prevent similar issues.
- **Mitigation Controls**: Use server-side rendering for dynamic secrets and enforce HTTPS to protect against network-level interception (though not directly applicable here).

## Conclusion
This walkthrough for Natas Level 0 demonstrates a fundamental web security flaw exploitable through simple inspection. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: always inspect the basics first. For real-world applications, regular VAPT assessments are essential to mitigate such risks.
