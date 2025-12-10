# 🟩Utech – Try Hack Me (THM) Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** August 14, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open ports, running services, and information leaks.
- **Commands Used:**  
rustscan <target_ip> -b 1000 -r 0-65535 -t 5000 -- -A
nmap -A <target_ip>

text
- **Findings:**
- File Transfer (FTP), Secure Shell (SSH), Node.js REST API (web, port 8081), and Apache (web, port 31331).
- Web server index and sitemap revealed likely hidden files and application routes.
- Source code and JavaScript files pointed to `/ping` and `/auth` API endpoints.

---

## 2. Exploitation Process

### Step 1 – Web Application Enumeration
- Explored web content and found a `/ping` endpoint accepting an `ip` parameter.
- Inspected related JavaScript files for API usage and potential security flaws.

### Step 2 – Command Injection Vulnerability
- **Tested:** Sending input with a command separator (e.g., `127.0.0.1;ls`) to `/ping?ip=...`.
- **Result:** Arbitrary commands executed by the API, allowing remote commands to be run on the server.
- **Extracted:** Discovered and dumped an SQLite database file containing user and password hash.

### Step 3 – Cracking Credentials
- Saved the hash to a file.  
- Used a popular wordlist to crack it with `john`:
john --format=raw-md5 <hashfile> --wordlist=<wordlist>

text
- **Result:** Recovered a weak password for the `r00t` account.

### Step 4 – System Access via SSH
- Logged in as `r00t` using the cracked password over SSH.
- Enumerated system privileges.

### Step 5 – Privilege Escalation with Docker Group
- Confirmed user belonged to the dangerous `docker` group (can run containers with root privileges).
- Identified a ready-to-use `bash` image.
- **Exploit:** Mounted server root inside a Docker container:
docker run -v /:/mnt --rm -it bash chroot /mnt sh

text
- **Gained:** Full root shell inside the host system.

### Step 6 – Flag Extraction
- As root, accessed and extracted the target flag (e.g., in `/root/`).

---

## 3. Proof of Concept (PoC)

- **Web Command Injection:**  
curl "http://<target_ip>:8081/ping?ip=127.0.0.1;ls"

text
Proved arbitrary code execution.
- **Password Hash Cracking:**  
Cracked database hash with `john` or `hashcat` and public wordlist.
- **Docker Privilege Escalation:**  
Ran a Docker container with mounted root filesystem for root shell.

---

## 4. Privilege Escalation

- Used **Docker group membership** to escalate from limited user to full root on the host system.
- Mounted and chrooted to the host's root filesystem for unrestricted access.

---

## 5. Mitigation Recommendations

- **API Input Validation:**  
- Sanitize all user input before passing to system commands in REST APIs.
- Use safe libraries, parameterization, or whitelists for executing system-level code.
- **Credential Security:**  
- Store passwords using strong hashing (e.g., bcrypt).
- Enforce strong, unique passwords and lock out after repeated failures.
- Enable multi-factor authentication for SSH access.
- **Docker Hardening:**  
- Limit Docker group membership to trusted admins only.
- Prohibit containers from mounting sensitive host folders.
- **Web Content Management:**  
- Remove unnecessary files (e.g., sitemaps, robots.txt) and restrict access to sensitive scripts/routes.
- **Patch and Monitor:**  
- Regularly update all system/server components and dependencies.
- Enable logging/alerting for suspicious API or Docker activity.

---

## 6. Lessons Learned

- **Command injection** in web APIs can lead to full system compromise.
- **Weak password practices** make brute-force and hash cracking trivial for attackers.
- Dangerous **default group memberships** (like Docker) can grant root access when chained with other flaws.
- Sensitive information in web directories and JavaScript can guide attackers in real-world scenarios.

---

## 7. Skills Practiced

- Network and service scanning (`rustscan`, `nmap`)
- Web application enumeration and analysis
- Exploiting command injection
- Credential/Password hash cracking
- SSH exploitation
- Docker-based privilege escalation
- Secure reporting and mitigation strategy

---
