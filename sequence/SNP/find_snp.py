#!/usr/bin/env python3
"""
从MEGA对齐的多序列FASTA文件中查找SNP位点
"""
from pathlib import Path
from collections import Counter
import argparse


def read_fasta(fasta_file):
    """
    读取FASTA文件
    
    Returns:
        dict: {序列ID: 序列}
    """
    sequences = {}
    current_id = None
    current_seq = []
    
    with open(fasta_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('>'):
                # 保存前一个序列
                if current_id is not None:
                    sequences[current_id] = ''.join(current_seq)
                
                # 开始新序列
                current_id = line[1:].strip()
                current_seq = []
            else:
                current_seq.append(line.upper())
        
        # 保存最后一个序列
        if current_id is not None:
            sequences[current_id] = ''.join(current_seq)
    
    return sequences


def find_snps(sequences, min_frequency=0.0, ignore_gaps=True):
    """
    查找SNP位点
    
    Args:
        sequences: 序列字典 {ID: 序列}
        min_frequency: 最小等位基因频率（默认0，即显示所有变异）
        ignore_gaps: 是否忽略gap（'-'）作为变异
        
    Returns:
        list: SNP位点信息列表
    """
    if not sequences:
        return []
    
    # 获取序列长度（假设已对齐，所有序列等长）
    seq_ids = list(sequences.keys())
    seq_length = max(len(seq) for seq in sequences.values())
    
    # 检查序列长度是否一致
    lengths = [len(seq) for seq in sequences.values()]
    if len(set(lengths)) > 1:
        print(f"警告: 序列长度不一致！长度范围: {min(lengths)} - {max(lengths)}")
        print("建议使用MEGA重新对齐序列")
    
    snp_sites = []
    
    # 遍历每个位置
    for pos in range(seq_length):
        # 获取该位置所有序列的碱基
        bases_at_pos = []
        for seq_id in seq_ids:
            seq = sequences[seq_id]
            if pos < len(seq):
                base = seq[pos]
                if not ignore_gaps or base != '-':
                    bases_at_pos.append((seq_id, base))
        
        if len(bases_at_pos) < 2:
            continue
        
        # 统计碱基频率
        base_counts = Counter([base for _, base in bases_at_pos])
        
        # 判断是否为SNP（存在2种或以上不同碱基）
        if len(base_counts) > 1:
            total_count = sum(base_counts.values())
            
            # 计算次要等位基因频率
            sorted_counts = sorted(base_counts.values(), reverse=True)
            minor_allele_freq = sorted_counts[1] / total_count if len(sorted_counts) > 1 else 0
            
            # 过滤低频变异
            if minor_allele_freq >= min_frequency:
                # 收集每个序列在该位置的碱基
                base_info = {}
                for seq_id in seq_ids:
                    seq = sequences[seq_id]
                    if pos < len(seq):
                        base_info[seq_id] = seq[pos]
                    else:
                        base_info[seq_id] = '-'
                
                snp_sites.append({
                    'position': pos + 1,  # 1-based position
                    'base_counts': base_counts,
                    'base_info': base_info,
                    'minor_allele_freq': minor_allele_freq
                })
    
    return snp_sites


def print_snp_report(snp_sites, sequences, output_file=None):
    """
    打印SNP报告
    """
    lines = []
    
    lines.append("=" * 80)
    lines.append(f"SNP检测报告")
    lines.append("=" * 80)
    lines.append(f"序列数量: {len(sequences)}")
    lines.append(f"SNP位点数量: {len(snp_sites)}")
    lines.append("=" * 80)
    lines.append("")
    
    if not snp_sites:
        lines.append("未检测到SNP位点")
        result = '\n'.join(lines)
        print(result)
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
        return
    
    # 详细SNP信息
    lines.append(f"{'位置':<8} {'碱基分布':<30} {'次要等位基因频率':<20}")
    lines.append("-" * 80)
    
    for snp in snp_sites:
        pos = snp['position']
        base_counts = snp['base_counts']
        maf = snp['minor_allele_freq']
        
        # 格式化碱基分布
        base_dist = ', '.join([f"{base}:{count}" for base, count in 
                               sorted(base_counts.items(), key=lambda x: -x[1])])
        
        lines.append(f"{pos:<8} {base_dist:<30} {maf:.3f}")
    
    lines.append("")
    lines.append("=" * 80)
    lines.append("各序列在SNP位点的碱基详情")
    lines.append("=" * 80)
    lines.append("")
    
    # 详细碱基信息表格
    seq_ids = list(sequences.keys())
    
    # 表头
    header = f"{'位置':<8} " + " ".join([f"{sid[:10]:>10}" for sid in seq_ids])
    lines.append(header)
    lines.append("-" * len(header))
    
    # 每个SNP位点
    for snp in snp_sites:
        pos = snp['position']
        base_info = snp['base_info']
        
        row = f"{pos:<8} " + " ".join([f"{base_info.get(sid, '-'):>10}" for sid in seq_ids])
        lines.append(row)
    
    result = '\n'.join(lines)
    print(result)
    
    # 保存到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"\n报告已保存到: {output_file}")


def export_snp_matrix(snp_sites, sequences, output_file):
    """
    导出SNP矩阵到CSV文件
    """
    import csv
    
    seq_ids = list(sequences.keys())
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # 写表头
        header = ['Position'] + seq_ids
        writer.writerow(header)
        
        # 写每个SNP位点
        for snp in snp_sites:
            pos = snp['position']
            base_info = snp['base_info']
            
            row = [pos] + [base_info.get(sid, '-') for sid in seq_ids]
            writer.writerow(row)
    
    print(f"SNP矩阵已导出到: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='从对齐的FASTA文件中检测SNP位点')
    parser.add_argument('fasta_file', help='输入的FASTA文件路径')
    parser.add_argument('--min-freq', type=float, default=0.0,
                        help='最小次要等位基因频率 (默认: 0.0)')
    parser.add_argument('--include-gaps', action='store_true',
                        help='将gap(-)视为变异 (默认: 忽略)')
    parser.add_argument('--output', '-o', help='输出报告文件路径 (可选)')
    parser.add_argument('--export-csv', help='导出SNP矩阵到CSV文件 (可选)')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    fasta_path = Path(args.fasta_file)
    if not fasta_path.exists():
        print(f"错误: 文件不存在 - {args.fasta_file}")
        return
    
    print(f"正在读取FASTA文件: {args.fasta_file}")
    sequences = read_fasta(args.fasta_file)
    print(f"成功读取 {len(sequences)} 条序列")
    print()
    
    print("正在检测SNP位点...")
    snp_sites = find_snps(sequences, 
                          min_frequency=args.min_freq,
                          ignore_gaps=not args.include_gaps)
    print()
    
    # 打印报告
    print_snp_report(snp_sites, sequences, args.output)
    
    # 导出CSV
    if args.export_csv and snp_sites:
        export_snp_matrix(snp_sites, sequences, args.export_csv)


if __name__ == '__main__':
    # 如果没有命令行参数，使用默认参数
    import sys
    if len(sys.argv) == 1:
        print("使用示例:")
        print("  python find_snp.py <fasta文件>")
        print("  python find_snp.py combined.fasta --min-freq 0.1")
        print("  python find_snp.py combined.fasta --output snp_report.txt")
        print("  python find_snp.py combined.fasta --export-csv snp_matrix.csv")
        print()
        print("选项:")
        print("  --min-freq FREQ     最小次要等位基因频率 (默认: 0.0)")
        print("  --include-gaps      将gap(-)视为变异 (默认: 忽略)")
        print("  --output FILE       输出报告到文件")
        print("  --export-csv FILE   导出SNP矩阵到CSV")
    else:
        main()
