# 🏴󠁡󠁦󠁷󠁡󠁲󠁿Natas Challenge - Level 7

## Executive Summary
This walkthrough documents the assessment of Natas Level 7, a beginner-level web security challenge designed to demonstrate path traversal vulnerabilities. The objective was to retrieve the password for Level 8 by exploiting a hint in the source code. The assessment identified a critical vulnerability where a comment exposed "/etc/natas8/webpage", allowing password retrieval via directory traversal. This finding highlights the risks of inadequate input validation. The vulnerability was rated as **High Severity**.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire.

### Objective
The primary goal is to obtain the password for Natas Level 8 by exploiting path traversal.

### Scope
- Target: Natas Level 7 web page (URL: http://natas7.natas.labs.overthewire.org).
- Assessment Type: White-box.
- Exclusions: No network scanning or advanced exploitation.

## Methodology
### Step 1: Initial Reconnaissance
- Accessed the target web page and inspected the source code.

### Step 2: Source Code Analysis
- Found a comment hinting at "/etc/natas8/webpage".

### Step 3: Path Traversal and Vulnerability Identification
- Accessed "/etc/natas8/webpage" directly and extracted the Level 8 password.

### Tools Utilized
- Web Browser: Google Chrome.

## Findings
### Vulnerability Details
- **Vulnerability Type**: Improper Input Validation via Path Traversal.
- **Severity**: High (CVSS Score: 7.5).
- **Description**: A source code comment exposed "/etc/natas8/webpage", accessible without validation.
- **Proof of Concept**:
  1. Inspect source code for the hint.
  2. Access "/etc/natas8/webpage" to retrieve the password.
- **Impact**: An attacker can access sensitive files, leading to credential theft.

### Affected Components
- Client-side source code exposure.
- File system access to "/etc/natas8/webpage".

## Solution and Exploitation
The password for Natas Level 8 was retrieved from "/etc/natas8/webpage".

- **Extracted Artifact**: Password for Level 8 (redacted).
- **Remediation Steps**:
  1. Validate inputs to restrict file access.
  2. Remove sensitive hints from code.
  3. Configure server-side restrictions.

## Learnings and Recommendations
### Key Learnings
- Improper input validation allows path traversal.
- Input sanitization is crucial.

### Recommendations
- **Short-Term**: Sanitize input handling.
- **Long-Term**: Follow OWASP guidelines and train developers.
- **Mitigation Controls**: Enforce file access restrictions and monitor attempts.

## Conclusion
This walkthrough demonstrates how path traversal can expose passwords. Regular VAPT assessments are essential to mitigate such risks.
