"""vault_paths.py — 固定缓存路径 / 主密码输入 / 审计追加：保险库只落 login_vault 固定目录，不落 skill 目录。"""
import os, sys, time

def home():
    u = os.path.expanduser("~")
    if os.environ.get("LOGIN_VAULT_HOME"):
        return os.environ["LOGIN_VAULT_HOME"]
    b = (os.environ.get("LOCALAPPDATA") if sys.platform == "win32" else
         os.path.join(u, "Library", "Caches") if sys.platform == "darwin" else
         os.environ.get("XDG_CACHE_HOME") or os.path.join(u, ".cache"))
    return os.path.join(b or u, "login_vault")

def paths():
    h = home()
    os.makedirs(h, exist_ok=True)
    j = lambda n: os.path.join(h, n)
    return {"salt": j("salt.bin"), "enc": j("vault.json.enc"), "audit": j("audit.log"), "fail": j("fail.json")}

def master():
    m = os.environ.get("LOGIN_VAULT_MASTER")
    if not m:
        import getpass
        m = getpass.getpass("主密码: ")
    if not m:
        raise SystemExit("须主密码（env LOGIN_VAULT_MASTER 或交互输入；勿把密码写进命令行历史）")
    return m

def audit(action, vid):
    p = paths()
    with open(p["audit"], "a", encoding="utf-8") as f:
        f.write("%s %s %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), action, vid))

def today():
    return time.strftime("%Y-%m-%d")
