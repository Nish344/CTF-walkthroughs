# 🛡️ PicoCTF Lab Walkthrough – Robots Sans

## 📌 Challenge Info

* **Category**: Web Exploitation
* **Difficulty**: Easy

---

## 📝 Challenge Description

Use robots.txt to find hidden resources and retrieve the flag.

---

## 🔍 Initial Recon

* **Files provided**: Website URL
* **Services/Ports**: HTTP
* **Hints given**: Robots.txt inspection suggested

---

## 🛠️ Tools & Commands Used

| Tool / Command | Purpose                   |
| -------------- | ------------------------- |
| Browser        | Access `/robots.txt`      |
| `base64 -d`    | Decode obfuscated strings |

---

## 🧠 Step-by-Step Solution

1. Accessed `/robots.txt` → found Base64 strings.
2. Decoded them:

   ```bash
   echo "ZmxhZzEudHh0" | base64 -d
   echo "anMvbXlmaWxlLnR4dA==" | base64 -d
   ```

   → Revealed `flag1.txt` and `js/myfile.txt`.
3. Navigated to `/js/myfile.txt` → found flag.

---

## 🧾 Flag

picoCTF{\[flag\]}

---

## 📚 Learning Outcomes

* Robots.txt can expose hidden paths.
* Base64 encoding is commonly used to obfuscate filenames.

