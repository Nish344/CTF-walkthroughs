# 🏴󠁡󠁦󠁷󠁡󠁲󠁿Natas Challenge - Level 6

Prepared by: Nishanth Antony  
Date: October 13, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 6, a beginner-level web security challenge designed to demonstrate file inclusion vulnerabilities. The objective was to retrieve the password for Level 7 by identifying and accessing an exposed include file. The assessment uncovered a critical vulnerability where the application referenced a sensitive file ("shared.inc") that was accessible via a source view link, revealing the password. This finding underscores the importance of securing include files and restricting their visibility. The vulnerability was rated as **High Severity** due to the direct exposure of authentication credentials.

Key Findings:
- A "View Source" link exposed the source code, revealing a reference to "shared.inc".
- Accessing "shared.inc" directly provided the input password.
- Submitting the input password retrieved the password for Level 7.
- No server-side validation prevented access to the include file.

Recommendations:
- Restrict access to include files using server configurations.
- Avoid exposing sensitive file references in client-side code.
- Implement proper access controls and file permission checks.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 7 by identifying and exploiting a file inclusion vulnerability to access a sensitive include file.

### Scope
- Target: Natas Level 6 web page (assumed URL: http://natas6.natas.labs.overthewire.org, accessible with credentials from Level 5).
- Assessment Type: White-box (source code inspection allowed).
- Exclusions: No network scanning, brute-forcing, or advanced exploitation was performed, as the challenge focused on file inclusion analysis.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included a standard web browser for source code inspection and file access. The process was non-destructive and focused on reconnaissance and file analysis.

### Step 1: Initial Reconnaissance
- Accessed the target web page using a standard web browser.
- Noted a "View Source" link on the page, indicating potential source code exposure.

### Step 2: Source Code Analysis
- Clicked the "View Source" link to inspect the page's source code.
- Identified a function that included a file named "shared.inc".

### Step 3: File Inclusion and Vulnerability Identification
- Accessed the "shared.inc" file directly via the browser.
- Found the input password within the file content.
- Submitted the input password through the webpage's input form.
- Observed the retrieval of the password for Level 7.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- No additional scripts or external tools were required.

## Findings
### Vulnerability Details
- **Vulnerability Type**: Improper Access Control (CWE-284: Improper Access Control) via Local File Inclusion (CWE-98: Improper Control of Filename for Include/Require Statement).
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The application exposed a "View Source" link that revealed a reference to "shared.inc", which contained sensitive data (the input password). Direct access to this file allowed retrieval of the password, bypassing intended access controls due to lack of file permission restrictions.
- **Proof of Concept**:
  1. Navigate to the Natas Level 6 page and click "View Source".
  2. Identify the inclusion of "shared.inc" in the source code.
  3. Access "shared.inc" directly and extract the input password.
  4. Submit the password via the webpage form to retrieve the Level 7 password.
- **Impact**: An attacker can access exposed include files to gain unauthorized access to sensitive data, such as passwords, leading to progression to higher levels. In real-world scenarios, this could result in credential theft or system compromise.

### Affected Components
- Client-side source code exposure.
- Include file ("shared.inc") accessibility.

## Solution and Exploitation
The password for Natas Level 7 was successfully retrieved by accessing "shared.inc" and submitting the contained password without any modifications to the application. In a real pentest, this would be reported as a finding rather than exploited further without authorization.

- **Extracted Artifact**: Password for Level 7 (redacted for this report).
- **Remediation Steps**:
  1. Restrict access to include files using server-side configurations (e.g., .htaccess or web server rules).
  2. Remove or obfuscate sensitive file references from client-side code.
  3. Validate and sanitize all file inclusion operations server-side.

## Learnings and Recommendations
### Key Learnings
- **File Inclusion Risks**: Exposed include files can leak sensitive logic or credentials if not properly secured.
- **Secure File Handling**: Include files should be placed outside the web root or protected with access controls.
- **Broader Implications**: This vulnerability highlights the need for defense-in-depth, including proper file permissions and regular code reviews.

### Recommendations
- **Short-Term**: Audit and secure include file locations and permissions.
- **Long-Term**: 
  - Follow OWASP guidelines for secure file handling and input validation.
  - Integrate automated tools (e.g., Burp Suite or OWASP ZAP) to detect exposed file references in CI/CD pipelines.
  - Train developers on secure coding practices to prevent file inclusion vulnerabilities.
- **Mitigation Controls**: Use directory traversal prevention, enforce least privilege file access, and monitor for unauthorized file access attempts.

## Conclusion
This walkthrough for Natas Level 6 demonstrates how file inclusion vulnerabilities can expose sensitive data, such as passwords, when include files are accessible. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: secure file handling is critical to prevent information disclosure. For real-world applications, regular VAPT assessments are essential to mitigate such risks.

