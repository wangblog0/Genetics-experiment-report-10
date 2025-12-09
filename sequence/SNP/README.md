# SNP位点检测工具

从MEGA对齐的多序列FASTA文件中自动检测SNP（单核苷酸多态性）位点。

## 文件说明

- `find_snp.py` - 主程序，SNP检测核心脚本
- `run_example.py` - 快速运行示例脚本
- `README.md` - 本说明文档

## 快速开始

### 方法1: 使用示例脚本（推荐）

```powershell
python run_example.py
```

默认会分析 `../others/HV1/combined.fasta` 文件，生成：
- `HV1_snp_report.txt` - 文本格式的详细报告
- `HV1_snp_matrix.csv` - CSV格式的SNP矩阵

若要分析其他文件，编辑 `run_example.py` 中的 `FASTA_FILE` 变量。

### 方法2: 直接使用主程序

```powershell
# 基本用法
python find_snp.py <fasta文件路径>

# 生成报告文件
python find_snp.py combined.fasta --output snp_report.txt

# 导出CSV矩阵
python find_snp.py combined.fasta --export-csv snp_matrix.csv

# 过滤低频变异（次要等位基因频率 >= 0.1）
python find_snp.py combined.fasta --min-freq 0.1

# 包含gap作为变异
python find_snp.py combined.fasta --include-gaps
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `fasta_file` | 输入的FASTA文件路径（必需） | - |
| `--min-freq` | 最小次要等位基因频率 | 0.0 |
| `--include-gaps` | 将gap(-)视为变异 | 默认忽略 |
| `--output` | 输出报告文件路径 | 屏幕显示 |
| `--export-csv` | 导出SNP矩阵到CSV文件 | 不导出 |

## 输出格式

### 文本报告

包含以下信息：
1. **统计摘要**：序列数量、SNP位点总数
2. **SNP位点列表**：位置、碱基分布、次要等位基因频率
3. **碱基详情表**：每个序列在各SNP位点的具体碱基

示例：
```
================================================================================
SNP检测报告
================================================================================
序列数量: 18
SNP位点数量: 45
================================================================================

位置     碱基分布                        次要等位基因频率    
--------------------------------------------------------------------------------
1        T:16, A:1, C:1                 0.056
50       C:17, T:1                      0.056
100      A:15, G:3                      0.167
...
```

### CSV矩阵

每行一个SNP位点，每列一个序列，便于在Excel或其他软件中进一步分析。

| Position | HV1-1-4 | HV1-1-5 | HV1-2-1 | ... |
|----------|---------|---------|---------|-----|
| 1        | A       | T       | T       | ... |
| 50       | C       | C       | T       | ... |
| 100      | A       | A       | G       | ... |

## 注意事项

1. **序列必须已对齐**：使用MEGA或其他工具对齐后再运行此脚本
2. **序列长度一致**：对齐后的序列应等长（用'-'填充）
3. **FASTA格式**：
   ```
   >序列ID1
   ATCGATCG...
   >序列ID2
   ATCGATCG...
   ```

## 常见问题

**Q: 如何对齐序列？**
A: 使用MEGA软件：
   1. 打开MEGA → Align → Edit/Build Alignment
   2. 导入FASTA文件
   3. 选择ClustalW或MUSCLE进行对齐
   4. 导出对齐后的FASTA文件

**Q: 为什么没有检测到SNP？**
A: 可能原因：
   - 序列完全一致
   - 序列未对齐
   - 序列长度差异过大

**Q: 如何只显示高频变异？**
A: 使用 `--min-freq` 参数，例如 `--min-freq 0.1` 只显示次要等位基因频率 ≥ 10% 的位点

## 示例工作流程

```powershell
# 1. 进入SNP目录
cd sequence\SNP

# 2. 运行HV1区域分析
python find_snp.py ../others/HV1/combined.fasta --output HV1_snp_report.txt --export-csv HV1_snp_matrix.csv

# 3. 运行HV2区域分析
python find_snp.py ../others/HV2/combined.fasta --output HV2_snp_report.txt --export-csv HV2_snp_matrix.csv

# 4. 查看结果
cat HV1_snp_report.txt
```

## 技术支持

如有问题，请检查：
1. Python版本（建议3.6+）
2. FASTA文件格式是否正确
3. 序列是否已对齐
