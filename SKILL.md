---
name: login-vault
version: 0.1.0
description: >
  本地加密登录信息管理 skill：邮箱/账号+口令的 Fernet(PBKDF2-310k) 加密保管、强密码生成、
  轮换与追加式审计；主密码永不落盘，list/rotate 恒掩码，明文仅 get --yes 且逐笔记审计，
  连错 5 次锁 60 秒，数据只存固定缓存 login_vault/；只管理用户本人账号，SMS 侧须 grant vault。
license: MIT
metadata:
  category: security
---

# login-vault

使用 `login-vault` skill 来完成用户请求。本地加密登录信息管理：建库 → 存(生成/录入) → 掩码列 → 受控取用 → 轮换审计。

## 运行流程

1. **主密码**：`set LOGIN_VAULT_MASTER=…`（用完 unset）或运行时 getpass 交互；主密码不存储，只存随机盐。
2. **建库**：`python scripts/vault.py init` 生成 `login_vault/vault.json.enc + salt.bin`（路径按平台缓存，`LOGIN_VAULT_HOME` 可覆盖）。
3. **入库**：`add --id 站点 --user 邮箱 --gen`（推荐，随机 12-64 位强密）或 `--secret 值`；重复 id 拒绝。
4. **查询**：`list` 恒掩码；`get --id X --yes` 出明文并记 `get-reveal` 审计（agent 只用于当次登录，不复述）。
5. **轮换/清理**：`rotate --id X --yes` 换新随机密；`rm --id X --yes` 删除；`audit` 查尾 30 条。

## 依赖

`cryptography`（Fernet+PBKDF2；缺失只报建议、经用户确认后 pip 安装，绝不自动装）。

## 数据契约与脚本

- 条目契约：[schemas/credential.schema.json](schemas/credential.schema.json)（仅内存态；磁盘只有密文）。
- [scripts/scripts.md](scripts/scripts.md)：vault_paths / vault_store / vault_util / vault。
- 知识库：[knowledge/knowledge.md](knowledge/knowledge.md)（加密与卫生 · SMS 与代理集成）。

## 红线

- 明文只经 `get --yes` 出口；任何密码/密文不写盘进 skill 目录、不进对话转述、不上网络。
- 只管理用户本人账号；他人凭据的存取尝试一律拒绝。
- 连错 ≥5 次锁 60 秒不可绕过；窗口内正确主密码也拒绝，防脚本撞库。
- 忘记主密码如实告知不可找回并引导网站侧重置；悬空链接 = 0；所有 .md ≤ 50 行（50 行红线只约束 markdown 文本；脚本 .py/.ps1/.sh/.cmd 不限行数，但仍禁裸 except、print 调试残留、>100 字符长行、超长函数）。
- 约束兜底见 [resistance/](resistance/resistance.md)。
