# LaTeX 编译指南

## 文件结构

```
latex/
├── book-storage-physics.tex           # ⭐ 全集主文件 (book类，推荐编译)
├── 01-magnetic-storage-hdd.tex        # 第1篇 · 磁性存储 (article类)
├── 02-nand-flash.tex                  # 第2篇 · NAND闪存 (article类)
├── 03-optical-storage.tex             # 第3篇 · 光学存储 (article类)
├── 04-emerging-memories.tex           # 第4篇 · 新兴存储 (article类)
├── 05-data-deletion-recovery.tex      # 第5篇 · 删除与恢复 (article类)
├── 00-collected-storage-physics.tex   # 旧版缩写全集 (book类，已弃用)
├── BUILD-GUIDE.md                     # 本文档
└── Makefile                           # (可选) 自动化编译
```

## 编译要求

### 必需软件
- **XeLaTeX** (必须 — 用于中文支持)
- **BibTeX** (用于参考文献)
- TeX 发行版：推荐 TeX Live 2024+ 或 MiKTeX

### 必需字体 (macOS)
- Songti SC (宋体)
- Heiti SC (黑体)

如果使用 Windows/Linux，请修改每篇 `.tex` 文件中的字体设置，例如：
```latex
% Windows
\setCJKmainfont{SimSun}[BoldFont=SimHei]
% Linux
\setCJKmainfont{Noto Serif CJK SC}[BoldFont=Noto Sans CJK SC]
```

### 必需 LaTeX 宏包
所有宏包均可通过 TeX Live/MiKTeX 包管理器安装：
- `ctex` — 中文排版
- `newtxtext`, `newtxmath` — Times风格数学字体
- `amsmath`, `mathtools`, `bm` — 数学增强
- `physics`, `siunitx` — 物理符号与单位
- `tikz`, `pgfplots`, `circuitikz` — 图形
- `biblatex` — 参考文献
- `tcolorbox` — 彩色文本框
- `hyperref`, `cleveref` — 超链接与交叉引用
- `fancyhdr`, `geometry`, `setspace` — 页面布局

## 编译命令

### 单篇编译 (以第1篇为例)

```bash
# 方法1: 手动三步
xelatex 01-magnetic-storage-hdd.tex
bibtex   01-magnetic-storage-hdd
xelatex 01-magnetic-storage-hdd.tex
xelatex 01-magnetic-storage-hdd.tex

# 方法2: latexmk (推荐)
latexmk -xelatex 01-magnetic-storage-hdd.tex
```

### 全集编译

```bash
latexmk -xelatex book-storage-physics.tex
```

> `book-storage-physics.tex` 是当前的全集主文件（内容内联，五篇合一）。
> `00-collected-storage-physics.tex` 是早期缩写版，已弃用，保留仅为存档。

### 清理编译产物

```bash
latexmk -C  # 清理所有辅助文件
# 或手动:
rm -f *.aux *.log *.out *.toc *.bbl *.blg *.bcf *.run.xml
```

## 预期输出

| 文件 | 预计页数 | 主要内容 |
|------|---------|---------|
| 第1篇 | ~22页 | 微磁学、LLG方程、Stoner-Wohlfarth、TMR |
| 第2篇 | ~18页 | FN隧穿WKB、阈值分布、退化物理、FTL |
| 第3篇 | ~15页 | 矢量衍射、JMAK相变、磁光Kerr、全息 |
| 第4篇 | ~14页 | STT/SOT、ReRAM、PCM、FeFET |
| 第5篇 | ~16页 | 剩磁、FTL残留、Landauer原理、KL散度 |
| 全集 | ~90页 | 五篇合一 + 总序 + 附录 |

## 已知问题与解决

1. **`! LaTeX Error: File 'xxx.sty' not found.`**
   → 通过 TeX Live Manager (`tlmgr install xxx`) 或 MiKTeX Console 安装缺失宏包。

2. **`! Package fontspec Error: The font "Songti SC" cannot be found.`**
   → 修改 `.tex` 文件中的 `setCJKmainfont` 为系统可用中文字体。

3. **TikZ 图片编译缓慢**
   → 可先注释掉 `\begin{figure}...\end{figure}` 中的 TikZ 代码，
   快速得到文本排版的草稿。

4. **参考文献未显示**
   → 确保已经运行 bibtex/biber。本系列使用 bibtex 引擎
   （因参考文献以 `thebibliography` 环境直接编写，
   实际上不需要外部 `.bib` 文件 —— 所有引用都在 `\begin{thebibliography}` 中）。

## 自定义修改

### 修改页面尺寸
编辑 `\usepackage[margin=...]{geometry}` 行。

### 修改字体大小
将 `\documentclass[11pt,...]{article}` 中的 `11pt` 改为 `10pt` 或 `12pt`。

### 生成英文版
将 `\usepackage[UTF8]{ctex}` 注释掉，并将中文内容替换为英文。

---

*最后更新：2026-06-10*
