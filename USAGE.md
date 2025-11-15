# 使用指南

本文档详细说明如何使用QQ图片缩放工具。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 基本使用

```bash
# 缩放单张图片
python resize_img.py image.jpg

# 缩放目录中的所有图片
python resize_img.py /path/to/images/

# 指定输出目录
python resize_img.py input.jpg -o ./resized/
```

## 详细参数说明

### 必需参数

- `input_path`: 输入文件或目录路径

### 可选参数

- `-o, --output`: 输出目录路径（默认：）
- `-s, --max-size`: 最大边长（默认：542像素）
- `-q, --quality`: 图片质量/压缩级别（1-100，默认：100，不压缩。控制所有类型：JPEG直接使用，PNG映射到compress_level）
- `-r, --recursive`: 递归处理子目录
- `-v, --verbose`: 显示详细输出
- `--dry-run`: 模拟运行，不实际修改文件

## 使用示例

### 示例1：缩放单张图片

```bash
# 缩放单张图片（覆盖原文件）
python resize_img.py photo.jpg

# 缩放单张图片并保存到指定目录
python resize_img.py photo.jpg -o ./resized/

# 自定义最大边长为500像素
python resize_img.py photo.jpg -s 500

# 设置图片质量为85（控制所有类型压缩）
python resize_img.py photo.jpg -q 85
```

### 示例2：批量处理目录

```bash
# 处理目录中的所有图片
python resize_img.py ./photos/

# 递归处理子目录
python resize_img.py ./photos/ -r

# 处理目录并保存到新目录
python resize_img.py ./photos/ -o ./resized_photos/

# 显示详细处理信息
python resize_img.py ./photos/ -v
```

### 示例3：模拟运行（安全测试）

```bash
# 模拟运行，查看哪些文件会被处理
python resize_img.py ./photos/ --dry-run -v

# 模拟递归处理
python resize_img.py ./photos/ --dry-run -r -v
```

## 实际应用场景

### 场景1：QQ聊天图片优化

```bash
# 将聊天图片目录中的所有图片缩放到QQ兼容尺寸
python resize_img.py ./qq_chat_images/ -o ./optimized_images/ -v
```

### 场景2：批量处理手机相册

```bash
# 递归处理手机相册目录
python resize_img.py ./手机相册/ -r -o ./优化后的图片/ -v
```

### 场景3：网站图片优化

```bash
# 将网站图片缩放到合适尺寸
python resize_img.py ./website_images/ -s 800 -o ./optimized/ -v
```

## 处理结果说明

### 处理状态

- **✓ 成功缩放**: 图片被成功缩放到目标尺寸
- **○ 跳过处理**: 图片尺寸合适，无需缩放
- **✗ 处理失败**: 图片处理过程中出现错误

### 输出示例

```
开始处理目录: ./photos/
最大边长: 542px
图片质量: 100
递归处理: 是
模拟运行: 否
--------------------------------------------------
缩放图片: ./photos/image1.jpg (800x600) -> (542x406)
图片尺寸合适，跳过: ./photos/image2.jpg (400x300)
缩放图片: ./photos/image3.jpg (1200x900) -> (542x406)
跳过不支持的文件格式: ./photos/document.pdf

处理完成:
  ✓ 成功缩放: 2 张
  ○ 跳过处理: 1 张
  ✗ 处理失败: 0 张
```

## 注意事项

1. **文件格式**: 只支持 JPG、JPEG、PNG 格式
2. **文件权限**: 确保有读写权限
3. **备份重要文件**: 建议先使用 `--dry-run` 测试
4. **大文件处理**: 超大图片可能需要更多内存
5. **质量设置**: quality参数统一控制所有类型的压缩（JPEG使用quality值1-100，PNG映射到compress_level 0-9，100对应无压缩）

## 故障排除

### 常见问题

**Q: 程序报错 "No module named 'PIL'"**
A: 请安装依赖：`pip install -r requirements.txt`

**Q: 图片处理失败**
A: 检查图片文件是否损坏，或尝试降低质量参数

**Q: 处理速度慢**
A: 大图片处理需要时间，可以尝试降低质量设置

**Q: 内存不足**
A: 处理超大图片时可能出现，建议分批处理

### 调试技巧

```bash
# 使用详细模式查看具体错误
python resize_img.py problem.jpg -v

# 使用模拟运行测试
python resize_img.py ./problem_dir/ --dry-run -v

# 检查单个文件
python resize_img.py specific_file.jpg
```

## 高级用法

### 集成到其他脚本

```python
from resize_img import QQImageResizer

# 创建缩放器实例
resizer = QQImageResizer(max_size=542)

# 处理单张图片
result = resizer.resize_image("input.jpg", "output.jpg")

# 处理目录
success, fail, skip = resizer.process_directory("./input/", "./output/")
```

### 自定义处理逻辑

可以修改 `resize_img.py` 中的 `QQImageResizer` 类来实现自定义的缩放逻辑。

---

如有问题，请查看 [README.md](README.md) 或提交 Issue。