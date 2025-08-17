# 🛡️ PicoCTF Lab Walkthrough – Secrets

## 📌 Challenge Info

* **Category**: Web Exploitation
* **Difficulty**: Easy

---

## 📝 Challenge Description

Exploit path traversal and directory exploration to locate a hidden flag.

---

## 🔍 Initial Recon

* **Files provided**: None
* **Services/Ports**: Web page with `/secret/` endpoint
* **Hints given**: "You are close to the flag."

---

## 🛠️ Tools & Commands Used

| Tool / Command       | Purpose                             |
| -------------------- | ----------------------------------- |
| Browser DevTools     | Inspect source code and directories |
| Manual path guessing | Explore hidden directories          |

---

## 🧠 Step-by-Step Solution

1. Found image at `/secret/assets/ugf2iyg.jpg` on index.
2. Navigated to `/secret/`, which hinted proximity to flag.
3. Explored `/secret/hidden/`, revealing a login page.
4. Inspected login page → discovered `/superhidden/file.css`.
5. Navigated to `/superhidden/` → flag hidden in white background of page.

---

## 🧾 Flag

picoCTF{\[flag\]}

---

## 📚 Learning Outcomes

* Path traversal and directory exposure can reveal hidden files.
* Source code inspection is crucial in web exploitation.
