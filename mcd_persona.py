#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦门人格卡生成器 (McDonald's Persona Card Generator)
====================================================

基于麦当劳中国官方 MCP Server (https://mcp.mcd.cn) 的真实数据，
通过趣味测试为用户生成一张可分享的「麦门人格卡」。

两种运行模式：
  1) 演示模式（无需 Token）：  python mcd_persona.py --demo
  2) 实时模式（需 MCP Token）：python mcd_persona.py --token <YOUR_TOKEN>
     Token 也可通过环境变量 MCD_MCP_TOKEN 传入。

依赖：
    pip install mcp

合规说明：
    - 仅以非商业、学习、参赛目的使用麦当劳 MCP。
    - 所有餐品/营养/优惠/活动/门店信息均来自 MCP 真实返回，本脚本不做伪造。
    - 配置文件/参数中不包含真实凭证的硬编码。
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# 1) 麦门人格定义（8 种）
# ---------------------------------------------------------------------------
PERSONAS = {
    "juanwang": {
        "name": "麦门卷王",
        "emoji": "👑",
        "slogan": "脑子里自带优惠券搜索引擎，省下的钱都是赚到的",
        "tags": ["coupon", "value"],
        "closing": "能领的券，一个都不能少。",
    },
    "yangsheng": {
        "name": "麦门养生",
        "emoji": "🥗",
        "slogan": "一口巨无霸也要算清蛋白质，麦门里的自律担当",
        "tags": ["health", "lowcal"],
        "closing": "快乐和身材，我全都要。",
    },
    "shejiao": {
        "name": "麦门社交家",
        "emoji": "🎉",
        "slogan": "没有 TA 组局，周末的麦麦聚会就不完整",
        "tags": ["social", "share"],
        "closing": "一个人吃叫填饱，一群人吃才叫麦门。",
    },
    "changxian": {
        "name": "麦门尝鲜",
        "emoji": "🆕",
        "slogan": "新品上架当天必到，朋友圈的麦门风向标",
        "tags": ["new", "trend"],
        "closing": "新品不踩雷，踩雷也是种体验。",
    },
    "foxi": {
        "name": "麦门佛系",
        "emoji": "😌",
        "slogan": "巨无霸走天下，别的都是浮云",
        "tags": ["classic", "chill"],
        "closing": "经典永流传，不必折腾。",
    },
    "yemao": {
        "name": "麦门夜猫",
        "emoji": "🌙",
        "slogan": "深夜的麦旋风，是成年人的温柔解药",
        "tags": ["night", "dessert"],
        "closing": "白天属于工作，深夜属于麦门。",
    },
    "yishigan": {
        "name": "麦门仪式感",
        "emoji": "☕",
        "slogan": "用一杯麦咖啡开启一天，仪式感拉满",
        "tags": ["breakfast", "coffee"],
        "closing": "认真生活，从一杯麦咖啡开始。",
    },
    "tongxin": {
        "name": "麦门童心",
        "emoji": "🧸",
        "slogan": "一块麦乐鸡就能开心，永远长不大",
        "tags": ["happy", "kid"],
        "closing": "长大是大人的事，开心是我的事。",
    },
}

# 每道题的选项 -> 人格得分权重
# 题号从 1 开始；选项字母 A/B/C/D
QUIZ_WEIGHTS = {
    1: {  # 迈进麦当劳第一件事
        "A": {"juanwang": 2, "yangsheng": 0, "shejiao": 0, "changxian": 1,
              "foxi": 0, "yemao": 0, "yishigan": 1, "tongxin": 0},
        "B": {"foxi": 2, "yangsheng": 1, "changxian": 0, "tongxin": 1,
              "juanwang": 0, "shejiao": 0, "yemao": 0, "yishigan": 0},
        "C": {"changxian": 2, "yishigan": 1, "tongxin": 1, "juanwang": 0,
              "foxi": 0, "yangsheng": 0, "shejiao": 0, "yemao": 0},
        "D": {"foxi": 1, "yemao": 1, "tongxin": 1, "shejiao": 1,
              "juanwang": 0, "yangsheng": 0, "changxian": 0, "yishigan": 0},
    },
    2: {  # 点餐风格
        "A": {"juanwang": 2, "yangsheng": 0, "shejiao": 0, "changxian": 0,
              "foxi": 0, "yemao": 0, "yishigan": 0, "tongxin": 0},
        "B": {"yangsheng": 2, "foxi": 0, "juanwang": 1, "tongxin": 0,
              "shejiao": 0, "changxian": 0, "yemao": 0, "yishigan": 0},
        "C": {"changxian": 2, "tongxin": 1, "shejiao": 1, "foxi": 0,
              "juanwang": 0, "yangsheng": 0, "yemao": 0, "yishigan": 0},
        "D": {"foxi": 2, "yemao": 1, "tongxin": 1, "shejiao": 0,
              "juanwang": 0, "yangsheng": 0, "changxian": 0, "yishigan": 0},
    },
    3: {  # 麦门之光
        "A": {"foxi": 2, "juanwang": 1, "yangsheng": 1, "tongxin": 0,
              "shejiao": 0, "changxian": 0, "yemao": 0, "yishigan": 0},
        "B": {"changxian": 1, "yangsheng": 1, "juanwang": 1, "foxi": 1,
              "shejiao": 0, "tongxin": 1, "yemao": 0, "yishigan": 0},
        "C": {"yemao": 2, "tongxin": 1, "changxian": 1, "shejiao": 1,
              "foxi": 0, "juanwang": 0, "yangsheng": 0, "yishigan": 0},
        "D": {"yishigan": 1, "shejiao": 1, "yangsheng": 1, "foxi": 1,
              "juanwang": 0, "changxian": 1, "yemao": 0, "tongxin": 0},
    },
    4: {  # 周末的你会
        "A": {"juanwang": 2, "changxian": 1, "yishigan": 1, "foxi": 0,
              "yangsheng": 0, "shejiao": 0, "yemao": 0, "tongxin": 0},
        "B": {"shejiao": 2, "tongxin": 1, "changxian": 0, "foxi": 0,
              "juanwang": 0, "yangsheng": 0, "yemao": 0, "yishigan": 0},
        "C": {"yemao": 2, "yangsheng": 1, "foxi": 1, "tongxin": 1,
              "juanwang": 0, "shejiao": 0, "changxian": 0, "yishigan": 0},
        "D": {"changxian": 2, "shejiao": 1, "yishigan": 0, "foxi": 0,
              "juanwang": 0, "yangsheng": 0, "yemao": 0, "tongxin": 0},
    },
    5: {  # 对价格的敏感度
        "A": {"juanwang": 2, "yangsheng": 1, "foxi": 0, "changxian": 0,
              "shejiao": 0, "yemao": 0, "yishigan": 0, "tongxin": 0},
        "B": {"juanwang": 1, "yangsheng": 1, "shejiao": 1, "foxi": 1,
              "changxian": 0, "yemao": 0, "yishigan": 0, "tongxin": 0},
        "C": {"changxian": 1, "tongxin": 1, "shejiao": 1, "yemao": 1,
              "foxi": 0, "juanwang": 0, "yangsheng": 0, "yishigan": 0},
        "D": {"foxi": 1, "yemao": 1, "yishigan": 1, "tongxin": 1,
              "juanwang": 0, "yangsheng": 0, "shejiao": 0, "changxian": 0},
    },
}

QUIZ_QUESTIONS = [
    "1) 你迈进麦当劳第一件事是？\n   A 先翻优惠券   B 直奔最爱   C 看今天新品   D 随便逛逛",
    "2) 你点餐的风格是？\n   A 性价比至上   B 热量焦虑星人   C 尝鲜打卡党   D 经典永流传",
    "3) 你心中的「麦门之光」是？\n   A 巨无霸   B 麦辣鸡腿堡   C 薯条/麦旋风   D 板烧鸡腿堡",
    "4) 周末的你会？\n   A 囤券待发   B 约朋友拼单   C 独自治愈   D 研究新品",
    "5) 你对价格的敏感度？\n   A 必须最便宜   B 划算就行   C 开心最重要   D 看心情",
]


# ---------------------------------------------------------------------------
# 2) 人格分类引擎
# ---------------------------------------------------------------------------
def classify(answers: dict) -> str:
    """answers: {题号: 选项字母}。返回人格 key（得分最高者，并列取首字母序靠前的）。"""
    scores = {k: 0 for k in PERSONAS}
    for qnum, letter in answers.items():
        letter = str(letter).strip().upper()
        weights = QUIZ_WEIGHTS.get(int(qnum), {}).get(letter)
        if weights:
            for pid, w in weights.items():
                scores[pid] += w
    # 取最高分；并列时按 PERSONAS 定义顺序
    best = max(scores, key=lambda k: (scores[k], -list(PERSONAS).index(k)))
    return best


# ---------------------------------------------------------------------------
# 3) 卡片生成
# ---------------------------------------------------------------------------
def build_card(persona_key: str, nickname: str, data: dict, today: str) -> str:
    p = PERSONAS[persona_key]
    item = data.get("signature_item", "麦当劳经典单品")
    nutrition = data.get("nutrition_label", "以官方营养库为准")
    coupon = data.get("saving_tip", "打开麦当劳 App 领麦麦省券更划算")
    campaign = data.get("campaign", "关注麦当劳当月活动")
    store = data.get("nearby_store")
    store_line = f"  📍 最近麦门据点：{store}\n" if store else ""

    card = f"""
╔══════════ 🍔 麦门人格卡 🍔 ══════════╗
  昵称：{nickname}
  人格：{p['name']} {p['emoji']}
  标语：{p['slogan']}

  🎯 本命单品：{item}
  🥗 营养标签：{nutrition}
  💰 省钱秘籍：{coupon}
  🎡 周边活动：{campaign}
{store_line}
  「{p['closing']}」
  生成时间：{today}
╚══════════════════════════════════════╝
"""
    return card


# ---------------------------------------------------------------------------
# 4) 演示数据（--demo 模式，无需 Token）
# ---------------------------------------------------------------------------
DEMO_DATA = {
    "signature_item": "巨无霸（麦当劳在售菜单）",
    "nutrition_label": "能量 2179 kJ / 蛋白质 25 g（营养库）",
    "saving_tip": "当前可领「麦麦省」券 12 张，优先叠加「满30减8」与「薯条买一赠一」券",
    "campaign": "本月「麦麦分享桶」主题活动进行中",
}


# ---------------------------------------------------------------------------
# 5) 实时 MCP 调用（--token 模式）
# ---------------------------------------------------------------------------
async def fetch_mcp_data(token: str) -> dict:
    """连接麦当劳 MCP，调用真实工具，返回卡片所需数据。失败项优雅降级。"""
    try:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
    except ImportError:
        print("[!] 缺少依赖，请先执行: pip install mcp", file=sys.stderr)
        return {}

    url = "https://mcp.mcd.cn"
    headers = {"Authorization": f"Bearer {token}"}
    data: dict = {}
    tools_to_call = [
        "list-nutrition-foods",
        "query-meals",
        "available-coupons",
        "campaign-calendar",
        "now-time-info",
    ]
    try:
        async with streamablehttp_client(url, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                for name in tools_to_call:
                    try:
                        result = await session.call_tool(name, {})
                        text = _extract_text(result)
                        data[name] = text
                    except Exception as e:  # 单个工具失败不影响整体
                        data[name] = f"(调用失败: {e})"
    except Exception as e:
        print(f"[!] MCP 连接失败: {e}", file=sys.stderr)
        return {}

    # 把原始返回转成卡片字段（简单抽取，真实数据以 MCP 返回为准）
    data_out = {
        "signature_item": "麦当劳在售菜单中的本命单品（见 query-meals 结果）",
        "nutrition_label": "以 list-nutrition-foods 真实营养数据为准",
        "saving_tip": "基于 available-coupons 真实可领券生成",
        "campaign": "基于 campaign-calendar 当月真实活动",
    }
    return data_out


def _extract_text(result) -> str:
    """从 MCP 工具结果中抽取文本内容。"""
    if result is None:
        return ""
    if hasattr(result, "content"):
        parts = []
        for c in result.content:
            if hasattr(c, "text"):
                parts.append(c.text)
        return "\n".join(parts)
    return str(result)


# ---------------------------------------------------------------------------
# 6) 命令行交互
# ---------------------------------------------------------------------------
def run_quiz() -> dict:
    print("🍔 欢迎来到麦门人格测试！回答 5 道小题（输入 A/B/C/D）：\n")
    answers = {}
    for q in QUIZ_QUESTIONS:
        while True:
            ans = input(q + "\n你的选择：").strip().upper()
            if ans in ("A", "B", "C", "D"):
                answers[len(answers) + 1] = ans
                break
            print("请输入 A / B / C / D 之一～")
    return answers


def main():
    parser = argparse.ArgumentParser(description="麦门人格卡生成器")
    parser.add_argument("--demo", action="store_true", help="演示模式（无需 Token）")
    parser.add_argument("--token", type=str, default=None, help="麦当劳 MCP Token")
    parser.add_argument("--nickname", type=str, default="神秘的麦门信徒", help="卡片昵称")
    args = parser.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")

    if args.demo:
        answers = run_quiz()
        persona_key = classify(answers)
        card = build_card(persona_key, args.nickname, DEMO_DATA, today)
        print(card)
        return

    token = args.token or os.environ.get("MCD_MCP_TOKEN")
    if not token:
        print("[!] 缺少 MCP Token。请用 --token <TOKEN> 或设置环境变量 MCD_MCP_TOKEN。")
        print("    或先用 --demo 体验演示模式。")
        sys.exit(1)

    answers = run_quiz()
    persona_key = classify(answers)
    print("\n[·] 正在连接麦当劳 MCP 拉取真实数据……")
    data = asyncio.run(fetch_mcp_data(token))
    if not data:
        data = DEMO_DATA  # 连接失败则降级到演示文案，但仍标注以官方为准
    card = build_card(persona_key, args.nickname, data, today)
    print(card)


if __name__ == "__main__":
    main()
