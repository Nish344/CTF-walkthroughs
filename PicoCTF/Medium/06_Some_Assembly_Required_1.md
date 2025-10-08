# 🛡️ PicoCTF Lab Walkthrough – Some Assembly Required 1

## 📌 Challenge Info

* **Category**: Web Exploitation
* **Difficulty**: Medium

---

## 📝 Challenge Description

Retrieve a flag hidden in a WebAssembly (WASM) module loaded by a web application.

---

## 🔍 Initial Recon

* **Files provided**: None
* **Services/Ports**: Web app with WebAssembly module
* **Hints given**: Inspect webpage source and network traffic

---

## 🛠️ Tools & Commands Used

| Tool / Command      | Purpose                                              |
| ------------------- | ---------------------------------------------------- |
| Browser DevTools    | Inspect source code and monitor network traffic      |

---

## 🧠 Step-by-Step Solution

1. **Initial Reconnaissance**

   * The challenge provided no explicit description, prompting an immediate inspection of the webpage’s source code.
   * The source code revealed a JavaScript file loading a WebAssembly module. The JavaScript was obfuscated, and no direct reference to the WASM file’s location or contents was provided.
   * This suggested that the flag might be embedded within the WASM module or its associated network requests.

2. **Network Traffic Analysis**

   * Using the browser’s Developer Tools, the network tab was monitored to capture all resources loaded by the webpage.
   * Reloading the page revealed a dedicated “WASM” tab in the network panel, indicating that a WebAssembly file was being fetched.
   * Inspecting the WASM file’s response showed the flag embedded directly in the response body.

3. **Flag Retrieval**

   * The flag was extracted from the WASM file’s network response, requiring no further decompilation or analysis of the WebAssembly module itself.
   * The flag format matched the expected `picoCTF{...}` pattern.

---

## 🧾 Flag

picoCTF{[REDACTED]}

---

## 📚 Learning Outcomes

* WebAssembly modules can contain sensitive data if not properly secured, and the flag was exposed in the network response.
* Developers may overlook WASM files when securing web applications, assuming their binary nature obscures content.
* Network traffic analysis is a powerful method for identifying hidden data in non-standard web resources.

---

## 🔒 Recommendations

1. **Secure WebAssembly Usage**
   * Avoid embedding sensitive data in WebAssembly files, as they can be inspected via network traffic.
   * Obfuscate or encrypt critical WASM components to prevent easy extraction.

2. **Robust Server-Side Validation**
   * Ensure sensitive data is served only after server-side authentication, not directly in client-side resources.
   * Use secure transmission protocols to protect WASM content.

3. **Input Sanitization**
   * Validate and sanitize all client requests to prevent unauthorized access to WASM resources.
   * Restrict access to WASM files based on authenticated sessions.
