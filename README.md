# 🍔 麦门人格卡 · McDonald's Persona Card

> 用**麦当劳中国官方 MCP 真实数据**，测出你的「麦门人格」，并附专属省钱方案、周边活动与就近门店——一张卡，看懂你是哪种麦门信徒。

[![基于麦当劳MCP](https://img.shields.io/badge/基于-麦当劳%20MCP-FFC72C?style=flat&logo=github&logoColor=white)](https://github.com/M-China/mcd-mcp-server)
[![WorkBuddy Skill](https://img.shields.io/badge/形态-WorkBuddy%20Skill-00A1EA?style=flat)](https://www.workbuddy.cn)
[![参赛项目](https://img.shields.io/badge/参赛-麦当劳程序员创意开发大赛-DA291C?style=flat)](https://github.com/M-China/mcd-developer-innovation-challenge)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat)](LICENSE)

---

## ✨ 这是什么？

「麦门人格卡」是一个把**麦当劳中国 MCP 能力**包装成**全民向趣味测试**的创意项目。

你只需要回答 5 道超轻量的选择题（或随口描述一下自己），它就会：

1. 🧠 判定你是 **8 种麦门人格**中的哪一种（卷王 / 养生 / 社交家 / 尝鲜 / 佛系 / 夜猫 / 仪式感 / 童心）
2. 🍟 从**真实在售菜单**里挑出你的「本命单品」
3. 🥗 用**真实营养数据**给你贴营养标签
4. 💰 用**真实优惠券**给你定制「省钱秘籍」
5. 🎡 用**真实当月活动**推荐「周边活动」
6. 📍 用**真实附近门店**告诉你「最近麦门据点」

最后生成一张**可截图、可一键复制、可直接发朋友圈/小红书**的精美人格卡。

> 所有数据 100% 来自麦当劳官方 MCP 接口，**零编造、零硬编码**。

---

## 🎭 麦门人格图鉴

| 人格 | Emoji | 一句话人设 |
|---|---|---|
| 麦门卷王 | 👑 | 脑子里自带优惠券搜索引擎，省下的钱都是赚到的 |
| 麦门养生 | 🥗 | 一口巨无霸也要算清蛋白质，麦门里的自律担当 |
| 麦门社交家 | 🎉 | 没有 TA 组局，周末的麦麦聚会就不完整 |
| 麦门尝鲜 | 🆕 | 新品上架当天必到，朋友圈的麦门风向标 |
| 麦门佛系 | 😌 | 巨无霸走天下，别的都是浮云 |
| 麦门夜猫 | 🌙 | 深夜的麦旋风，是成年人的温柔解药 |
| 麦门仪式感 | ☕ | 用一杯麦咖啡开启一天，仪式感拉满 |
| 麦门童心 | 🧸 | 一块麦乐鸡就能开心，永远长不大 |

---

## 🖼️ 效果示例（演示卡片）

```
╔══════════ 🍔 麦门人格卡 🍔 ══════════╗
  昵称：阿麦
  人格：麦门卷王 👑
  标语：脑子里自带优惠券搜索引擎，省下的钱都是赚到的

  🎯 本命单品：巨无霸（来自麦当劳在售菜单）
  🥗 营养标签：能量 2179 kJ / 蛋白质 25 g（来自营养库）
  💰 省钱秘籍：当前可领「麦麦省」券 12 张，优先用「满30减8」+ 你的「薯条买一赠一」券
  🎡 周边活动：本月「麦麦分享桶」主题活动进行中
  📍 最近麦门据点：XX 路餐厅（来自附近门店）

  「能领的券，一个都不能少。」
  生成时间：2026-10-10
╚══════════════════════════════════════╝
```

> 真实运行时，上述每一项都会替换为你账号下的**实时数据**。

---

## 🚀 快速开始

### 方式一：WorkBuddy（推荐，零代码，还能拿积分奖励）

1. 在 [mcd.cn](https://open.mcd.cn/mcp) 用手机号申请 **麦当劳 MCP Token**（教程见 [`GUIDE_MCP_TOKEN.md`](GUIDE_MCP_TOKEN.md)）。
2. 打开 WorkBuddy → 左侧「专家·技能·连接器」→「连接器」→「自定义连接器」→「配置 MCP」，粘贴 [`mcp-config.example.json`](mcp-config.example.json) 并把 `${MCD_MCP_TOKEN}` 换成你的 Token。
3. 启用 `mcd-mcp` 连接器。
4. 把 [`SKILL.md`](SKILL.md) 导入为你的 Skill，或直接在对话框说：**「测一下我的麦门人格」**，AI 会调用麦当劳 MCP 生成你的专属卡片。

### 方式二：Python 命令行（开发者）

```bash
pip install mcp
# 演示模式（无需 Token，用内置示例数据）
python mcd_persona.py --demo

# 实时模式（拉取你的真实数据，Token 可用参数或环境变量传入）
export MCD_MCP_TOKEN="你的Token"
python mcd_persona.py --token "$MCD_MCP_TOKEN"
```

---

## 📂 项目结构

| 文件 | 说明 |
|---|---|
| `README.md` | 项目介绍（本文件） |
| `SKILL.md` | WorkBuddy Skill 定义，零代码即可用 |
| `MCP_INTEGRATION.md` | 实际使用的 MCP Server / Tool / 调用流程 / 业务价值 |
| `mcp-config.example.json` | 脱敏 MCP 配置示例（仅环境变量占位符） |
| `mcd_persona.py` | Python 源码（含 `--demo` 演示模式） |
| `CONTEST_DECLARATION.md` | 参赛声明（官方原文，未改动） |
| `workbuddy.md` | WorkBuddy 对话上下文（参与专项积分奖励） |
| `GUIDE_MCP_TOKEN.md` | MCP Token 申请手把手教程 |
| `GUIDE_WORKBUDDY_RUN.md` | 在 WorkBuddy 里跑起来、生成第一张卡片的教程 |
| `GUIDE_SUBMIT.md` | GitHub 建仓 / 上传 / Issue 报名教程 |
| `GUIDE_PROMOTE.md` | Star 拉人气推广作战方案 |

---

## 🏆 参赛信息

- 参赛赛事：[麦当劳程序员创意开发大赛](https://github.com/M-China/mcd-developer-innovation-challenge)
- 本项目**真实使用**麦当劳中国 MCP（`mcd-mcp`，`https://mcp.mcd.cn`）。
- 仅以非商业、学习、参赛目的使用麦当劳 MCP，遵守其《使用条款》与《MCP 服务规则》。

---

## ⚠️ 免责声明

本项目为麦当劳程序员节创意开发大赛**参赛作品**，由作者独立开发，**非麦当劳官方产品**。项目输出仅供参考，不构成医疗、营养或专业建议；餐品信息、价格、优惠及供应状态**以麦当劳官方渠道实时结果为准**。

---

<p align="center">🍟 测测你的麦门人格，然后 star 一下吧 👉 <a href="https://github.com/M-China/mcd-developer-innovation-challenge">麦当劳程序员创意开发大赛</a></p>
