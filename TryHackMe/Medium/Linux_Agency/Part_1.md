# Cybersecurity Report: Penetration Testing of Linux Agency CTF Environment

## Executive Summary

This report documents the penetration testing activities conducted on the TryHackMe (THM) Capture The Flag (CTF) challenge titled "Linux Agency." The challenge simulates a Linux-based environment with 30 levels (missions), each requiring the discovery of a flag to progress. As of the current assessment, the first 10 missions have been successfully completed. The testing began with authorized SSH access using provided credentials (user: agent47, password: 640509040147).

The primary objectives were to enumerate system resources, identify vulnerabilities in file permissions and configurations, exploit these to retrieve flags, and escalate privileges horizontally by switching users. No vertical privilege escalation (e.g., to root) was required for these missions.

Key findings include:
- Weaknesses in file placement, permissions, and visibility, allowing unauthorized access to sensitive data (flags).
- Reliance on default or predictable configurations for user authentication and file storage.
- Successful horizontal escalation via the `su` command using discovered flags as passwords.

Recommendations focus on hardening file permissions, implementing least-privilege principles, and enhancing monitoring. Skills practiced include Linux command-line proficiency, file enumeration techniques, and basic reconnaissance in a constrained environment.

This report is structured to provide a comprehensive overview of the reconnaissance, exploitation, proof-of-concept demonstrations, privilege escalation, mitigations, and lessons learned.

## Reconnaissance Steps

Reconnaissance involved initial access to the target machine and systematic enumeration of the file system, user directories, and running services. No external network scanning (e.g., Nmap) was performed, as the challenge assumes internal access via SSH. Instead, focus was on internal enumeration to identify services, files, and potential entry points for each mission.

1. **Initial Access and Service Identification**:
   - Connected to the target machine via SSH using `ssh agent47@<machine-ip>` with the password `640509040147`.
   - Upon login, the Message of the Day (MOTD) was displayed, which is a system-wide banner configurable in `/etc/motd`. This was inspected for initial clues.
   - Enumerated running services implicitly through user interactions, noting that SSH (port 22) was the primary access method. No additional ports or services were scanned, as the CTF is console-based.

2. **File System Enumeration per Mission**:
   - **Mission 1**: Inspected the MOTD during SSH login, revealing the flag directly. This highlights how MOTD can leak information if not sanitized.
   - **Mission 2**: Navigated to the current user's home directory (`cd ~`) and listed files (`ls`), identifying a plain-text file containing the flag.
   - **Mission 3**: Similar to Mission 2, used `ls` to identify a file, then previewed its contents mentally before reading.
   - **Mission 4**: Enumerated files with `ls`, noting a binary or non-readable file, prompting use of tools to extract strings.
   - **Mission 5**: Discovered a directory via `ls`; enumerated its contents to find the flag file.
   - **Mission 6**: Standard `ls` showed no files; used `ls -a` to reveal hidden files (those starting with `.`).
   - **Mission 7**: `ls -a` revealed a hidden directory; navigated into it (`cd .hidden_folder`) and enumerated contents.
   - **Mission 8**: Encountered permission issues in the working directory; enumerated absolute paths (`cd /home/mission7`) to access home directory files.
   - **Mission 9**: No local files found; performed system-wide search using `find / -user mission8 2>/dev/null` to locate files owned by the previous user, filtering errors for cleaner output.
   - **Mission 10**: Identified a large dictionary file (e.g., rockyou.txt or similar, with over 14 million entries); used `wc -l` to confirm size, then prepared for pattern-based searching.

These steps relied on basic Linux commands to map the environment without advanced tools, simulating insider threat reconnaissance.

## Exploitation Process

Exploitation focused on retrieving flags by leveraging misconfigurations in file storage and permissions. Each mission built on the previous, requiring horizontal movement between users. The process involved reading files without modifying the system, adhering to CTF rules.

- **Mission 1**: The flag was exploited directly from the MOTD, which is displayed on login. No additional commands were needed beyond observing the output.
- **Mission 2**: After switching users (see Privilege Escalation), navigated to home (`cd ~`) and listed files (`ls`). The flag file was readable due to default permissions allowing owner/group access.
- **Mission 3**: Identified the flag file via `ls`; read it with `cat flag.txt`, exploiting plain-text storage.
- **Mission 4**: The file appeared empty or binary; used `strings flag.bin` to extract printable strings, revealing the hidden flag embedded within non-text data.
- **Mission 5**: Enumerated a subdirectory (`ls subdirectory/`); read the flag file inside, exploiting nested storage without proper access controls.
- **Mission 6**: Hidden file not visible in standard listings; exploited with `ls -a` to reveal `.flag`, then `cat .flag`.
- **Mission 7**: Hidden directory found with `ls -a`; navigated (`cd .hidden/`) and read the flag, exploiting dot-prefixed concealment.
- **Mission 8**: Permission denied on relative paths due to directory restrictions; exploited by using absolute path (`cd /home/mission7`), then `ls` and `cat flag.txt`.
- **Mission 9**: System-wide file owned by previous user; exploited with `find / -user mission8 2>/dev/null`, locating `/flag.txt`, then `cat /flag.txt`.
- **Mission 10**: Large wordlist file; manual reading impractical, so exploited with `grep "mission10" /path/to/wordlist.txt`, filtering for the flag pattern.

These exploits demonstrate how simple enumeration can bypass basic obfuscation techniques in Linux environments.

## Proof of Concept (PoC)

Below are the exact commands and outputs (simulated based on provided details) for each mission, serving as reproducible PoCs.

- **Mission 1**:
  ```
  ssh agent47@<ip> -p 22
  Password: 640509040147
  [MOTD displays: mission1 flag]
  ```

- **Mission 2**:
  ```
  su mission1
  Password: mission1 flag
  cd ~
  ls
  # Output: flag.txt
  cat flag.txt
  # Output: mission2 flag
  ```

- **Mission 3**:
  ```
  su mission2
  Password: mission2 flag
  cd ~
  ls
  # Output: secret.txt
  cat secret.txt
  # Output: mission3 flag
  ```

- **Mission 4**:
  ```
  su mission3
  Password: mission3 flag
  cd ~
  ls
  # Output: binaryfile
  strings binaryfile
  # Output: mission4 flag (among other strings)
  ```

- **Mission 5**:
  ```
  su mission4
  Password: mission4 flag
  cd ~
  ls
  # Output: folder/
  ls folder/
  # Output: flag.txt
  cat folder/flag.txt
  # Output: mission5 flag
  ```

- **Mission 6**:
  ```
  su mission5
  Password: mission5 flag
  cd ~
  ls
  # Output: (empty)
  ls -a
  # Output: .flag
  cat .flag
  # Output: mission6 flag
  ```

- **Mission 7**:
  ```
  su mission6
  Password: mission6 flag
  cd ~
  ls -a
  # Output: .hidden_folder/
  cd .hidden_folder/
  ls
  # Output: flag.txt
  cat flag.txt
  # Output: mission7 flag
  ```

- **Mission 8**:
  ```
  su mission7
  Password: mission7 flag
  # Initial commands fail with "Permission denied"
  cd /home/mission7
  ls
  # Output: flag.txt
  cat flag.txt
  # Output: mission8 flag
  ```

- **Mission 9**:
  ```
  su mission8
  Password: mission8 flag
  cd ~
  ls -a
  # Output: (no flag)
  find / -user mission8 2>/dev/null
  # Output: /flag.txt (among others)
  cat /flag.txt
  # Output: mission9 flag
  ```

- **Mission 10**:
  ```
  su mission9
  Password: mission9 flag
  cd ~
  ls
  # Output: wordlist.txt
  wc -l wordlist.txt
  # Output: 14344391 wordlist.txt
  grep "mission10" wordlist.txt
  # Output: mission10 flag (filtered result)
  ```

## Privilege Escalation Techniques

Privilege escalation was horizontal, switching between non-privileged users via the `su` command. Each flag served as the password for the next user (e.g., `missionN` user).

- Technique: `su <next_user>` followed by entering the discovered flag as the password.
- This was repeated for each mission, exploiting weak password policies where flags (sensitive data) double as credentials.
- No kernel exploits, SUID binaries, or cron jobs were used; escalation relied on user misconfiguration.

## Mitigation Recommendations

To prevent similar exploits in production environments:

- **File Permissions and Visibility**: Use `chmod` and `chown` to restrict files to owner-only access (e.g., `chmod 600 flag.txt`). Avoid storing sensitive data in world-readable locations or MOTD.
- **Hidden Files/Directories**: Do not rely on dot-prefixing for security; implement ACLs (Access Control Lists) or SELinux for finer-grained controls.
- **Password Policies**: Enforce strong, unique passwords; avoid reusing data like flags as credentials. Implement multi-factor authentication for SSH.
- **File System Hardening**: Regularly audit file ownership with `find / -user <user>` and remove unnecessary files. Use tools like `tripwire` for integrity monitoring.
- **User Isolation**: Limit user home directories with `chroot` or containers (e.g., Docker) to prevent cross-user enumeration.
- **Logging and Monitoring**: Enable auditd to log file accesses and `su` attempts; review logs for anomalous behavior.
- **Least Privilege**: Run services as non-root users; apply principle of least privilege to all configurations.

## Lessons Learned & Skills Practiced

- **Lessons Learned**: This CTF emphasized that basic obfuscation (e.g., hidden files) is insufficient against determined attackers. It highlighted the importance of absolute paths in permission-troubled environments and the power of tools like `find` and `grep` for large-scale searches. Predictable patterns (e.g., flags as passwords) can lead to chained exploits.
- **Skills Practiced**:
  - Linux navigation and commands: `cd`, `ls (-a)`, `cat`, `strings`, `find`, `grep`, `wc`.
  - File enumeration and searching in constrained environments.
  - Horizontal privilege escalation via `su`.
  - Debugging permission issues with path specifications.
  - Pattern recognition in CTF scenarios, building persistence across levels.
