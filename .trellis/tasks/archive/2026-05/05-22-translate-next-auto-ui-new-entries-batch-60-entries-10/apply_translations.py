#!/usr/bin/env python3
"""Apply batch-10 translations (60 entries) to translations/strings.json.

Files cleared (55 unique files; 60 entries):
  - 5 two-entry files: pane/welcome_view.rs, notebooks/link.rs,
    external_secrets/mod.rs, notebooks/notebook/details_bar.rs,
    warp_completer/signatures/testing/legacy.rs (DO_NOT_TRANSLATE — test fixture).
  - 50 single-entry leaves spanning ai/auth/banner/chip/code/coding/context_chips/
    drive/editor/env_vars/notebooks/pane_group/plugin/prompt/remote_server/
    resource_center/reward/search/settings/settings_view/tab_configs/terminal/
    themes/view_components + 1 wgpu debug label (DO_NOT_TRANSLATE).

Special handling:
  - WGPU_DEBUG_LABEL_IDS (1): wgpu texture debug label (developer-only).
    target=None + flags=[batch_flag, do_not_translate, wgpu_debug_label].
  - TEST_FIXTURE_IDS (2): test signature fixtures in `crates/warp_completer/src/
    signatures/testing/{legacy,v2}.rs`, never user-facing (used in unit tests).
    target=None + flags=[batch_flag, do_not_translate, test_fixture].

Invariants:
  - placeholders preserved exactly (positional {} and named {e}/{name}/{e:?}/{editor}).
  - <keybinding> custom placeholder preserved verbatim (runtime-substituted by
    `text.replace("<keybinding>", &keystroke.displayed())` in ai/agent_tips.rs).
  - whitespace single-direction (preserve src leading/trailing space presence).
  - brand/path/JSON-literal verbatim (Warp, Warp on Web, Oz, Agent, MCP, Docker,
    YAML, Java, java, git).
  - ASCII `...` -> `……` (1 occurrence: '+ Add new repo...').
  - `'…'` -> `『…』` (1 occurrence: `'/'` -> `『/』`).
  - `"…"` -> `「…」` (paragraph_placeholder has none in batch).
"""

from __future__ import annotations
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STRINGS_PATH = ROOT / "translations" / "strings.json"
CANDIDATES = Path(__file__).resolve().parent / "candidates.json"

BATCH_FLAG = "pr-long-tail-ui-leaves-ai-auth-code-settings-terminal-batch"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- translations -----------------------------------------------------------

TRANSLATIONS: dict[str, str | None] = {
    # ====== app/src/pane_group/pane/welcome_view.rs (2) ======
    # `Add repository` is the EditableBinding action label for "open a folder as a repo".
    "01KQXQV129YE5SV2X0SFG65NCY": "添加仓库",
    # `New tab` here labels the PaneConfiguration of the welcome view (the freshly-opened tab).
    "01KQXQV12DWNATNY8DP90KAS8T": "新建标签页",

    # ====== app/src/notebooks/link.rs (2) ======
    # Secondary action title + tooltip on a notebook directory link.
    "01KQXQV12DDCRKH4YF8RJXZTV2": "新会话",
    "01KQXQV12EXFSBZ214R8DYQ7CJ": "在此目录中打开新的终端会话",

    # ====== app/src/external_secrets/mod.rs (2) ======
    # InvalidPlatform branch — when external-secret backend isn't supported on this OS.
    "01KQXQV12EZHDB4HX2CJ2GR16Q": "平台不受支持",
    # `{}` is the backend display name (e.g. "1Password"). Keep positional placeholder.
    "01KQXQV12JAFW2RET2GTWW19N1": "{} 未返回任何机密信息（可能未配置或未通过认证）",

    # ====== app/src/notebooks/notebook/details_bar.rs (2) ======
    "01KQXQV12G0D94MTASCJ3B1557": "登录以编辑",
    # `{editor}` is the named placeholder for the editor's display name.
    "01KQXQV12JFMEE7JN5211E4T19": "{editor} 正在编辑",

    # ====== crates/warp_completer/src/signatures/testing/legacy.rs (2) ======
    # DO_NOT_TRANSLATE — these are test-fixture Signature objects used only by
    # unit tests of the warp_completer crate; never displayed to users.
    "01KQXQV12DD16TNDK158CBP5SJ": None,  # "Launch a java application"
    "01KQXQV12JNKJG2HMK0YGZMAHH": None,  # "the stupid content tracker" (git tagline)

    # ====== app/src/ai/agent_tips.rs (1) ======
    # `<keybinding>` is replaced at runtime with the user's actual keystroke.
    # Preserve the literal "<keybinding>" tag exactly.
    "01KQXQV12CSTW7ZM6BXAVMFYMR": "按住 <keybinding> 可直接向 Agent 朗读您的提示词。",

    # ====== app/src/ai/ambient_agents/mod.rs (1) ======
    "01KQXQV12EAT3JZ6ZKZKADPBGA": "积分不足。请升级您的 Warp 套餐以继续运行云端 Agent。",

    # ====== app/src/ai/artifacts/mod.rs (1) ======
    # Screenshot artifact load-failure description shown in the lightbox.
    "01KQXQV12B3FNZNMTDKT02HB1X": "加载失败",

    # ====== app/src/ai/conversation_details_panel.rs (1) ======
    # `Oz` is a Warp product (cloud agent). Keep verbatim.
    "01KQXQV12H4F64EQMQ1YT7YMH0": "在 Oz 网页应用中查看此次运行",

    # ====== app/src/ai/execution_profiles/editor/mod.rs (1) ======
    "01KQXQV12E6J0T8261C86J0HHV": "Profile 编辑器",

    # ====== app/src/ai/facts/view/mod.rs (1) ======
    "01KQXQV12J8GPMAJA2T0738VRM": "您已离线。部分规则将以只读方式显示。",

    # ====== app/src/auth/auth_view_shared_helpers.rs (1) ======
    # Auth modal header when offline mode is active.
    "01KQXQV12H9SVCYQ5QTEGXY8SE": "正在以离线模式使用 Warp",

    # ====== app/src/auth/mod.rs (1) ======
    # Log-out modal button when there are long-running processes.
    "01KQXQV12GE2WJJHTM7SZ85BAC": "显示正在运行的进程",

    # ====== app/src/banner/view.rs (1) ======
    "01KQXQV12B29CTTYFFPR1Q1PZH": "不再向我显示",

    # ====== app/src/chip_configurator/modal_shell.rs (1) ======
    "01KQXQV12E4MNDMW3RMP26KSAH": "恢复默认",

    # ====== app/src/code/editor/nav_bar.rs (1) ======
    # `Hunk:` label in diff editor nav bar.
    "01KQXQV12CCJQ62V1YQJPMTPKF": "差异块：",

    # ====== app/src/code/footer.rs (1) ======
    # Restart language-server button in code editor footer.
    "01KQXQV12ETWGSCWZ695BH0J2J": "重启服务器",

    # ====== app/src/code/local_code_editor.rs (1) ======
    "01KQXQV12BYVJDHJD8MEZCG9QX": "丢弃此版本",

    # ====== app/src/coding_entrypoints/project_buttons.rs (1) ======
    "01KQXQV12AWVXA1NZXXB4XF3F6": "创建新项目",

    # ====== app/src/context_chips/current_prompt.rs (1) ======
    # `Copy {chip.title()}` — copy the chip value (e.g., "Copy file path").
    # `{}` is positional. Keep at end (Chinese verb-object order).
    "01KQXQV12AR8PY9NRSFM4MXNZK": "复制 {}",

    # ====== app/src/drive/workflows/ai_assist.rs (1) ======
    "01KQXQV12GXPGZEKGRG28JG57E": "出错了，请再试一次。",

    # ====== app/src/editor/autosuggestion_ignore_view.rs (1) ======
    # Autosuggestion overlay tooltip.
    "01KQXQV12C9J5R9QFER0N1PKRC": "忽略此建议",

    # ====== app/src/env_vars/view/fixed_view_components.rs (1) ======
    "01KQXQV12E40PQDKX5VBK3DBPE": "从回收站恢复环境变量",

    # ====== app/src/notebooks/editor/block_insertion_menu.rs (1) ======
    "01KQXQV12CEV403SQG6G9RFQZT": "插入命令块",

    # ====== app/src/pane_group/pane/get_started_view.rs (1) ======
    # EditableBinding action label opening a new terminal session.
    "01KQXQV12GTM7E3H5Y6TA1Y1VY": "终端会话",

    # ====== app/src/pane_group/pane/view/header/sharing.rs (1) ======
    # Tooltip on share button when conversation is local-only. Preserve `\n`
    # newline and `Settings > Privacy` literal path.
    "01KQXQV12GBWQGSHRKR37GCXK8": "此对话无法分享，因为它未存储在云端。\n要同步至云端并分享，请在「设置」 > 「隐私」中启用相应设置，然后重新发起一次请求。",

    # ====== app/src/plugin/host/native/service_impl.rs (1) ======
    # `{e:?}` is Debug formatting of the error. Preserve verbatim.
    "01KQXQV12BR2R3YFXS1P2H047P": "执行失败：{e:?}",

    # ====== app/src/prompt/editor_modal.rs (1) ======
    # Label for "same line" prompt-line style.
    "01KQXQV12F77EVSADBBG5JJ588": "单行提示符",

    # ====== app/src/remote_server/unix/mod.rs (1) ======
    # gRPC error response when reply could not be delivered. `{e}` is the error.
    "01KRNVKAHP6X6DJWZB6WMHTKY3": "无法送达响应：{e}",

    # ====== app/src/resource_center/main_page.rs (1) ======
    "01KQXQV12DX5JAF61C5KM4N0ZY": "全部标记为已读",

    # ====== app/src/reward_view.rs (1) ======
    # Referral reward CTA button (BUTTON_CTA).
    "01KQXQV12HY1G02NQWC1DMVR6J": "去体验！",

    # ====== app/src/search/external_secrets/view.rs (1) ======
    "01KQXQV12FWHBNN91SCSCW99ND": "搜索机密信息",

    # ====== app/src/search/notebook_embedding/notebooks/notebook_search_item.rs (1) ======
    "01KQXQV12D14D490A426HC4CRV": "对其他用户不可见",

    # ====== app/src/search/notebook_embedding/view.rs (1) ======
    "01KQXQV12FKQXKHXDPQ92RPSHD": "搜索引用",

    # ====== app/src/search/slash_command_menu/static_commands/bindings.rs (1) ======
    # `{}` is the slash command name (e.g. "/feedback").
    "01KQXQV12GAMCYJJKD7RFRXHK9": "斜杠命令：{}",

    # ====== app/src/search/slash_command_menu/static_commands/commands.rs (1) ======
    # `/continue-locally` slash command description.
    "01KS2GEPZFKZ2SNVWY5R9QK9ZA": "在本地继续此云端对话",

    # ====== app/src/settings/ai.rs (1) ======
    # DefaultSessionMode::DockerSandbox display label.
    "01KQXQV12DK9N5D3YWRBBBDEK0": "本地 Docker 沙箱",

    # ====== app/src/settings/import/iterm_parser.rs (1) ======
    # Imported iTerm profile description label. `{name}` named placeholder.
    "01KQXQV12E1GJRGTZKQTP0STK4": "配置文件：{name}",

    # ====== app/src/settings_view/appearance_page.rs (1) ======
    # `.expect("Cursor does not exist")` panic when cursor enum index out of range.
    "01KQXQV12AAYJXHVJ0JYES5AP9": "光标不存在",

    # ====== app/src/settings_view/billing_and_usage/usage_history_model.rs (1) ======
    "01KQXQV12BJQ1DDCRH4S1A5X0R": "获取对话用量失败",

    # ====== app/src/settings_view/billing_and_usage_page.rs (1) ======
    "01KS2GEPXVXH0WJWVHY8APJVAS": "请联系团队管理员购买附加积分。",

    # ====== app/src/settings_view/custom_inference_modal.rs (1) ======
    # Endpoint editing modal Save button.
    "01KQXQV12FM0QMHQBF2XV44TTB": "保存",

    # ====== app/src/settings_view/features/startup_shell.rs (1) ======
    # Custom-shell executable path input placeholder.
    "01KQXQV12BK5KK5B8PRDFF171Z": "可执行文件路径",

    # ====== app/src/settings_view/pane_manager.rs (1) ======
    # `.expect("Window should have corresponding settings view")` panic.
    "01KQXQV12J15JGA4N071MZBCKE": "窗口应有对应的设置视图",

    # ====== app/src/settings_view/platform/expire_api_key_button.rs (1) ======
    "01KQXQV12BG7YE73MAGJB8QEJD": "删除 API 密钥失败。请再试一次。",

    # ====== app/src/settings_view/privacy_page.rs (1) ======
    # Lowercased name for the safe-mode toggle pair lookup; existing
    # `Secret redaction` (capitalised) -> 保密信息脱敏. Keep same Chinese.
    "01KQXQV12JH96FDFWJWAJSESV0": "保密信息脱敏",

    # ====== app/src/settings_view/settings_file_footer.rs (1) ======
    "01KQXQV12CSKHKXXYW6F8GM2SG": "用 Oz 修复",

    # ====== app/src/tab_configs/action_sidecar.rs (1) ======
    # Tooltip when this action is already the default.
    "01KQXQV129V5WWB7TQVYZDDFX5": "已是默认",

    # ====== app/src/tab_configs/branch_picker.rs (1) ======
    # Source already uses unicode ellipsis '…' (…). Preserve verbatim.
    "01KQXQV12CXKAXZ0D29QMPBWNY": "正在获取分支…",

    # ====== app/src/tab_configs/repo_picker.rs (1) ======
    # Source uses ASCII `...` — convert to '……' per project convention.
    "01KQXQV128GWRY9RFMCEKNHV43": "+ 添加新仓库……",

    # ====== app/src/terminal/shared_session/mod.rs (1) ======
    "01KQXQV12FB4XKYZKK1SYDVBQ7": "分享链接已复制",

    # ====== app/src/terminal/shared_session/share_modal/denied_body.rs (1) ======
    "01KQXQV12H0E6FZGNRCZ7MFHDJ": "查看套餐",

    # ====== app/src/themes/theme_chooser.rs (1) ======
    "01KQXQV12DS1J28R6DT4YVGKZ0": "未找到匹配的主题！",

    # ====== app/src/view_components/filterable_dropdown.rs (1) ======
    "01KQXQV12DQY59HQFQWDKQ8KGQ": "未找到匹配项。",

    # ====== crates/warpui/src/rendering/wgpu/texture_with_bind_group.rs (1) ======
    # DO_NOT_TRANSLATE — wgpu TextureDescriptor.label (developer/profiler-only debug label).
    "01KQXQV12CXMZ9YCS71XZSFN0R": None,  # "Glyph atlas texture"
}

# DO_NOT_TRANSLATE buckets ----------------------------------------------------

TEST_FIXTURE_IDS: set[str] = {
    "01KQXQV12DD16TNDK158CBP5SJ",  # Launch a java application
    "01KQXQV12JNKJG2HMK0YGZMAHH",  # the stupid content tracker
}

WGPU_DEBUG_LABEL_IDS: set[str] = {
    "01KQXQV12CXMZ9YCS71XZSFN0R",  # Glyph atlas texture
}

DO_NOT_TRANSLATE_IDS: set[str] = TEST_FIXTURE_IDS | WGPU_DEBUG_LABEL_IDS

assert len(TRANSLATIONS) == 60, f"expected 60, got {len(TRANSLATIONS)}"
assert all(
    TRANSLATIONS[eid] is None for eid in DO_NOT_TRANSLATE_IDS
), "DO_NOT_TRANSLATE_IDS must have None target in TRANSLATIONS"

# --- invariants -------------------------------------------------------------

PLACEHOLDER_RE = re.compile(r"\{[^{}]*\}")
STRFTIME_RE = re.compile(r"%-?[A-Za-z%]")

# Brand/literals that must remain verbatim if present in source.
BRAND_LITERALS = [
    "Warp on Web",
    "Warp",
    "Oz",
    "MCP",
    "Agent",
    "GitHub",
    "Docker",
    "YAML",
    "<keybinding>",
    # NOTE: Settings > Privacy is translated to 「设置」 > 「隐私」 in target,
    # following existing translation precedent — do NOT enforce verbatim.
]


def placeholders(s: str) -> list[str]:
    return sorted(PLACEHOLDER_RE.findall(s))


def strftime_codes(s: str) -> list[str]:
    return sorted(STRFTIME_RE.findall(s))


def check_invariants(src: str, tgt: str, eid: str) -> list[str]:
    problems: list[str] = []
    src_ph = placeholders(src)
    tgt_ph = placeholders(tgt)
    if src_ph != tgt_ph:
        problems.append(f"placeholders differ: src={src_ph} vs tgt={tgt_ph}")

    src_strf = strftime_codes(src)
    tgt_strf = strftime_codes(tgt)
    if src_strf != tgt_strf:
        problems.append(f"strftime directives differ: src={src_strf} vs tgt={tgt_strf}")

    # whitespace single-direction
    if src.startswith(" ") != tgt.startswith(" "):
        problems.append("leading whitespace mismatch")
    if src.endswith(" ") != tgt.endswith(" "):
        problems.append("trailing whitespace mismatch")
    if src.startswith("\n") != tgt.startswith("\n"):
        problems.append("leading newline mismatch")
    if src.endswith("\n") != tgt.endswith("\n"):
        problems.append("trailing newline mismatch")
    if src.count("\n") != tgt.count("\n"):
        problems.append(f"newline count differs: src={src.count(chr(10))} tgt={tgt.count(chr(10))}")

    # brand literals: each brand literal that appears in source must remain in target.
    # Skip 'git' if source only contains it as part of a larger English word (not the case here).
    for brand in BRAND_LITERALS:
        if brand in src and brand not in tgt:
            problems.append(f"brand literal {brand!r} missing in target")

    # ASCII '...' should not appear in target (project convention: convert to '……').
    if "..." in tgt:
        problems.append("'...' still in target (should be '……')")

    # <keybinding> literal — protected via BRAND_LITERALS above.

    return problems


def main() -> int:
    with STRINGS_PATH.open() as f:
        data = json.load(f)

    cands = json.loads(CANDIDATES.read_text())
    cand_ids = {c["id"] for c in cands}
    assert set(TRANSLATIONS.keys()) == cand_ids, (
        f"Translation keys != candidates: missing={cand_ids - TRANSLATIONS.keys()}, "
        f"extra={TRANSLATIONS.keys() - cand_ids}"
    )

    entries = data["entries"]
    by_id = {e["id"]: e for e in entries}
    missing = [eid for eid in TRANSLATIONS if eid not in by_id]
    if missing:
        print("missing ids:", missing, file=sys.stderr)
        return 1

    pre_translated = sum(1 for e in entries if e["status"] == "translated")
    pre_snapshot = {
        e["id"]: (e.get("target"), e["status"])
        for e in entries
        if e["status"] == "translated"
    }

    errors: list[str] = []
    applied = 0
    for eid, tgt in TRANSLATIONS.items():
        entry = by_id[eid]
        if entry["status"] != "new":
            errors.append(f"{eid}: status not 'new' (got {entry['status']!r})")
            continue
        if entry.get("audit", {}).get("verdict") != "auto_ui":
            errors.append(f"{eid}: verdict not 'auto_ui'")
            continue
        src = entry["source"]

        if eid in DO_NOT_TRANSLATE_IDS:
            if tgt is not None:
                errors.append(f"{eid}: DO_NOT_TRANSLATE_IDS must have None target, got {tgt!r}")
                continue
            entry["target"] = None
            entry["status"] = "translated"
            flags = entry.get("flags") or []
            for flag in (BATCH_FLAG, "do_not_translate"):
                if flag not in flags:
                    flags.append(flag)
            if eid in WGPU_DEBUG_LABEL_IDS and "wgpu_debug_label" not in flags:
                flags.append("wgpu_debug_label")
            if eid in TEST_FIXTURE_IDS and "test_fixture" not in flags:
                flags.append("test_fixture")
            entry["flags"] = flags
            entry["updated_at"] = NOW
            applied += 1
            continue

        if tgt is None:
            errors.append(f"{eid}: tgt is None but eid not in DO_NOT_TRANSLATE_IDS")
            continue

        problems = check_invariants(src, tgt, eid)
        if problems:
            errors.append(f"{eid}: {problems}\n  src={src!r}\n  tgt={tgt!r}")
            continue

        entry["target"] = tgt
        entry["status"] = "translated"
        flags = entry.get("flags") or []
        if BATCH_FLAG not in flags:
            flags.append(BATCH_FLAG)
        entry["flags"] = flags
        entry["updated_at"] = NOW
        applied += 1

    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1

    # Post-mutation: pre_snapshot byte-identical
    for eid, (prev_target, prev_status) in pre_snapshot.items():
        e = by_id[eid]
        if e.get("target") != prev_target or e["status"] != prev_status:
            print(f"ERROR: prior translated entry mutated: {eid}", file=sys.stderr)
            return 1

    status_counter = Counter(e["status"] for e in entries)
    md = data.setdefault("metadata", {})
    stats = md.setdefault("stats", {})
    stats["new"] = status_counter.get("new", 0)
    stats["translated"] = status_counter.get("translated", 0)
    stats["fuzzy"] = status_counter.get("fuzzy", 0)
    stats["approved"] = status_counter.get("approved", 0)
    stats["obsolete"] = status_counter.get("obsolete", 0)
    md["entry_count"] = len(entries)
    md["last_changed_at"] = NOW

    STRINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"applied {applied}/60 translations")
    print(f"stats: {dict(status_counter)}")
    print(f"pre_translated={pre_translated} -> post_translated={status_counter.get('translated', 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
