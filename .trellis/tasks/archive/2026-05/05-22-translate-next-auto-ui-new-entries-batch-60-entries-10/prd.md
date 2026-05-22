# Translate next auto_ui new entries — batch 60 entries 10 (Strategy: long-tail leaf-sweep — clear 55 single/double-entry files across ai/auth/banner/chip/code/coding/context_chips/drive/editor/env_vars/notebooks/pane_group/plugin/prompt/remote_server/resource_center/reward/search/settings/settings_view/tab_configs/terminal/themes/view_components + 1 wgpu debug label + 2 test fixtures)

## Goal

清扫 **55 个 auto_ui-new 文件** 共 **60 条**，55 个文件全部清零。本批是 batch-9 之后的尾部清扫：余量 81 → 21（-60），五个二条文件全部清零，加上 50 个单条叶节点。3 条标记 `do_not_translate`（2 条测试夹具 + 1 条 wgpu 调试标签），57 条实际翻译。

| 文件 | 数量 | 说明 |
|---|---|---|
| `app/src/pane_group/pane/welcome_view.rs` | 2 | 欢迎视图（添加仓库 EditableBinding + 标签页配置名） |
| `app/src/notebooks/link.rs` | 2 | 笔记本目录链接二级动作（标题 + tooltip） |
| `app/src/external_secrets/mod.rs` | 2 | 外部机密信息错误（平台不支持 + 后端未返回机密信息） |
| `app/src/notebooks/notebook/details_bar.rs` | 2 | 笔记本协作详情栏（登录提示 + 协作者编辑中） |
| `crates/warp_completer/src/signatures/testing/legacy.rs` | 2 | **DO_NOT_TRANSLATE** — 单元测试签名夹具，永不显示给用户 |
| `app/src/ai/agent_tips.rs` | 1 | Agent tip（语音 prompt，含 `<keybinding>` 运行时替换标记） |
| `app/src/ai/ambient_agents/mod.rs` | 1 | 云端 Agent 积分不足提示 |
| `app/src/ai/artifacts/mod.rs` | 1 | 截图制品加载失败描述 |
| `app/src/ai/conversation_details_panel.rs` | 1 | View in Oz web app tooltip |
| `app/src/ai/execution_profiles/editor/mod.rs` | 1 | Profile 编辑器标题 |
| `app/src/ai/facts/view/mod.rs` | 1 | 规则页离线提示 |
| `app/src/auth/auth_view_shared_helpers.rs` | 1 | 离线模式认证 header |
| `app/src/auth/mod.rs` | 1 | 登出模态长任务进程按钮 |
| `app/src/banner/view.rs` | 1 | 横幅永久关闭按钮 |
| `app/src/chip_configurator/modal_shell.rs` | 1 | Chip 编辑器恢复默认按钮 |
| `app/src/code/editor/nav_bar.rs` | 1 | Diff 导航栏 Hunk 标签 |
| `app/src/code/footer.rs` | 1 | 代码编辑器语言服务器重启按钮 |
| `app/src/code/local_code_editor.rs` | 1 | 丢弃本地代码版本按钮 |
| `app/src/coding_entrypoints/project_buttons.rs` | 1 | 创建项目 EditableBinding |
| `app/src/context_chips/current_prompt.rs` | 1 | 右键菜单 Copy {chip} 项（位置占位符） |
| `app/src/drive/workflows/ai_assist.rs` | 1 | AI 元数据生成通用错误 |
| `app/src/editor/autosuggestion_ignore_view.rs` | 1 | 自动建议忽略 tooltip |
| `app/src/env_vars/view/fixed_view_components.rs` | 1 | 从回收站恢复环境变量 tooltip |
| `app/src/notebooks/editor/block_insertion_menu.rs` | 1 | 插入命令块按钮 tooltip |
| `app/src/pane_group/pane/get_started_view.rs` | 1 | Get Started 终端会话 EditableBinding |
| `app/src/pane_group/pane/view/header/sharing.rs` | 1 | 不可分享对话 tooltip 长文（含 `\n` 换行 + Settings > Privacy 路径） |
| `app/src/plugin/host/native/service_impl.rs` | 1 | JS 函数调用失败（含 `{e:?}` Debug 占位符） |
| `app/src/prompt/editor_modal.rs` | 1 | 单行提示符样式标签 |
| `app/src/remote_server/unix/mod.rs` | 1 | gRPC 错误响应（含 `{e}` 占位符） |
| `app/src/resource_center/main_page.rs` | 1 | 资源中心通知全部标记已读 |
| `app/src/reward_view.rs` | 1 | 推荐主题奖励 CTA |
| `app/src/search/external_secrets/view.rs` | 1 | 机密信息搜索占位符 |
| `app/src/search/notebook_embedding/notebooks/notebook_search_item.rs` | 1 | 笔记本不可见警告 |
| `app/src/search/notebook_embedding/view.rs` | 1 | 引用搜索占位符 |
| `app/src/search/slash_command_menu/static_commands/bindings.rs` | 1 | 斜杠命令绑定描述（含 `{}` 占位符） |
| `app/src/search/slash_command_menu/static_commands/commands.rs` | 1 | `/continue-locally` 命令描述 |
| `app/src/settings/ai.rs` | 1 | DefaultSessionMode::DockerSandbox 显示名 |
| `app/src/settings/import/iterm_parser.rs` | 1 | iTerm 配置文件导入描述（含 `{name}` 命名占位符） |
| `app/src/settings_view/appearance_page.rs` | 1 | `.expect()` panic：光标枚举越界 |
| `app/src/settings_view/billing_and_usage/usage_history_model.rs` | 1 | 对话用量获取失败日志 |
| `app/src/settings_view/billing_and_usage_page.rs` | 1 | 非管理员附加积分提示 |
| `app/src/settings_view/custom_inference_modal.rs` | 1 | 端点保存按钮 |
| `app/src/settings_view/features/startup_shell.rs` | 1 | 自定义 shell 可执行文件路径占位符 |
| `app/src/settings_view/pane_manager.rs` | 1 | `.expect()` panic：窗口缺设置视图 |
| `app/src/settings_view/platform/expire_api_key_button.rs` | 1 | API 密钥删除失败提示 |
| `app/src/settings_view/privacy_page.rs` | 1 | safe-mode toggle binding 查找键（小写 `secret redaction`） |
| `app/src/settings_view/settings_file_footer.rs` | 1 | 用 Oz 修复设置错误按钮 |
| `app/src/tab_configs/action_sidecar.rs` | 1 | "已是默认" tooltip |
| `app/src/tab_configs/branch_picker.rs` | 1 | 分支列表加载占位符（源已用 unicode `…`） |
| `app/src/tab_configs/repo_picker.rs` | 1 | + 添加新仓库 footer（ASCII `...` → `……`） |
| `app/src/terminal/shared_session/mod.rs` | 1 | 会话分享链接复制 toast |
| `app/src/terminal/shared_session/share_modal/denied_body.rs` | 1 | 分享受限模态 View plans 按钮 |
| `app/src/themes/theme_chooser.rs` | 1 | 主题搜索无结果 |
| `app/src/view_components/filterable_dropdown.rs` | 1 | 通用下拉无结果占位符 |
| `crates/warpui/src/rendering/wgpu/texture_with_bind_group.rs` | 1 | **DO_NOT_TRANSLATE** — wgpu Glyph atlas texture 调试标签 |

继 batch-9 之后，auto_ui-new 余量 81 → 21（-60）；`translated` 2160 → 2220，`new` 4522 → 4462，`fuzzy` 保持 52。

## What I already know

- 当前 `strings.json` 统计（应用前）：`entry_count=6734`, `translated=2160`, `new=4522`, `fuzzy=52`。
- glossary 现有 95 条；本批沿用既有术语：`Warp` / `Warp on Web` / `Oz` / `Agent` / `MCP` / `keybinding → 快捷键` / `shell → shell（保留英文）` / `secret → 机密信息`（`secret redaction → 保密信息脱敏` 沿用既有翻译；二者并存）/ `workflow → 工作流` / `notebook → 笔记本` / `prompt → 提示词` / `repository → 仓库` / `session → 会话` / `add-on credits → 附加积分` / `Profile（执行配置）→ Profile（保留品牌词）` / `Hunk → 差异块`。无新增术语，`term_count` 保持 95。
- **占位符**：8 条含位置/命名占位符 —
  - `{}`（external_secrets L246 / context_chips L1368 / search/bindings L34）— 位置
  - `{editor}`（details_bar L191）— 命名
  - `{e:?}`（plugin/service_impl L49）— 命名 + Debug fmt
  - `{e}`（remote_server/unix L225）— 命名
  - `{name}`（iterm_parser L764）— 命名
  - `<keybinding>`（agent_tips L456）— **运行时自定义标记**（非 Rust fmt），由 `text.replace("<keybinding>", &keystroke.displayed())` 在渲染前替换；必须保留字面值。
  
  无 strftime。
- **`.expect` 内部诊断 panic 串（3 条）**：
  - `Cursor does not exist`（settings_view/appearance_page L4341）— 光标 nth 越界
  - `Window should have corresponding settings view`（settings_view/pane_manager L32）— 窗口 ID 查表缺失
  - `Modal button mouse state should be set`（workspace/native_modal L163）— 本批未取，留待 batch-11
  
  本批包含的 2 条 panic（appearance_page、pane_manager）沿用既有 panic 翻译惯例：叙述部分译中文，标识符保留英文。第三条本批未选。
- **DO_NOT_TRANSLATE 分类**（3 条）：
  - **`wgpu_debug_label`**（1 条）：`Glyph atlas texture`（`crates/warpui/src/rendering/wgpu/texture_with_bind_group.rs` L26）— wgpu `TextureDescriptor.label`，仅开发者/性能分析工具可见。沿用 batch-7 wgpu 调试标签处置：`target=null + status=translated + flags=[batch_flag, do_not_translate, wgpu_debug_label]`。
  - **`test_fixture`**（2 条）：`Launch a java application` / `the stupid content tracker`（`crates/warp_completer/src/signatures/testing/legacy.rs` L243 / L91，同条目第二 occurrence 在 `testing/v2.rs`）— `warp_completer` 单元测试用 `Signature` dummy 对象，仅在测试代码内引用，**绝不**渲染给用户。沿用 wgpu 调试标签的处置模板，新增专用 flag `test_fixture`：`target=null + status=translated + flags=[batch_flag, do_not_translate, test_fixture]`。
- **`<keybinding>` (agent_tips L456)**：源 `Hold <keybinding> to speak your prompt directly to the agent.`。`<keybinding>` 是 Warp Agent tips 框架的运行时占位标记，由 `text.replace("<keybinding>", &keystroke.displayed())`（agent_tips.rs L388）在渲染前替换为用户绑定的实际按键串。**必须**逐字保留 `<keybinding>` 字面值。
- **`Settings > Privacy`（pane_group/pane/view/header/sharing.rs L31）**：UI 导航面包屑。既有翻译 `'Visit Settings > Privacy to modify your secret redaction settings.' → '请前往「设置」 > 「隐私」 修改您的密钥脱敏设置。'`，本批沿用同一风格：`Settings > Privacy → 「设置」 > 「隐私」`。
- **`+ Add new repo...` (tab_configs/repo_picker L22)**：源使用 ASCII `...`，按项目惯例转为 `……`。译「+ 添加新仓库……」。
- **`Fetching branches…` (tab_configs/branch_picker L19)**：源已使用 unicode `…`，**直接复用**，不转。译「正在获取分支…」。
- **`This conversation cannot be shared ...\nTo sync to cloud ...` (sharing.rs L31)**：源含字面 `\n`（Rust raw newline in continuation literal），译文严格保留中间的 `\n`，并将前后两句各自完整翻译。
- **`Out of credits` 既有翻译**：`'Out of credits' → '积分不足'`。本批 ambient_agents L22 沿用此译法。

## Scope by file

### app/src/pane_group/pane/welcome_view.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129YE5SV2X0SFG65NCY` | 47 | `Add repository` | `添加仓库` |
| `01KQXQV12DWNATNY8DP90KAS8T` | 74 | `New tab` | `新建标签页` |

### app/src/notebooks/link.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DDCRKH4YF8RJXZTV2` | 59 | `New session` | `新会话` |
| `01KQXQV12EXFSBZ214R8DYQ7CJ` | 60 | `Open a new terminal session in this directory` | `在此目录中打开新的终端会话` |

### app/src/external_secrets/mod.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12EZHDB4HX2CJ2GR16Q` | 254 | `Platform not supported` | `平台不受支持` |
| `01KQXQV12JAFW2RET2GTWW19N1` | 246 | `{} didn't return secrets (likely not configured or authenticated)` | `{} 未返回任何机密信息（可能未配置或未通过认证）` |

### app/src/notebooks/notebook/details_bar.rs (2)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12G0D94MTASCJ3B1557` | 140 | `Sign in to edit` | `登录以编辑` |
| `01KQXQV12JFMEE7JN5211E4T19` | 191 | `{editor} is editing` | `{editor} 正在编辑` |

### crates/warp_completer/src/signatures/testing/legacy.rs (2) — DO_NOT_TRANSLATE

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DD16TNDK158CBP5SJ` | 243 | `Launch a java application` | `null`（test_fixture） |
| `01KQXQV12JNKJG2HMK0YGZMAHH` | 91 | `the stupid content tracker` | `null`（test_fixture） |

### app/src/ai/agent_tips.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CSTW7ZM6BXAVMFYMR` | 456 | `Hold <keybinding> to speak your prompt directly to the agent.` | `按住 <keybinding> 可直接向 Agent 朗读您的提示词。` |

### app/src/ai/ambient_agents/mod.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12EAT3JZ6ZKZKADPBGA` | 22 | `Out of credits. Upgrade your Warp plan to continue running cloud agents.` | `积分不足。请升级您的 Warp 套餐以继续运行云端 Agent。` |

### app/src/ai/artifacts/mod.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12B3FNZNMTDKT02HB1X` | 364 | `Failed to load` | `加载失败` |

### app/src/ai/conversation_details_panel.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H4F64EQMQ1YT7YMH0` | 652 | `View this run in the Oz web app` | `在 Oz 网页应用中查看此次运行` |

### app/src/ai/execution_profiles/editor/mod.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12E6J0T8261C86J0HHV` | 137 | `Profile Editor` | `Profile 编辑器` |

### app/src/ai/facts/view/mod.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12J8GPMAJA2T0738VRM` | 34 | `You are offline. Some rules will be read only.` | `您已离线。部分规则将以只读方式显示。` |

### app/src/auth/auth_view_shared_helpers.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H9SVCYQ5QTEGXY8SE` | 194 | `Using Warp Offline` | `正在以离线模式使用 Warp` |

### app/src/auth/mod.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GE2WJJHTM7SZ85BAC` | 114 | `Show running processes` | `显示正在运行的进程` |

### app/src/banner/view.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12B29CTTYFFPR1Q1PZH` | 179 | `Don't show me again` | `不再向我显示` |

### app/src/chip_configurator/modal_shell.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12E4MNDMW3RMP26KSAH` | 32 | `Restore default` | `恢复默认` |

### app/src/code/editor/nav_bar.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CCJQ62V1YQJPMTPKF` | 155 | `Hunk:` | `差异块：` |

### app/src/code/footer.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12ETWGSCWZ695BH0J2J` | 1201 | `Restart server` | `重启服务器` |

### app/src/code/local_code_editor.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BYVJDHJD8MEZCG9QX` | 2380 | `Discard this version` | `丢弃此版本` |

### app/src/coding_entrypoints/project_buttons.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12AWVXA1NZXXB4XF3F6` | 40 | `Create new project` | `创建新项目` |

### app/src/context_chips/current_prompt.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12AR8PY9NRSFM4MXNZK` | 1368 | `Copy {}` | `复制 {}` |

### app/src/drive/workflows/ai_assist.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GXPGZEKGRG28JG57E` | 75 | `Something went wrong. Please try again.` | `出错了，请再试一次。` |

### app/src/editor/autosuggestion_ignore_view.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12C9J5R9QFER0N1PKRC` | 142 | `Ignore this suggestion` | `忽略此建议` |

### app/src/env_vars/view/fixed_view_components.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12E40PQDKX5VBK3DBPE` | 122 | `Restore environment variables from trash` | `从回收站恢复环境变量` |

### app/src/notebooks/editor/block_insertion_menu.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CEV403SQG6G9RFQZT` | 318 | `Insert block` | `插入命令块` |

### app/src/pane_group/pane/get_started_view.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GTM7E3H5Y6TA1Y1VY` | 41 | `Terminal session` | `终端会话` |

### app/src/pane_group/pane/view/header/sharing.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GBWQGSHRKR37GCXK8` | 31 | `This conversation cannot be shared because it is not stored in the cloud.\nTo sync to cloud and share, enable the setting under Settings > Privacy, and then make another request.` | `此对话无法分享，因为它未存储在云端。\n要同步至云端并分享，请在「设置」 > 「隐私」中启用相应设置，然后重新发起一次请求。` |

### app/src/plugin/host/native/service_impl.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BR2R3YFXS1P2H047P` | 49 | `Failed with error: {e:?}` | `执行失败：{e:?}` |

### app/src/prompt/editor_modal.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12F77EVSADBBG5JJ588` | 602 | `Same line prompt` | `单行提示符` |

### app/src/remote_server/unix/mod.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KRNVKAHP6X6DJWZB6WMHTKY3` | 225 | `Response could not be delivered: {e}` | `无法送达响应：{e}` |

### app/src/resource_center/main_page.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DX5JAF61C5KM4N0ZY` | 436 | `Mark all as read` | `全部标记为已读` |

### app/src/reward_view.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12HY1G02NQWC1DMVR6J` | 32 | `Try it out!` | `去体验！` |

### app/src/search/external_secrets/view.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FWHBNN91SCSCW99ND` | 44 | `Search for a secret` | `搜索机密信息` |

### app/src/search/notebook_embedding/notebooks/notebook_search_item.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12D14D490A426HC4CRV` | 110 | `Not visible to other users` | `对其他用户不可见` |

### app/src/search/notebook_embedding/view.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FKQXKHXDPQ92RPSHD` | 29 | `Search for a reference` | `搜索引用` |

### app/src/search/slash_command_menu/static_commands/bindings.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12GAMCYJJKD7RFRXHK9` | 34 | `Slash command: {}` | `斜杠命令：{}` |

### app/src/search/slash_command_menu/static_commands/commands.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KS2GEPZFKZ2SNVWY5R9QK9ZA` | 455 | `Continue this cloud conversation locally` | `在本地继续此云端对话` |

### app/src/settings/ai.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DK9N5D3YWRBBBDEK0` | 333 | `Local Docker Sandbox` | `本地 Docker 沙箱` |

### app/src/settings/import/iterm_parser.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12E1GJRGTZKQTP0STK4` | 764 | `Profile: {name}` | `配置文件：{name}` |

### app/src/settings_view/appearance_page.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12AAYJXHVJ0JYES5AP9` | 4341 | `Cursor does not exist` | `光标不存在` |

### app/src/settings_view/billing_and_usage/usage_history_model.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BJQ1DDCRH4S1A5X0R` | 132 | `Failed to fetch conversation usage` | `获取对话用量失败` |

### app/src/settings_view/billing_and_usage_page.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KS2GEPXVXH0WJWVHY8APJVAS` | 1745 | `Contact a team admin to purchase add-on credits.` | `请联系团队管理员购买附加积分。` |

### app/src/settings_view/custom_inference_modal.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FM0QMHQBF2XV44TTB` | 838 | `Save` | `保存` |

### app/src/settings_view/features/startup_shell.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BK5KK5B8PRDFF171Z` | 101 | `Executable path` | `可执行文件路径` |

### app/src/settings_view/pane_manager.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12J15JGA4N071MZBCKE` | 32 | `Window should have corresponding settings view` | `窗口应有对应的设置视图` |

### app/src/settings_view/platform/expire_api_key_button.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12BG7YE73MAGJB8QEJD` | 76 | `Failed to delete API key. Please try again.` | `删除 API 密钥失败。请再试一次。` |

### app/src/settings_view/privacy_page.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12JH96FDFWJWAJSESV0` | 2020 | `secret redaction` | `保密信息脱敏` |

### app/src/settings_view/settings_file_footer.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CSKHKXXYW6F8GM2SG` | 252 | `Fix with Oz` | `用 Oz 修复` |

### app/src/tab_configs/action_sidecar.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV129V5WWB7TQVYZDDFX5` | 142 | `Already the default` | `已是默认` |

### app/src/tab_configs/branch_picker.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CXKAXZ0D29QMPBWNY` | 19 | `Fetching branches…` | `正在获取分支…` |

### app/src/tab_configs/repo_picker.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV128GWRY9RFMCEKNHV43` | 22 | `+ Add new repo...` | `+ 添加新仓库……` |

### app/src/terminal/shared_session/mod.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12FB4XKYZKK1SYDVBQ7` | 39 | `Sharing link copied` | `分享链接已复制` |

### app/src/terminal/shared_session/share_modal/denied_body.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12H0E6FZGNRCZ7MFHDJ` | 13 | `View plans` | `查看套餐` |

### app/src/themes/theme_chooser.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DS1J28R6DT4YVGKZ0` | 752 | `No matching themes!` | `未找到匹配的主题！` |

### app/src/view_components/filterable_dropdown.rs (1)

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12DQY59HQFQWDKQ8KGQ` | 563 | `No matches found.` | `未找到匹配项。` |

### crates/warpui/src/rendering/wgpu/texture_with_bind_group.rs (1) — DO_NOT_TRANSLATE

| ID | Line | Source | Translation |
|---|---|---|---|
| `01KQXQV12CXMZ9YCS71XZSFN0R` | 26 | `Glyph atlas texture` | `null`（wgpu_debug_label） |

## Decisions / Anomalies

- **`Add repository` (welcome_view L47)**：EditableBinding action label，与既有 `'Add Repository to Sidebar' → '添加仓库到侧边栏'` 对齐。译「添加仓库」。
- **`New tab` (welcome_view L74)**：PaneConfiguration 默认名。既有 `Create new tab → 新建标签页`、`Create New Tab: {} → 新建标签页：{}`。译「新建标签页」。
- **`{} didn't return secrets ...` (external_secrets L246)**：`{}` 是 SecretBackend 显示名（如 `1Password`/`AWS Secrets Manager`），保留位置占位符。译「{} 未返回任何机密信息（可能未配置或未通过认证）」。
- **`{editor} is editing` (details_bar L191)**：`{editor}` 是命名占位符（编辑者邮箱别名），保留。`is editing` 译「正在编辑」。
- **`Hold <keybinding> to speak ...` (agent_tips L456)**：`<keybinding>` 是 Warp 自定义运行时标记（详见 agent_tips.rs L388 `text.replace("<keybinding>", &keystroke.displayed())`），必须逐字保留 `<keybinding>` 字符串。译「按住 <keybinding> 可直接向 Agent 朗读您的提示词。」。
- **`Out of credits. Upgrade your Warp plan to continue running cloud agents.` (ambient_agents L22)**：与既有 `'Out of credits' → '积分不足'` 对齐前半句；后半「升级 Warp 套餐」沿用 plan glossary。译「积分不足。请升级您的 Warp 套餐以继续运行云端 Agent。」。
- **`View this run in the Oz web app` (conversation_details_panel L652)**：`Oz` 是 Warp 云端 Agent 产品（既有 `View in Oz → 在 Oz 中查看`、`Cloud Oz → Cloud Oz`），保留品牌。译「在 Oz 网页应用中查看此次运行」。
- **`Profile Editor` (execution_profiles L137)**：execution profile 编辑器标题。`Profile` 在 Warp 语境下是品牌词（与终端 Profile 不同），保留英文，与既有 `Manage profiles → 管理 Profile`（本批新增）/ `profile_model_selector` 风格一致。译「Profile 编辑器」。
- **`You are offline. Some rules will be read only.` (facts/view/mod L34)**：rules glossary 译「规则」。译「您已离线。部分规则将以只读方式显示。」。
- **`Using Warp Offline` (auth_view_shared_helpers L194)**：认证模态 header，离线模式登录。译「正在以离线模式使用 Warp」（避免「Warp 离线」歧义）。
- **`Don't show me again` (banner/view L179)**：与既有 `'Don't show again' → '不再显示'` 接近，但本条多一个「me」（更正式）。译「不再向我显示」（保留人称差别）。
- **`Hunk:` (code/editor/nav_bar L155)**：diff 导航栏前缀标签，`hunk` 是 diff 术语指「差异块」。译「差异块：」（中文全角冒号）。
- **`Restart server` (code/footer L1201)**：language server 重启按钮。译「重启服务器」。
- **`Create new project` (project_buttons L40)**：EditableBinding。译「创建新项目」。
- **`Copy {}` (current_prompt L1368)**：上下文菜单 Copy 项，`{}` 是 chip 标题。`复制 + 名词` 自然，译「复制 {}」。
- **`Something went wrong. Please try again.` (drive/workflows/ai_assist L75)**：通用 AiProviderError/Other 文案。与既有 `'Something went wrong. Please try again later.' → '出错了。请稍后再试。'` 接近但无「later」。译「出错了，请再试一次。」（与原文「Please try again」对应「请再试一次」）。
- **`Insert block` (notebooks/editor/block_insertion_menu L318)**：插入「命令块」按钮 tooltip。`block` 在 Warp 语境下译「命令块」（与既有 `block` 术语一致）。译「插入命令块」。
- **`Terminal session` (get_started_view L41)**：GetStartedView 中的「打开新终端会话」EditableBinding label。译「终端会话」。
- **`This conversation cannot be shared ...\nTo sync to cloud ...` (sharing.rs L31)**：长 tooltip 含字面 `\n`。保留 `\n`。`Settings > Privacy` 沿用既有 `「设置」 > 「隐私」` 风格。译「此对话无法分享，因为它未存储在云端。\n要同步至云端并分享，请在「设置」 > 「隐私」中启用相应设置，然后重新发起一次请求。」。
- **`Failed with error: {e:?}` (plugin/service_impl L49)**：`{e:?}` 是 Debug fmt（命名占位符 + 修饰符），逐字保留。译「执行失败：{e:?}」。
- **`Same line prompt` (prompt/editor_modal L602)**：prompt 行样式标签（单行 vs 多行）。译「单行提示符」。
- **`Response could not be delivered: {e}` (remote_server/unix L225)**：gRPC 错误响应 message。`{e}` 是错误显示。译「无法送达响应：{e}」。
- **`Mark all as read` (resource_center/main_page L436)**：通知中心通用动作。译「全部标记为已读」。
- **`Try it out!` (reward_view L32)**：推荐奖励主题 CTA。译「去体验！」（CTA 语气）。
- **`Search for a secret` / `Search for a reference`**：搜索栏占位符。与既有 `'Search for a command' → '搜索命令'` 风格对齐（"搜索 + 宾语"）。译「搜索机密信息」/「搜索引用」。
- **`Not visible to other users` (notebook_search_item L110)**：警告文。译「对其他用户不可见」。
- **`Slash command: {}` (bindings L34)**：斜杠命令 BindingDescription。译「斜杠命令：{}」。
- **`Continue this cloud conversation locally` (commands L455)**：`/continue-locally` 命令描述，与既有 `'Continue this cloud conversation' → '继续此云端会话'` 接近，但添加了 "locally"。译「在本地继续此云端对话」（突出 locally 副词位）。
- **`Local Docker Sandbox` (settings/ai L333)**：DefaultSessionMode label。译「本地 Docker 沙箱」。
- **`Profile: {name}` (iterm_parser L764)**：iTerm 配置文件导入描述。`Profile` 在此 = iTerm Profile（不是 Warp Profile，是 iTerm 术语），译「配置文件」更贴近 iTerm 中文版用语；`{name}` 命名占位符保留。译「配置文件：{name}」。
- **`Cursor does not exist` (appearance_page L4341, `.expect`)**：光标 enum nth 越界 panic。译「光标不存在」。
- **`Failed to fetch conversation usage` (usage_history_model L132)**：报错日志。译「获取对话用量失败」。
- **`Contact a team admin to purchase add-on credits.` (billing_and_usage_page L1745)**：与 batch-9 `'Restricted due to billing issue. Contact your team admin to update their payment method.' → '因账单问题受限。请联系团队管理员更新支付方式。'` 风格对齐。译「请联系团队管理员购买附加积分。」。
- **`Save` (custom_inference_modal L838)**：端点保存按钮，与项目惯例 `Save → 保存` 一致。
- **`Executable path` (startup_shell L101)**：自定义 shell 输入占位符。译「可执行文件路径」。
- **`Window should have corresponding settings view` (pane_manager L32, `.expect`)**：内部 panic。译「窗口应有对应的设置视图」。
- **`Failed to delete API key. Please try again.` (expire_api_key_button L76)**：与既有 `'Failed to delete domain restriction' → '删除域名限制失败'` / `'Failed to delete invite' → '删除邀请失败'` 风格对齐。译「删除 API 密钥失败。请再试一次。」。
- **`secret redaction` (privacy_page L2020)**：小写形式的 toggle binding 查找键（用于 ToggleSettingActionPair 命名）。既有 `Secret redaction → 保密信息脱敏`、`Custom secret redaction → 自定义保密信息脱敏`。译「保密信息脱敏」（保持术语一致；不因大小写差异分译）。
- **`Fix with Oz` (settings_file_footer L252)**：设置错误时用 Oz 修复按钮。译「用 Oz 修复」（保留 Oz 品牌）。
- **`Already the default` (action_sidecar L142)**：tooltip。译「已是默认」。
- **`Fetching branches…` (branch_picker L19)**：源已使用 unicode `…`，**直接复用**。译「正在获取分支…」。
- **`+ Add new repo...` (repo_picker L22)**：源使用 ASCII `...`，按项目惯例转 `……`。译「+ 添加新仓库……」（保留 `+ ` 前缀）。
- **`Sharing link copied` (shared_session/mod L39)**：复制 toast。`Sharing link` 与既有 `Copy session sharing link → 复制会话分享链接` 中的「分享链接」一致。译「分享链接已复制」。
- **`View plans` (share_modal/denied_body L13)**：受限模态 CTA。`plans` glossary → 「套餐」。译「查看套餐」。
- **`No matching themes!` (theme_chooser L752)**：主题搜索无结果。译「未找到匹配的主题！」。
- **`No matches found.` (filterable_dropdown L563)**：通用下拉空状态。译「未找到匹配项。」。
- **`Glyph atlas texture` (texture_with_bind_group L26)**：wgpu `TextureDescriptor.label`，仅 GPU 调试器/性能分析器可见，**不**翻译。`target=null + flags=[batch_flag, do_not_translate, wgpu_debug_label]`，沿用 batch-7 wgpu 处置惯例。
- **`Launch a java application` / `the stupid content tracker` (warp_completer/signatures/testing/legacy L243 / L91)**：`warp_completer` 单元测试 `Signature` dummy 对象（`pub fn git_signature()` / `pub fn java_signature()` 等），仅在测试文件内引用，**绝不**渲染给用户。`target=null + flags=[batch_flag, do_not_translate, test_fixture]`，新增专用 flag `test_fixture` 以区别于 `extractor_false_positive_*` 类（这里不是误提取，确实是源码字面量；只是非用户面）。

## Glossary delta

无新增术语。`term_count` 保持 95。
