#!/usr/bin/env python3
"""Apply 103 teams_page.rs auto_ui translations + 4 glossary additions."""
import json
import datetime
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-teams-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TRANSLATIONS = {
    "01KQXQV127D4E0MW6SFPV3F79X": " 以恢复访问权限。",
    "01KQXQV1283ENWQPMAHK774TG1": "添加域名限制",
    "01KQXQV1291QW76M2C3F971F23": "允许使用 @{domain} 邮箱的 Warp 用户查找并加入团队。",
    "01KQXQV129D5W898RXHS4HZXHH": "作为管理员，您可以选择是否允许团队成员通过邀请链接邀请他人。",
    "01KQXQV129JE1CATP3ZQZ83G7D": "取消邀请",
    "01KQXQV129K8YWH1MWSB38B6GQ": "允许与您使用相同邮箱域名的 Warp 用户查找并加入团队。",
    "01KQXQV129NA9N07Q666KYSEPW": "额外成员按您套餐的人均费率计费。{prorated_message}",
    "01KQXQV129X0M9YTJPXGGJ0BZE": "额外成员按您套餐的人均费率计费：${monthly_cost:.0}/月或 ${yearly_cost:.0}/年，取决于您的计费周期。{prorated_message}",
    "01KQXQV12A03NHX85Q3N1GX2SZ": "删除团队",
    "01KQXQV12A0FCNFPKVPFKNMW0Z": "联系管理员申请访问权限",
    "01KQXQV12A47S0G7E8XZS4ZTRM": "删除域名限制",
    "01KQXQV12A4ETJ3542QMKSVGGE": "删除待处理邮箱邀请",
    "01KQXQV12A97GMY65KXEVAQ2R2": "已删除邀请",
    "01KQXQV12AB3Y4N9KNC57KF087": "联系支持",
    "01KQXQV12AGAVQW3N1NP8AS626": "降为普通成员",
    "01KQXQV12AGSGMR7N4B7HK2BDP": "删除团队",
    "01KQXQV12AHC6KJDHG6PV7QKAB": "创建团队",
    "01KQXQV12AN11K8PNAWPE6TQN3": "创建团队",
    "01KQXQV12B0QNBJ17TD4J2RTZB": "切换邀请链接失败",
    "01KQXQV12B4W6KR8YN7H4GQCVH": "生成账单链接失败。请通过 feedback@warp.dev 联系我们",
    "01KQXQV12B59W6PKQ3DYNS1PDJ": "重置邀请链接失败",
    "01KQXQV12B5BT4QV9D0W2GYP31": "重命名团队失败",
    "01KQXQV12B9VNABNF3Q7S7HHB2": "加载邀请链接失败。",
    "01KQXQV12BBG6FCXCMB6600Z29": "已添加域名限制：{}",
    "01KQXQV12BBRPKS8KDFZP0SSYW": "多个域名，用逗号分隔",
    "01KQXQV12BEN809HQ75M2A6Q8C": "转让团队所有权失败",
    "01KQXQV12BFEE2NQZXMM73X2B8": "发送邀请失败",
    "01KQXQV12BHVHVJC3MQ95P55FH": "加入团队失败",
    "01KQXQV12BJ1D8J9ZRFE1K5DSB": "生成升级链接失败。请通过 feedback@warp.dev 联系我们",
    "01KQXQV12BK32D5XG37N75322R": "邮箱邀请的有效期为 7 天。",
    "01KQXQV12BP36R5K3FVKJJCPP6": "多个邮箱，用逗号分隔",
    "01KQXQV12BP45AQP40X2YSCS30": "删除域名限制失败",
    "01KQXQV12BS9KETVZCGMJH992B": "离开团队出错",
    "01KQXQV12BTZNJ5E3YZQW3610R": "切换团队可发现性失败",
    "01KQXQV12BWKYP8XQECJ4RZTPF": "添加域名限制失败",
    "01KQXQV12BWP7AFD1RTFGFT0BY": "更新团队成员角色失败",
    "01KQXQV12BYBK56DW4VVAF55G1": "删除邀请失败",
    "01KQXQV12C95KSERGT5DYTNYD6": "通过链接邀请",
    "01KQXQV12CCJ52TFYJDY09PW6Y": "无效域名：{}",
    "01KQXQV12CEMCG0J81RA0G92T8": "生成 Stripe 账单门户链接",
    "01KQXQV12CJXRH1AYTPK64TQTC": "生成升级链接",
    "01KQXQV12CK9NSK9NJ5VM2BG9Y": "通过邮箱邀请",
    "01KQXQV12CTV44ZF43WG0XKJ3S": "免费套餐使用限额",
    "01KQXQV12CV2GF9MDQQ9YY4WK9": "无效邮箱：{}",
    "01KQXQV12D4D4FCBCKM8NA2MNT": "打开管理面板",
    "01KQXQV12D5K9C0XY43SPXY3X1": "离开团队",
    "01KQXQV12DA5HV65R8V5JERFDF": "链接已复制到剪贴板！",
    "01KQXQV12DBF42P6VW4R8PN830": "加入此团队，开始协作处理工作流、笔记本等内容。",
    "01KQXQV12DDZ9SGBBTCZ8F5Q7Z": "仅允许使用特定域名邮箱的用户通过邀请链接加入您的团队。",
    "01KQXQV12DFMGDJQ72292MBN2Q": "离开团队",
    "01KQXQV12DVEZF8ZTKWFHMG8YG": "允许团队被发现",
    "01KQXQV12DVMJCJ9NCYQVFGQ6Y": "通过团队发现加入团队",
    "01KQXQV12DX69T1RZXEVCXW8HF": "管理套餐",
    "01KQXQV12E1X2D15PHS3R6K4FG": "将用户移出团队",
    "01KQXQV12E45X8W9RFRK4M937B": "套餐使用限额",
    "01KQXQV12E569C9FRX80SC61JS": "已重置邀请链接",
    "01KQXQV12E7MPC2RC039QKRJCZ": "重置链接",
    "01KQXQV12EABWYGQ10Z889G820": "移出团队",
    "01KQXQV12EB0KKAS9CS5AC3MP9": "按域名限制",
    "01KQXQV12ED4B322SH5BFYBQ2W": "提升为管理员",
    "01KQXQV12EHGYWDG8V54DTZ0CQ": "移除域名",
    "01KQXQV12EM08V3FJBM5MEBDKQ": "打开管理面板",
    "01KQXQV12EN67BNH3E81P95C37": "或者，加入您公司内的现有团队",
    "01KQXQV12EPYQAAZFYMWMJ18XM": "请 ",
    "01KQXQV12FB2QMHX0HNSGAF8P3": "共享工作流",
    "01KQXQV12FHCT92RCFRWN12DEH": "共享笔记本",
    "01KQXQV12FPSYKVJ0GN4YMPXEX": "发送邮箱邀请",
    "01KQXQV12G7M199RMYFZ4X1NQE": "切换团队可发现性",
    "01KQXQV12G888HYRZ07PCD850Y": "由于付款问题，团队邀请已被限制。请联系团队管理员以恢复访问权限。",
    "01KQXQV12G8J3HZAWRSDBXNZAZ": "已成功加入 {}",
    "01KQXQV12G8Q7NKMJGD2JYMKK9": "团队成员",
    "01KQXQV12G9F9091KV54737008": "部分提供的邮箱地址无效、已被邀请或已是团队成员。",
    "01KQXQV12GDR38BB98VCEM7B67": "团队名称",
    "01KQXQV12GQENT6FQMTM7GSZ54": "已成功重命名团队",
    "01KQXQV12GQKX13ETYC379DQVE": "已成功更新团队成员角色",
    "01KQXQV12GRXTY8TPB50P929QZ": "团队成员",
    "01KQXQV12GSAWDEGBNQGF4V06C": "由于付款问题，团队邀请已被限制。请通过 support@warp.dev 联系我们以恢复访问权限。",
    "01KQXQV12GV16EVKMAC8SZT018": "部分提供的域名无效，或已被添加。",
    "01KQXQV12GVVPV253QB3V71NAR": "已成功加入团队",
    "01KQXQV12GXJK7Z9K94WQCX815": "已成功转让团队所有权",
    "01KQXQV12GXTSEVFQ6Q1FY71VQ": "由于订阅付款问题，团队邀请已被限制。",
    "01KQXQV12GZB5B9VGN2GQDNYJ8": "已成功离开团队",
    "01KQXQV12H263XQT1KKGE5DKNP": "升级到 Lightspeed 套餐",
    "01KQXQV12H3PPXZ4F9XN8A42X4": "已切换团队可发现性",
    "01KQXQV12H862RSXF93B3HFX2N": "升级到 Turbo 套餐",
    "01KQXQV12HDRNE58XKJJT5H30M": "转让团队所有权？",
    "01KQXQV12HF54V649FM89VXZXP": "创建团队后，您可以通过共享云端 Agent 运行、环境、自动化和产物，协作开展由 Agent 驱动的开发。您还可以为队友和 Agent 创建共享的知识库。",
    "01KQXQV12HJP5PZ0KV64KW05T7": "升级到 Build",
    "01KQXQV12HM3693JT3KB5SKN55": "转让所有权",
    "01KQXQV12HXYRQ034AZ6R9AEMN": "已切换邀请链接",
    "01KQXQV12J0SEZSS4RBG7HYKTA": "您的邀请已在发送途中！",
    "01KQXQV12J2NFWSC8QKX896KPZ": "您当前处于离线状态。",
    "01KQXQV12J3HJ6F4W12VS0CZDP": "更新您的付款信息",
    "01KQXQV12J68QEDBZ2EHSWP0XK": "您将为该团队成员使用 Warp 的部分费用付款。",
    "01KQXQV12J6RFEQ8EQSKXNZR8B": "您的新团队名称",
    "01KQXQV12J6XKQSARPHG5SK7QA": "您已达到当前套餐的团队成员上限。请联系团队管理员以添加更多成员。",
    "01KQXQV12JA0RHNAQENTMY7SMM": "您已超出当前套餐的团队成员上限。请通过 support@warp.dev 联系我们升级您的团队。",
    "01KQXQV12JD3B4YNH9S1TB11DB": "您已达到当前套餐的团队成员上限。请通过 support@warp.dev 联系我们添加更多成员。",
    "01KQXQV12JDFJPGRWJJVZJ3AFZ": "您的 {} 条邀请已在发送途中！",
    "01KQXQV12JFMHS2M8XYJNVH3SN": "您已超出当前套餐的团队成员上限。升级以添加更多成员。",
    "01KQXQV12JK7P5P311A4HDEP8Z": "您已达到当前套餐的团队成员上限。升级以添加更多成员。",
    "01KQXQV12JMKQHRP63R0SQRR6Q": "您的管理员将为该团队成员使用 Warp 的部分费用付款。",
    "01KQXQV12JW59TVJ0NC0VNCMPA": "您已超出当前套餐的团队成员上限。请联系团队管理员升级您的团队。",
}

NEW_GLOSSARY_TERMS = {
    "admin": {
        "en": "admin",
        "zh": "管理员",
        "notes": "团队管理员角色。'team admin' → '团队管理员'；'admin panel' → '管理面板'；'Demote from admin' → '降为普通成员'；'Promote to admin' → '提升为管理员'。",
        "do_not_translate": False,
    },
    "invite": {
        "en": "invite",
        "zh": "邀请",
        "notes": "团队邀请操作或邀请对象。动词和名词共用 '邀请'。'invite link' → '邀请链接'；'cancel invite' → '取消邀请'；'pending invite' → '待处理邀请'；'email invitation' → '邮箱邀请'。",
        "do_not_translate": False,
    },
    "plan": {
        "en": "plan",
        "zh": "套餐",
        "notes": "订阅套餐计费层级。'Free plan' / 'Build plan' / 'Lightspeed plan' / 'Turbo plan' / 'Enterprise plan' 中 'plan' 译为 '套餐'，计划名（Build/Lightspeed/Turbo 等）保留英文。'Manage plan' → '管理套餐'；'Compare plans' → '比较套餐'。不与作为名词的 'plan'（计划/规划）混；后者出现在 AI/agent 上下文中（'create a plan' → '制定计划'）。",
        "do_not_translate": False,
    },
    "discoverable": {
        "en": "discoverable",
        "zh": "可发现",
        "notes": "Team discovery 功能：是否允许同域用户搜索到团队。'Make team discoverable' → '允许团队被发现'；'team discoverability' → '团队可发现性'；'Toggle Team Discoverability' → '切换团队可发现性'。",
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
        # history left as-is (previous batches kept it empty); flag is the audit trail
        e["updated_at"] = NOW
        updated += 1

    # Update stats
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

    # Update glossary
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
