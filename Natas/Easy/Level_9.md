# 🏴󠁡󠁦󠁷󠁡󠁲󠁿**Natas Challenge - Level 9**

**Prepared by:** Nishanth Antony  
**Date:** October 16, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation  
**Platform:** Over The Wire  

---

## **Executive Summary**
This walkthrough documents the assessment of **Natas Level 9**, a beginner-level web security challenge focused on **directory browsing** and **command injection vulnerabilities**. The objective was to retrieve the password for **Natas Level 10**. The assessment revealed **two critical vulnerabilities**:

1. **Directory browsing enabled**, allowing full traversal of the web root and direct access to `/etc/natas_webpass/natas10`.
2. **Command injection** in a search form, enabling arbitrary command execution via unsanitized input.

Both methods successfully retrieved the **Level 10 password**, highlighting severe flaws in input validation and server configuration. These vulnerabilities were rated **High Severity** due to direct exposure of sensitive credentials.

**Key Findings:**
- Directory listing enabled on the web server.
- Direct access to `/etc/natas_webpass/natas10` via URL.
- Command injection via input field (e.g., `; cat /etc/natas_webpass/natas10`).
- No input sanitization or command execution restrictions.

**Recommendations:**
- Disable directory browsing.
- Sanitize and validate all user inputs.
- Use allowlists for command execution.
- Restrict file system access outside the web root.

---

## **Introduction**

### **Background**
Natas is an educational web security challenge series hosted by OverTheWire, designed to teach common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### **Objective**
The primary goal of this level is to obtain the password for **Natas Level 10** by exploiting either **directory browsing** or **command injection**.

### **Scope**
- **Target:** `http://natas9.natas.labs.overthewire.org` (accessible with Level 8 credentials).
- **Assessment Type:** White-box (source inspection allowed).
- **Exclusions:** No network scanning, brute-forcing, or external tools beyond browser and Burp Suite.

---

## **Methodology**
The assessment followed a structured penetration testing approach aligned with **OWASP Testing Guide** and **PTES** methodologies. Tools used included a standard web browser and **Burp Suite** for request analysis.

### **Step 1: Initial Reconnaissance**
- Accessed the target web page.
- Observed a search form and a dictionary file reference (`words.txt`).

### **Step 2: Directory Browsing Discovery**
- Navigated to the parent directory (`../`) via URL manipulation.
- Discovered **directory listing was enabled**.
- Browsed to `/etc/natas_webpass/natas10` and retrieved the password.

### **Step 3: Command Injection Exploitation**
- Identified the search form submitted input to a backend script.
- Injected a semicolon (`;`) followed by `cat /etc/natas_webpass/natas10`.
- Command output was reflected in the response, revealing the password.

### **Tools Utilized**
- **Web Browser:** Google Chrome (Version 117 or equivalent)
- **Burp Suite:** For intercepting and modifying POST requests

---

## **Findings**

### **Vulnerability Details**

| **Vulnerability** | **Type** | **CWE** | **Severity** | **CVSS Score** |
|-------------------|---------|--------|--------------|----------------|
| Directory Browsing | Information Disclosure | CWE-548 | High | 7.5 |
| Command Injection | OS Command Injection | CWE-78 | Critical | 9.8 |

#### **1. Directory Browsing (CWE-548)**
- **Description:** The web server allowed directory listing, exposing the full file structure.
- **Proof of Concept:**
  1. Navigate to `http://natas9.natas.labs.overthewire.org/..`
  2. Traverse to `/etc/natas_webpass/natas10`
  3. Read file contents directly in the browser.
- **Impact:** Full system file access, including password files.

#### **2. Command Injection (CWE-78)**
- **Description:** User input in the search form was passed to a shell command without sanitization.
- **Proof of Concept:**
  ```http
  POST /index.php HTTP/1.1
  Host: natas9.natas.labs.overthewire.org
  ...
  key=; cat /etc/natas_webpass/natas10 #
  ```
  - The `#` comments out the rest of the command, preventing errors.
- **Impact:** Arbitrary command execution with web server privileges.

---

## **Solution and Exploitation**

The password for **Natas Level 10** was successfully retrieved using **both methods**:

1. **Directory Browsing:**  
   Accessed: `http://natas9.natas.labs.overthewire.org/../../../../etc/natas_webpass/natas10`

2. **Command Injection:**  
   Payload: `; cat /etc/natas_webpass/natas10 #`  
   → Response contained the password in plaintext.

> **Extracted Artifact:** Password for Level 10 (redacted for this report).

---

## **Burp Suite Request (Command Injection)**

```http
POST /index.php HTTP/1.1
Host: natas9.natas.labs.overthewire.org
Authorization: Basic bmF0YXM5OnBhc3N3b3Jk
Content-Type: application/x-www-form-urlencoded
Content-Length: 41

key=; cat /etc/natas_webpass/natas10 #
```

**Response (truncated):**
```html
<pre>
[password redacted]
</pre>
```

---

## **Learnings and Recommendations**

### **Key Learnings**
- **Directory Browsing:** Even without code execution, enabled listings can leak sensitive files.
- **Command Injection:** Never pass unsanitized user input to system commands.
- **Defense in Depth:** Multiple weak controls compound risk.

### **Recommendations**

| **Timeline** | **Action** |
|--------------|-----------|
| **Short-Term** | Disable directory browsing (`Options -Indexes` in Apache). |
| | Sanitize input using allowlists and escape shell commands. |
| **Long-Term** | 
- Adopt OWASP Input Validation Cheat Sheet.
- Use `escapeshellarg()` or `escapeshellcmd()` in PHP.
- Place web root outside sensitive directories.
- Integrate SAST/DAST tools in CI/CD.

**Mitigation Controls:**
- Web Application Firewall (WAF) with command injection rules.
- File system permissions: deny read access to `/etc/natas_webpass/`.
- Monitor logs for `..`, `;`, `|`, and shell metacharacters.

---

## **Conclusion**
This walkthrough for **Natas Level 9** demonstrates how **directory browsing** and **command injection** can be exploited to gain unauthorized access to sensitive files. Both vulnerabilities were trivial to exploit due to missing input validation and misconfigured server settings. The dual exploitation paths emphasize the importance of **layered security controls**.

Progressing to higher levels will involve more advanced techniques, but the core lesson remains: **never trust user input, and never expose the file system**.

For real-world applications, **regular VAPT assessments**, **secure configuration**, and **developer training** are essential to prevent such critical flaws.

---

<xaiArtifact artifact_id="2ec75f68-3989-437f-906a-f99b6c4b8074" artifact_version_id="cd188515-db9a-4251-ae59-80f04b2330aa" title="Natas_Level_9_Report.md" contentType="text/markdown">

# **Natas Challenge - Level 9**

## **Executive Summary**
Assessment revealed **directory browsing** and **command injection** vulnerabilities allowing retrieval of the **Natas Level 10 password** from `/etc/natas_webpass/natas10`. Rated **High to Critical Severity**.

## **Methodology**
1. Discovered directory listing enabled.
2. Navigated to password file via `../../../../etc/natas_webpass/natas10`.
3. Exploited command injection with `; cat /etc/natas_webpass/natas10 #`.

## **Burp Request**
```http
POST /index.php HTTP/1.1
Host: natas9.natas.labs.overthewire.org
Content-Type: application/x-www-form-urlencoded

key=; cat /etc/natas_webpass/natas10 #
```

## **Findings**
- **Directory Browsing (CWE-548):** Enabled, allowed file traversal.
- **Command Injection (CWE-78):** Unsanitized input led to arbitrary command execution.

## **Solution**
Password retrieved via both methods. **Redacted**.

## **Recommendations**
- Disable directory browsing.
- Sanitize inputs with allowlists.
- Use `escapeshellarg()` in PHP.
- Restrict file system access.

## **Conclusion**
Critical flaws due to missing validation and configuration. Regular security testing is essential.

</xaiArtifact>
