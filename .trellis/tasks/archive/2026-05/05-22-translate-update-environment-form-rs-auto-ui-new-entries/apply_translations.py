#!/usr/bin/env python3
"""Apply 30 update_environment_form.rs auto_ui translations and glossary additions
for the settings-update-env-form batch (6th in settings_view series).
"""
import json
import datetime
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
STRINGS = REPO / "translations" / "strings.json"
GLOSSARY = REPO / "translations" / "glossary.json"
BATCH_FLAG = "pr-settings-update-env-form-batch"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# 30 entries: status=new + audit.verdict=auto_ui + occurrence in update_environment_form.rs
TRANSLATIONS = {
    # ---- Form header / button labels ----
    # L478 ActionButton "Delete environment"
    "01KQXQV12AP6DP970XF906VPZK": "删除环境",
    # L840 submit-button "Create environment"
    "01KQXQV12APJ1JCMPXJ8PGGV1N": "创建环境",
    # L1740 header title "Edit environment"
    "01KQXQV12BX8B1NAZX8V454BJT": "编辑环境",
    # L1657 inline link "Share with team"
    "01KQXQV12FMQZBQ92HAZ79GJ96": "与团队共享",

    # ---- Basic form fields ----
    # L267 docker_image_label "Docker image"
    "01KS2GEQ31YHRK679C0QMR8ZMT": "Docker 镜像",
    # L271 setup_commands_helper (orchestration modal)
    "01KS2GEQF82H082R1H0ES9P6QW": "按 Enter 或点击提交按钮以添加每条命令。",
    # L280 default name_placeholder
    "01KQXQV12BZ0D62V33Y66889D4": "环境名称",
    # L283 docker_image_label default "Docker image reference"
    "01KQXQV12BK7QNBW7PW24KB33V": "Docker 镜像引用",
    # L287 default setup_commands_helper (long)
    "01KQXQV12FQ7JEK933RCHPDYQN": (
        "设置命令将各自独立运行。每条命令均从工作区根目录（/workspace）执行。"
        "若某条命令依赖前一条，请使用 && 将它们组合。"
    ),
    # L369 DESCRIPTION_PLACEHOLDER
    "01KQXQV12JH6P9KS1AA71R0P8S": "例如，此环境适用于所有专注于前端的 Agent",
    # L1866 form label "Setup command(s)"
    "01KQXQV12FFA57P0CSR42J52X9": "设置命令",

    # ---- GitHub repos selection ----
    # L265 orchestration_modal repos_placeholder_authed
    "01KS2GEPRPX577TTYK0HJ6YQMZ": "浏览 GitHub 仓库……",
    # L370 REPOS_PLACEHOLDER_AUTHED
    "01KQXQV12BXG4CAT5X329AK99Z": "输入仓库（owner/repo 格式）",
    # L371 REPOS_PLACEHOLDER_UNAUTHED
    "01KQXQV12EKFBFDQSNVJRQ3NFQ": "粘贴仓库 URL",
    # L2119 button "Auth with GitHub"
    "01KQXQV129PNP1MBZRDKXGYPEF": "通过 GitHub 授权",
    # L2476 helper text
    "01KQXQV12HYQAN43263H80T5X2": "输入 owner/repo 并按 Enter 添加，或从下拉列表中选择。",
    # L2502 inline question "Missing a repo?"
    "01KQXQV12DRMY37PN03DF196WD": "缺少某个仓库？",
    # L2520 link "Configure access on GitHub"
    "01KQXQV12A7EXA85KHJCH3AN07": "在 GitHub 上配置访问权限",
    # L2689 empty-state "No repositories found"
    "01KQXQV12DWAZH4KKNM385PBYJ": "未找到仓库",

    # ---- Docker image suggestion ----
    # L2974 tooltip "Open image at {docker_hub_url}"
    "01KQXQV12ES2YZ7C7GRW7HK5T0": "在 {docker_hub_url} 打开镜像",
    # L3100 button "Suggest image"
    "01KQXQV12GKJ3D9VMX9P313A7G": "建议镜像",
    # L3103 tooltip
    "01KQXQV12HV4PDDZ03TVVGTRPC": "Warp 将基于您选择的仓库建议 Docker 镜像。",
    # L3230 warning-box message
    "01KQXQV12JSS8WB1DZ6J93PMW6": "您需要授予对 GitHub 仓库的访问权限，Warp 才能建议 Docker 镜像。",
    # L3265 warning-box "We couldn't find a good match..."
    "01KQXQV12H1XTJMBC4DWABPAES": "我们未能找到合适的匹配。建议为这些仓库使用自定义 Docker 镜像。",

    # ---- Error / warning messages ----
    # L1362 dropdown load-error message
    "01KS2GEQ0KRPSJ5VXZQ28DRKEK": "无法加载 GitHub 仓库。您可以粘贴仓库 URL，或重试。",
    # L1562 error_message "Failed to suggest a Docker image"
    "01KQXQV12BZCGMQQJDBYS0PK66": "建议 Docker 镜像失败",
    # L1575 "Unknown response from suggestCloudEnvironmentImage"
    "01KQXQV12HSXMP1BE6TVJ2H8FV": "suggestCloudEnvironmentImage 返回未知响应",
    # L1589 format!("Failed to suggest a Docker image: {}", e)
    "01KQXQV12B1D74SDRGFRJHPCA5": "建议 Docker 镜像失败：{}",
    # L1694 long warning message
    "01KQXQV12EEWE5MDZ01KW1CEK5": (
        "个人环境不能与外部集成或团队 API 密钥一同使用。"
        "为获得最佳体验，请使用共享环境。"
    ),
    # L2167 fallback error "Failed to load GitHub repositories"
    "01KQXQV12BZ48QPGTBJWXQW09Q": "加载 GitHub 仓库失败",
}

NEW_GLOSSARY_TERMS = {
    "docker_image": {
        "en": "Docker image",
        "zh": "Docker 镜像",
        "notes": "Environment 配置中的容器镜像。'Docker image' → 'Docker 镜像'；'Docker image reference' → 'Docker 镜像引用'；'Suggest image' → '建议镜像'；'custom Docker image' → '自定义 Docker 镜像'。'Docker' 保留英文产品名。与 'base_image / 基础镜像' 区分：base image 是 environment 的基础层，docker image 是 environment 整体可指向的镜像引用。",
        "do_not_translate": False,
    },
    "github_repos": {
        "en": "GitHub repos",
        "zh": "GitHub 仓库",
        "notes": "GitHub 仓库的简写形式 'repos'。'GitHub repos' / 'GitHub repositories' → 'GitHub 仓库'；'Browse GitHub repos' → '浏览 GitHub 仓库'；'Auth with GitHub' → '通过 GitHub 授权'；'Configure access on GitHub' → '在 GitHub 上配置访问权限'。沿用 repository 词族；'GitHub' 保留英文产品名。",
        "do_not_translate": False,
    },
    "workspace_root": {
        "en": "workspace root",
        "zh": "工作区根目录",
        "notes": "Setup commands 的工作目录基准。'workspace root' → '工作区根目录'；'/workspace' 路径字面值保留不译。",
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
        # Skip if inside a placeholder — but our placeholders don't contain ...
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


def main():
    check_invariants()

    data = json.loads(STRINGS.read_text())
    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}

    missing = [k for k in TRANSLATIONS if k not in by_id]
    assert not missing, f"Missing IDs: {missing}"
    assert len(TRANSLATIONS) == 30, f"Expected 30 entries, got {len(TRANSLATIONS)}"

    # Placeholder integrity check before write
    for eid, target in TRANSLATIONS.items():
        err = check_placeholders(by_id[eid], target)
        if err:
            print(f"ERROR {eid}: {err}")
            sys.exit(1)

    updated = 0
    for eid, target in TRANSLATIONS.items():
        e = by_id[eid]
        assert e["status"] == "new", f"{eid} not new: {e['status']}"
        assert e.get("audit", {}).get("verdict") == "auto_ui", f"{eid} not auto_ui"
        files = {o.get("file") for o in e.get("occurrences", [])}
        assert "app/src/settings_view/update_environment_form.rs" in files, (
            f"{eid} no update_environment_form occurrence: {files}"
        )
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
