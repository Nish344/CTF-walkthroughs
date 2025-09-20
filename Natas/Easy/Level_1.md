# 🏴󠁡󠁦󠁷󠁡󠁲󠁿 Natas Challenge - Level 1

Prepared by: Nishanth Antony  
Date: September 20, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 1, a beginner-level web security challenge designed to demonstrate ineffective client-side restrictions and information disclosure vulnerabilities. The objective was to retrieve the password for Level 2 despite right-click functionality being disabled on the page. The assessment identified a critical vulnerability where sensitive credentials were exposed in the client-side HTML source code, easily accessible by bypassing the trivial restriction. This finding highlights the futility of relying on client-side controls for security and the risks of embedding sensitive data in web pages. No advanced exploitation was required, and the vulnerability was rated as **High Severity** due to the direct exposure of authentication credentials.

Key Findings:
- Right-click context menu disabled via JavaScript, but easily bypassed.
- Sensitive information (password) embedded in HTML comments, accessible via alternative source viewing methods.
- No authentication or specialized tools needed for extraction.

Recommendations:
- Avoid client-side restrictions for security enforcement; use server-side protections.
- Implement server-side storage for sensitive data.
- Conduct regular code reviews to eliminate client-side exposures.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 2 by identifying and exploiting basic information disclosure issues, while bypassing a client-side restriction on right-clicking.

### Scope
- Target: Natas Level 1 web page.
- Assessment Type: White-box (source code inspection allowed).
- Exclusions: No network scanning, brute-forcing, or server-side exploitation was performed, as the challenge focuses on client-side analysis and bypass techniques.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included standard web browser features. The process was non-destructive and focused on reconnaissance, restriction bypass, and information gathering.

### Step 1: Initial Reconnaissance
- Accessed the target web page using a standard web browser.
- Reviewed the page content for any visible indicators of sensitive information.
- Attempted to right-click on the page to inspect the source, but observed that the context menu was disabled, triggering an alert: "Right clicking has been blocked!"

### Step 2: Bypassing Client-Side Restriction
- Bypassed the right-click disablement by using the keyboard shortcut Ctrl+U (or Cmd+Option+U on macOS) to directly view the page source.
- Alternatively, accessed the source via the browser menu (View > Page Source).

### Step 3: Source Code Inspection and Vulnerability Identification
- Examined the HTML source code in the browser's source viewer.
- Searched for comments, hidden elements, or inline text containing sensitive data (e.g., using Ctrl+F for keywords like "password" or scanning for HTML comments <!-- -->).
- Identified the password for Level 2 embedded directly within an HTML comment.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- Built-in Features: Keyboard shortcuts (Ctrl+U) and View Page Source option.
- No additional scripts, developer tools, or external tools were required.

## Findings
### Vulnerability Details
- **Vulnerability Type**: Information Disclosure (CWE-200: Exposure of Sensitive Information to an Unauthorized Actor) combined with Ineffective Client-Side Control (CWE-1021: Improper Restriction of Rendered UI Layers or Frames).
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The web application attempts to prevent source code inspection by disabling the right-click context menu via JavaScript (using oncontextmenu="return false;" and an alert). However, this is a weak client-side control that can be bypassed easily. The password for the next level remains exposed in an HTML comment within the source code, which is transmitted to the client browser.
- **Proof of Concept**:
  1. Navigate to the Natas Level 1 page.
  2. Attempt to right-click and note the blockage alert.
  3. Press Ctrl+U to view the source code.
  4. Locate the comment containing the string: "<!--The password for natas2 is [REDACTED]-->".
- **Impact**: An attacker can trivially bypass the restriction and obtain credentials for subsequent levels or, in a real-world scenario, gain unauthorized access to protected resources. Client-side restrictions provide no real security and can be ignored or disabled by users.

### Affected Components
- Client-side JavaScript for UI restrictions.
- Client-side HTML rendering.
- No server-side vulnerabilities were tested in this level.

### Source Code Discovery
```html
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas1", "pass": "0n***********************" };</script></head>
<body oncontextmenu="javascript:alert('right clicking has been blocked!');return false;">
<h1>natas1</h1>
<div id="content">
You can find the password for the
next level on this page, but rightclicking has been blocked!

<!--The password for natas2 is TguM************************* -->
</div>
</body>
</html>
```

## Solution and Exploitation
The password for Natas Level 2 was successfully extracted from the HTML source code without any modifications to the application or advanced techniques. In a real pentest, this would be reported as a finding rather than exploited further without authorization.

- **Extracted Artifact**: Password for Level 2 (redacted for this report).
- **Remediation Steps**:
  1. Remove all sensitive information from client-side code.
  2. Avoid relying on JavaScript-based UI restrictions for security; enforce protections server-side.
  3. Store credentials securely on the server (e.g., in a database with proper access controls).
  4. Use environment variables or secure vaults for configuration secrets.

## Learnings and Recommendations
### Key Learnings
- **Client-Side Restrictions Are Weak**: Disabling features like right-click offers minimal security, as users can bypass them using keyboard shortcuts, browser menus, or by disabling JavaScript entirely.
- **Source Code Exposure**: Sensitive information in client-side code remains vulnerable, emphasizing the need to secure server-side logic and avoid embedding secrets in HTML, JavaScript, or other client-accessible resources.
- **Broader Implications**: This vulnerability underscores the importance of understanding that client-side controls can be manipulated, highlighting the need for defense-in-depth, including code reviews, static analysis tools (e.g., SAST), and secure development lifecycle (SDLC) integration.

### Recommendations
- **Short-Term**: Conduct a full source code audit of the application to identify and remove any exposed secrets or ineffective controls.
- **Long-Term**: 
  - Adopt OWASP best practices for handling sensitive data and client-side security.
  - Implement automated scanning tools (e.g., GitHub Secrets Scanning) in CI/CD pipelines.
  - Train developers on secure coding to prevent reliance on client-side restrictions.
- **Mitigation Controls**: Use server-side authentication and authorization for sensitive data access. Enforce HTTPS to protect against network-level interception (though not directly applicable here). Consider content security policies (CSP) to limit script behaviors.

## Conclusion
This walkthrough for Natas Level 1 demonstrates how trivial client-side restrictions fail to protect against basic inspection techniques, leading to information disclosure. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: client-side security is illusory—always secure the server. For real-world applications, regular VAPT assessments are essential to mitigate such risks.
