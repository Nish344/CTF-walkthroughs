# 🏴󠁡󠁦󠁷󠁡󠁲󠁿Natas Challenge - Level 11

Prepared by: Nishanth Antony  
Date: November 03, 2025  
Difficulty: Easy  
Category: Web Exploitation    
Platform: Over The Wire    

## Executive Summary
This walkthrough documents the assessment of Natas Level 11, a beginner-level web security challenge designed to demonstrate weak encryption vulnerabilities. The objective was to retrieve the password for Natas Level 12 by exploiting a XOR-based cookie encryption mechanism. The assessment identified a critical vulnerability where user preferences were stored in a cookie encrypted with a short, static XOR key ("eDWo") and base64-encoded, allowing decryption, modification, and re-encryption to enable the "showpassword" feature. This finding highlights the risks of using reversible encryption with hardcoded keys and the need for strong cryptographic practices. The vulnerability was rated as **High Severity** due to the direct exposure of authentication credentials.

Key Findings:
- Cookie encrypted with XOR using static key "eDWo" and base64-encoded.
- Original cookie ("HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=") decrypted to JSON: {"showpassword":"no","bgcolor":"#ffffff"}.
- Modified JSON to {"showpassword":"yes","bgcolor":"#ffffff"}, re-encrypted, and set as new cookie.
- No server-side validation prevented cookie tampering.

Recommendations:
- Use strong, authenticated encryption (e.g., AES-GCM) with secure keys.
- Avoid hardcoding keys in source code.
- Implement server-side session management and tamper-proof tokens.
- Sign cookies with HMAC for integrity.

## Introduction
### Background
Natas is an educational web security challenge series hosted by OverTheWire, aimed at teaching common web vulnerabilities through progressive levels. Each level requires obtaining a password to access the next, simulating real-world penetration testing scenarios.

### Objective
The primary goal of this level is to obtain the password for Natas Level 12 by manipulating a weakly encrypted cookie to set "showpassword" to "yes".

### Scope
- Target: Natas Level 11 web page.
- Assessment Type: White-box (source code inspection allowed).
- Exclusions: No network scanning, brute-forcing, or advanced exploitation was performed, as the challenge focused on encryption weaknesses.

## Methodology
The assessment followed a structured penetration testing approach aligned with OWASP Testing Guide and PTES (Penetration Testing Execution Standard) methodologies. Tools used included a standard web browser for cookie inspection and a custom PHP script for decryption/encryption. The process was non-destructive and focused on cookie analysis and manipulation.

### Step 1: Initial Reconnaissance
- Accessed the target web page using a standard web browser.
- Inspected cookies via developer tools and noted the "data" cookie.

### Step 2: Source Code Analysis
- Reviewed the PHP source code, revealing XOR encryption with key "eDWo" and base64 encoding.

### Step 3: Cookie Decryption and Manipulation
- Decoded the base64 cookie value.
- Applied XOR decryption with key "eDWo" to reveal the JSON.
- Modified the JSON to enable "showpassword".
- Re-encrypted with XOR and base64-encoded the new value.
- Set the new cookie in the browser and refreshed to reveal the password.

### Tools Utilized
- Web Browser: Google Chrome (Version 117 or equivalent).
- PHP Script: Custom code for XOR operations (detailed below).

## Findings
### Vulnerability Details
- **Vulnerability Type**: Insecure Cryptographic Storage (CWE-327: Use of a Broken or Risky Cryptographic Algorithm) via Weak XOR Encryption.
- **Severity**: High (CVSS Score: 7.5 - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).
- **Description**: The application uses a static, hardcoded XOR key ("eDWo") to encrypt a JSON cookie, which is base64-encoded. This reversible scheme allows full decryption and tampering without authentication.
- **Proof of Concept**:
  1. Extract the "data" cookie: "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=".
  2. Base64-decode and XOR-decrypt with "eDWo" to get original JSON.
  3. Modify JSON, re-encrypt, base64-encode, and set as new cookie.
  4. Refresh the page to display the Level 12 password.
- **Impact**: An attacker can manipulate cookies to escalate privileges or disclose sensitive data, leading to credential theft.

### Affected Components
- Cookie storage and encryption logic.
- Hardcoded XOR key.

## Solution and Exploitation
The password for Natas Level 12 was successfully retrieved by modifying the cookie to set "showpassword" to "yes" and reloading the page. The exploitation used the following PHP code for decryption and generation of the new cookie:

```php
<?php
function xor_encrypt($input, $key) {
    $key_length = strlen($key);
    $output = '';
    for ($i = 0; $i < strlen($input); $i++) {
        $output .= $input[$i] ^ $key[$i % $key_length];
    }
    return $output;
}

// Given XOR key
$key = "eDWo";

// URL-decoded base64 cookie
$cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=";

// Decode from base64
$decoded = base64_decode($cookie);

// XOR decrypt the JSON string
$json = xor_encrypt($decoded, $key);

// Decode the JSON
$data = json_decode($json, true);

echo "Decrypted cookie content:\n";
print_r($data);

// If you want to create a new cookie with "showpassword" => "yes"
$new_data = array("showpassword" => "yes", "bgcolor" => "#ffffff");
$plain_text = json_encode($new_data);

// XOR encrypt
$encrypted = xor_encrypt($plain_text, $key);

// Base64 encode the final cookie
$final_cookie = base64_encode($encrypted);

echo "\nGenerated cookie:\n" . $final_cookie . "\n";
?>
```

- **Extracted Artifact**: Password for Level 12 (redacted for this report).
- **Remediation Steps**:
  1. Replace XOR with strong encryption (e.g., AES) and secure key management.
  2. Remove hardcoded keys and use environment variables or vaults.
  3. Add HMAC signatures for cookie integrity.
  4. Validate cookie data server-side.

## Learnings and Recommendations
### Key Learnings
- **Weak Encryption Vulnerabilities**: XOR with short, static keys is easily reversible.
- **Secure Cookie Management**: Sensitive data in cookies requires strong encryption and integrity checks.
- **Key Management**: Hardcoding keys exposes them to attackers via source code.
- **Broader Implications**: This underscores the need for cryptographic best practices in web applications.

### Recommendations
- **Short-Term**: Audit cookie encryption and remove hardcoded keys.
- **Long-Term**: 
  - Follow OWASP Cryptographic Storage Cheat Sheet.
  - Integrate automated tools (e.g., Burp Suite or OWASP ZAP) to detect weak encryption in CI/CD pipelines.
  - Train developers on secure key management and encryption algorithms.
- **Mitigation Controls**: Use Secure and HttpOnly cookie flags, enforce HTTPS, and monitor for cookie tampering.

## Conclusion
This walkthrough for Natas Level 11 demonstrates how weak XOR encryption in cookies can be exploited to manipulate application behavior and disclose passwords. By following VAPT methodologies, the vulnerability was identified and "exploited" efficiently using a custom PHP script. Progressing to higher levels will involve more complex techniques, but the foundational lesson remains: never rely on weak or client-side encryption for security. For real-world applications, regular VAPT assessments are essential to mitigate such risks.

