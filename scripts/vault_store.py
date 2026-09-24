"""vault_store.py — PBKDF2(31万次)+Fernet(AES-128-GCM) 加密读写与连错锁定：错≥5次锁60秒；主密码不落盘只落盐。"""
import base64, json, os, time
from vault_paths import paths

def crypto():
    try:
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        return Fernet, PBKDF2HMAC, hashes
    except ImportError:
        raise SystemExit("缺依赖 cryptography：经用户确认后 pip install cryptography")

def key(master):
    _, K, H = crypto()
    p = paths()
    if not os.path.exists(p["salt"]):
        with open(p["salt"], "wb") as f:
            f.write(os.urandom(16))
    with open(p["salt"], "rb") as f:
        salt = f.read()
    kdf = K(algorithm=H.SHA256(), length=32, salt=salt, iterations=310000)
    return base64.urlsafe_b64encode(kdf.derive(master.encode("utf-8")))

def load(master):
    F, _, _ = crypto()
    p = paths()
    f = json.load(open(p["fail"], encoding="utf-8")) if os.path.exists(p["fail"]) else {}
    if f.get("until", 0) > time.time():
        raise SystemExit("锁定中：主密码连错≥5次，剩 %d 秒" % int(f["until"] - time.time()))
    if not os.path.exists(p["enc"]):
        raise SystemExit("保险库不存在：先 init（设置主密码）")
    try:
        with open(p["enc"], "rb") as fh:
            data = json.loads(F(key(master)).decrypt(fh.read()).decode("utf-8"))
    except Exception:
        n = f.get("n", 0) + 1
        out = {"n": 0, "until": time.time() + 60} if n >= 5 else {"n": n}
        json.dump(out, open(p["fail"], "w", encoding="utf-8"))
        raise SystemExit("解密失败：主密码错误 %d/5 次或库已损坏" % min(n, 5))
    json.dump({"n": 0}, open(p["fail"], "w", encoding="utf-8"))
    return data

def save(master, data):
    F, _, _ = crypto()
    p = paths()
    blob = F(key(master)).encrypt(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    with open(p["enc"], "wb") as f:
        f.write(blob)
