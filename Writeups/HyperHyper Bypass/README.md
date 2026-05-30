# HyperHyper Bypass

**CTF:** ImaginaryCTF 2026

**Category:** Web

**Difficulty:** Unknown

**Tags:** HLL

**Author:** Unknown

**Date:** 2026

## Objective
Manipulate a HyperLogLog (HLL) estimation so it returns a value greater than 1e17 and causes the server to return the flag.

## Overview

The application is a Flask web server that accepts base64-encoded strings via a `/click` endpoint and stores three HLL registers client-side in a `b64_strings` cookie. If the HLL estimate exceeds a threshold (10^17), the server reads and returns `flag.txt`.

## Analysis

- The server decodes inputs, hashes them with MD5, and selects one of three registers based on `hash[-1] % 3`.
- The HLL `estimate()` computes cardinality from ranks (leading zero bits in the MD5 hash).
- With only three registers (m=3), achieving 1e17 requires extremely high ranks (many leading zero bits), which is infeasible by brute force.

## Solution

The solution relies on using known MD5 records that produce hashes with many leading zero bits. We identified three input strings (from public MD5 min-record lists) that map to the three required buckets:

| Register | Input String | MD5 Hash (hex, prefix) | Bucket (`last_byte % 3`) |
| --- | --- | --- | --- |
| 0 | `08ni(g0u3ada_JiyongYoun-HLETRD` | `00000000000000d4...57` | 87 (mod 3) = 0 |
| 1 | `0v1-}P1wBlcd_JiyongYoun-HLETRD` | `00000000000001fc...ee` | 238 (mod 3) = 1 |
| 2 | `{bkgNR5ES7}-0x69BE027C97` | `000000000000003e...92` | 146 (mod 3) = 2 |

Steps:

1. **Prepare Payload:** Base64-encode the three input strings above.

2. **Inject Cookie:** Manually edit the `b64_strings` cookie in the browser's Developer Tools (Application → Storage/Cookies). Set the cookie value to the base64 array for the three inputs. Example value used in the solve:

```
["MDhuaShnMHUzYWRhX0ppeW9uZ1lvdW4tSExFVFJE", "MHYxLX1QMXdCbGNkX0ppeW9uZ1lvdW4tSExFVFJE", "e2JrZ05SNUVTN30tMHg2OUJFMDI3Qzk3"]
```

3. **Trigger Flag:** Click the "Click Me" button in the application UI. The server decodes the cookie, updates the three HLL registers with the extreme hashes, the HLL `estimate()` returns a value above the threshold, and the server responds with the flag.

Notes:

- The exact base64 strings above correspond to the three input strings listed earlier.
- Using these known low-value MD5 inputs is significantly faster than brute force and is sufficient to drive the HLL estimate above 1e17 for this challenge setup.

## Mitigation

Do not trust client-controlled HLL state. Store HLL registers server-side or authenticate and integrity-protect client state (HMAC). Enforce sanity limits on estimates and avoid using probabilistic counters as authorization gates.

## Conclusion

Flag: `ictf{weeks_of_computing_or_osint_still_only_3_clicks_though}`
