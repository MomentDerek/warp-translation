#!/usr/bin/env python3
"""Apply 36 teams_page.rs + referrals_page.rs auto_ui translations and glossary additions
for the settings-teams-referrals batch (7th in settings_view series).
"""
import json
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-teams-referrals-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

TARGET_FILES = {
    "app/src/settings_view/teams_page.rs",
    "app/src/settings_view/referrals_page.rs",
}

# 36 entries: status=new + audit.verdict=auto_ui + occurrence in teams_page.rs or referrals_page.rs
TRANSLATIONS = {
    # ============================================================
    # teams_page.rs (18 entries) — capacity warnings, CTAs, invite
    # ============================================================
    # L1924 banner headline "Your team is full"
    "01KS2GEQR866ZY5N4YCND15197": "您的团队已满员",
    # L1925 banner headline "You've exceeded your member limit"
    "01KS2GEQQFJJMSBEAMZM4565G8": "您已超出成员上限",
    # L1926 banner headline "Payment past due"
    "01KS2GEQEHAW091HY5V7R6QAPR": "付款逾期",
    # L1927 banner headline "Subscription unpaid"
    "01KS2GEQN33ZBEXT9XWFY8H93H": "订阅未付款",

    # L1939 detail: reached member limit
    "01KS2GEQQNPGNM5RYJSXSP0S56": "您已达到当前套餐的成员上限。",
    # L1941 detail: exceeded member limit (long)
    "01KS2GEQQK1WYB32GH9NNG7EZB": "您已超出当前套餐的成员上限。现有团队成员仍可保留访问权限，但您无法再添加新成员。",
    # L1947 detail: invites restricted (unpaid)
    "01KS2GEQNJTMRPJ47B8KD3CYZM": "因订阅未付款，团队邀请已被限制。",

    # L1959 CTA "Contact a team admin to grow the team."
    "01KS2GEPXFFWH0EENGYRMVZ94G": "请联系团队管理员以扩充团队。",
    # L1963 CTA "Upgrade to grow your team."
    "01KS2GEQPP3RQECYX3ZBM8YYNG": "升级以扩充您的团队。",
    # L1964 CTA "Contact sales to grow your team."
    "01KS2GEPYHZ18KRGY793XCV2HH": "联系销售以扩充您的团队。",
    # L1966 CTA "Update your payment information to restore access."
    "01KS2GEQPH55DQTQYWGZ4G2BKX": "更新您的付款信息以恢复访问。",
    # L1968 CTA "Contact support to restore access."
    "01KS2GEPYVGDAYYNJS1MKEJGJ0": "联系支持以恢复访问。",
    # L2007 button "Contact sales"
    "01KS2GEPY9K4DPADH5QY5SSEP6": "联系销售",

    # L2583 button "Invite team members"
    "01KS2GEQ9C452CCPY298VFQD3T": "邀请团队成员",
    # L2759 tab label "By email"
    "01KS2GEPRY37PJJ6S206ECFRKX": "通过邮件",
    # L3186 tab label "By discovery"
    "01KS2GEPRV79SX3B59FK6BXP4H": "通过发现",

    # L2893 plan capacity (named placeholders {plan_display}, {cap})
    "01KS2GEQR7EHB6VCAW6DKCACX0": "您的套餐（{plan_display}）最多支持 {cap} 位成员。",
    # L2957 inline question with TRAILING SPACE (concatenated with link)
    "01KS2GEQPRV9MAX077VYH9FKNN": "想要扩充您的团队？ ",

    # ============================================================
    # referrals_page.rs (18 entries) — header, gifts, toasts/errors
    # ============================================================
    # L45 page header "Invite a friend to Warp"
    "01KQXQV12C7PXPGZWMY15Q782S": "邀请好友加入 Warp",
    # L46 page subtitle
    "01KQXQV12G91X2DZ4H84SNAA8W": "注册以参与 Warp 推荐计划",
    # L53 toast error
    "01KQXQV12BWYHWC172SDRW74Y5": "加载推荐码失败。",
    # L64 toast "Link copied."
    "01KQXQV12D6JYZ650VCQVZTPNY": "链接已复制。",
    # L65 toast "Successfully sent emails."
    "01KQXQV12G1A2AJK513FAAQXRQ": "邮件发送成功。",
    # L68 marketing copy with trailing "*" footnote marker
    "01KQXQV12CSEYV5XJ5KN926H60": "推荐好友即可获得 Warp 专属周边礼品*",

    # L90 "Current referral"
    "01KQXQV12AW13P7JHDW0XN47C0": "当前推荐",
    # L91 "Current referrals"
    "01KQXQV12ANNWX5WXNKW2KW50T": "当前推荐数",
    # L99 "Certain restrictions apply."
    "01KQXQV129BK347QH0ABCBBQGH": "适用一定限制。",
    # L103 LEADING SPACE preserved (concatenated after another string)
    "01KQXQV110WAM9E2X4RHCAN18B": " 如果您对推荐计划有任何疑问，请联系 referrals@warp.dev。",

    # L158 gift "Exclusive theme"
    "01KQXQV12B9D5MYBVRAD60A5AK": "专属主题",
    # L165 gift "Keycaps + stickers"
    "01KQXQV12D6MDF64K7YFE1BJ3Y": "键帽 + 贴纸",
    # L186 gift "Baseball cap"
    "01KQXQV129RPX4SMMGDKGY25MK": "棒球帽",
    # L200 gift "Premium Hydro Flask" (brand stays English)
    "01KQXQV12EZ9QD0C6KTHS492TY": "Hydro Flask 高端水壶",

    # L339 toast with positional placeholder
    "01KQXQV12GP60H167FHQ7TS8XN": "已成功发送 {} 份邀请",
    # L340 toast with Debug formatter {:?}
    "01KQXQV12GK7R4VY3QYT499A1F": "已成功向以下地址发送邀请：{:?}",
    # L465 validation error
    "01KQXQV12ECRG2VG1XCT0D0J7N": "请输入邮箱地址。",
    # L467 validation error with named placeholder
    "01KQXQV12E1RRBXE8B2GXPB3ET": "请确认以下邮箱地址有效：{invalid_email}",
}

NEW_GLOSSARY_TERMS = {
    "referral": {
        "en": "referral",
        "zh": "推荐",
        "notes": "Warp 推荐计划相关。'referral program' → '推荐计划'；'referral code' → '推荐码'；'Current referral(s)' → '当前推荐 / 当前推荐数'；'Invite a friend' → '邀请好友'。统一译 '推荐'，避免与 'recommend / 推荐' 混淆时按上下文消歧。",
        "do_not_translate": False,
    },
    "upgrade": {
        "en": "upgrade",
        "zh": "升级",
        "notes": "套餐升级动作。'Upgrade to grow your team' → '升级以扩充您的团队'；'Upgrade plan' → '升级套餐'。与 'downgrade / 降级' 对应。",
        "do_not_translate": False,
    },
}


def check_invariants():
    """Enforce full-width punctuation invariant + placeholder integrity."""
    # Forbid half-width sentence punctuation (,.!?:;) immediately after a CJK character
    # — allowed inside placeholders {}, URLs, regex, ASCII identifiers.
    forbidden = re.compile(r"[一-鿿][,.!?:;](?![\w/])")
    problems = []
    for eid, target in TRANSLATIONS.items():
        for m in forbidden.finditer(target):
            problems.append((eid, m.group(0), m.start()))
    if problems:
        print("ERROR: half-width punctuation adjacent to Chinese characters:")
        for eid, frag, pos in problems:
            print(f"  {eid} at pos {pos}: {frag!r}")
        sys.exit(1)

    # Forbid bare "..." in targets (must use "……")
    for eid, target in TRANSLATIONS.items():
        if "..." in target:
            print(f"ERROR {eid}: bare '...' detected; use '……' instead")
            sys.exit(1)


def check_placeholders(src_entry, target):
    """Confirm placeholder count and names match between source and target."""
    src = src_entry.get("source", "")
    src_phs = re.findall(r"\{[^{}]*\}", src)
    tgt_phs = re.findall(r"\{[^{}]*\}", target)
    if sorted(src_phs) != sorted(tgt_phs):
        return f"placeholder mismatch: source={src_phs} target={tgt_phs}"
    return None


def check_whitespace_preservation(src_entry, target):
    """Preserve leading/trailing whitespace from source."""
    src = src_entry.get("source", "")
    if src.startswith(" ") and not target.startswith(" "):
        return "leading-space lost"
    if src.endswith(" ") and not target.endswith(" "):
        return "trailing-space lost"
    return None


def main():
    check_invariants()

    data = json.loads(STRINGS.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs: {missing}"
    assert len(TRANSLATIONS) == 36, f"Expected 36 entries, got {len(TRANSLATIONS)}"

    # Placeholder + whitespace integrity check before write
    for eid, target in TRANSLATIONS.items():
        err = check_placeholders(by_id[eid], target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)
        err = check_whitespace_preservation(by_id[eid], target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)

    updated = 0
    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        assert e["status"] == "new", f"{eid} not new: {e['status']}"
        assert e.get("audit", {}).get("verdict") == "auto_ui", f"{eid} not auto_ui"
        files = {o.get("file") for o in e.get("occurrences", [])}
        assert files & TARGET_FILES, f"{eid} no teams/referrals occurrence: {files}"
        e["target"] = target
        e["status"] = "translated"
        flags = e.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        e["flags"] = flags
        e["updated_at"] = NOW
        updated += 1

    # Recompute stats inside metadata (the canonical location)
    status_counts = {"new": 0, "translated": 0, "fuzzy": 0, "approved": 0, "obsolete": 0, "uncertain": 0}
    for e in entries:
        s = e["status"]
        status_counts[s] = status_counts.get(s, 0) + 1
    # uncertain is verdict-based, not status-based; carry over from prior metadata
    prior_uncertain = data.get("metadata", {}).get("stats", {}).get("uncertain", 0)
    status_counts["uncertain"] = prior_uncertain
    md = data.setdefault("metadata", {})
    md["entry_count"] = len(entries)
    md["stats"] = status_counts
    md["last_changed_at"] = NOW

    STRINGS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated {updated} entries in strings.json")
    print(f"New stats: {status_counts}")

    g = json.loads(GLOSSARY.read_text())
    added = 0
    for k, v in NEW_GLOSSARY_TERMS.items():
        if k not in g["terms"]:
            g["terms"][k] = v
            added += 1
        else:
            print(f"Glossary term '{k}' already exists, skipping")
    g["metadata"]["term_count"] = len(g["terms"])
    GLOSSARY.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {added} glossary terms (total: {g['metadata']['term_count']})")


if __name__ == "__main__":
    main()
