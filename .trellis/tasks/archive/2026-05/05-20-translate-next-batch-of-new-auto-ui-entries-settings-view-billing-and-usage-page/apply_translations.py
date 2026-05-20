#!/usr/bin/env python3
"""Apply 62 billing_and_usage_page.rs auto_ui translations + glossary additions."""
import json
import datetime
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-billing-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TRANSLATIONS = {
    # ---- leading-space tail fragments (concat after link/button) ----
    # L3186 " for security features like SSO and automatically applied zero data retention."
    "01KQXQV120BWD7K03BQA47MN7X": "以获取 SSO 等安全功能与自动启用的零数据保留策略。",
    # L3220 " for more credits and access to more models."
    "01KQXQV120Q3EJM0N2YDDGZT1J": "以获取更多积分以及更多模型访问权限。",
    # L3177 " for more AI credits."
    "01KQXQV120T2FT45QC5XJF25KH": "以获取更多 AI 积分。",
    # L3137 " for a more flexible pricing model."
    "01KQXQV120TR84GR1P5R38W7D4": "以获得更灵活的定价方案。",
    # L3153 " for increased access to AI features."
    "01KQXQV120VV2X83JBPTPYCQ75": "以扩大 AI 功能的访问权限。",
    # L3195 " for custom limits and dedicated support."
    "01KQXQV120VV7W0J6H6ZPWW3BQ": "以获取自定义限额与专属支持。",
    # L2131 " to continue."
    "01KQXQV126WSZ0TBQF5JHV078J": "以继续使用。",
    # L1700 " to purchase add-on credits."
    "01KQXQV12762CP6Z0SN8J1ZH74": "以购买附加积分。",
    # L3118 " to regain access to AI features."
    "01KQXQV127GHR9B5HX07NNCHF4": "以恢复 AI 功能访问权限。",

    # ---- top-of-file constants (warnings, headers, descriptions) ----
    # L84 "View details on overage usage"
    "01KQXQV12HB0S75NE55KQK317Y": "查看超额使用详情",
    # L85 "Enable premium model usage overages"
    "01KQXQV12BZ9Z7J6JJC9BD2E0E": "启用高级模型超额使用",
    # L86 "Premium model usage overages are enabled"
    "01KQXQV12E22SA98TPZKV3HP6Q": "已启用高级模型超额使用",
    # L87 "Premium model usage overages are not enabled"
    "01KQXQV12ECB64CKB8S1WGHZHG": "未启用高级模型超额使用",
    # L88 OVERAGE_TOGGLE_DESCRIPTION
    "01KQXQV12AM8BNCG00YG29E6N0": "在超出套餐限额后继续使用高级模型。用量按每 $20 一档计费，直至达到您的支出限额；任何剩余余额将在预定的计费日扣款。",
    # L90 "Ask a team admin to enable overages for more AI usage."
    "01KQXQV129KQ89V0PC1EPCQEE8": "请联系团队管理员启用超额使用以获得更多 AI 用量。",
    # L94 "Usage ascending"
    "01KQXQV12HVN28JKDK6GE6CDHJ": "用量升序",
    # L95 "Usage descending"
    "01KQXQV12HCCPTATVPM4X9AF8M": "用量降序",
    # L98 AUTO_RELOAD_EXCEED_LIMIT_WARNING_STRING
    "01KQXQV129JAHVRGDC4KS8HSAS": "下次充值将超出您的月度支出限额，自动充值已停用。请提高限额以启用自动充值。",
    # L100 AUTO_RELOAD_DELINQUENT_WARNING_STRING
    "01KQXQV12E0D7Z74C6HXGRE3PP": "因账单问题受限。请更新付款方式以购买附加积分。",
    # L102 RESTRICTED_BILLING_USAGE_WARNING_STRING
    "01KQXQV1290ETBG6DG8FXXMS51": "由于最近一次自动充值失败，已停用自动充值。请更新您的付款方式后重试。",
    # L105 "Usage History"
    "01KQXQV12HPSQA3TNPT8ZG1DAZ": "用量历史",
    # L107 "Usage reporting is currently limited"
    "01KQXQV12HMAX6EK1SGWBJ4Z2C": "用量报告当前受限",
    # L109 ENTERPRISE_USAGE_CALLOUT_BODY_ADMIN_PREFIX
    "01KQXQV12B6DB04ZR8PFSTGXEV": "当前视图尚未完整支持企业版积分用量。如需最准确的支出跟踪，请",
    # L113 ENTERPRISE_USAGE_CALLOUT_BODY_NON_ADMIN
    "01KQXQV12B7SNWNW74EGN3E4E1": "当前视图尚未完整支持企业版积分用量。请联系团队管理员获取详细用量报告。",
    # L115 ADDON_CREDITS_DESCRIPTION
    "01KQXQV129T9W57J6GTTEQKS99": "附加积分以预付套餐形式购买，可在每个计费周期内结转，自购买起一年后过期。购买越多，单位积分价格越优惠。基础套餐积分用完后，将开始消耗附加积分。",
    # L117 ADDITIONAL_ADDON_CREDITS_DESCRIPTION_FOR_TEAM
    "01KQXQV12ECFNJ8N527K1XPBEX": "购买的附加积分将在团队内共享。",
    # L120 "Cloud agent trial"
    "01KQXQV129JTE39KFRT6R79ENR": "云端 Agent 试用",

    # ---- buttons / labels / short UI ----
    # L281 "Overage spending limit"
    "01KQXQV12EXTA8KKSN4M07PB4H": "超额支出限额",
    # L305 "Monthly spending limit"
    "01KQXQV12D25VW9FTFQR28CEVA": "月度支出限额",
    # L333 "Load more"
    "01KQXQV12DVGR0DVEABSWC8ZAS": "加载更多",
    # L429 "Failed to update workspace settings"
    "01KQXQV12BK7R57F99AFG6VSA1": "更新工作区设置失败",
    # L442 "Successfully purchased add-on credits"
    "01KQXQV12GE80XV5PH1XTQX3YF": "附加积分购买成功",
    # L1079 "Upgrade Plan"
    "01KQXQV12H8WD45B61FSG39JRF": "升级套餐",
    # L1170 "New agent"
    "01KQXQV12DDFM44R3VB6CY1PMS": "新建 Agent",
    # L1207 "Buy more"
    "01KQXQV1296X2M2YK39YYDV92V": "购买更多",
    # L1399 "Not set"
    "01KQXQV12DT6TZRZTWKXT5A4VS": "未设置",
    # L1409 "Sets the monthly overage spending limit beyond the plan amount"
    "01KQXQV12F0RE7FESV36T6ASG5": "设置套餐额度之外的月度超额支出限额",
    # L1415 "Monthly overage spending limit"
    "01KQXQV12DAJRYT12AA6XCHPRG": "月度超额支出限额",
    # L1644 "Add-on credits"
    "01KQXQV129CY67JRNM53N4VSQ6": "附加积分",
    # L1700 "Switch to the Build plan"
    "01KQXQV12G89W0765VB3HX8AKC": "切换至 Build 套餐",
    # L1742 "Contact your Account Executive for more add-on credits."
    "01KQXQV12A268G12B1P2A9TQPV": "请联系您的客户经理以获取更多附加积分。",
    # L1757 "Contact a team admin to purchase add-on credits."
    "01KQXQV12A4VD0XRF4PANHY73M": "请联系团队管理员购买附加积分。",
    # L1814 "Sets the monthly limit spent on add-on credits"
    "01KQXQV12F1Q4XGSCFD6TDN6SK": "设置购买附加积分的月度支出限额",
    # L1829 "Monthly spend limit"
    "01KQXQV12DS9DYWVC8RTR8P7WZ": "月度支出限额",
    # L1859 "Purchased this month"
    "01KQXQV12ERX5NCAWFGEM93AV7": "本月已购买",
    # L1944 "Auto reload"
    "01KQXQV129HG6SAD30RTAWDS2N": "自动充值",
    # L1951 "When enabled, auto reload will automatically purchase {auto_reload_amount} credits when your add-on credit balance reaches 100 credits remaining."
    "01KQXQV12H4V0772C131FT5Y6F": "启用后，当您的附加积分余额降至剩余 100 积分时，自动充值将自动购买 {auto_reload_amount} 积分。",
    # L2105 "One-time purchase"
    "01KQXQV12DE4DARTZMD60PMFJ7": "一次性购买",
    # L2125 "Reloading would exceed your monthly limit. "  (trailing space preserved — followed by another fragment)
    "01KQXQV12EXK7R5RAW8QVTET4F": "本次充值将超出您的月度限额。 ",
    # L2128 "Increase your limit"
    "01KQXQV12CJVMKPF64PAH2AHVY": "提高您的限额",
    # L2203 "Total overages"
    "01KQXQV12HEQGB1ARR547D4NVV": "超额总计",
    # L2230 "Usage resets on {formatted_date}"
    "01KQXQV12HN1X3D1RFVWW0TMFQ": "用量将于 {formatted_date} 重置",
    # L2285 "Your credit limit is prorated because you joined midway through the billing cycle."
    "01KQXQV12JG6Q8W25XHK3FJ5HH": "您的积分限额按比例计算，因为您在计费周期中途加入。",
    # L2286 "This credit limit is prorated because this user joined midway through the billing cycle."
    "01KQXQV12G5P6Z5JZRAN09PGBQ": "该积分限额按比例计算，因为此用户在计费周期中途加入。",
    # L2396 "This is the {refresh_duration} limit of AI credits for your account."
    # NOTE: {refresh_duration} substitutes an English word like "weekly"/"monthly".
    # Per translation-contract §2, do NOT prepend Chinese function-words; keep the placeholder bracketed by neutral context.
    "01KQXQV12GTPXP8FQEB6GR86GV": "这是您账户的 {refresh_duration} AI 积分上限。",
    # L2549 "Last 30 days"
    "01KQXQV12DE06JTGM11MX49537": "最近 30 天",
    # L2662 "No usage history"
    "01KQXQV12DAFXGT998MQS434GH": "暂无用量历史",
    # L2674 "Kick off an agent task to view usage history here."
    "01KQXQV12DRXCR0E7VVCV33KKD": "启动一个 Agent 任务以在此查看用量历史。",
    # L2986 "Team total"
    "01KQXQV12GGMNMVXW59NA73SGA": "团队总计",
    # L3123 "Contact your team admin to resolve billing issues."
    "01KQXQV12A97T9VDC6B43G4F7X": "请联系团队管理员解决账单问题。",
    # L3174 "Upgrade to Max"
    "01KQXQV12H9RH2PG489DR2C494": "升级至 Max",
    # L3192 "Upgrade to Enterprise"
    "01KQXQV12H3MR5ZR0E55TRKD55": "升级至 Enterprise",
}

NEW_GLOSSARY_TERMS = {
    "overage": {
        "en": "overage",
        "zh": "超额",
        "notes": "billing 上下文中的超额使用与计费。'premium model usage overages' → '高级模型超额使用'；'Overage spending limit' → '超额支出限额'；'Total overages' → '超额总计'。",
        "do_not_translate": False,
    },
    "add_on": {
        "en": "add-on",
        "zh": "附加",
        "notes": "billing 上下文中的附加产品。'add-on credits' → '附加积分'；'Purchased add-on credits' → '购买的附加积分'；'add-on package' → '附加套餐'。区别于 plan-internal credits（基础套餐积分）。",
        "do_not_translate": False,
    },
    "billing_cycle": {
        "en": "billing cycle",
        "zh": "计费周期",
        "notes": "订阅计费周期。'midway through the billing cycle' → '计费周期中途'；'roll over each billing cycle' → '在每个计费周期内结转'。",
        "do_not_translate": False,
    },
    "spending_limit": {
        "en": "spending limit",
        "zh": "支出限额",
        "notes": "billing 中的支出上限。'Monthly spending limit' → '月度支出限额'；'Overage spending limit' → '超额支出限额'；'Monthly spend limit' 同义同译。",
        "do_not_translate": False,
    },
    "prorated": {
        "en": "prorated",
        "zh": "按比例计算",
        "notes": "用户中途加入团队/计费周期时的额度计算。'Your credit limit is prorated' → '您的积分限额按比例计算'。",
        "do_not_translate": False,
    },
}


def main():
    data = json.loads(STRINGS.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs: {missing}"

    updated = 0
    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        assert e["status"] == "new", f"{eid} not new: {e['status']}"
        assert e.get("audit", {}).get("verdict") == "auto_ui", f"{eid} not auto_ui"
        e["target"] = target
        e["status"] = "translated"
        flags = e.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        e["flags"] = flags
        e["updated_at"] = NOW
        updated += 1

    stats = data.get("stats") or {}
    status_counts = {"new": 0, "translated": 0, "fuzzy": 0, "obsolete": 0}
    for e in entries:
        status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1
    stats.update({
        "entry_count": len(entries),
        "translated": status_counts["translated"],
        "fuzzy": status_counts["fuzzy"],
        "new": status_counts["new"],
        "obsolete": status_counts.get("obsolete", 0),
    })
    data["stats"] = stats

    STRINGS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated {updated} entries in strings.json")
    print(f"New stats: {stats}")

    g = json.loads(GLOSSARY.read_text())
    added = 0
    for k, v in NEW_GLOSSARY_TERMS.items():
        if k not in g["terms"]:
            g["terms"][k] = v
            added += 1
    g["metadata"]["term_count"] = len(g["terms"])
    GLOSSARY.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {added} glossary terms (total: {g['metadata']['term_count']})")


if __name__ == "__main__":
    main()
