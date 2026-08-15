# 存储物理原理文集

凝聚态物理与信息存储交叉的专题教材——从磁畴、量子隧穿到信息擦除，定位为「四大力学 + 固体物理」程度。

共五篇：前三篇分别阐述三大经典存储技术（磁、半导体电荷、光学）的物理原理，第四篇扩展到新兴非易失性存储，第五篇把全部物理收敛到「数据删除与恢复」这一应用问题。

## 目录结构

```
├── README.md                          # 本说明
└── latex/                             # LaTeX 正式排版（含 TikZ 图与交叉引用）
    ├── book-storage-physics.tex       # ⭐ 全集主文件（book 类，五篇合一）
    ├── 01-magnetic-storage-hdd.tex    # 第1篇 · 磁性存储（HDD）
    ├── 02-nand-flash.tex              # 第2篇 · NAND 闪存
    ├── 03-optical-storage.tex         # 第3篇 · 光学存储
    ├── 04-emerging-memories.tex       # 第4篇 · 新兴非易失性存储
    ├── 05-data-deletion-recovery.tex  # 第5篇 · 数据删除与恢复
    ├── generate_figures.py            # 生成 figures/ 中 14 张插图的脚本
    ├── figures/                       # 14 张 PDF 插图（供 .tex 引用）
    └── BUILD-GUIDE.md                 # 详细编译指南（字体 / 宏包 / 排错）
```

## 文件关系

- **`book-storage-physics.tex` 是全集主文件**：五篇内容内联合一，是「最终成书」的唯一入口，编译得到 `book-storage-physics.pdf`。
- **`01–05` 是各篇的单篇版**（`article` 类），可独立编译，便于单篇阅读与修改。
  > 全集与单篇是**并行维护的两套源码**（全集为内联合集，并非通过 `\input` 引用单篇），修改某一篇内容时需同步两处。
- **`generate_figures.py` → `figures/`**：脚本用 matplotlib 生成 14 张 PDF 插图，`.tex` 通过 `\includegraphics{...}` 引用。
- **物理依赖**：第 1–3 篇（经典存储）→ 第 4 篇（新兴存储）→ 第 5 篇（删除与恢复，汇聚前四篇的物理）。

## 阅读顺序

第1篇(HDD) → 第2篇(NAND) → 第3篇(光学) → 第4篇(新兴) → 第5篇(删除与恢复)

## 编译

详见 `latex/BUILD-GUIDE.md`。快速开始：

```bash
cd latex
latexmk -xelatex book-storage-physics.tex        # 编译全集（推荐）
latexmk -xelatex 01-magnetic-storage-hdd.tex     # 编译单篇
```
