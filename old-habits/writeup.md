---
title: "Old Habits"
ctf: "DEADFACE CTF 2026"
date: 2026-10-18
category: osint
difficulty: hard
points: 350
flag_format: "deadface{...}"
author: "AN (team 1761)"
---

# Old Habits

## Summary

`spookyboi`'s hidden backup cache contains `mort1cia`'s MD5-crypt password hash and a note that she
reuses the same personal password everywhere. Her public GhostTown posting history includes a
thread where `gh0st404` admits he set her `charon` password to something easy to remember based on
an old Halloween photo of her dressed as a Disney princess. A targeted crack of the hash confirms
`princess2015`; `su - mort1cia` with that password reads the flag.

## Solution

### Step 1: Read the credential cache as spookyboi

The `cryptctl` capability from Dangerous Capability gives a `spookyboi` shell:

```bash
printf 'cat ~/.backup/creds.bak; exit\n' | /opt/crypto/cryptctl
```

```text
# Kingmaker cred cache. mort1cia STILL has not changed her password since the
# op kicked off -- and she reuses the same personal one everywhere, even on her
# old GhostTown account. If you need into her box, read her posting history.
# format: user:hash
mort1cia:$1$de4df4ce$1pZYBMgWLPXg1tZo6pke20
```

### Step 2: Follow the GhostTown posting history

The GhostTown thread
`https://ghosttown.deadface.io/t/50/yo-mort1cia-we-need-to-talk-about-ur-past` contains the hint:

- `gh0st404`: "got ur account setup on charon like u asked... i didnt know what password u wanted
  so i just picked somethin easy for u to remember. found this old halloween pic of u from like
  forever ago... why are u dressed like a disney princess... pink dress, tiara, magic wand, THE
  WHOLE THING"
- `mort1cia`: "James. First, you had absolutely no business looking through my old photographs.
  Second, change that password immediately."

The password is therefore a princess-themed variation, probably with the year of the old photo.
The hash is MD5-crypt (`$1$`), so it can be verified locally with `passlib`:

```python
from passlib.hash import md5_crypt

target = "$1$de4df4ce$1pZYBMgWLPXg1tZo6pke20"
for candidate in candidates:          # princess, pinkprincess, ..., princess2015, ...
    if md5_crypt.verify(candidate, target):
        print("FOUND:", candidate)
        break
```

`deadface-2026/old-habits/crack_mort1cia.py` generates the princess/tiara/disney candidates with
year suffixes and prints:

```text
trying 16655 candidates
FOUND: princess2015
```

### Step 3: Become mort1cia and read the flag

From the `svc-deploy` shell on charon:

```text
charon:~$ su - mort1cia
Password: princess2015
charon:~$ id
uid=1007(mort1cia) gid=1007(mort1cia) groups=1007(mort1cia),1007(mort1cia)
charon:~$ cat ~/flag.txt
deadface{0s1nt_n3v3r_f0rg3ts}
```

The same password also matches the reused personal credential described in the backup note.

## Flag

```text
deadface{0s1nt_n3v3r_f0rg3ts}
```
