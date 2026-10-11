# 把完整 Skill 安装到另一台电脑

本仓库为私有仓库，需要自己的 GitHub 账号具有访问权限。Skill 不含代理密码、订阅、Cookie 或 Claude 登录凭据。只有 SKILL.md 而没有 assets/references/scripts 是不完整安装。

## 方法 A：下载 ZIP，不依赖旧电脑的 Codex 安装器

1. 登录 GitHub，打开 [仓库](https://github.com/lst016/claude-environment-skill)。
2. 点 **Code → Download ZIP**，在新电脑解压。
3. 打开终端，进入解压出的仓库目录；目录名由你的下载位置决定。
4. 安装前检查下列命令对应的源目录，已有同名 Skill 会自动移到 `skill-backups` 中保留。

macOS/Linux（需要 Python 3.9+）：

```bash
python3 skills/claude-environment-setup/scripts/install_skill.py --target both
```

Windows PowerShell（已安装 Python 3.9+，Python Launcher 可用时）：

```powershell
py -3 skills/claude-environment-setup/scripts/install_skill.py --target both
```

只装一边，把 both 换成 codex 或 claude。脚本复制本目录内的全部文件；不安装客户端、不改网络、不迁移账号。默认目录为用户主目录下 `.codex/skills/claude-environment-setup` 和 `.claude/skills/claude-environment-setup`。

如果已在 Skill 目录内，直接运行 `python3 scripts/install_skill.py --target both`（Windows 用 `py -3`）。不依赖仓库根目录 README。

## 方法 B：自己已有 Git 或 GitHub CLI

`gh` 已安装时，先用自己的账号完成 `gh auth login`，然后：

```bash
gh repo clone lst016/claude-environment-skill
cd claude-environment-skill
python3 skills/claude-environment-setup/scripts/install_skill.py --target both
```

也可 `git clone https://github.com/lst016/claude-environment-skill.git`，使用系统已有的凭据管理器。不要把访问 Token 拼进命令或仓库 URL。

## 无 Python 时手动安装

将仓库内 `skills/claude-environment-setup` **整个文件夹**复制到需要的用户 Skill 目录。已有同名文件夹先移到 skills 外的备份目录，再复制新版本。不要把备份留在可自动扫描的 skills 目录里。

自定义了 `CODEX_HOME` 的机器，应复制到实际 `$CODEX_HOME/skills`；本安装脚本只写上面两处默认目录。Windows 对应用户主目录通常为 `%USERPROFILE%`，不使用 macOS `/Users/...` 路径。

## 打开教程与调用

直接打开已安装目录中的 `references/guide.html`。全部图片/样式在本地包内，不需要访问旧电脑；页面官方链接和软件服务仍需网络。也可阅读 `references/illustrated-guide.md`。

安装后开启新会话；Codex 如果未加载则重启应用。调用：

- Codex：`使用 $claude-environment-setup，从零配置这台电脑，先检查现有状态。`
- Claude Code：`/claude-environment-setup`

要迁移网络环境，继续读图文指南第 0、1、7 步。复制 Skill 不能使新电脑自动获得旧电脑的线路和登录状态。

## 更新与回退

重新下载新版本，先比较自己的改动，再运行同一安装命令。旧副本保留在该工具用户配置目录的 `skill-backups/claude-environment-setup/日期` 下；脚本输出具体位置。

回退时先退出使用该 Skill 的会话，把当前目录移到备份位置，再将需要的旧副本移回 skills 目录。不会删除旧副本，也不把整个用户配置目录覆盖掉。

## 验证范围

安装器在本机临时目录通过“首次完整复制、保留旧版本、从已安装副本更新”测试。本机 macOS 两边安装另作哈希核对；尚未在另一台物理电脑或 Windows 上运行安装。
