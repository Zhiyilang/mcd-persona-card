# 🚀 GitHub 建仓 / 上传 / Issue 报名 手把手教程

> 适用：技术小白。全部用 GitHub 网页操作，**不用装任何软件、不用敲命令**。
> 目标：把本文件夹里的所有文件变成一个**公开仓库**，再用一个 Issue 报名参赛。

---

## 一、在 GitHub 创建公开仓库

1. 打开 👉 https://github.com ，登录你的账号（没有就先注册，很简单）。
2. 右上角点 **「+」→「New repository」**（新建仓库）。
3. 填写：
   - **Repository name（仓库名）**：建议用 `mcd-persona-card`（和项目一致，利于被搜到）
   - **Description（描述）**：`🍔 麦门人格卡 · 用麦当劳官方MCP真实数据生成可分享人格卡`
   - **Visibility（可见性）**：务必选 **Public（公开）** ✅（私有仓库无法参赛！）
   - 不要勾选 "Add a README file"（我们已经有了）
4. 点 **「Create repository」**。

## 二、把本文件夹的所有文件上传进去

> 最简单：直接把这些文件**拖进 GitHub 网页**。

1. 进入你刚建好的空仓库页面。
2. 找到并点击 **「uploading an existing file」**（或页面中间的「upload files」）。
3. 打开你电脑上的 `mcd-persona-card` 文件夹，**全选所有文件**，直接**拖拽**到 GitHub 上传区域。
4. 等待上传完成（文件不多，很快）。
5. 页面底部 **Commit changes** 的方框里随便写一句，比如 `init: 麦门人格卡参赛项目`，点 **「Commit changes」**。

### ⚠️ 必须包含的文件（少一个都无法报名成功）

| 文件名 | 是否必须 | 说明 |
|---|---|---|
| `README.md` | ✅ 必须 | 项目介绍（已帮你写好） |
| `CONTEST_DECLARATION.md` | ✅ 必须 | **官方原文，一字不能改**（已原样放入） |
| `MCP_INTEGRATION.md` | ✅ 必须 | MCP 接入说明（已写好） |
| `mcp-config.example.json` | ✅ 必须 | 脱敏配置（仅占位符，已写好） |
| `workbuddy.md` | 拿积分奖励要 | WorkBuddy 对话记录（已写好） |
| `SKILL.md` / `mcd_persona.py` 等 | ✅ 源代码 | 项目主体（已写好） |

> 上传后，在仓库根目录能看到这些文件名，**拼写和大小写都要和上面一致**。

## 三、用 Issue 报名

1. 打开活动主仓库 👉 https://github.com/M-China/mcd-developer-innovation-challenge
2. 点顶部 **「Issues」** 标签 → 点 **「New issue」**。
3. 按下面格式填写（**正文不要超过 1000 字、不要带图片**，否则报名失败）：

```
Issue 标题：麦门人格卡 · 用麦当劳官方MCP生成可分享人格卡

【参赛申请】
项目名称：麦门人格卡
项目地址：https://github.com/Zhiyilang/mcd-persona-card
项目简介：基于麦当劳中国官方MCP真实数据，通过趣味测试为用户生成可分享的「麦门人格卡」，包含本命单品、营养标签、省钱秘籍、周边活动与就近门店，好玩好传播。
```

4. 项目地址已替换为你的仓库链接：`https://github.com/Zhiyilang/mcd-persona-card`（若你改了仓库名请同步修改）。
5. 点 **「Submit new issue」**。

## 四、确认报名成功

- 提交后，**系统会自动在那个 Issue 下回复**。
- 显示「报名成功」= 完成；显示失败原因 = 按提示改完重新提交 Issue 即可。
- 报名成功后，项目只要 **Star 数 > 0** 就会进入排行榜（在活动仓库的 `RANKING.md` 查看）。

---

## ⏰ 关键时间节点（北京时间）

| 节点 | 时间 | 你要做什么 |
|---|---|---|
| 报名截止 | **2026-10-25 23:59** | 务必在此之前完成 Issue 报名 |
| 定榜快照 | **2026-10-26 00:00** | 此刻的累计 Star 数决定最终名次 |
| 信息提交截止 | 2026-11-14 | 中奖后按要求填收货信息/手机号 |

> 💡 也就是说：**你要在 10-25 前尽量多攒真实 Star，10-26 这一刻的 Star 数就是你的成绩。**

---

完成后，立刻看 [`GUIDE_PROMOTE.md`](GUIDE_PROMOTE.md) 学怎么合规地拉 Star 冲一等奖！
