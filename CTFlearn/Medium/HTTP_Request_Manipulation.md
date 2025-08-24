# Vulnerability Assessment and Penetration Testing (VAPT) Report – HTTP Request Manipulation

**Prepared by:** Nishanth Antony  
**Date:** August 24, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation  
**Platform:** CTFlearn  

---

## 1. Reconnaissance Steps  
**Objective:** Identify vulnerabilities in the web application and its request handling.  
**Commands Used:**  
- None (manual inspection via browser and Burp Suite).  

**Findings:**  
- Web application used a GET request: `GET /post.php?=1`.  
- Page source revealed a hidden HTML comment: `<!-- Username: admin, Password: secret -->`.  
- Hypothesized that a POST request with these credentials was required for authentication.  

---

## 2. Exploitation Process  
**Step 1 – Request Interception**  
- Intercepted the GET request to `post.php?=1` using Burp Suite’s Proxy module.  
- Inspected the response in browser Developer Tools (F12) to identify the hidden comment with credentials.  

**Step 2 – HTTP Method Manipulation**  
- Used Burp Suite’s Repeater module to craft a POST request:  
  - Changed method from GET to POST.  
  - Set URL to `post.php`.  
  - Added body: `username=admin&password=secret`.  

**Step 3 – Flag Retrieval**  
- Sent the POST request via Burp Suite.  
- Server responded with the flag in the picoCTF{...} format.  

---

## 3. Proof of Concept (PoC)  
- **HTTP POST Request:**  
  - Intercepted `GET /post.php?=1` and modified to:  
    ```http
    POST /post.php HTTP/1.1
    Host: web.ctflearn.com
    Content-Type: application/x-www-form-urlencoded
    
    username=admin&password=secret
    ```  
  - Response contained the flag.  

---

## 4. Privilege Escalation  
- Not applicable; challenge focused on HTTP request manipulation and flag retrieval.  

---

## 5. Mitigation Recommendations  
- **Secure Data Exposure:**  
  - Avoid embedding sensitive data (e.g., credentials) in HTML comments or client-side code.  
  - Use server-side storage for sensitive information.  
- **Request Validation:**  
  - Enforce server-side validation of HTTP methods (e.g., only allow POST for authentication).  
  - Reject unexpected methods with appropriate error codes.  
- **Session Management:**  
  - Implement secure session tokens (e.g., JWT, HttpOnly/Secure cookies) for authentication.  
- **Code Review:**  
  - Conduct regular audits to detect and remove sensitive data leaks in source code.  
- **Content Security Policy (CSP):**  
  - Use CSP headers to restrict client-side script execution and mitigate data exposure risks.  

---

## 6. Lessons Learned  
- **Data Leakage:** Hidden HTML comments can expose sensitive information like credentials.  
- **HTTP Method Misconfiguration:** Improper method handling (e.g., accepting GET instead of POST) enables exploitation.  
- **Request Manipulation:** Tools like Burp Suite are critical for testing and modifying HTTP requests.  

---

## 7. Skills Practiced  
- Web request interception and manipulation (Burp Suite)  
- Source code inspection (Developer Tools)  
- HTTP method exploitation  
- Secure reporting and mitigation strategies  
