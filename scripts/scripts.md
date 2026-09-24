# scripts（脚本库）

凭据管理脚本：英文小写命名，均 ≤50 行；数据只写固定缓存 `login_vault/`（`LOGIN_VAULT_HOME` 可覆盖），不写 skill 目录。

- [`vault_paths.py`](vault_paths.py)：平台固定缓存解析（win=%LOCALAPPDATA% · mac=~/Library/Caches · linux=~/.cache）；`paths()` 四文件（salt.bin / vault.json.enc / audit.log / fail.json）、`master()`（env 或 getpass，不落历史）、`audit()` 追加、`today()`。
- [`vault_store.py`](vault_store.py)：`crypto()` 依赖守卫（缺 cryptography 报确认式建议）；`key()` PBKDF2-HMAC-SHA256 310k 次派生 Fernet 密钥；`load()` 解密+连错5次锁60s+清零计数；`save()` 加密回写。
- [`vault.py`](vault.py)：CLI `init | add(--gen 生成强密码) | get(--yes 出明文并记审计) | list(恒掩码) | rm(--yes) | rotate(--yes) | audit(尾30条)`。
- [`vault_util.py`](vault_util.py)：`gen()` secrets 四类字符强口令（12-64）、`mask()` 尾4掩码、`view()` 条目视图（reveal 受控）。

## 运行约定

1. `set LOGIN_VAULT_MASTER=…`（或 getpass 交互）后运行；用完 unset。
2. 首次 `vault.py init` 建库；主密码不落盘，只落随机盐——忘记主密码无法找回。
3. 依赖：`cryptography`（须经用户确认后 pip 安装，本 skill 不自装）。
