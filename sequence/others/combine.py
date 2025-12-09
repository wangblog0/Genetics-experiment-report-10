#!/usr/bin/env python3
"""
合并所有.seq文件到一个FASTA文件
"""
from pathlib import Path

def combine_seq_to_fasta(input_dir='.', output_file='combined.fasta'):
    """
    将目录下所有.seq文件合并成一个FASTA文件
    
    Args:
        input_dir: 输入目录路径
        output_file: 输出的FASTA文件名
    """
    # 获取当前目录
    input_path = Path(input_dir)
    
    # 查找所有.seq文件并排序
    seq_files = sorted(input_path.glob('*.seq'))
    
    if not seq_files:
        print(f"在 {input_dir} 目录下未找到.seq文件")
        return
    
    print(f"找到 {len(seq_files)} 个.seq文件")
    
    # 打开输出文件
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for seq_file in seq_files:
            # 获取文件名（不含扩展名）作为序列ID
            seq_id = seq_file.stem
            
            print(f"处理: {seq_file.name}")
            
            # 读取序列内容
            with open(seq_file, 'r', encoding='utf-8') as in_f:
                sequence = in_f.read().strip()
            
            # 写入FASTA格式
            # 格式: >序列ID
            #      序列内容
            out_f.write(f">{seq_id}\n")
            out_f.write(f"{sequence}\n")
    
    print(f"\n成功生成 {output_file}")
    print(f"共包含 {len(seq_files)} 条序列")

if __name__ == '__main__':
    # 在当前目录下运行
    combine_seq_to_fasta(input_dir='.', output_file='combined.fasta')
