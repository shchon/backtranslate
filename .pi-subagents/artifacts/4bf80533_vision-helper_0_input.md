# Task for vision-helper

请分析这张 App 设计截图，按照以下需求详细描述：

图片路径：C:\Users\duduba\Pictures\Uxcel Go iOS 28.png

分析需求：
我需要参考这个设计的视觉风格，对现有的 Kivy Python Android App 做 UI 风格迭代，请重点分析以下5个方面：

1. **配色方案**：提取主色、辅助色、强调色（给出HEX色值）、背景色、卡片背景色、文字颜色（标题/正文/辅助文字），标注每个颜色的使用位置。

2. **字体层级**：标题的字号、正文字号、数字/统计值的字号，字重(Bold/Regular/Light)，字体的对比关系。

3. **间距与留白**：模块之间的间距、卡片内边距、元素之间的呼吸感，估算具体的间距值（px/pt）。

4. **组件样式**：按钮的形状（圆角大小/全圆角/直角）、卡片圆角、导航栏样式、是否有阴影、边框样式、分隔线、图标风格。

5. **整体布局结构**：页面的排版结构（上下/左右/网格/卡片流）、导航位置（顶部/底部Tab）、内容组织方式。

请尽可能详细，输出结构化的设计Token，我用来翻译成Kivy KV语言的样式代码。

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