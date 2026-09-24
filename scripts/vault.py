"""vault.py — init|add|get|list|rm|rotate|audit：凭据加密仅存本地；明文须 --yes（记审计）；list 恒掩码。"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8", errors="replace")
import vault_paths as vp, vault_store as vs, vault_util as vu

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["init", "add", "get", "list", "rm", "rotate", "audit"])
    ap.add_argument("--id"); ap.add_argument("--user"); ap.add_argument("--secret"); ap.add_argument("--url"); ap.add_argument("--note")
    ap.add_argument("--length", type=int, default=20); ap.add_argument("--gen", action="store_true"); ap.add_argument("--yes", action="store_true")
    a = ap.parse_args(); p = vp.paths(); out = lambda x: print(json.dumps(x, ensure_ascii=False, indent=2))
    if a.cmd == "init":
        if os.path.exists(p["enc"]):
            out({"inited": True})
        elif not os.environ.get("LOGIN_VAULT_MASTER"):
            sys.exit("init 须经 env LOGIN_VAULT_MASTER 设主密码（用完 unset）")
        else:
            vs.save(vp.master(), {"entries": []}); vp.audit("init", "-"); out({"created": p["enc"]})
        sys.exit(0)
    data = vs.load(vp.master()); ents = {e["id"]: e for e in data["entries"]}
    if a.cmd == "add":
        if not (a.id and a.user) or not (a.secret or a.gen) or a.id in ents:
            sys.exit("add 须唯一 --id --user 与 --secret|--gen")
        sec = vu.gen(a.length) if a.gen else a.secret
        data["entries"].append({"id": a.id, "user": a.user, "secret": sec, "url": a.url or "", "note": a.note or "", "created": vp.today()})
        vs.save(vp.master(), data); vp.audit("add", a.id); out({"added": a.id, "generated": bool(a.gen)})
    elif a.cmd == "get":
        e = ents.get(a.id)
        if not e:
            sys.exit("无 id=" + str(a.id))
        vp.audit("get-reveal" if a.yes else "get-masked", a.id); out(vu.view(e, a.yes))
    elif a.cmd == "list":
        vp.audit("list", "-"); out({"count": len(ents), "entries": [vu.view(e) for e in ents.values()]})
    elif a.cmd == "rm":
        if a.id not in ents or not a.yes:
            sys.exit("rm 须已存在 --id 与 --yes")
        data["entries"] = [x for x in data["entries"] if x["id"] != a.id]
        vs.save(vp.master(), data); vp.audit("rm", a.id); out({"removed": a.id})
    elif a.cmd == "rotate":
        e = ents.get(a.id)
        if not e:
            sys.exit("无 id=" + str(a.id))
        e["secret"] = vu.gen(a.length); e["rotated"] = vp.today()
        vs.save(vp.master(), data); vp.audit("rotate", a.id); out({"rotated": a.id, "secret": vu.mask(e["secret"]), "hint": "明文经 get --yes"})
    else:
        tail = open(p["audit"], encoding="utf-8").read().splitlines()[-30:] if os.path.exists(p["audit"]) else []
        out({"audit_tail": tail})
