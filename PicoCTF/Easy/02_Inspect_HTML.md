# 🛡️ PicoCTF Lab Walkthrough – Inspect HTML

## 📌 Challenge Info
- **Category**: Web Exploitation
- **Points**: Not specified
- **Difficulty**: Easy
- **Challenge Link**: N/A

---

## 📝 Challenge Description
A webpage contained a flag inside an HTML comment, visible through source code inspection.

---

## 🔍 Initial Recon
- **Files provided**: None
- **Services/Ports**: Web server
- **Hints given**: None

---

## 🛠️ Tools & Commands Used
| Tool / Command | Purpose |
|----------------|---------|
| Browser "View Page Source" | Inspect HTML comments |

---

## 🧠 Step-by-Step Solution
1. Opened webpage.
2. Used **Ctrl+U** (View Page Source).
3. Found:
   ```html
   <!-- Flag: picoCTF{flag} -->
Extracted flag.

🧾 Flag
```text
picoCTF{flag}
```

📚 Learning Outcomes
- HTML comments can accidentally reveal sensitive data.
- Always review page source in web testing.

🔗 References
OWASP – Information Leakage

yaml
Copy
Edit
