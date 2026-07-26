

# 📐 Uxcel Go iOS 设计截图 —— 全维度视觉风格分析

---

## 1️⃣ 配色方案

| 色彩角色 | HEX 色值 | 使用位置 |
|---|---|---|
| **主色（Primary）** | `#7C5CFF`（蓝紫） | 选中卡片边框、"Start" 气泡标签、底部导航选中图标（毕业帽）、"UX" 字母中的紫色部分、"Intro to Typography" 中的紫色 a 字母 |
| **辅助色（Accent Pink）** | `#FF6B9D`（玫粉） | 等级标签 "A" 圆形徽章背景 |
| **解锁指示色** | `#FF5252`（红） / `#5CFF6B`（绿） | 拼图图标中的红色和绿色拼图块（"UX Design Principles"） |
| **多色图标** | 彩虹配色 | "Intro to Color Theory" 三色圆环图标（红、绿、蓝/紫） |
| **背景色** | `#FFFFFF`（纯白） | 整体页面背景 |
| **锁定卡片背景** | `#F5F5F7`（极浅灰） | "Level Test 1" 锁定卡片的填充色 |
| **选中卡片边框** | `#7C5CFF` 粗边（约 3pt） | 当前选中的课程卡片外框 |
| **普通卡片边框** | `#E8E8ED`（浅灰） | 未选中卡片的细边框 |
| **标题文字** | `#1A1A1A`（近黑） | "Getting Started with UX Design"、课程名称 |
| **辅助文字** | `#8E8E93`（中灰） | "LEVEL 1" 标签、未选中 Tab 图标 |
| **统计/数字** | `#666666`（深灰） | 闪电符号旁的 "0" |

---

## 2️⃣ 字体层级

| 文字元素 | 估算字号 (pt) | 估算字号 (dp) | 字重 | 颜色 |
|---|---|---|---|---|
| 顶部下拉标题 | 17–18pt | 17–18dp | Medium (500) | `#1A1A1A` |
| 标签 "LEVEL 1" | 12–13pt | 12–13dp | Semibold (600) | `#8E8E93` |
| 主标题 | 26–28pt | 26–28dp | Bold (700) | `#000000` |
| "Start" 按钮文字 | 16–17pt | 16–17dp | Bold (700) | `#FFFFFF` |
| 课程名称 | 16–18pt | 16–18dp | Semibold (600) | `#1A1A1A` |
| 数字 "0" | 14–15pt | 14–15dp | Regular (400) | `#666666` |
| 底部导航文字 | 10–11pt | 10–11dp | Regular (400) | `#8E8E93` |

> **字体对比关系**：主标题与课程名称有约 40% 的字号差距，配合 Bold vs Semibold 形成清晰的层级。辅助文字 "LEVEL 1" 与主标题字号差约 2.5 倍，颜色更浅，视觉退后。

---

## 3️⃣ 间距与留白

| 间距区域 | 估算值 (pt) | 估算值 (dp) | 说明 |
|---|---|---|---|
| 顶部状态栏 → 下拉选择器 | ~24pt | ~24dp | 标准安全区 |
| 下拉选择器 → "LEVEL 1" 标签 | ~16pt | ~16dp | 模块间呼吸感 |
| "LEVEL 1" → 主标题 | ~8pt | ~8dp | 紧密关联的两个层级 |
| 主标题 → 第一个卡片 | ~12pt | ~12dp | 内容起始间距 |
| 卡片之间间距 | ~12–16pt | ~12–16dp | 统一的卡片间隔 |
| 卡片左右内边距 | ~20pt | ~20dp | 内容到卡片边缘 |
| 卡片上下内边距 | ~14–16pt | ~14–16dp | 图标+文字行高 |
| 图标 ↔ 课程名称间距 | ~12pt | ~12dp | 图标与文字的水平间距 |
| 底部内容 → Tab Bar | ~20pt | ~20dp | 内容区底部留白 |
| 全局横向边距 | ~20–24pt | ~20–24dp | 卡片到屏幕边缘 |

> **留白特征**：整体留白充足，卡片之间不拥挤，视觉呼吸感强。属于"宽松型"布局，适合学习类 App 的长时间阅读场景。

---

## 4️⃣ 组件样式

| 组件 | 样式参数 | 说明 |
|---|---|---|
| **卡片** | 圆角 radius: 16–20pt (16–20dp)；边框: 1pt solid `#E8E8ED` | 大圆角卡片，柔和亲和 |
| **选中卡片** | 边框: 3pt solid `#7C5CFF`；圆角不变 | 粗紫色边框高亮选中状态 |
| **"Start" 气泡按钮** | 背景: `#7C5CFF`；圆角: ~12pt；下方带三角形箭头指向卡片 | 浮层提示样式，带引导箭头 |
| **等级标签徽章** | 圆形直径 ~28pt；背景: `#FF6B9D`；文字: 白色 Bold | 右上角圆形徽章 |
| **底部导航栏** | 高度: ~83pt（含底部安全区）；图标大小: ~28pt；选中: `#7C5CFF`；未选中: `#C7C7CC` | 6 个 Tab，扁平图标风格 |
| **下拉选择器** | 圆角: ~12pt；边框: 1pt `#E8E8ED`；右侧有下拉箭头 | 顶部课程切换器 |
| **完成状态图标** | 圆形灰色背景 `#E8E8ED` + 白色对勾 | 课程完成指示 |
| **锁定状态图标** | 灰色锁图标 | 未解锁课程 |
| **阴影** | 无明显阴影 | 依靠边框 + 背景色差区分层级 |
| **分隔线** | 无传统分隔线 | 用卡片间距代替分隔线，整体更轻盈 |
| **图标风格** | 彩色 emoji / 扁平线性 | 彩色、趣味性、非严肃商务风 |

---

## 5️⃣ 整体布局结构

```
┌─────────────────────────────────┐
│  状态栏 (9:41 / 信号 / 电池)      │  ← iOS 状态栏
├─────────────────────────────────┤
│  [UX Design Foundations  ▼]  ⚡0 │  ← 课程下拉选择器 + 积分
├─────────────────────────────────┤
│  LEVEL 1                         │  ← 辅助标签
│  Getting Started with UX Design  │  ← 主标题（可展开/折叠）
│        [ Start ] ▲                │  ← 浮层气泡按钮
│  ┌─────────────────────────────┐ │
│  │ 🎓 "UX" What is UX Design?  │ │  ← 选中卡片（紫边框）
│  └─────────────────────────────┘ │
│  ┌─────────────────────────────┐ │
│  │ 🧩 UX Design Principles ✓   │ │  ← 普通卡片
│  └─────────────────────────────┘ │
│  ┌─────────────────────────────┐ │
│  │ 🎨 Intro to Color Theory ✓  │ │
│  └─────────────────────────────┘ │
│  ┌─────────────────────────────┐ │
│  │ 🔤 Intro to Typography ✓    │ │
│  └─────────────────────────────┘ │
│  ┌─────────────────────────────┐ │
│  │ 🏰 Level Test 1 🔒          │ │  ← 锁定卡片（浅灰背景）
│  └─────────────────────────────┘ │
├─────────────────────────────────┤
│  [🎓] [⭐] [🏆] [📖] [🏷] [👤] │  ← 底部 6-Tab 导航栏
└─────────────────────────────────┘
```

**布局特征总结**：
- **结构**：上→下三段式（顶部筛选区 + 中间卡片流 + 底部导航）
- **卡片流**：垂直堆叠，等高卡片，统一圆角和间距
- **导航位置**：底部 Tab Bar（6 个图标），符合 iOS 规范
- **内容组织**：层级式（Level → Unit → Lesson），支持展开/折叠
- **状态反馈**：通过边框颜色（紫=选中）、背景色（灰=锁定）、图标（✓=完成）三套视觉语言区分课程状态

---

## 🎨 结构化设计 Token（Kivy KV 映射参考）

```kv
# ============================================================
# Uxcel Go 风格设计 Token → Kivy KV 样式参考
# ============================================================

# --- 颜色 Tokens ---
primary_color:       "#7C5CFF"     # 主色：选中边框、按钮、选中 Tab
accent_pink:         "#FF6B9D"     # 辅助色：等级徽章
card_border_default: "#E8E8ED"     # 默认卡片边框
card_border_active:  "#7C5CFF"     # 选中卡片边框（同 primary）
card_bg_default:     "#FFFFFF"     # 默认卡片背景
card_bg_locked:      "#F5F5F7"     # 锁定卡片背景
page_bg:             "#FFFFFF"     # 页面背景
text_title:          "#000000"     # 主标题
text_heading:        "#1A1A1A"     # 课程名称/二级标题
text_secondary:      "#8E8E93"     # 辅助文字（LEVEL 标签）
text_muted:          "#666666"     # 数字/统计
tab_icon_active:     "#7C5CFF"     # 选中 Tab 图标
tab_icon_inactive:   "#C7C7CC"     # 未选中 Tab 图标

# --- 字号 Tokens ---
font_size_label:     12sp          # "LEVEL 1" 标签
font_size_dropdown:  17sp          # 下拉选择器文字
font_size_title:     26sp          # 主标题
font_size_course:    17sp          # 课程名称
font_size_button:    16sp          # "Start" 按钮
font_size_number:    14sp          # 统计数字
font_size_tab_label: 10sp          # 底部 Tab 文字

# --- 圆角 Tokens ---
corner_card:         16dp          # 卡片圆角
corner_dropdown:     12dp          # 下拉框圆角
corner_badge:        14dp          # 等级徽章（圆形，直径 28dp）

# --- 间距 Tokens ---
margin_global:       20dp          # 全局横向边距
padding_card_h:      20dp          # 卡片水平内边距
padding_card_v:      14dp          # 卡片垂直内边距
gap_between_cards:   14dp          # 卡片间距
gap_title_level:     8dp           # "LEVEL" 与主标题间距
gap_title_card:      12dp          # 主标题与第一卡片间距
gap_icon_text:       12dp          # 图标与课程名称间距
gap_section_top:     16dp          # 模块间间距

# --- 边框 Tokens ---
card_border_width:   1dp           # 默认卡片边框粗细
card_border_active_width: 3dp      # 选中卡片边框粗细（强调）

# --- 字体字重（Kivy 需通过 font_name + bold 参数实现）---
# label_level:      font_name: "Roboto-Medium"     (Semibold 600)
# title_main:       font_name: "Roboto-Bold"       (Bold 700)
# course_name:      font_name: "Roboto-Medium"     (Semibold 600)
# button_start:     font_name: "Roboto-Bold"       (Bold 700)
```

---

## 📋 综合风格关键词

| 维度 | 关键词 |
|---|---|
| **视觉风格** | 现代扁平、亲和友好、教育科技风 |
| **配色基调** | 白底 + 紫主色 + 粉点缀，干净清爽 |
| **卡片语言** | 大圆角、粗边框选中、无边框分隔 |
| **图标风格** | 彩色 emoji、趣味性、非商务 |
| **目标用户感知** | 轻松、鼓励、游戏化学习 |

---

## ⚠️ 注意事项（Kivy 适配提醒）

1. **圆角实现**：Kivy 的 `RoundRelativeLayout` 或 `RoundedRectangle` 需要 `kivy.garden.rrect` 或自定义 canvas 绘制圆角矩形。大圆角（16dp）在 Android 上可能需要 `corner_radius` 参数。
2. **彩色 emoji 图标**：Kivy 原生对 emoji 支持有限，建议使用 PNG/SVG 图标资源替代，或集成 `emoji` 库。
3. **底部 Tab Bar**：Kivy 无原生 Tab Bar 组件，需自定义 `BoxLayout` + `Image` 实现。注意 Android 底部导航的安全区（~24dp）。
4. **选中状态高亮**：通过动态切换 `Line` canvas 指令的 `color` 和 `width` 实现粗边框效果。
5. **字体**：建议使用 Noto Sans / Roboto 字体家族，Kivy 需通过 `font_name` 指定并打包字体文件。

---

<details>
<summary><b>原始图片信息</b></summary>

- **文件路径**: `C:\Users\duduba\Pictures\Uxcel Go iOS 28.png`
- **原始分辨率**: 1179 × 2676 px（iPhone 14 Pro Max / iPhone 15 Pro Max 分辨率）
- **截图来源**: Uxcel App（Mobbin 收录）
- **分析精度**: 由于截图为像素级截图，HEX 色值和字号为基于视觉比例的合理估算，实际值可能有 ±5% 偏差。

</details>

---