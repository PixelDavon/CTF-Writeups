# zipzalabim

**CTF:** BeeCTF 2025

**Category:** Forensics

**Difficulty:** Easy

**Tags:** Wireshark

**Author:** 

**Date:** 2025

## Objective
Recover a corrupted ZIP file referenced in a PCAP and extract the hidden flag.

## Overview

This beginner forensic challenge revolves around packet capture (PCAP) analysis and archive recovery. Players are given a network capture file named `confundo.pcap` containing a small number of packets. Hidden within this traffic is a link to a Pastebin snippet, which redirects to a downloadable ZIP file hosted on Google Drive. The downloaded archive appears corrupted or broken, and the solve is to repair the compressed file and extract the hidden flag.

## Analysis

The packet capture is relatively small, consisting of about 50 packets. Opening the PCAP in Wireshark and following the TCP stream reveals the embedded URL. Because the file is also small, the same data can be extracted quickly with `strings`.

The ZIP file itself opens as corrupted in Windows, so the archive headers and layout need to be repaired before extraction will succeed.

## Solution

Open `confundo.pcap` in Wireshark and inspect the traffic:

1. Right-click one of the TCP packets.
2. Select **Follow** > **TCP Stream**.

If you want a quicker extraction, use `strings`:

```bash
strings confundo.pcap | grep pastebin
```

Both methods reveal the Pastebin URL:

```text
https://pastebin.com/BYabV9KT
```

That Pastebin contains the Google Drive download link:

```text
https://drive.google.com/file/d/1lqGZeukmaP6F7m8eBxQFzBSDEBC0HmhF/view?usp=sharing
```

Visiting the Google Drive link downloads `zipzalabim.zip`. On Windows (😶), attempting to unzip or open the archive normally shows that it is corrupted or damaged.

Repair the archive with WinRAR:

1. Open `zipzalabim.zip` in WinRAR.
2. Select **Tools** > **Repair archive** (or press `Alt + R`).
3. Choose an output destination and click **OK**.

WinRAR rebuilds the archive structure and produces a functional file. After extracting the repaired ZIP archive, the flag file becomes readable.

## Conclusion

Flag: `BEECTF{z1mz4l4b1iim_c0rupt3edd_d4mnnn}`
