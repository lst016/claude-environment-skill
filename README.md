# Claude 环境配置：真实 UI 图文 Skill

从自己的线路和账号开始，把 kookeey、Clash、BitBrowser 与 Claude Code 串起来。新电脑有完整安装入口；已有电脑优先复用现有环境。

- **[图文教程（Markdown）](skills/claude-environment-setup/references/illustrated-guide.md)**：真实界面配“在哪里点、填什么、看到什么算成功”。
- **[离线图文页面](skills/claude-environment-setup/references/guide.html)**：下载完整仓库后直接打开，可放大截图。
- **[装到另一台电脑](skills/claude-environment-setup/references/install.md)**：ZIP、Git、Python 安装器或手动复制；旧版本自动备份。
- **[Agent 入口](skills/claude-environment-setup/SKILL.md)** · **[排障](skills/claude-environment-setup/references/troubleshooting.md)**
- **[购买/查看 IP](https://www.kookeey.net/clientarea/#/static/list)**：用户指定 kookeey 入口。

![真实 UI：BitBrowser SOCKS5 空白代理表单](skills/claude-environment-setup/assets/ui/bitbrowser-proxy.png)

## 本版补齐了什么

4 张旧会话用户原图：kookeey 购买页、Clash 全红、CLI 旧 MiniMax、网络重连。另有 2 张本次补拍的 BitBrowser 空白配置表单。全部保留原始像素；[来源与哈希](skills/claude-environment-setup/assets/ui/sources.json) 可查。失败截图明确标注为失败，历史价格、出口、节点名称不能照抄。含密码的线路截图和私人聊天没有打包。

主流程面向 macOS。Windows 附官方安装入口和手动检查差异，尚未 Windows 实机验收；自动检查脚本在 Windows 明确拒绝成功判断。新电脑按教程重新获取端口、线路和账号，Skill 本身不会迁移这些状态。

## 安装和调用

先下载/克隆此私有仓库，并进入仓库目录。需要 Python 3.9+：

```bash
python3 skills/claude-environment-setup/scripts/install_skill.py --target both
```

Windows 用 `py -3` 替换 `python3`。已有同名副本会保留到相应工具配置目录的 skill-backups，默认安装 Codex 和 Claude Code 两边；自定义 CODEX_HOME 见[安装说明](skills/claude-environment-setup/references/install.md)。安装后开新会话，必要时重启应用。

Codex：`使用 $claude-environment-setup 检查现有环境。`  
Claude Code：`/claude-environment-setup`

## 只读检查

在 Skill 目录运行 `python3 scripts/inspect_environment.py`，输出工具版本和经过过滤的认证/provider 状态。明确传 `--ports 你的P 你的B` 才检查对应监听；没有历史端口默认值。`--skip-auth` 可跳过本机认证检查。脚本不改设置、不输出认证值、不发模型请求。

配置校验、网页回复、CLI 模型调用、真机操作及故障恢复分别验收。安装成功不等于网络或账号已在新机可用。

## 验证记录

本版结果见 [验证记录](VALIDATION.md)。软件步骤依据 [Claude Code 官方说明](https://code.claude.com/docs/en/setup)、[BitBrowser 官网](https://www.bitbrowser.net/download) 和 [Mihomo 文档](https://wiki.metacubex.one/)。图文布局由 Claude 制作，内容与代码由 Codex 核对。
