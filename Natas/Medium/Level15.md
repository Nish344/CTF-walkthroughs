# 🏴󠁡󠁦󠁷󠁡󠁲󠁿**Natas Challenge – Level 15**

**Prepared by:** Nishanth Antony  
**Date:** November 09, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation (SQL Injection)  
**Platform:** Over The Wire  

---

## **Executive Summary**
This walkthrough documents the assessment of **Natas Level 15**, a medium-difficulty challenge focused on **blind SQL injection** exploitation using automated tools. The objective was to retrieve the password for **Natas Level 16** by exploiting a vulnerable `username` GET parameter on the `index.php?debug` page. The assessment confirmed a **time-based / boolean-based blind SQL injection** vulnerability due to unsanitized input being concatenated into a backend query. Using **sqlmap**, the entire `users` table was dumped, revealing the credentials for `natas16`. This vulnerability was rated **Critical Severity** due to full database compromise.

**Key Findings:**
- Blind SQL injection in `username` parameter (`index.php?debug`).
- Response string **"This user exists"** used as boolean indicator.
- No input sanitization or parameterized queries.
- Successful automated exploitation via **sqlmap** with `--dump`.

**Recommendations:**
- Use **prepared statements / parameterized queries**.
- Implement **input validation** and **allowlisting**.
- Remove debug modes in production.
- Deploy **WAF** with SQLi rules.

---

## **Introduction**

### **Background**
Natas is an educational web security challenge series hosted by OverTheWire. Level 15 introduces **blind SQL injection**, where no direct error messages or data are leaked, but logical responses confirm query outcomes.

### **Objective**
Exploit blind SQL injection to extract the password for **natas16** from the database.

### **Scope**
- **Target:** `http://natas15.natas.labs.overthewire.org/index.php?debug`
- **Assessment Type:** Black-box (with debug mode enabled)
- **Tool Focus:** Automated exploitation using **sqlmap**

---

## **Methodology**
The assessment followed **OWASP Testing Guide** and **PTES** standards. Primary tool: **sqlmap**.

### **Step 1: Reconnaissance**
- Accessed `index.php?debug` → observed form with `username` field.
- Responses:
  - Valid user → **"This user exists."**
  - Invalid user → **"This user doesn't exist."**
- Confirmed **boolean-based blind SQL injection**.

### **Step 2: Manual Confirmation (Optional)**
- Payload: `natas16' AND 1=1-- -` → "This user exists."
- Payload: `natas16' AND 1=2-- -` → "This user doesn't exist."
→ Verified injection point.

### **Step 3: Automated Exploitation with sqlmap**
Executed the following command:

```bash
sqlmap -u "http://natas15.natas.labs.overthewire.org/index.php?debug" \
  --string="This user exists" \
  --auth-type=Basic \
  --auth-cred="natas15:SdqIqBsFcz3yotlNYErZSZwblkm0lrvx" \
  --data="username=natas16" \
  --level=5 --risk=3 \
  -D natas15 -T users -C username,password --dump
```

**Command Breakdown:**
| Option                        | Purpose |
|------------------------------|--------|
| `-u`                          | Target URL |
| `--string="This user exists"` | Boolean true indicator |
| `--auth-type/cred`            | Basic auth (natas15 credentials) |
| `--data`                      | Force POST data (though GET in this case) |
| `--level=5 --risk=3`          | Aggressive testing (includes advanced payloads) |
| `-D -T -C --dump`             | Dump `username` and `password` from `users` table |

### **Step 4: Result**
sqlmap successfully:
- Identified **MySQL** backend
- Confirmed **blind boolean-based** injection
- Extracted full `users` table → revealed **natas16** password

---

## **Findings**

### **Vulnerability Details**

| **Vulnerability**     | **Type**               | **CWE** | **Severity** | **CVSS Score** |
|-----------------------|------------------------|--------|--------------|----------------|
| Blind SQL Injection   | Improper Neutralization | CWE-89 | Critical     | 9.8            |

- **Proof of Concept:** Full database dump via sqlmap
- **Impact:** Complete confidentiality breach — all user credentials exposed

---

## **Solution and Exploitation**

**Successful sqlmap Output :**  

<img width="327" height="104" alt="image" src="https://github.com/user-attachments/assets/4d253ad1-00fd-46fd-ae26-934d5f5a8373" />


> **Extracted Artifact:** Password for natas16 (redacted in report)

---

## **Learnings and Recommendations**

### **Key Learnings**
- **Blind SQLi** requires logical inference — automated tools excel here.
- Debug modes (`?debug`) dramatically increase attack surface.
- **sqlmap** is extremely effective when boolean/time-based responses exist.
- Simple string comparison leaks query results.

### **Recommendations**

| **Timeline** | **Action** |
|--------------|-----------|
| **Short-Term** | Remove `debug` parameter in production |
| | Replace all queries with **parameterized statements** |
| **Long-Term** | 
- Use **ORMs** (PDO, Hibernate) with automatic escaping
- Implement **database access controls** and auditing
- Deploy **WAF + SQLi detection** (ModSecurity, Cloudflare)

**Mitigation Controls:**
- **Input allowlisting** (alphanumeric only)
- **Least privilege DB user**
- **Error handling** (never leak query logic)

---

## **Conclusion**
**Natas Level 15** effectively demonstrates **real-world blind SQL injection** and the power of **automated exploitation tools** like **sqlmap**. Even without direct data output, a single boolean response string ("This user exists") was sufficient to extract the entire user database.

**Core Lesson:**  
> **Never concatenate user input into SQL — even in "internal" or debug endpoints.**

This remains one of the **most common and devastating** vulnerabilities in web applications. **Parameterized queries are the gold standard** — and tools like sqlmap show why prevention is mandatory.

For production systems, **secure coding**, **defense-in-depth**, and **regular automated scanning** are essential.
