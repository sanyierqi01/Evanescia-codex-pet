# Evanescia Codex Pet · 绯英 / 尺刀绯绯狐

> 我是尺刀绯绯狐，爱你。

一个以《崩坏：星穹铁道》绯英（Evanescia）为灵感的同人桌宠与 Codex 外观项目。粉色长发、白色长耳、红色发带与尺刀，让小狐狸陪你写代码、等待任务、检查结果。

![绯绯狐动作预览](assets/previews/all-states.gif)

## 项目包含什么

| 内容 | 状态与范围 |
| --- | --- |
| Codex 自定义桌宠 | v2 透明精灵图，9 种动作、16 个视线方向，73 帧；已在作者的 Windows Codex 中显示 |
| 深色与浅色主题 | 粉紫夜色、樱花浅色两套主题导入文本；请在自己的客户端导入并选择 |
| 花饰按钮和界面 | 独立网页预览，可切换配色和动作；可自行选择本地视频作为预览背景 |
| 安装与校验工具 | Python 安装器、图集校验器和自动化测试；不需要账户凭据 |

**原生 Codex 与网页预览的区别：**原生桌宠使用本项目的 `pet.json` 和图集；原生配色使用主题导入。花饰按钮、布局和视频背景是网页设计演示，不能通过本仓库直接替换原生 Codex 按钮或窗口结构。本项目不修改 Codex 程序文件。

## 快速开始：安装桌宠

下载仓库 ZIP 并解压，或运行：

```sh
git clone https://github.com/sanyierqi01/Evanescia-codex-pet.git
cd Evanescia-codex-pet
python scripts/install_pet.py
```

需要 Python 3.10+；安装器仅使用标准库。Windows 也可使用 `py scripts/install_pet.py`。

默认安装至 `$CODEX_HOME/pets/feiying-fox`；未设置 `CODEX_HOME` 时使用用户主目录下的 `.codex/pets/feiying-fox`。安装后在 **Codex → 设置 → 宠物**中刷新并选择 **尺刀绯绯狐**。部分客户端需要重新打开设置或重启应用。

```sh
# 只查看目标路径和操作，不写入文件
python scripts/install_pet.py --dry-run
# 自定义 Codex 数据目录
python scripts/install_pet.py --codex-home /path/to/.codex
# 已有同名宠物时，先备份原目录再安装
python scripts/install_pet.py --replace
```

安装器不会修改账户选择状态或全局配置。默认遇到同名目录会停止；`--replace` 将旧目录保留为带时间戳的备份。回退时退出 Codex，将本次安装目录移走，再把备份目录改回 `feiying-fox`。也可仅在设置里选回其他宠物。

**兼容性：**此本地 manifest 格式在 Windows Codex `26.1007.2314.0` 上完成安装和实际显示验证；其他版本和平台尚未实机验证。若设置中没有自定义宠物入口，请先确认客户端是否支持该功能。ChatGPT Work 云端宠物需要通过对应 Pets 功能单独导入，不会随本地安装自动同步。

## 导入原生配色

打开 `themes/codex-theme-dark.txt` 或 `themes/codex-theme-light.txt`，复制完整的 `codex-theme-v1:...` 文本，在支持主题导入的 Codex **设置 → 外观**中导入并选用。不同版本的入口可能不同。

| 主题 | 背景 | 强调色 | 文字 |
| --- | --- | --- | --- |
| 粉紫夜色 | `#21172F` | `#EAA4CF` | `#F9EFF8` |
| 樱花浅色 | `#FFF4FA` | `#A72B69` | `#39243C` |

主题文本使用 `Microsoft YaHei UI` 和 `Cascadia Code`；系统未安装时请在外观设置选择已有字体。主题文件已做格式校验，但当前用户会话仅确认了桌宠显示，未确认配色已实时生效。

## 花饰界面预览

在仓库根目录启动本地服务器：

```sh
python -m http.server 8765 --bind 127.0.0.1
```

访问 <http://127.0.0.1:8765/preview/>，可切换深浅色、观看全部动作和视线方向、复制主题文本，并选择自己的本地视频。所选视频只在浏览器本地播放，不会上传；仓库不附带官方立绘、游戏音乐或来源不明的壁纸视频。

## 图集与制作

最终图集：[`assets/pet/spritesheet.png`](assets/pet/spritesheet.png)，尺寸 **1536 × 2288**，8 列 × 11 行，每格 **192 × 208**，透明 PNG。

| 行 | 状态 | 帧数 |
| --- | --- | --- |
| 0 | idle / 待机 | 6 |
| 1 | running-right / 向右移动 | 8 |
| 2 | running-left / 向左移动 | 8 |
| 3 | waving / 挥手 | 4 |
| 4 | jumping / 跳跃 | 5 |
| 5 | failed / 失败反馈 | 8 |
| 6 | waiting / 等待 | 6 |
| 7 | running / 执行任务 | 6 |
| 8 | review / 检查 | 6 |
| 9–10 | look / 视线方向 | 16 |

美术通过 AI 图像生成制作，同一角色参考贯穿各动作；生成后统一分格、清理背景、拼接并验证。创作思路见 [`docs/creation.md`](docs/creation.md)，原始检查结果的脱敏副本见 [`qa/`](qa/)。检查记录包括图集结构、跳跃落地、方向盲审与 Pets 服务预检；这些是本次素材的验证记录，不代表所有 Codex 版本均兼容。

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate_atlas.py
python -m unittest discover -s tests -v
```

最终图集 SHA-256：

```text
0954000743b9d59bd05f10700e4b0724a42f1e480c7d14aad946448d8ab0d875
```

## 授权与来源

脚本、网页代码、主题配置和文档使用 **MIT**，见 [`LICENSE`](LICENSE)。`assets/` 下的 AI 生成同人美术与衍生预览另按 **CC BY-NC 4.0** 提供贡献者有权许可的部分，见 [`assets/LICENSE.md`](assets/LICENSE.md)。角色、游戏名称和相关标识的权利仍属于原权利人；本项目不是 HoYoverse 或 OpenAI 官方项目，也不声称获得其授权。素材许可不授予第三方角色权利。

原始参考图、壁纸视频、个人 Library 链接、云端宠物 ID、配置备份、聊天记录和应用源码摘录均未纳入公开版本。官方说明和参考入口见 [`docs/sources.md`](docs/sources.md)。

欢迎通过 Issue 提供兼容性反馈；提交新素材时请说明来源与许可。详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## English introduction

Evanescia Codex Pet is an unofficial Evanescia-inspired companion and appearance kit. It includes an animated v2 pet with 9 motion states and 16 gaze directions, two importable color themes, a flower-decorated web preview, and a portable local installer. Native pet display was verified on one Windows Codex build; decorative buttons and video backgrounds belong to the separate web preview. Code is MIT-licensed; fan-art assets have separate noncommercial terms and retain third-party character rights.
