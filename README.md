# QQ图片缩放工具

一个专门用于缩放图片尺寸的Python工具，让在QQ（手机版）中发送的图片能和表情包大小一样缩放。

## 功能特性

- 🔄 **智能缩放**: 自动按比例缩放图片，最长边不超过542像素
- 📱 **QQ优化**: 专门针对QQ手机版发送图片的尺寸限制优化
- 🖼️ **格式支持**: 支持PNG和JPG格式图片
- ⚡ **高效处理**: 小于542像素的图片自动跳过，只处理需要缩放的图片
- 🛠️ **简单易用**: 提供命令行界面，一键批量处理

## 安装

### 环境要求

- Python 3.7+
- Pillow库

### 安装步骤

1. 克隆项目：
```bash
git clone https://github.com/yourusername/qq-image-resizer.git
cd qq-image-resizer
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```bash
# 缩放单个图片
python resize_img.py input.jpg

# 缩放整个文件夹的图片
python resize_img.py /path/to/images/

# 指定输出目录
python resize_img.py input.jpg --output ./resized/

# 按序号重命名所有图片
python resize_img.py /path/to/images/ --rename
```

### 参数说明

- `input_path`: 输入文件或目录路径（必需）
- `--output`, `-o`: 输出目录路径（可选，默认为当前目录）
- `--max-size`, `-s`: 最大边长（可选，默认为542）
- `--quality`, `-q`: 图片质量/压缩级别（可选，默认100，不压缩。）
- `--rename`: 按序号重命名所有图片（可选，生成00001.jpg, 00002.png等文件名）

## 技术原理

QQ手机版发送图片时，如果图片尺寸超过542像素，会自动放大显示。本工具通过以下步骤处理：

1. **检测尺寸**: 读取图片的宽度和高度
2. **判断需求**: 如果最长边 ≤ 542像素，跳过处理
3. **按比例缩放**: 保持宽高比，将最长边缩放到542像素
4. **质量保持**: 保持图片质量，优化文件大小

## 项目结构

```
qq-image-resizer/
├── resize_img.py      # 主程序文件
├── requirements.txt   # 依赖文件
├── README.md         # 说明文档
└── examples/         # 示例文件
    ├── input/        # 输入图片示例
    └── output/       # 输出图片示例
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 更新日志

### v1.0.1
- 修改默认参数

### v1.0.0
- 初始版本发布
- 支持PNG和JPG格式
- 实现智能缩放功能