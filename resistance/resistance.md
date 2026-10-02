# resistance（约束库 / 兜底库）

login-vault 红线与降级策略；不得删除本目录约束条目。

## 红线

1. 凭据只以 Fernet 密文存固定缓存 `login_vault/vault.json.enc`；主密码不落盘（只落盐）；任何明文禁止写盘、写日志、写对话输出（`get --yes` 是唯一出口且记审计）。
2. `list`/`add`/`rotate` 输出一律掩码（尾4位）；agent 转述口令须 `get --yes` 且只用于当次登录，不得复述进后续回复。
3. 连错主密码 ≥5 次锁 60 秒；禁止任何绕过锁定/批量试密的脚本化行为。
4. 只管理**用户本人所有**的账号凭据；拒绝存储、获取、尝试他人凭据——本 skill 不是渗透工具。
5. 不自动安装依赖（缺 cryptography 报确认后安装）；不联网、不同步、不上传密文（用户明示的多设备同步除外）。
6. note 字段禁放助记词/私钥/恢复码等不可重置秘密（引导冷备份）；SMS privacy 采集中 credential 类别按 privacy_cat 默认 1 天留存。
7. 悬空链接 = 0；所有 .md ≤ 50 行（50 行红线只约束 markdown 文本；脚本 .py/.ps1/.sh/.cmd 不限行数，但仍禁裸 except、print 调试残留、>100 字符长行、超长函数）；SKILL.md 含 YAML frontmatter；缓存不落 skill 目录。

## 降级策略

- 主密码遗忘 → 明示不可找回；引导重建库+逐站 rotate 重置（网站侧"忘记密码"流程）。
- vault.json.enc 损坏/篡改 → Fernet 校验失败按解密失败处理；从用户自有密文备份恢复。
- fail.json 异常（计数卡死）→ 删除 fail.json 重开计数（audit 仍可查锁定历史）。
- 多进程并发 → 无锁设计，串行调用；冲突时后写覆盖前写，避免并行 save。
