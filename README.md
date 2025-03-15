![deepseek-color](https://github.com/user-attachments/assets/535dd91a-6844-4890-930e-4d939863f0d0)
# 多语言文件翻译器

这是一个基于 Deepseek API 的多语言文件翻译工具，支持多种语言之间的互译。

## 功能特点

- 支持多种语言之间的互译
- 实时显示翻译进度
- 友好的图形用户界面
- 支持大文件翻译
- 保留原文格式
- 安全的 API 密钥输入

## 安装步骤

1. 确保已安装 Python 3.7 或更高版本
2. 安装依赖包(py文件时，使用)：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 运行程序(py文件时，使用)：
   ```bash
   python translator.py
   ```
2. 在程序界面中输入您的 Deepseek API 密钥
3. 选择源文件语言和目标语言
4. 点击"浏览"按钮选择要翻译的文本文件
5. 点击"开始翻译"按钮开始翻译
6. 等待翻译完成，翻译后的文件将保存在原文件同目录下，文件名后缀为"_translated.txt"

## 注意事项

- 请确保您有有效的 Deepseek API 密钥
- 注册api网址:https://platform.deepseek.com/
- 建议翻译前备份原文件
- 程序支持的文件格式为 .txt
- 翻译过程中请保持网络连接 
