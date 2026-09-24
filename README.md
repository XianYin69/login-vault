# login-vault

本地加密登录信息管理 Agent Skill：邮箱/账号 + 口令的加密保管、强密码生成、轮换与审计。主密码不落盘、明文不出库（`get --yes` 唯一出口）、连错锁定。

## 依赖

- `cryptography`（Fernet+PBKDF2；须经用户确认后安装，本 skill 不自装）

## 快速开始

```bash
set LOGIN_VAULT_MASTER=<主密码>        # 用完 unset；或运行时 getpass 交互输入
python scripts/vault.py init                          # 首次建库（仅盐+密文文件）
python scripts/vault.py add --id github --user me@x.io --gen   # 生成 20 位强密码入库
python scripts/vault.py list                          # 掩码清单
python scripts/vault.py get --id github --yes         # 出明文（记审计 get-reveal）
python scripts/vault.py rotate --id github --yes      # 换新随机密+时间戳
python scripts/vault.py audit                         # 尾 30 条操作审计
```

## 数据边界

库、盐、审计全在 `%LOCALAPPDATA%\login_vault\`（`LOGIN_VAULT_HOME` 可覆盖；macOS `~/Library/Caches`、Linux `~/.cache`）。忘记主密码 = 数据不可找回。只管理用户本人账号；SMS 侧调用需 `grant vault`。

## 结构

[SKILL.md](SKILL.md) 入口 · [scripts/](scripts/scripts.md) 脚本 · [schemas/](schemas/credential.schema.json) 契约 · [knowledge/](knowledge/knowledge.md) 知识库 · [resistance/](resistance/resistance.md) 红线与兜底 · [agent/](agent/CLAUDE.md) 四格式提示词
