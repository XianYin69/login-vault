# SMS 与 agent 集成

## 权限键 vault

- SMS（skill_manage_system）权限模型含 `vault` 键：`python scripts/permissions.py grant vault --write`（会话日目录 permissions.json，默认拒绝）。
- dispatch.py 的 SKILL_REQ 映射：子任务命中 login-vault → requires 追加 vault；未授予则该派发拒绝执行。

## agent 取用流程（最小暴露）

1. `vault.py list` → 掩码清单（可缓存到对话）用于选择 id。
2. `vault.py get --id X --yes` → 仅当前需要的一次出明文；用完不转述、不再写入任何文件。
3. 登录成功即可；agent 不复述口令，回复中密码一律以 `••••` 代。

## 与其他技能的关系

- captcha-assist：真人验证由用户完成，login-vault 不代填任何验证码/OTP。
- camera-vision / safe-mouse-automation：无共享数据；vault 目录与它们的缓存目录互不读写。

## 反模式

- 把主密码放进 env 文件、对话历史、SMS privacy records（隐私采集含 credential 类别默认留存 1 天且必须授权，见 SMS privacy_cat.py）。
- 用 vault 存第三方站点 API key 之外的"共享秘密"给多 agent 并发写——vault 无并发锁，串行使用。
