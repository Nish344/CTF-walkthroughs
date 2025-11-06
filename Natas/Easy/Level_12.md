# 🏴󠁡󠁦󠁷󠁡󠁲󠁿Natas Challenge - Level 12  
**Prepared by:** Nishanth Antony  
**Date:** November 06, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation  
**Platform:** Over The Wire  

## Executive Summary  
This walkthrough documents the successful exploitation of **Natas Level 12**, a beginner-level web security challenge focused on **insecure file upload** vulnerabilities. The objective was to obtain the password for **Natas Level 13** by bypassing weak client-side and server-side file validation to upload and execute a malicious PHP script.  

The assessment revealed a **critical file upload flaw** where the application:  
- Relied solely on **file extension checks** (`.jpg` allowed).  
- Assigned **predictable server-side filenames**.  
- Failed to validate **MIME type** or **file content**.  
- Permitted **request tampering** via intercepted HTTP uploads.  

By uploading a PHP shell disguised as a `.jpg` file and modifying the `filename` parameter in the POST request to `.php`, arbitrary code execution was achieved. The vulnerability was rated **Critical Severity** due to full system compromise potential.  

**Key Findings:**  
- File upload accepts `.jpg` but does **not validate content or MIME type**.  
- Server renames uploaded files but **does not sanitize the provided filename**.  
- **No execution restrictions** in the upload directory.  
- Password retrieved via `system("cat /etc/natas_webpass/natas13")`.  

**Recommendations:**  
- Enforce **strict MIME type validation** (e.g., `image/jpeg`).  
- **Scan file content** using magic bytes or libraries (e.g., `finfo`).  
- Store uploads outside web root or **disable script execution** (`.htaccess`, `php.ini`).  
- Use **randomized, non-guessable filenames**.  

---

## Introduction  

### Background  
Natas is a war-game series by OverTheWire designed to teach web application security through progressive exploitation challenges. Each level requires retrieving a password to unlock the next, simulating real-world penetration testing.  

### Objective  
Exploit the file upload functionality in **Natas Level 12** to upload and execute a PHP backdoor, then read the password for **Natas Level 13** from `/etc/natas_webpass/natas13`.  

### Scope  
- **Target:** Natas Level 12 file upload form.  
- **Assessment Type:** Black-box with request interception.  
- **Exclusions:** No brute force, no directory traversal, no external tools beyond browser and proxy.  

---

## Methodology  

The assessment followed **OWASP Testing Guide (WSTG-INFO-5, WSTG-BUSL-4)** and **PTES** standards. Tools used:  
- **Browser:** Google Chrome (DevTools + Network tab)  
- **Proxy:** Burp Suite Community / Browser Intercept  
- **Text Editor:** For crafting malicious PHP payload  

### Step 1: Initial Reconnaissance  
- Accessed the upload form at `http://natas12:<pass>@natas.labs.overthewire.org/`.  
- Observed:  
  - File input accepts `.jpg` files.  
  - Form uses `POST` with `filename` parameter.  
  - Uploaded files are accessible via generated URL (e.g., `upload/abc123.jpg`).  

### Step 2: Upload Behavior Analysis  
- Uploaded a legitimate `.jpg` image.  
- Intercepted request and noted:  
  ```http
  POST /index.php HTTP/1.1
  Content-Type: multipart/form-data; boundary=----WebKitFormBoundary...

  ------WebKitFormBoundary...
  Content-Disposition: form-data; name="filename"

  image.jpg
  ------WebKitFormBoundary...
  Content-Disposition: form-data; name="uploadedfile"; filename="image.jpg"
  Content-Type: image/jpeg

  <binary JPEG data>
  ```  
- Server response included link: `upload/<random>.jpg`  

### Step 3: Bypassing Extension Check  
- Created malicious PHP file:  
  ```php
  <?php echo system("cat /etc/natas_webpass/natas13"); ?>
  ```  
- Saved as `shell.jpg` (to pass local checks).  
- Intercepted upload request and modified:  
  - Changed `filename="shell.jpg"` → `filename="shell.php"`  
  - Kept `Content-Type: image/jpeg` (not validated server-side)  

### Step 4: Execution & Password Retrieval  
- Submitted modified request.  
- Server saved file as `upload/<random>.php`.  
- Accessed URL: `http://natas12:...@natas.labs.overthewire.org/upload/<random>.php`  
- Output: **Password for Natas 13** displayed in plaintext.  

---

## Findings  

### Vulnerability Details  
- **Vulnerability Type:** Unrestricted File Upload (CWE-434)  
- **Severity:** Critical (CVSS: 9.8 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)  
- **Description:**  
  The application trusts the `filename` parameter and does **not validate file content or MIME type**. Attackers can upload executable PHP scripts by:  
  1. Disguising payload as `.jpg` locally.  
  2. Changing extension to `.php` during upload.  
  3. Executing via web-accessible path.  

- **Proof of Concept (PoC):**  
  ```bash
  # Payload: shell.php (locally saved as shell.jpg)
  <?php echo system("cat /etc/natas_webpass/natas13"); ?>

  # Intercepted & Modified Request Snippet:
  filename="shell.php"
  Content-Type: image/jpeg  # Not checked!
  ```  
  → File uploaded as `upload/xyz123.php` and executed.  

- **Impact:**  
  - **Remote Code Execution (RCE)**  
  - Full compromise of password storage  
  - Potential lateral movement in multi-user environments  

### Affected Components  
- File upload handler (`index.php`)  
- Lack of `.htaccess` or PHP execution restrictions  
- No server-side content validation  

---

## Solution and Exploitation  

**Password for Natas Level 13 successfully retrieved.**  

### Exploitation Script (Manual via Browser)  
1. **Create payload:**  
   ```php
   <?php echo system("cat /etc/natas_webpass/natas13"); ?>
   ```  
   Save as `shell.jpg`.  

2. **Upload via form → Intercept with DevTools/Burp.**  

3. **Modify request:**  
   ```diff
   - filename="shell.jpg"
   + filename="shell.php"
   ```  

4. **Forward request → Note upload URL.**  

5. **Visit:** `http://natas12:<pass>@natas.labs.overthewire.org/upload/<file>.php`  
   → Password displayed.  

---

## Learnings and Recommendations  

### Key Learnings  
- **Client-side checks are meaningless** — always validate server-side.  
- **MIME type spoofing** is trivial if not verified with file signatures.  
- **Execution in upload directories = RCE** if PHP is parsed.  
- **Random filenames help**, but **content validation is mandatory**.  

### Recommendations  

| **Control** | **Implementation** |
|-----------|---------------------|
| **MIME Validation** | Use `finfo_file()` to check magic bytes |
| **Content Scanning** | Reject non-image files; use `getimagesize()` |
| **Execution Disable** | `.htaccess`: `php_flag engine off` |
| **File Naming** | Use UUIDs: `uuid4().'.jpg'` |
| **Storage Location** | Outside web root + serve via script |

---

## Conclusion  

Natas Level 12 effectively demonstrates the **dangers of insecure file uploads** when relying on extension checks alone. By combining **payload crafting**, **request tampering**, and **server misconfiguration**, full code execution was achieved in under 5 minutes.  

This vulnerability underscores a **common real-world flaw** seen in legacy systems and misconfigured CMS plugins. Progressing to higher Natas levels will introduce **filter bypasses**, **RCE chains**, and **privilege escalation** — but the core lesson remains:  

> **Never trust user-supplied filenames or content without rigorous server-side validation.**  

Regular **VAPT**, **secure coding training**, and **automated SAST/DAST** in CI/CD pipelines are essential to prevent such critical flaws in production.  
