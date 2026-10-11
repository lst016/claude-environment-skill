# Claude 图文环境配置 Skill

把 kookeey 静态住宅 IP、Clash 分流、BitBrowser、可选 iPhone 和 Claude Code 官方订阅登录串成一套可复用流程。配置前先检查已有环境，配置后用实际请求验收。

![一次配置，三处验收](skills/claude-environment-setup/assets/01-overview.png)

## 直接使用

- **完整图文教程**：[按步骤查看](skills/claude-environment-setup/references/illustrated-guide.md)
- **给 Agent 的入口**：[SKILL.md](skills/claude-environment-setup/SKILL.md)
- **故障处理**：[端口冲突、旧 MiniMax 覆盖与手机控制](skills/claude-environment-setup/references/troubleshooting.md)
- **购买或查看 IP**：[kookeey 静态住宅线路](https://www.kookeey.net/clientarea/#/static/list)

全部图片为原创操作示意，不是用户账号截图；没有包含账号、真实出口、代理凭据或私人会话。具体界面、价格和软件选项以当前产品为准。本 Skill 不自动购买、不承诺防封、不默认清理本机身份。

## 图文内容

| 章节 | 内容 |
|---|---|
| 总览 | Mac、BitBrowser、iPhone 三个入口分别验收 |
| kookeey | 参数、已有线路、订单确认与续费 |
| Clash | 前置→住宅、规则顺序、端口与实际出口 |
| iPhone | Shadowrocket 代理通过、VPN 与当前 IP |
| Claude Code | OAuth、旧 provider 覆盖、实际模型请求 |

![kookeey 参数核对示意](skills/claude-environment-setup/assets/02-kookeey.png)

## 安装

仓库中的 Skill 位于 `skills/claude-environment-setup`。私有仓库需要当前 GitHub 账号具有访问权限；不要把访问令牌写进安装命令或仓库文件。

使用 Codex 自带的 `skill-installer`，指定本仓库与上述目录；也可以将该目录完整复制到：

- Codex：`~/.codex/skills/claude-environment-setup`
- Claude Code：`~/.claude/skills/claude-environment-setup`

已有同名 Skill 时先比较和备份，不直接覆盖。安装后在新一轮/新会话加载；Claude Code 如未发现，重开会话。

Codex 调用示例：

> 使用 $claude-environment-setup 检查现有环境，按需配置 kookeey 住宅出口，并验证 Claude 网页与 CLI。

Claude Code 调用：

> /claude-environment-setup

也可自然语言请求“按 Claude 图文环境 Skill 检查网络和登录”。Skill 被调用不代表已授权付款、重置账号或向外发送资料。

## 只读检查

在 Skill 目录运行：

```bash
python3 scripts/inspect_environment.py
```

输出工具版本、PATH 是否有旧 Claude、provider 覆盖字段是否存在、本机监听和经过过滤的认证状态。不输出设置值、账号、Token 或密码；不改配置，不发模型请求。`--skip-auth` 可跳过本机钥匙串相关认证检查，`--ports` 可指定实际端口。

该脚本通过不代表实际代理出口、网页账号、手机网络、付款、模型调用或断线恢复已验证。

## 来源与维护

基于 2026-10-10 至 11 的本机实际流程提炼，去除私人数据后保留机制、验证方法与已遇到的故障。网络实现参考 [Mihomo 文档](https://wiki.metacubex.one/)，服务条件查阅 [Anthropic 支持地区](https://www.anthropic.com/supported-countries)。示意图由 Claude 制作，Skill 指令与代码由 Codex 整理审查。

更新时先核对当前 UI/版本，不把历史端口、IP、报价和时区写成所有机器的默认事实。

## 本版校验（2026-10-11）

- Skill 结构校验通过。
- MiniMax 独立 CLI 实际运行 5 项隐私/只读边界测试，5 通过、0 失败；测试使用合成数据。
- 主代理核对 12 个本地文档/图片链接，5 张 PNG 和 5 张 SVG 均有效；逐图检查文字、布局和示意标记。
- 正常本机权限实际运行只读检查脚本成功，认证输出经过过滤；没有重新执行住宅网络配置、手机配置或付款。
- 图片设计使用 Claude，代码与内容由 Codex 审查。复杂环境差异仍需调用 Skill 时按实际设备验收。
