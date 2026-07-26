# Task for vision-helper

详细分析这张韩国 KakaoBank iOS App 截图。请读取图片并给出完整的、结构化的设计分析报告。

图片路径：C:\Users\duduba\Pictures\KakaoBank iOS 1.png

请务必完整分析并输出以下所有内容，每个部分都要有具体的数值和HEX色值：

## 1. 配色方案
- 页面整体背景色（HEX值）
- 顶部状态栏/导航栏背景色和文字颜色
- 主色（用于按钮、高亮文字等，给出HEX值）
- 辅助色/强调色（给出HEX值和用途）
- 卡片背景色（HEX值）
- 卡片边框颜色和宽度
- 标题文字颜色（HEX值）
- 正文文字颜色（HEX值）
- 金额/数字颜色（HEX值）
- 辅助文字颜色（HEX值）
- 分隔线颜色

## 2. 字体层级
请逐一列出所见文字的：字号(pt/dp)、字重(Bold/Medium/Regular/Light)、颜色：
- 页面主标题
- 金额数字（最大的那个）
- 次级金额数字
- 账户名称/卡片标题
- 账户号/辅助信息
- 标签文字
- 按钮文字
- 底部Tab文字

## 3. 间距与留白
- 页面左右边距（从屏幕边缘到内容）
- 卡片之间的垂直间距
- 卡片内部上下内边距
- 卡片内部左右内边距
- 标题与内容之间的间距
- 是否有安全区域

## 4. 组件样式
- 卡片圆角值（dp）
- 卡片是否有阴影（如有，描述阴影参数）
- 卡片是否有边框（如有，描述颜色和宽度）
- 按钮样式（填充/描边、圆角值、高度）
- 是否有分隔线
- 顶部导航栏样式
- 底部Tab栏样式（如有）
- 图标风格

## 5. 整体布局
- 描述页面从上到下的布局结构（每个区域的用途）
- 内容是用卡片还是列表排列
- 是否有分组/分段
- 导航方式

请在最后输出可直接用于Kivy KV语言的设计Token代码块。

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