# 🟩 CyberHeroes – Try Hack Me (THM) Walkthrough Report  

**Prepared by:** Nishanth Antony  
**Date:** September 17, 2025  
**Difficulty:** Easy  
**Category:** Client-Side Exploitation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify client-side vulnerabilities in the web application.
- **Commands Used:**  
  - Browser inspection tools to view page source code.
- **Findings:**
  - The web page at `http://<target_ip>` contains a login form.
  - Source code inspection revealed a JavaScript function `authenticate()` handling login logic client-side.
  - The function checks for username `"h3ck3rBoi"` and password equal to the reverse of `"54321@terceSrepuS"` (i.e., `"SuperSecret@12345"`).
  - Successful authentication triggers an AJAX GET request to a specific TXT file path containing the flag.

---

## 2. Exploitation Process

### Step 1 – Source Code Analysis
- Inspected the HTML source code in the browser.
- Identified the `authenticate()` function:
  ```javascript
  function authenticate() {
    a = document.getElementById('uname')
    b = document.getElementById('pass')
    const RevereString = str => [...str].reverse().join('');
    if (a.value=="h3ck3rBoi" & b.value==RevereString("54321@terceSrepuS")) { 
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("flag").innerHTML = this.responseText ;
          document.getElementById("todel").innerHTML = "";
          document.getElementById("rm").remove() ;
        }
      };
      xhttp.open("GET", "RandomLo0o0o0o0o0o0o0o0o0o0gpath12345_Flag_"+a.value+"_"+b.value+".txt", true);
      xhttp.send();
    }
    else {
      alert("Incorrect Password, try again.. you got this hacker !")
    }
  }
  ```
- Reversed the string `"54321@terceSrepuS"` to obtain the password `"SuperSecret@12345"`.

### Step 2 – Credential Testing
- Entered username: `h3ck3rBoi`
- Entered password: `SuperSecret@12345`
- Submitted the form, triggering the AJAX request to load the flag from the TXT file.
- The flag was displayed on the page.

---

## 3. Proof of Concept (PoC)

- **Client-Side Login Bypass:**  
  - Access `http://<target_ip>` in a browser.
  - View source code to extract hardcoded credentials.
  - Enter username `h3ck3rBoi` and password `SuperSecret@12345`.
  - The application loads and displays the flag via AJAX.

---

## 4. Privilege Escalation

- Not applicable; the vulnerability is client-side and directly exposes the flag without server-side escalation.

---

## 5. Mitigation Recommendations

- **Server-Side Authentication:**  
  - Move all authentication logic to the server-side to prevent exposure of credentials in client-side code.
  - Use secure hashing (e.g., bcrypt) for passwords and validate via API calls.
- **Obfuscation Limitations:**  
  - Avoid relying on client-side checks or obfuscation (e.g., string reversal) as they can be easily bypassed.
- **Resource Protection:**  
  - Restrict access to sensitive files (e.g., flag TXT files) with server-side authentication or IP whitelisting.
  - Use secure random file naming and directory indexing prevention.
- **Code Review:**  
  - Conduct regular code audits to identify and remove hardcoded secrets.
  - Implement content security policies (CSP) to mitigate XSS risks.
- **General Security:**  
  - Use HTTPS to encrypt traffic and monitor for client-side tampering.

---

## 6. Lessons Learned

- **Client-Side Security Risks:** Hardcoded credentials in JavaScript are easily discoverable and reversible.
- **Obfuscation Ineffectiveness:** Simple techniques like string reversal provide no real security against inspection.
- **AJAX Vulnerabilities:** Exposed endpoints can leak sensitive data if not protected server-side.
- **Browser Tools Exploitation:** Source code viewing enables quick identification of flaws.

---

## 7. Skills Practiced

- Web source code inspection
- JavaScript analysis and string manipulation
- Client-side authentication bypassing
- Secure reporting and mitigation strategies
