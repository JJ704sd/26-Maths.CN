# 26-Maths.CN：数学建模论文手工作台

从队友提供的代码、数据与结果出发，整理模型证据、逐节撰写论文，并使用 LaTeX 排版与验收。基于 [jihe520/MathModelAgent](https://github.com/jihe520/MathModelAgent) 的 skills 定制，优先支持 2026 全国大学生数学建模竞赛。

## 快速开始

```powershell
git clone https://github.com/JJ704sd/26-Maths.CN.git
cd 26-Maths.CN
```

1. 阅读 [安装与编译](docs/安装与编译.md)，准备 XeLaTeX。
2. 把赛题、数据、队友代码、运行方式和已有结果放入本地 `work/`。该目录默认不提交。
3. 在 AI 助手中提供本仓库绝对路径，请它读取 `skills/5writing/SKILL.md`，按 [论文手使用流程](docs/论文手使用流程.md) 工作。
4. 先确认模型理解与提纲，再逐节起草；最后读取 `skills/6verity/SKILL.md` 做验收。

**默认协作约定**：交付 LaTeX 源码与 PDF；可复现队友代码、另建验证脚本；修改核心模型前确认。缺失证据、未完成编译或核验不能判定为已就绪。

## 文档与入口

| 入口 | 用途 |
| --- | --- |
| [使用流程](docs/论文手使用流程.md) | 材料交接、提示词、逐节写作、结果更新 |
| [安装与编译](docs/安装与编译.md) | Windows MiKTeX、宏包、PDF 编译、常见问题 |
| [论文手训练](docs/论文手训练.md) | 七天训练与提交检查 |
| [AI 使用记录模板](docs/AI使用记录模板.md) | 记录真实工具使用与核验过程 |
| [写作 skill](skills/5writing/SKILL.md) | 论文手主入口 |
| [验收 skill](skills/6verity/SKILL.md) | 证据、引用、编译、逐页视觉检查 |
| [2026 国赛规则摘要](skills/5writing/references/cumcm-2026.md) | 官方格式与 AI 披露要求 |

## 验证范围

2026-09-07，在 Windows + MiKTeX 25.12 / XeTeX 4.16 下完成国赛 LaTeX 模板两轮编译及 6 页测试稿视觉检查。修正了目录、摘要页码、Windows 代码字体与不必要分页。仍有黑体字形回退提示，测试稿未发现缺字或重叠。其他赛事模板及 Typst 模板未做本轮编译验收。

模板包含上游示例数据、示例引用和待填内容，必须替换为队伍真实成果；测试编译通过不等于可提交。不要将 AI 检测分数作为写作目标，按官方要求声明使用并核验内容。

## 来源与同步

本仓库包含上游 skills 与必要模板资源，不包含上游前后端服务。详见 [来源与修改说明](UPSTREAM.md) 和 [上游许可原文](UPSTREAM-LICENSE.md)。不上传安装器、系统字体、密钥、私人题目材料与测试输出。本仓库未设置自动同步任务，后续变更需审查后提交推送。
