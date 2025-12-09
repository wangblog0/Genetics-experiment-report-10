#!/usr/bin/env python3
"""
快速运行SNP检测的示例脚本
"""
import subprocess
import sys
from pathlib import Path

# 配置区域
FASTA_FILE = "../others/HV1/combined.fasta"  # FASTA文件路径
OUTPUT_REPORT = "HV1_snp_report.txt"         # 输出报告文件
OUTPUT_CSV = "HV1_snp_matrix.csv"            # 输出CSV矩阵
MIN_FREQUENCY = 0.0                          # 最小等位基因频率

def run_snp_detection():
    """运行SNP检测"""
    fasta_path = Path(FASTA_FILE)
    
    if not fasta_path.exists():
        print(f"错误: FASTA文件不存在 - {FASTA_FILE}")
        print("请修改脚本中的 FASTA_FILE 变量")
        return
    
    # 构建命令
    cmd = [
        sys.executable,
        "find_snp.py",
        str(fasta_path),
        "--min-freq", str(MIN_FREQUENCY),
        "--output", OUTPUT_REPORT,
        "--export-csv", OUTPUT_CSV
    ]
    
    print("=" * 60)
    print("运行SNP检测")
    print("=" * 60)
    print(f"输入文件: {fasta_path}")
    print(f"输出报告: {OUTPUT_REPORT}")
    print(f"输出CSV:  {OUTPUT_CSV}")
    print(f"最小频率: {MIN_FREQUENCY}")
    print("=" * 60)
    print()
    
    # 运行命令
    subprocess.run(cmd)

if __name__ == '__main__':
    print("SNP检测快速运行脚本")
    print()
    print("配置说明:")
    print(f"  - 如需分析其他文件，请修改本脚本中的 FASTA_FILE 变量")
    print(f"  - 当前设置: {FASTA_FILE}")
    print()
    
    # 询问用户
    response = input("按回车键开始运行，或输入 'q' 退出: ").strip().lower()
    if response == 'q':
        print("已取消")
        sys.exit(0)
    
    run_snp_detection()
