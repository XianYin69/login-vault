"""vault_util.py — 口令工具：secrets 强密码生成（四类必含 12-64）、尾4掩码、条目视图（reveal 仅 get --yes）。"""
import secrets

SY = "!@#$%^&*()-_=+[]{};:,.<>?"
POOL = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789" + SY


def gen(n=20):
    n = max(12, min(64, int(n)))
    while True:
        p = "".join(secrets.choice(POOL) for _ in range(n))
        if any(c.isupper() for c in p) and any(c.islower() for c in p) and any(c.isdigit() for c in p) and any(c in SY for c in p):
            return p


def mask(s):
    return "*" * max(4, len(s) - 4) + s[-4:] if len(s) > 4 else "****"


def view(e, reveal=False):
    return {"id": e["id"], "user": e["user"], "secret": e["secret"] if reveal else mask(e["secret"]),
            "url": e.get("url", ""), "note": e.get("note", "")}
