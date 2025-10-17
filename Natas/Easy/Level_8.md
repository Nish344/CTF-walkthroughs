# 🏴󠁡󠁦󠁷󠁡󠁲󠁿Natas Challenge - Level 8

Prepared by: Nishanth Antony  
Date: October 15, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 8, a beginner-level web security challenge designed to demonstrate password decoding vulnerabilities. The objective was to retrieve the password for Level 9 by decoding an encoded input password provided in the source code. The assessment identified a critical vulnerability where the decoding process (Base64, reverse, hex conversion) was exposed, allowing unauthorized access to the password. This finding underscores the risks of using reversible encoding for authentication and the need for secure cryptographic practices. The vulnerability was rated as **High Severity** due to the direct exposure of authentication credentials.

Key Findings:
- Source code contained an encoded password ("3d3d516343746d4d6d315669563536362") and decoding function.
- Decoding via Base64, reversal, and hex conversion revealed the input password.
- Submitting the decoded password retrieved the password for Level 9.
- No secure encryption was used to protect the password.

Recommendations:
- Use strong, irreversible hashing (e.g., bcrypt) for password storage.
- Avoid exposing decoding logic or encoded values in client-side code.
- Implement server-side validation to prevent unauthorized access.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 9 by decoding an encoded input password and submitting it to the application.

### Scope
- Target: Natas Level 8 web page (assumed URL: http://natas8.natas.labs.overthewire.org, accessible with credentials from Level 7).
- Assessment Type: White-box (source code inspection allowed).
- Exclusions: No network scanning, brute-forcing, or advanced exploitation was performed, as the challenge focused on decoding.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included a standard web browser and Burp Suite for request analysis. The process was non-destructive and focused on source code analysis and decoding.

### Step 1: Initial Reconnaissance
- Accessed the target web page using a standard web browser.
- Inspected the page source code via developer tools.

### Step 2: Source Code Analysis
- Located an encoded password ("3d3d516343746d4d6d315669563536362") and a decoding function (`encodeSecret`) in the source code.
```php
  <?php
$encodedSecret = "3d3d516343746d4d6d315669563536362";
function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}
if(array_key_exists("submit", $_POST)) {
    if(encodeSecret($_POST['secret']) == $encodedSecret) {
        print "Access granted. The password for natas9 is <censored>";
    } else {
        print "Wrong secret";
    }
}
?>
```

### Step 3: Decoding and Vulnerability Identification
- Followed the decoding steps:
  1. Converted the encoded text to Base64.
  2. Reversed the resulting string.
  3. Converted the reversed string’s binary representation to hexadecimal.
- Used the decoded result as the input password and submitted it via a POST request.
- Observed the retrieval of the password for Level 9.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- Burp Suite: For capturing and analyzing the POST request.

## Findings
### Vulnerability Details
- **Vulnerability Type**: Insecure Cryptographic Storage (CWE-257: Storing Passwords in a Recoverable Format) via Reversible Encoding.
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The application stored an encoded password and provided a reversible decoding function (Base64, reverse, hex), allowing attackers to derive the input password and gain access to the Level 9 password.
- **Proof of Concept**:
  1. Inspect the source code for the encoded password and decoding function.
  2. Decode "3d3d516343746d4d6d315669563536362" using the outlined steps.
  3. Submit the decoded password via a POST request to retrieve the Level 9 password.
- **Impact**: An attacker can reverse-engineer the decoding process to access sensitive data, leading to credential theft and progression to higher levels. In real-world scenarios, this could result in unauthorized access to protected resources.

### Affected Components
- Client-side source code exposure.
- Password decoding logic.

## Solution and Exploitation
The password for Natas Level 9 was successfully retrieved by decoding the input password and submitting it via a POST request without any modifications to the application. In a real pentest, this would be reported as a finding rather than exploited further without authorization.

- **Extracted Artifact**: Password for Level 9 (redacted for this report).
- **Remediation Steps**:
  1. Replace reversible encoding with strong, irreversible hashing (e.g., bcrypt).
  2. Remove decoding logic and encoded values from client-side code.
  3. Validate authentication server-side with secure methods.

## Learnings and Recommendations
### Key Learnings
- **Encoding Weaknesses**: Reversible encoding is insecure for protecting passwords.
- **Secure Password Handling**: Use strong cryptographic methods to store sensitive data.
- **Broader Implications**: This vulnerability highlights the need for secure coding practices and regular security audits.

### Recommendations
- **Short-Term**: Audit and replace encoding with secure hashing.
- **Long-Term**: 
  - Follow OWASP guidelines for cryptographic storage and authentication.
  - Integrate automated tools (e.g., Burp Suite or OWASP ZAP) to detect insecure encoding in CI/CD pipelines.
  - Train developers on secure password management practices.
- **Mitigation Controls**: Enforce use of salted hashes, restrict access to source code, and monitor for unauthorized decoding attempts.

## Conclusion
This walkthrough for Natas Level 8 demonstrates how reversible encoding vulnerabilities can expose passwords when decoding logic is accessible. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: secure cryptographic practices are essential to prevent information disclosure. For real-world applications, regular VAPT assessments are essential to mitigate such risks.
