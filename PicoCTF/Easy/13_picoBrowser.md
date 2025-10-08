# 🛡️ PicoCTF Lab Walkthrough – picoBrowser

## 📌 Challenge Info

* **Category**: Web Exploitation
* **Difficulty**: Easy

---

## 📝 Challenge Description

Retrieve a flag by manipulating the HTTP User-Agent header to mimic a specific browser.

---

## 🔍 Initial Recon

* **Files provided**: None
* **Services/Ports**: Web app with User-Agent-based access control
* **Hints given**: Manipulate HTTP headers to access restricted content

---

## 🛠️ Tools & Commands Used

| Tool / Command      | Purpose                                              |
| ------------------- | ---------------------------------------------------- |
| Burp Suite          | Intercept and modify HTTP requests                   |
| Browser DevTools    | Inspect initial webpage response                    |

---

## 🧠 Step-by-Step Solution

1. **Initial Reconnaissance**

   * The challenge implied that the server checked the User-Agent header to determine access to restricted content.
   * The webpage was loaded, and the initial response was inspected using Burp Suite.

2. **User-Agent Manipulation**

   * Using Burp Suite’s Proxy feature, the HTTP request was intercepted during a page load.
   * The User-Agent header was modified to `picoBrowser`, hypothesizing that the server expected a specific, custom browser identifier.
   * The modified request was forwarded, resulting in a redirect to a new page.

   ```
   GET /flag HTTP/1.1
   Host: jupiter.challenges.picoctf.org
   Cookie: _ga=GA1.2.179520224.175365076; _gid=GA1.2.97541682.175365076; cf_clearance=
   User-Agent: picoBrowser
   Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
   Sec-Fetch-Site: same-origin
   Sec-Fetch-Mode: navigate
   Sec-Fetch-User: ?1
   Sec-Fetch-Dest: document
   Referer: https://jupiter.challenges.picoctf.org/problem/5052/?flag
   Accept-Encoding: gzip, deflate, br
   Priority: u=0, i
   Connection: keep-alive
   ```

3. **Iterative Exploitation**

   * The redirected page was intercepted again using Burp Suite.
   * The User-Agent was set to `picoBrowser` once more, and the request was forwarded.
   * This action revealed the flag in the server’s response.

---

## 🧾 Flag

picoCTF{[REDACTED]}

---

## 📚 Learning Outcomes

* Servers often use User-Agent headers to enforce access control, but this can be bypassed by spoofing the expected value.
* The challenge required persistence, as the server checked the User-Agent across multiple requests.
* Burp Suite’s ability to intercept and modify HTTP requests was critical for success.

---

## 🔒 Recommendations

1. **Robust Server-Side Validation**
   * Move access control logic to the server side, validating User-Agent alongside other factors like session tokens.
   * Avoid relying solely on client-provided headers for authentication.

2. **Input Sanitization**
   * Validate and sanitize User-Agent headers to prevent spoofing-based attacks.
   * Use allowlists for expected browser identifiers.

3. **Secure Redirection**
   * Implement secure redirection logic that doesn’t rely on client-side headers for validation.
   * Use server-side checks to ensure authorized access at each step.
