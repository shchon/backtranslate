# Task for vision-helper

分析这张韩国 KakaoBank 银行 App 设计截图，重点提取以下信息：

图片路径：C:\Users\duduba\Pictures\KakaoBank iOS 1.png

请重点分析以下5个方面：

1. **配色方案**：主色、辅助色、强调色（给出HEX色值）、背景色（深色/浅色）、卡片背景色、文字颜色层级（标题/正文/辅助/数字/金额），每个颜色标注使用位置。

2. **字体层级**：最大的数字（金额）是多少字号、什么字重？标题字号？正文字号？辅助文字字号？字体粗细的对比关系如何？

3. **间距与留白**：全局横向边距多少？卡片之间间距多少？卡片内部上下左右内边距？模块之间的呼吸感？

4. **组件样式**：卡片的圆角大小、是否有阴影、是否有边框？按钮圆角？导航栏样式（顶部/底部）？列表项之间如何分隔？图标风格？

5. **整体布局结构**：页面是什么结构（上中下三段？卡片流？列表？）？导航位置？内容组织方式？有没有明显的区域分组？

请输出结构化的设计Token（可直接翻译成Kivy KV样式代码）。

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