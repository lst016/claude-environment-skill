---
name: claude-environment-setup
description: Configure or troubleshoot a reusable Claude environment with kookeey static residential proxies, Clash Verge, a dedicated BitBrowser environment, optional iPhone Shadowrocket, and Claude Code subscription login. Use when setting up these linked components or diagnosing proxy-port and stale-provider conflicts.
---

# Claude 环境配置与排障

把用户已有网络、专用浏览器、邮箱和 Claude Code 串成可验证流程。优先复用现有状态，再补缺失项。教程包含旧会话真实 UI、补拍空白表单和明确标注的示意图。先区分首次搭建、迁移和已有环境复用。

## 先定位任务

- 首次搭建或需要图文指导：读 [图文操作指南](references/illustrated-guide.md)。
- 端口冲突、授权后仍显示 MiniMax、手机点击失败：读 [故障处理](references/troubleshooting.md)。
- 安装/更新此 Skill：读 [跨电脑安装说明](references/install.md)；不要把本 Skill 安装误解为购买 IP 或修改代理授权。
- 仅检查本机：可运行 `python3 scripts/inspect_environment.py --ports P B`（将 P/B 换成当前实际数字；省略 --ports 则跳过端口检查）。它不改配置、不输出密码、不发模型请求；输出认证字段经过白名单过滤。

## 工作顺序

1. **确认现有状态与目标。** 核对系统、客户端、代理监听、当前组选择、专用浏览器、CLI 入口和账号目标。状态不明时先只读检查。不要自动重置浏览器、退出账号或清理历史。
2. **配置网络。** 先备份，确认前置可连，再建立“前置 → 住宅 → 目标”的链路；域名优先规则、国内白名单和海外兜底按顺序匹配。设置文件、运行配置、系统代理和进程代理必须分别核对。
3. **完成浏览器和邮箱链路。** 优先遵守当前用户项目内的专用环境约定。通用 Skill 不固定环境序号/名称；新机先识别已有或同步环境，没有才创建专用环境，并在本机建立其代理入口。收信、验证链接、OAuth 使用同一专用环境。不要假定主系统时区等于浏览器时区。
4. **检查官方订阅登录。** 在新 CLI 进程核对 `auth status` 和一次最小实际请求；网页授权成功不能代替请求验证。旧 provider 覆盖只在备份后按目标处理，保留其他设置。
5. **按需配置手机。** 手机不是 Mac 配置的自动副本。Shadowrocket 的住宅节点、前置和 Safari 当前出口分别验收。需要自动操作时优先使用已可用的 iPhone Use；未连接时不要直接改手机。
6. **交付记录。** 保存日期/时区、修改位置、备份、当前入口、实际命令和结果、未验证项。区分配置校验、真实网页请求、CLI 模型调用和真机操作。按用户的知识库工作流保存，不把原始资料直接写入 Wiki。

## 固定选择与边界

- 购买/查看静态住宅 IP 统一从用户指定的 [kookeey 静态线路页面](https://www.kookeey.net/clientarea/#/static/list) 进入。它是入口，不假定该路由永远显示相同按钮。核对当前商品、协议、城市、到期、总价和续费，再由用户确认交易；使用 Skill 本身不授权新付款。
- 示例城市洛杉矶、30 天、5Mbps 是历史配置参考，不是当前报价或必须参数。按用户预算、实际用途及供应商当前页面选择。
- 不承诺防封，不把换 IP、本机清理或修改 Apple 账号当作获得服务资格的手段。使用前核对服务当前支持条件。
- 保持凭据在供应商页面、钥匙串或权限受限的私有配置中；不把认证、临时 OAuth URL、授权码、完整订阅地址或真实账号写入 Git 仓库、图示和一般日志。
- 代理端口与住宅出口都是可变配置。7897/7898 只作为历史示例；找到当前监听者和实际出口后再操作。不要让两个代理客户端争用同一端口。
- `dialer-proxy` 必须引用真实存在的前置节点/组；避免引用住宅节点自身形成环路。代理组没有 DIRECT 和 TUN 开启，均不能证明客户端退出后会阻断流量。
- 不默认执行 claude-cleanup 或任何身份重置。已有成功环境的日常复用不需要重复清理。

## 可移植性

- 图片、教程、安装说明与脚本都在本 Skill 目录内，禁止引用旧电脑的绝对路径或未打包的根目录文件。
- macOS 为主流程；Windows 手动差异见图文指南，尚未实机验证。检查脚本在 Windows 明确返回不支持，不作成功判断。
- 迁移 Skill 不迁移线路、账号、Cookie 或认证；按当前机器重建并验收。

## 完成标准

| 环节 | 最少证据 |
|---|---|
| Mac 分流 | 国内测试命中 DIRECT；目标请求命中指定住宅链；其他海外按预期；端口与核心确认 |
| BitBrowser | 已复用目标环境；专用入口可用；目标窗口实际请求显示预期出口 |
| 邮箱 | 已进入收件箱/能收所需验证邮件，不只看到提交成功 |
| Claude 网页 | 正确账号可完成真实回复；套餐状态另核对 |
| Claude Code | 入口、provider、认证符合目标，实际模型请求成功 |
| iPhone（涉及时） | 节点保存启用，Safari 读取当前请求返回的出口并交叉检查 |
| 恢复/断线保护（要求时） | 各场景单独实测；未做则明确列出 |

仅完成某一环节就只报告该环节。付款流水、续费、客户端退出、重启恢复和长时间稳定性没有验证时，不由“Pro 显示正常”或“单次请求成功”推断。
