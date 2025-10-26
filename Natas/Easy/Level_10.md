# 🏴󠁡󠁦󠁷󠁡󠁲󠁿Natas Challenge - Level 10

Prepared by: Nishanth Antony  
Date: October 17, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 10, a beginner-level web security challenge designed to demonstrate command injection vulnerabilities. The objective was to retrieve the password for Natas Level 11 by exploiting a flaw in the search functionality. The assessment identified a critical vulnerability where user input was passed to a `grep` command via the `passthru` function without adequate sanitization, allowing manipulation with wildcards. This finding highlights the risks of insufficient input validation and the need for robust command execution controls. The vulnerability was rated as **High Severity** due to the direct exposure of authentication credentials.

Key Findings:
- Search form executes a `grep` command using unsanitized user input via `passthru`.
- Special characters (`/[{\[];&`) are filtered, but the wildcard `.*` is not blocked.
- Input `.* /etc/natas_webpass/natas11` manipulated the command to reveal the password file.
- No strict input validation prevented command injection.

Recommendations:
- Implement strict input allowlisting.
- Avoid passing user input directly to system commands.
- Use secure alternatives like `exec` with proper escaping.
- Conduct regular security testing.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 11 by exploiting a command injection vulnerability in the search form.

### Scope
- Target: Natas Level 10 web page (http://natas10.natas.labs.overthewire.org, accessible with credentials from Level 9).
- Assessment Type: White-box (source inspection allowed).
- Exclusions: No network scanning, brute-forcing, or advanced exploitation was performed, as the challenge focused on command injection.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included a standard web browser and Burp Suite for request analysis. The process was non-destructive and focused on input manipulation.

### Step 1: Initial Reconnaissance
- Accessed the target web page using a standard web browser.
- Identified a search form that executed a `grep` command via `passthru`.

### Step 2: Input Analysis
- Noted that special characters (`/[{\[];&`) were filtered but wildcards (`.*`) were permitted.
- Analyzed the command structure to exploit the unfiltered wildcard.

### Step 3: Command Injection and Vulnerability Identification
- Crafted the input `.* /etc/natas_webpass/natas11` to manipulate the `grep` command into `grep -i .* /etc/natas_webpass/natas11`.
- Submitted the input via the web form and observed the password in the response.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- Burp Suite: For intercepting and analyzing the POST request.

## Findings
### Vulnerability Details
- **Vulnerability Type**: OS Command Injection (CWE-78: Improper Neutralization of Special Elements used in an OS Command).
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The search form passes user input to a `grep` command via `passthru` with partial filtering (blocking `/[{\[];&`), but allowing wildcards (`.*`) to manipulate the command and access `/etc/natas_webpass/natas11`.
- **Proof of Concept**:
  1. Navigate to the Natas Level 10 page and locate the search form.
  2. Enter `.* /etc/natas_webpass/natas11` as input.
  3. Submit the form and observe the password for Level 11 in the output.
- **Impact**: An attacker can inject commands to access sensitive files, leading to credential theft and progression to higher levels. In real-world scenarios, this could enable full system compromise.

### Affected Components
- Search form input handling.
- `passthru` function execution.

## Solution and Exploitation
The password for Natas Level 11 was successfully retrieved by submitting the crafted input `.* /etc/natas_webpass/natas11` via the search form, exploiting the command injection vulnerability without any modifications to the application. In a real pentest, this would be reported as a finding rather than exploited further without authorization.

- **Extracted Artifact**: Password for Level 11 (redacted for this report).
- **Remediation Steps**:
  1. Implement strict input allowlisting to block wildcards and special characters.
  2. Avoid using `passthru` with user input; use safer functions with escaping (e.g., `escapeshellarg`).
  3. Restrict file system access to prevent reading sensitive files.
  4. Validate all commands server-side.

## Learnings and Recommendations
### Key Learnings
- **Command Injection Risks**: Insufficient sanitization allows attackers to manipulate system commands.
- **Importance of Input Validation**: Strict allowlisting and proper escaping are critical to prevent injection.
- **Security Testing**: Regular penetration testing can identify such vulnerabilities by simulating attacker inputs.
- **Broader Implications**: This vulnerability emphasizes the need for secure coding practices and server hardening.

### Recommendations
- **Short-Term**: Audit input handling and add wildcard filtering.
- **Long-Term**: 
  - Follow OWASP Command Injection Prevention Cheat Sheet.
  - Integrate automated tools (e.g., Burp Suite or OWASP ZAP) to detect injection flaws in CI/CD pipelines.
  - Train developers on secure command execution practices.
- **Mitigation Controls**: Deploy a WAF with command injection rules, enforce least privilege for web server processes, and monitor for suspicious input patterns.

## Conclusion
This walkthrough for Natas Level 10 demonstrates how command injection vulnerabilities can be exploited through unsanitized input, leading to unauthorized access to sensitive files like passwords. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: robust input validation is essential to prevent command execution attacks. For real-world applications, regular VAPT assessments are essential to mitigate such risks.
