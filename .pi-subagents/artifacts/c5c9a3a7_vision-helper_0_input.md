# Task for vision-helper

请详细分析这张韩国 KakaoBank iOS App 截图，提取完整的视觉设计系统。

图片路径：C:\Users\duduba\Pictures\KakaoBank iOS 1.png

请完整输出以下所有内容，每个部分必须给出具体的 HEX 色值和数值（dp/pt）：

## 1. 配色方案
- 页面整体背景色 HEX
- 顶部导航栏背景色和文字颜色
- 主色调 HEX（用于高亮、按钮等）
- 辅助色 HEX（每个标注用途）
- 卡片背景色 HEX
- 卡片边框颜色和宽度
- 标题/正文/辅助/金额文字颜色 HEX
- 分隔线颜色

## 2. 字体层级
逐一列出：页面主标题、金额数字（最大的那个）、次级金额、账户名/卡片标题、辅助信息、标签、按钮文字、Tab 文字 —— 各自的字号(pt)、字重、颜色

## 3. 间距与留白
- 全局左右边距
- 卡片之间的垂直间距
- 卡片内部上下/左右内边距
- 标题与内容的间距

## 4. 组件样式
- 卡片圆角值、阴影参数、边框规格
- 按钮样式（填充/描边/圆角/高度）
- 分隔线样式
- 顶部导航栏和底部 Tab 栏样式
- 图标风格

## 5. 整体布局结构
从上到下描述每个区域的用途和排列方式

## 6. 设计 Token 代码块
输出可直接翻译为 Kivy KV 样式的设计参数汇总

## Acceptance Contract
Acceptance level: attested
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Return concrete findings with file paths and severity when applicable

Required evidence: review-findings, residual-risks

Finish with a fenced JSON block tagged `acceptance-report` in this shape:
Use empty arrays when no items apply; array fields contain strings unless object entries are shown.
`criteriaSatisfied[].status` must be exactly one of: satisfied, not-satisfied, not-applicable.
`commandsRun[].result` must be exactly one of: passed, failed, not-run.
`manualNotes` and `notes` are optional strings; an empty string means no note and does not satisfy `manual-notes` evidence.
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "specific proof"
    }
  ],
  "changedFiles": [
    "src/file.ts"
  ],
  "testsAddedOrUpdated": [
    "test/file.test.ts"
  ],
  "commandsRun": [
    {
      "command": "command",
      "result": "passed",
      "summary": "short result"
    }
  ],
  "validationOutput": [
    "validation output or concise summary"
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "short description of the diff",
  "reviewFindings": [
    "blocker: file.ts:12 - issue found, or no blockers"
  ],
  "manualNotes": "anything else the parent should know"
}
```