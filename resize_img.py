#!/usr/bin/env python3
"""
QQ图片缩放工具

专门用于缩放图片尺寸，让在QQ（手机版）中发送的图片能和表情包大小一样缩放。
测试界限是542像素，超过这个尺寸就会放大，所以按比例缩放最长边为542像素。
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from PIL import Image


class QQImageResizer:
    """QQ图片缩放器"""
    
    def __init__(self, max_size=542, quality=100):
        """
        初始化缩放器
        
        Args:
            max_size (int): 最大边长，默认为542像素
            quality (int): 图片质量/压缩级别 (1-100，默认: 100，不压缩)
                          对于JPEG：直接使用quality值
                          对于PNG：映射到compress_level (100->0无压缩, 1->9最大压缩)
        """
        self.max_size = max_size
        self.quality = quality
        self.supported_formats = {'.jpg', '.jpeg', '.png'}
    
    def should_resize(self, width, height):
        """
        判断图片是否需要缩放
        
        Args:
            width (int): 图片宽度
            height (int): 图片高度
            
        Returns:
            bool: 是否需要缩放
        """
        return max(width, height) > self.max_size
    
    def calculate_new_size(self, width, height):
        """
        计算新的图片尺寸
        
        Args:
            width (int): 原始宽度
            height (int): 原始高度
            
        Returns:
            tuple: (新宽度, 新高度)
        """
        if width > height:
            # 宽度是长边
            new_width = self.max_size
            new_height = int(height * (self.max_size / width))
        else:
            # 高度是长边或正方形
            new_height = self.max_size
            new_width = int(width * (self.max_size / height))
        
        return new_width, new_height
    
    def resize_image(self, input_path, output_path=None):
        """
        缩放单张图片
        
        Args:
            input_path (str): 输入图片路径
            output_path (str, optional): 输出图片路径
            
        Returns:
            bool: 是否成功处理
        """
        try:
            # 检查文件格式
            file_ext = Path(input_path).suffix.lower()
            if file_ext not in self.supported_formats:
                print(f"跳过不支持的文件格式: {input_path}")
                return False
            
            # 打开图片
            with Image.open(input_path) as img:
                width, height = img.size
                
                # 检查是否需要缩放
                if not self.should_resize(width, height):
                    print(f"图片尺寸合适，跳过: {input_path} ({width}x{height})")
                    return False
                
                # 计算新尺寸
                new_width, new_height = self.calculate_new_size(width, height)
                print(f"缩放图片: {input_path} ({width}x{height}) -> ({new_width}x{new_height})")
                
                # 缩放图片
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 确定输出路径
                if output_path is None:
                    output_path = input_path
                
                # 保存图片
                if file_ext in {'.jpg', '.jpeg'}:
                    # JPEG使用quality参数 (1-100)
                    resized_img.save(output_path, 'JPEG', quality=self.quality)
                else:  # PNG
                    # PNG将quality映射到compress_level (0-9)
                    # quality=100 -> compress_level=0 (无压缩)
                    # quality=1 -> compress_level=9 (最大压缩)
                    compress_level = int((100 - self.quality) * 9 / 99) if self.quality < 100 else 0
                    resized_img.save(output_path, 'PNG', compress_level=compress_level)
                
                return True
                
        except Exception as e:
            print(f"处理图片失败 {input_path}: {e}")
            return False
    
    def process_directory(self, input_dir, output_dir=None, rename=False):
        """
        处理目录中的所有图片
        
        Args:
            input_dir (str): 输入目录路径
            output_dir (str, optional): 输出目录路径
            rename (bool): 是否按序号重命名所有图片
            
        Returns:
            tuple: (成功数量, 失败数量, 跳过数量)
        """
        input_path = Path(input_dir)
        
        if not input_path.exists():
            print(f"错误: 目录不存在: {input_dir}")
            return 0, 0, 0
        
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = input_path
        
        success_count = 0
        fail_count = 0
        skip_count = 0
        
        # 如果启用重命名，使用计数器
        if rename:
            counter = 1
            
        # 遍历目录中的所有文件
        for file_path in input_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                file_ext = file_path.suffix.lower()
                
                if rename:
                    # 重命名模式：生成序号文件名
                    while True:
                        new_name = f"{counter:05d}{file_ext}"
                        if output_dir:
                            target_file = output_path / new_name
                        else:
                            target_file = input_path / new_name
                        
                        # 检查冲突：如果目标文件已存在且不是当前文件，序号递增
                        if target_file.exists() and target_file != file_path:
                            counter += 1
                            continue
                        break
                    
                    # 检查是否需要缩放
                    try:
                        with Image.open(file_path) as img:
                            width, height = img.size
                            needs_resize = self.should_resize(width, height)
                            
                            if needs_resize:
                                # 需要缩放：缩放后保存到新文件名
                                new_width, new_height = self.calculate_new_size(width, height)
                                print(f"缩放并重命名: {file_path.name} -> {new_name} ({width}x{height}) -> ({new_width}x{new_height})")
                                
                                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                                
                                if file_ext in {'.jpg', '.jpeg'}:
                                    resized_img.save(target_file, 'JPEG', quality=self.quality)
                                else:  # PNG
                                    compress_level = int((100 - self.quality) * 9 / 99) if self.quality < 100 else 0
                                    resized_img.save(target_file, 'PNG', compress_level=compress_level)
                                
                                success_count += 1
                            else:
                                # 不需要缩放：根据输出目录决定重命名或复制
                                if output_dir and Path(output_dir).resolve() != input_path.resolve():
                                    # 输出目录不是原目录：复制并重命名
                                    shutil.copy2(file_path, target_file)
                                    print(f"复制并重命名: {file_path.name} -> {new_name} ({width}x{height})")
                                else:
                                    # 输出目录是原目录：直接重命名
                                    if file_path != target_file:
                                        file_path.rename(target_file)
                                        print(f"重命名: {file_path.name} -> {new_name} ({width}x{height})")
                                    else:
                                        # 文件名已经是目标文件名，跳过
                                        print(f"跳过（已是目标文件名）: {file_path.name} ({width}x{height})")
                                        skip_count += 1
                                        counter += 1
                                        continue
                                
                                success_count += 1
                            
                            counter += 1
                    except Exception as e:
                        print(f"处理图片失败 {file_path}: {e}")
                        fail_count += 1
                        counter += 1
                else:
                    # 非重命名模式：原有逻辑
                    if output_dir:
                        relative_path = file_path.relative_to(input_path)
                        output_file = output_path / relative_path
                        output_file.parent.mkdir(parents=True, exist_ok=True)
                    else:
                        output_file = None
                    
                    # 处理图片
                    result = self.resize_image(str(file_path), str(output_file) if output_file else None)
                    
                    if result is True:
                        success_count += 1
                    elif result is False:
                        skip_count += 1
                    else:
                        fail_count += 1
        
        return success_count, fail_count, skip_count


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='QQ图片缩放工具 - 按比例缩放图片最长边为542像素',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python resize_img.py image.jpg                    # 缩放单张图片
  python resize_img.py /path/to/images/            # 缩放目录中的所有图片
  python resize_img.py input.jpg -o ./resized/     # 指定输出目录
  python resize_img.py input.jpg -s 500            # 自定义最大边长
  python resize_img.py input.jpg --quality 85      # 设置图片质量
  python resize_img.py /path/to/images/ --rename   # 按序号重命名所有图片
  python resize_img.py /path/to/images/ --recursive # 递归处理子目录
        """
    )
    
    parser.add_argument('input_path', help='输入文件或目录路径')
    parser.add_argument('-o', '--output', help='输出目录路径')
    parser.add_argument('-s', '--max-size', type=int, default=542, 
                       help='最大边长（默认: 542）')
    parser.add_argument('-q', '--quality', type=int, default=100,
                       help='图片质量/压缩级别 (1-100，默认: 100，不压缩。)')
    parser.add_argument('--rename', action='store_true',
                       help='按序号重命名所有图片')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='递归处理子目录')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='显示详细输出')
    parser.add_argument('--dry-run', action='store_true',
                       help='模拟运行，不实际修改文件')
    args = parser.parse_args()
    
    # 验证参数
    if args.quality < 1 or args.quality > 100:
        print("错误: 质量参数必须在1-100之间")
        sys.exit(1)
    
    if args.max_size < 10:
        print("错误: 最大边长不能小于10像素")
        sys.exit(1)
    
    # 创建缩放器实例
    resizer = QQImageResizer(max_size=args.max_size, quality=args.quality)
    
    # 设置详细模式
    if args.verbose:
        print(f"最大边长: {args.max_size}px")
        print(f"图片质量: {args.quality}")
        print(f"按序号重命名: {'是' if args.rename else '否'}")
        print(f"递归处理: {'是' if args.recursive else '否'}")
        print(f"模拟运行: {'是' if args.dry_run else '否'}")
        print("-" * 50)
    
    input_path = Path(args.input_path)
    
    if input_path.is_file():
        # 处理单个文件
        if args.verbose:
            print(f"开始处理单个文件: {args.input_path}")
        
        if args.dry_run:
            # 模拟运行模式
            try:
                with Image.open(args.input_path) as img:
                    width, height = img.size
                    if resizer.should_resize(width, height):
                        new_width, new_height = resizer.calculate_new_size(width, height)
                        print(f"[模拟] 将缩放: {args.input_path} ({width}x{height}) -> ({new_width}x{new_height})")
                    else:
                        print(f"[模拟] 无需缩放: {args.input_path} ({width}x{height})")
            except Exception as e:
                print(f"[模拟] 处理失败: {args.input_path} - {e}")
        else:
            # 实际处理
            result = resizer.resize_image(args.input_path, args.output)
            
            if result is True:
                print("✓ 图片缩放完成")
            elif result is False:
                print("✓ 图片无需缩放")
            else:
                print("✗ 图片处理失败")
            
    elif input_path.is_dir():
        # 处理目录
        if args.verbose:
            print(f"开始处理目录: {args.input_path}")
        
        if args.dry_run:
            # 模拟运行模式
            success_count = 0
            skip_count = 0
            fail_count = 0
            
            for file_path in input_path.rglob('*') if args.recursive else input_path.glob('*'):
                if file_path.is_file() and file_path.suffix.lower() in resizer.supported_formats:
                    try:
                        with Image.open(file_path) as img:
                            width, height = img.size
                            if resizer.should_resize(width, height):
                                new_width, new_height = resizer.calculate_new_size(width, height)
                                print(f"[模拟] 将缩放: {file_path} ({width}x{height}) -> ({new_width}x{new_height})")
                                success_count += 1
                            else:
                                print(f"[模拟] 无需缩放: {file_path} ({width}x{height})")
                                skip_count += 1
                    except Exception as e:
                        print(f"[模拟] 处理失败: {file_path} - {e}")
                        fail_count += 1
            
            print(f"\n[模拟] 处理完成:")
            print(f"  ✓ 将缩放: {success_count} 张")
            print(f"  ○ 将跳过: {skip_count} 张")
            print(f"  ✗ 将失败: {fail_count} 张")
        else:
            # 实际处理
            success, fail, skip = resizer.process_directory(args.input_path, args.output, args.rename)
            
            print(f"\n处理完成:")
            print(f"  ✓ 成功缩放: {success} 张")
            print(f"  ○ 跳过处理: {skip} 张")
            print(f"  ✗ 处理失败: {fail} 张")
        
    else:
        print(f"错误: 路径不存在: {args.input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()