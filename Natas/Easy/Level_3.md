# Natas Challenge - Level 3

Prepared by: Nishanth Antony  
Date: July 18, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 3, a beginner-level web security challenge designed to demonstrate information disclosure through misuse of configuration files like robots.txt. The objective was to find the password for Level 4 by leveraging exposed paths. The assessment identified a critical vulnerability where the robots.txt file inadvertently revealed a hidden subdirectory containing sensitive credentials. This finding highlights the risks of using robots.txt to "hide" sensitive areas and the potential for information leakage via publicly accessible files. No advanced tools or exploitation were required, and the vulnerability was rated as **High Severity** due to the direct disclosure of authentication credentials.

Key Findings:
- robots.txt file exposes disallowed paths, including a /s3cr3t subdirectory.
- Sensitive file in the subdirectory contains usernames and passwords.
- No authentication or specialized tools needed for extraction.

Recommendations:
- Avoid listing sensitive paths in robots.txt; use server-side access controls instead.
- Disable directory listing and secure hidden resources.
- Conduct regular reviews of public configuration files to prevent disclosures.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 4 by identifying and exploiting information disclosure issues through inspection of the robots.txt file and subsequent navigation.

### Scope
- Target: Natas Level 3 web page (URL: http://natas3.natas.labs.overthewire.org, accessible with credentials from Level 2).
- Assessment Type: White-box (source code and configuration file inspection allowed).
- Exclusions: No network scanning, brute-forcing, or server-side exploitation was performed, as the challenge focuses on reconnaissance and path discovery.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included standard web browser features for file access and navigation. The process was non-destructive and focused on reconnaissance, configuration file review, and information gathering.

### Step 1: Initial Reconnaissance
- Accessed the target web page using a standard web browser.
- Reviewed the page content for hints, which mentioned: "There is nothing on this page."

### Step 2: Inspecting robots.txt
- Navigated to the standard robots.txt file: http://natas3.natas.labs.overthewire.org/robots.txt.
- Analyzed its contents, which included directives like "User-agent: *" and "Disallow: /s3cr3t/", inadvertently disclosing the existence of a hidden /s3cr3t subdirectory.

### Step 3: Directory and File Enumeration
- Navigated to the disclosed path: http://natas3.natas.labs.overthewire.org/s3cr3t/.
- Observed directory listing was enabled, exposing a file (e.g., users.txt or similar).
- Accessed the file to extract the username and password for Level 4.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- Built-in Features: Manual URL navigation to robots.txt and subdirectories.
- No additional scripts, scanners, or external tools were required.

## Findings
### Vulnerability Details
- **Vulnerability Type**: Information Disclosure (CWE-200: Exposure of Sensitive Information to an Unauthorized Actor) via Misconfigured robots.txt (CWE-538: Insertion of Sensitive Information into Externally-Accessible File or Directory).
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The robots.txt file, intended for search engine crawlers, lists disallowed paths including /s3cr3t/, which attackers can use to discover hidden resources. With directory indexing enabled, the subdirectory exposes a sensitive file containing plaintext credentials.
- **Proof of Concept**:
  1. Navigate to /robots.txt and note the "Disallow: /s3cr3t/" entry.
  2. Browse to /s3cr3t/ to view the directory listing.
  3. Access the exposed file (e.g., /s3cr3t/users.txt) and locate the credentials for natas4.
- **Impact**: An attacker could use the disclosed paths to access sensitive data, leading to credential theft and unauthorized access to higher levels. In real-world scenarios, this could reveal admin panels, backups, or internal files.

### Affected Components
- Web server configuration (robots.txt and directory indexing).
- No client-side vulnerabilities were tested in this level.

## Solution and Exploitation
The username and password for Natas Level 4 were successfully extracted from the file in the /s3cr3t subdirectory without any modifications to the application. In a real pentest, this would be reported as a finding rather than exploited further without authorization.

- **Extracted Artifact**: Credentials for Level 4 (redacted for this report).
- **Remediation Steps**:
  1. Remove sensitive path listings from robots.txt or avoid using it for security.
  2. Disable directory listing in the web server configuration (e.g., "Options -Indexes" in Apache).
  3. Secure hidden directories with authentication or IP restrictions.
  4. Store credentials in protected, non-public locations.

## Learnings and Recommendations
### Key Learnings
- **robots.txt Misuse**: The robots.txt file can inadvertently expose sensitive paths if not configured carefully, as it is publicly accessible and often scanned by attackers.
- **Information Disclosure**: Developers should avoid listing sensitive directories or files in publicly accessible configuration files, emphasizing the need for proper access controls over obfuscation.
- **Broader Implications**: This vulnerability underscores the importance of secure-by-default configurations and tools like robots.txt scanners in vulnerability assessments.

### Recommendations
- **Short-Term**: Review and sanitize robots.txt; disable indexing on sensitive directories.
- **Long-Term**: 
  - Adopt OWASP best practices for configuration file security and path protection.
  - Implement automated tools (e.g., Gobuster or Feroxbuster) for testing in development pipelines.
  - Train teams on the limitations of robots.txt and the preference for server-side security.
- **Mitigation Controls**: Use .htaccess or equivalent to deny access to sensitive paths; monitor logs for robots.txt and disallowed path accesses.

## Conclusion
This walkthrough for Natas Level 3 demonstrates how a common configuration file like robots.txt can lead to significant information disclosure when misused. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: do not rely on obscurity for security. For real-world applications, regular VAPT assessments are essential to mitigate such risks.
