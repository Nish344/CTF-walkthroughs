# Bricks Heist – Hack The Box (HTB) Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** August 12, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation / Post-Exploitation / Threat Intelligence  
**Platform:** [Hack The Box](https://www.hackthebox.com)  

---

## 1. Reconnaissance Steps

**Objective:** Identify open services and possible points of attack.

- **Command:**
nmap -A 10.201.20.107

text
- **Findings:**
- **Port 80:** Python HTTP server
- **Port 443:** Apache hosting **WordPress 6.5**
- **Port 3306:** MySQL (authentication required)
- `robots.txt` referenced `/wp-admin/` → confirmed WordPress instance.
- The WordPress site became the primary target for further enumeration.

---

## 2. Exploitation Process

### Step 1 – WordPress Enumeration
- **Tool:**
```bash
wpscan --url https://10.201.20.107 --disable-tls-checks
```

text
- **Result:** Detected outdated **WordPress theme** with public exploit: **CVE-2024-25600**.

### Step 2 – Exploiting CVE-2024-25600
- Searched exploit databases and found a Python script to abuse the vulnerability.
- **Execution:** Ran the exploit to gain a reverse shell.
- **Challenge:** Initial shell was **unstable** (limited commands).

---

## 3. Proof of Concept (PoC)

- Successfully retrieved the **first flag** using:
```bash
cat 650c844110baced87e1606453b93f22a.txt
```

text
- Flag content confirmed exploitation success.

---

## 4. Privilege Escalation / Post-Exploitation

### Step 3 – Shell Stabilization
- Verified bash availability:
```bash
bash --version
```

text
- Used bash to upgrade the shell for stable command execution.

### Step 4 – Service Enumeration
- Checked for unusual services:
```bash
systemctl | grep running
```

text
- Found **TRYHACK3M** service running → potential CTF-related clue.

### Step 5 – Investigating Cryptominer Activity
- Navigated to suspicious directory:
```bash
cd /lib/NetworkManager
ls -la
cat inet.conf
```

text
- Discovered **obfuscated wallet addresses** in miner logs.

### Step 6 – Decoding Wallet Info
- Used **CyberChef** to decode hex string → revealed **two BTC wallet addresses**.
- Verified one valid wallet via blockchain explorer.

### Step 7 – Threat Intel
- Conducted OSINT search on wallet → linked to **LockBit** ransomware group.

---

## 5. Mitigation Recommendations

- **Update WordPress themes/plugins** regularly → patch known CVEs.
- Restrict direct file access → move sensitive files outside web root.
- Remove **unauthorized services** like cryptominers and audit service configs.
- Monitor system with IDS/IPS for anomalous shells or connections.
- **Secure logging**:
- Avoid storing sensitive info (wallet IDs) unencrypted.
- Harden all entry points:
- Disable unused ports/services.
- Apply **Principle of Least Privilege** to apps and accounts.

---

## 6. Lessons Learned

- Outdated CMS components are high-risk targets.
- A stable shell is crucial for reliable post-exploitation work.
- Even after exploitation → valuable intel can be gathered for **threat attribution**.
- Unauthorized services often indicate compromise persistence.

---

## 7. Skills Practiced

- **Service Enumeration:** `nmap`, `wpscan`
- **Exploit Development/Use:** Public CVE exploitation (Python script)
- **Shell Management:** Stabilizing a reverse shell with bash
- **Linux Post-Exploitation:** `systemctl`, file/log analysis
- **Cyber Threat Intel:** Using OSINT and blockchain tools for attribution
- **Data Decoding:** CyberChef for de-obfuscation

---
