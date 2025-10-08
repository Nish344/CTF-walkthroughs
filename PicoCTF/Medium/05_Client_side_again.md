# 🛡️ PicoCTF Lab Walkthrough – Client-side-again

## 📌 Challenge Info

* **Category**: Web Exploitation
* **Difficulty**: Medium

---

## 📝 Challenge Description

Deobfuscate a JavaScript file to reconstruct the flag by satisfying client-side password validation logic.

---

## 🔍 Initial Recon

* **Files provided**: Obfuscated JavaScript file
* **Services/Ports**: Web app with client-side password validation
* **Hints given**: Analyze JavaScript obfuscation, array rotation, and substring checks

---

## 🛠️ Tools & Commands Used

| Tool / Command      | Purpose                                              |
| ------------------- | ---------------------------------------------------- |
| Browser DevTools    | Inspect webpage source and JavaScript code           |
| JavaScript Console  | Test and debug deobfuscated code                    |
| Text Editor         | Analyze and rewrite JavaScript logic                 |

---

## 🧠 Step-by-Step Solution

1. **Source Code Analysis**

   * Inspected the webpage’s source code, identifying an obfuscated JavaScript file responsible for password verification.
   * Found an array `_0x5a46` with strings and a rotation function that shifted the array 435 times.

   ```javascript:disable-run
   var _0x5a46 = ['f49bf}', '_again_e', 'this', 'Password Verified', 'Incorrect password', 'getElementById', 'value', 'substring', 'picoCTF{', 'not_this'];
   (function(array, times){
       var rotate = function(n){
           while(--n){ array.push(array.shift()); }
       };
       rotate(++times);
   })(_0x5a46, 0x1b3);
   ```

2. **Deobfuscation**

   * Analyzed the array rotation logic: the array length was 10, so rotating 435 times was equivalent to 5 left rotations (435 % 10 = 5).
   * Reconstructed the array after rotation:

   ```javascript
   ['getElementById', 'value', 'substring', 'picoCTF{', 'not_this', 'f49bf}', '_again_e', 'this', 'Password Verified', 'Incorrect password']
   ```

3. **Function Deobfuscation**

   * The `_0x4b5b` function mapped indices to array elements:

   ```javascript
   var _0x4b5b = function(_0x2d8f05, _0x4b81bb) {
       _0x2d8f05 = _0x2d8f05 - 0x0;
       return _0x5a46[_0x2d8f05];
   };
   ```

   * Mapped indices to strings (e.g., `_0x4b5b('0x3')` → `picoCTF{`).

4. **Rewriting the Verify Function**

   * Deobfuscated the `verify` function:

   ```javascript
   function verify() {
       checkpass = document.getElementById('pass').value;
       split = 4;
       if (checkpass.substring(0, 8) == 'picoCTF{') {
           if (checkpass.substring(7, 9) == '{n') {
               if (checkpass.substring(8, 16) == 'not_this') {
                   if (checkpass.substring(3, 6) == 'oCT') {
                       if (checkpass.substring(24, 30) == 'f49bf}') {
                           if (checkpass.substring(6, 11) == 'F{not') {
                               if (checkpass.substring(16, 24) == '_again_e') {
                                   if (checkpass.substring(12, 16) == 'this') {
                                       alert('Password Verified');
                                   }
                               }
                           }
                       }
                   }
               }
           }
       } else {
           alert('Incorrect password');
       }
   }
   ```

5. **Flag Reconstruction**

   * Reconstructed the flag by satisfying all substring conditions:

   | Position       | Substring         | Must Equal   |
   |----------------|-------------------|--------------|
   | 0–8            | substring(0,8)    | picoCTF{     |
   | 3–6            | substring(3,6)    | oCT          |
   | 6–11           | substring(6,11)   | F{not        |
   | 7–9            | substring(7,9)    | {n           |
   | 8–16           | substring(8,16)   | not_this     |
   | 12–16          | substring(12,16)  | this         |
   | 16–24          | substring(16,24)  | _again_e     |
   | 24–30          | substring(24,30)  | f49bf}       |

   * Character-by-character reconstruction:

   ```
   p (0) i (1) c (2) o (3) C (4) T (5) F (6) { (7) n (8) o (9) t (10) _ (11) t (12) h (13) i (14) s (15) _ (16) a (17) g (18) a (19) i (20) n (21) _ (22) e (23) f (24) 4 (25) 9 (26) b (27) f (28) } (29)
   ```

   * Initial reconstructed flag: `picoCTF{not_this_again_e_f49bf}`.
   * Noted a discrepancy: the actual flag was `picoCTF{[REDACTED]}` (corrected a typo in reconstruction, missing an underscore between `again` and `e`).

6. **Flag Retrieval**

   * Submitted the corrected flag after recognizing the typo in reconstruction.

---

## 🧾 Flag

picoCTF{[REDACTED]}

---

## 📚 Learning Outcomes

* Client-side validation is insecure, as attackers can reverse-engineer logic to extract sensitive data like flags.
* JavaScript obfuscation, while complicating analysis, can be defeated through systematic deobfuscation and array reconstruction.
* Typos in flag reconstruction highlight the importance of verifying results against expected formats.

---

## 🔒 Recommendations

1. **Secure WebAssembly Usage**
   * Avoid embedding sensitive data in WebAssembly (WASM) files, as they can be inspected via network traffic.
   * Obfuscate or encrypt critical WASM components to prevent easy analysis.

2. **Robust Server-Side Validation**
   * Move authentication logic, such as password verification, to the server side to prevent client-side bypasses.
   * Use secure session management instead of relying on easily manipulated client-side logic.

3. **Avoid Client-Side Obfuscation**
   * Client-side JavaScript obfuscation provides minimal security, as attackers can deobfuscate code with effort.
   * Implement server-side checks and cryptographic protections for sensitive data.

4. **Input Sanitization**
   * Validate and sanitize all user inputs to prevent manipulation of client-side logic.
   * Use allowlists for expected values instead of relying on specific strings.

5. **Error Handling**
   * Ensure consistent flag formats to avoid confusion from typos or misconfigurations (e.g., `_again_e` vs. `_againef49bf`).
