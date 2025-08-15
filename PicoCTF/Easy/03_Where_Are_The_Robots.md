# 🛡️ PicoCTF Lab Walkthrough – Where Are the Robots

## 📌 Challenge Info
- **Category**: Web Exploitation
- **Points**: Not specified
- **Difficulty**: Easy
- **Challenge Link**: N/A

---

## 📝 Challenge Description
A misconfigured `robots.txt` file exposed a hidden HTML page containing the flag.

---

## 🔍 Initial Recon
- **Files provided**: None
- **Services/Ports**: Web server
- **Hints given**: None

---

## 🛠️ Tools & Commands Used
| Tool / Command | Purpose |
|----------------|---------|
| Browser | View `robots.txt` |
| Direct URL access | Retrieve hidden file |

---

## 🧠 Step-by-Step Solution
1. Navigated to:
https://jupiter.challenges.picoctf.org/problem/56830/robots.txt

2. Found:
Disallow: /1bb4c.html

3. Visited:
https://jupiter.challenges.picoctf.org/problem/56830/1bb4c.html

4. Found flag:
picoCTF{ca1cu1at1ng_Mach1n3s_1bb4c}

---

## 🧾 Flag
picoCTF{ca1cu1at1ng_Mach1n3s_1bb4c}

---

## 📚 Learning Outcomes
- `robots.txt` can reveal sensitive endpoints.
- Always review `robots.txt` during recon.

---

## 🔗 References
- [robots.txt Specification](https://www.robotstxt.org/)
