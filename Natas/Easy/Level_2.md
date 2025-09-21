# 🏴󠁡󠁦󠁷󠁡󠁲󠁿Natas Challenge - Level 2

Prepared by: Nishanth Antony  
Date: September 21, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 2, a beginner-level web security challenge designed to demonstrate information disclosure through directory enumeration and insecure file exposure. The objective was to locate the password for Level 3 by identifying hidden directories and files. The assessment identified a critical vulnerability where directory listing was enabled, allowing unauthorized access to sensitive files containing credentials. This finding highlights the risks of improper web server configuration and the exposure of sensitive data via guessable paths. No advanced tools or exploitation were required, and the vulnerability was rated as **High Severity** due to the direct disclosure of authentication credentials.

Key Findings:
- Exposed /files directory via source code inspection, leading to directory listing.
- Sensitive file (users.txt) containing passwords accessible without restrictions.
- No authentication or specialized tools needed for extraction.

Recommendations:
- Disable directory listing on the web server.
- Implement proper access controls and directory indexing restrictions.
- Conduct regular configuration reviews to prevent unauthorized access to hidden resources.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 3 by identifying and exploiting information disclosure issues through directory enumeration and file access.

### Scope
- Target: Natas Level 2 web page (assumed URL: http://natas2.natas.labs.overthewire.org, accessible with credentials from Level 1).
- Assessment Type: White-box (source code inspection and manual enumeration allowed).
- Exclusions: No network scanning, brute-forcing, or server-side exploitation was performed, as the challenge focuses on client-side analysis and basic web navigation.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included standard web browser features for source inspection and navigation. The process was non-destructive and focused on reconnaissance, path discovery, and information gathering.

### Step 1: Initial Reconnaissance and Source Code Inspection
- Accessed the target web page using a standard web browser.
- Reviewed the page content, which displayed a message: "You can find the password for the next level somewhere on this page." with a link to a pixel image.
- Inspected the HTML source code (via Ctrl+U or View Page Source) and identified an <img> tag sourcing from "files/pixel.png", revealing the existence of a /files directory.

### Step 2: Directory Enumeration
- Navigated to the hinted directory: http://natas2.natas.labs.overthewire.org/files/.
- Observed that directory listing was enabled, exposing files including pixel.png and users.txt (note: the provided methodology mentioned "subdirectories" and "usernames," but assessment confirmed these as files, with users.txt being the key artifact).

### Step 3: File Access and Vulnerability Identification
- Accessed the exposed file: http://natas2.natas.labs.overthewire.org/files/users.txt.
- Analyzed the file contents, which listed usernames and passwords, including the entry for natas3.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- Built-in Features: View Page Source and manual URL navigation.
- No additional scripts, scanners, or external tools were required.

## Findings
### Vulnerability Details
- **Vulnerability Type**: Information Disclosure (CWE-200: Exposure of Sensitive Information to an Unauthorized Actor) via Directory Listing (CWE-548: Exposure of Information Through Directory Listing).
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The web application exposes a directory (/files) through a reference in the HTML source code. With directory indexing enabled on the server, users can list and access files without authentication. A sensitive file (users.txt) contains plaintext credentials, including the password for the next level.
- **Proof of Concept**:
  1. Navigate to the Natas Level 2 page and view the source code.
  2. Browse to /files/ to view the directory listing (pixel.png and users.txt).
  3. Access /files/users.txt and locate the line: "natas3: [REDACTED]".
- **Impact**: An attacker could enumerate directories and access sensitive files, leading to credential theft and unauthorized progression to higher privilege levels. In a real-world scenario, this could enable lateral movement or data exfiltration.

### Affected Components
- Web server configuration (e.g., Apache or similar with Indexes enabled).
- Client-side HTML rendering exposing path hints.
- No server-side vulnerabilities beyond configuration were tested in this level.

### Screenshot of Source Code Discovery
The following screenshot captures the HTML source code viewed via Ctrl+U, highlighting the <img> tag referencing "files/pixel.png", which hints at the /files directory, along with other elements like the page content and wechall integration script:

<img width="800" height="187" alt="image" src="https://github.com/user-attachments/assets/63ccd060-b181-4dd4-bc4a-759dad7bc7b4" />

## Solution and Exploitation
The password for Natas Level 3 was successfully retrieved from the users.txt file without any modifications to the application. In a real pentest, this would be reported as a finding rather than exploited further without authorization.

- **Extracted Artifact**: Password for Level 3 (redacted for this report).
- **Remediation Steps**:
  1. Disable directory listing in the web server configuration (e.g., remove "Options Indexes" in Apache .htaccess or httpd.conf).
  2. Remove or secure sensitive files from publicly accessible directories.
  3. Use robots.txt or access controls (e.g., .htaccess deny rules) to restrict enumeration.
  4. Avoid hinting at hidden paths in client-side code.

## Learnings and Recommendations
### Key Learnings
- **Directory Enumeration Risks**: Exposed directories can reveal sensitive information if not properly secured, often through simple URL manipulation or source code hints.
- **Web Server Configuration**: Improper settings like enabled directory indexing allow attackers to discover and access hidden files, emphasizing the need for secure defaults.
- **Broader Implications**: This vulnerability highlights the importance of least privilege in file permissions and the use of tools like dirbuster for testing, alongside secure development practices.

### Recommendations
- **Short-Term**: Audit web directories for exposed listings and sensitive files; implement immediate access denials.
- **Long-Term**: 
  - Adopt OWASP best practices for web server hardening and secure file handling.
  - Integrate automated vulnerability scanners (e.g., Nikto or OWASP ZAP) in CI/CD pipelines.
  - Train developers and administrators on secure configuration to prevent enumeration risks.
- **Mitigation Controls**: Enforce HTTPS, use web application firewalls (WAF) to block enumeration patterns, and monitor access logs for suspicious navigation.

## Conclusion
This walkthrough for Natas Level 2 demonstrates how basic directory enumeration, triggered by a source code hint, can lead to critical information disclosure. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: secure your configurations and avoid exposing paths. For real-world applications, regular VAPT assessments are essential to mitigate such risks.
