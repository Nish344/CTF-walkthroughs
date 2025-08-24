# Vulnerability Assessment and Penetration Testing (VAPT) Report – Noxtal

**Prepared by:** Nishanth Antony  
**Date:** August 24, 2025  
**Difficulty:** Easy  
**Category:** Client-Side Exploitation  
**Platform:** CTFlearn  

---

## 1. Reconnaissance Steps  
**Objective:** Identify website structure and potential client-side vulnerabilities.  
**Commands Used:**  
- None (manual inspection via browser and Chrome Developer Tools).  

**Findings:**  
- Blog website with multiple links: “Home,” “About,” “Cybersec Blog.”  
- “Cybersec Blog” link likely relevant due to challenge context.  
- No server-side vulnerabilities identified; focus shifted to client-side storage (cookies, local storage, session storage).  

---

## 2. Exploitation Process  
**Step 1 – Website Navigation**  
- Tested all website links to understand functionality.  
- Identified “Cybersec Blog” as the likely target for flag storage based on thematic relevance.  

**Step 2 – Client-Side Inspection**  
- Opened Chrome Developer Tools and navigated to the “Application” tab.  
- Inspected “Local Storage” for the website’s domain (https://web.ctflearn.com).  
- Found key-value pair containing the flag: `picoCTF{...}`.  

**Step 3 – Flag Retrieval**  
- Copied flag from local storage.  
- Verified other storage mechanisms (cookies, session storage) for completeness; no additional data found.  
- Submitted flag successfully.  

---

## 3. Proof of Concept (PoC)  
- **Local Storage Access:**  
  - Used Chrome Developer Tools > Application > Local Storage.  
  - Identified and extracted flag: `Flag{...}`.  

---

## 4. Privilege Escalation  
- Not applicable; challenge focused on client-side flag retrieval without privilege escalation.  

---

## 5. Mitigation Recommendations  
- **Secure Client-Side Storage:**  
  - Avoid storing sensitive data (e.g., flags) in local storage or cookies.  
  - Use server-side storage with proper authentication and encryption.  
- **Input Validation:**  
  - Sanitize and validate all inputs to prevent injection attacks, even if not exploited in this challenge.  
- **API Security:**  
  - Secure API endpoints with authentication and rate limiting to prevent unauthorized access.  
- **Developer Training:**  
  - Educate developers on secure coding practices to avoid client-side data exposure.  
  - Use static analysis tools to detect vulnerabilities during development.  
- **Monitoring and Logging:**  
  - Implement logging to detect suspicious client-side activities.  
  - Use intrusion detection systems to monitor for automated scans.  

---

## 6. Lessons Learned  
- **Client-Side Vulnerabilities:** Sensitive data stored in local storage is easily accessible to users.  
- **Browser Tools:** Familiarity with Developer Tools is critical for identifying client-side data leaks.  
- **Secure Design:** Avoid client-side storage for sensitive information to prevent trivial exploitation.  

---

## 7. Skills Practiced  
- Web navigation and enumeration  
- Client-side storage inspection (Chrome Developer Tools)  
- Understanding of local storage vulnerabilities  
- Secure reporting and mitigation strategies
