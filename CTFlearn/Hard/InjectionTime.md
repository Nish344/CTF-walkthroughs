# CTFlearn Web Exploitation Labs – Detailed Walkthrough

**Prepared by:** Anonymous  
**Date:** August 12, 2025  
**Platform:** [CTFlearn](https://ctflearn.com)  
**Category:** Web Exploitation  
**Labs Covered:** Injection Time (Hard)

---

## Lab 1: Injection Time (Hard)

### 1. Reconnaissance Steps

- **Goal:** Find out how the website works and look for places to attack.
- **Visited site:** `https://web.ctflearn.com/web8/?id=1`
- **Observation:** The site uses a URL parameter `id` to show data.
- **Tried changing `id` values** (e.g., `id=2`, `id=3`) to see how the response changed.
- **Conclusion:** The `id` parameter is being used by the server to fetch data from a database.

### 2. Exploitation Process

- **Suspected** a SQL Injection vulnerability (where you can "trick" the site to run extra database commands).
- **Decided to use:** `sqlmap`, an automated tool for testing and exploiting SQL injection.
- **Ran this command:**

```bash
sqlmap -u "https://web.ctflearn.com/web8/?id=1" --batch --risk=3 --level=5 --dump
```

text
- **What this does:** Tries lots of different ways to see if it can get the site's database to reveal information.

### 3. Proof of Concept (PoC)

- **Result:** sqlmap found the vulnerability, grabbed the database content, and printed the flag (something like `picoCTF{...}`).
- **Confirmed** by submitting the flag — challenge solved!

### 4. Privilege Escalation Techniques

- **Not applicable** for this web app: the main goal was to get sensitive data (the flag) directly from the database, not escalate to higher user permissions.

### 5. Mitigation Recommendations

- **Always check and clean up user input:** Use prepared statements in SQL; never just stick user data directly into database queries.
- **Limit what users can send:** For example, only allow numbers in an `id` field.
- **Use security tools:** Scan for vulnerabilities before releasing your site.
- **Monitor for weird activity:** Alerts and logs can help spot misuse early.

### 6. Lessons Learned & Skills Practiced

- How important input validation is to keep data safe.
- How to spot, test, and exploit SQL injection.
- Using sqlmap and understanding web parameters.
- Documenting technical findings clearly.
