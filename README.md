# 基本人脸识别系统 (Basic Face Recognition System)

## 项目简介 (Project Introduction)

这是一个基于Python开发的基本人脸识别系统，能够从人员照片数据库中识别具体的人。本系统使用免费开源资源，适合独立开发者使用。

## 技术路线 (Technical Route)

### 1. 技术栈选型 (Technology Stack)

#### 核心库 (Core Libraries)
- **face_recognition**: 基于dlib的人脸识别库，简单易用，准确率高
  - 优点：API简洁，封装完善，支持人脸检测、特征提取和比对
  - 基于dlib的深度学习模型，准确率达99.38%
  
- **OpenCV (cv2)**: 图像处理库
  - 用于图像读取、预处理和显示
  - 强大的计算机视觉功能
  
- **NumPy**: 数值计算库
  - 用于处理图像数据和特征向量

- **Pillow**: Python图像处理库
  - 用于图像格式转换和基本操作

#### 为什么选择这些技术？
1. **免费开源**: 所有库都是开源的，无需付费
2. **易于使用**: face_recognition提供了高级API，降低了开发难度
3. **跨平台**: 支持Windows、Linux、MacOS
4. **活跃社区**: 有大量文档和社区支持
5. **准确性好**: 基于深度学习模型，在LFW数据集上准确率99.38%

### 2. 系统架构设计 (System Architecture)

```
┌─────────────────────────────────────────┐
│          用户界面 (User Interface)        │
│         命令行接口 (CLI)                   │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│        主程序 (Main Program)              │
│         - 录入模式                         │
│         - 识别模式                         │
└─────────────┬───────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────────┐  ┌──────▼──────┐
│ 人脸编码器  │  │  人脸识别器   │
│  Encoder   │  │  Recognizer  │
└───┬────────┘  └──────┬───────┘
    │                  │
    └────────┬─────────┘
             │
    ┌────────▼─────────┐
    │   人脸数据库      │
    │  Face Database   │
    │  (编码特征向量)    │
    └──────────────────┘
```

### 3. 工作流程 (Workflow)

#### 人脸录入流程 (Face Enrollment)
1. 读取待录入的人脸图片
2. 检测图片中的人脸
3. 提取人脸特征向量（128维编码）
4. 将特征向量和人员信息保存到数据库

#### 人脸识别流程 (Face Recognition)
1. 读取待识别的人脸图片
2. 检测图片中的人脸
3. 提取人脸特征向量
4. 与数据库中的特征向量进行比对
5. 返回最匹配的人员信息和相似度

### 4. 核心算法原理 (Core Algorithm)

#### 人脸检测 (Face Detection)
- 使用HOG (Histogram of Oriented Gradients) 或 CNN方法
- 定位图片中人脸的位置

#### 特征提取 (Feature Extraction)
- 使用深度学习模型提取128维人脸特征向量
- 每个人脸被转换为一个128维的数字向量

#### 人脸比对 (Face Comparison)
- 计算两个特征向量之间的欧氏距离
- 距离越小，相似度越高
- 设置阈值（通常0.6）判断是否为同一人

## 快速开始 (Quick Start)

### 1. 安装依赖 (Install Dependencies)

```bash
pip install -r requirements.txt
```

**注意**: 
- 在Linux上，可能需要先安装cmake和dlib依赖：
  ```bash
  sudo apt-get install cmake
  sudo apt-get install libboost-all-dev
  ```
- 在Windows上，建议使用Anaconda环境

### 2. 准备人脸数据库 (Prepare Face Database)

将已知人员的照片放入 `face_database/` 目录：

```
face_database/
├── 张三.jpg
├── 李四.jpg
└── 王五.jpg
```

### 3. 录入人脸 (Enroll Faces)

```bash
python main.py --mode enroll --database face_database
```

这将扫描 `face_database/` 目录中的所有图片，提取人脸特征并保存。

### 4. 识别人脸 (Recognize Faces)

```bash
python main.py --mode recognize --image test.jpg
```

这将识别 `test.jpg` 中的人脸，并返回匹配结果。

## 使用示例 (Usage Examples)

### 示例1: 批量录入人脸
```bash
python main.py --mode enroll --database ./photos
```

### 示例2: 识别单张照片
```bash
python main.py --mode recognize --image ./unknown.jpg
```

### 示例3: 批量识别
```bash
python main.py --mode batch_recognize --folder ./test_images
```

## 项目结构 (Project Structure)

```
SIE/
├── README.md                 # 项目文档
├── requirements.txt          # 依赖列表
├── main.py                   # 主程序入口
├── src/
│   ├── __init__.py
│   ├── face_encoder.py       # 人脸编码模块
│   └── face_recognizer.py    # 人脸识别模块
├── face_database/            # 人脸数据库目录
│   └── .gitkeep
├── encodings/                # 编码文件存储
│   └── .gitkeep
└── examples/                 # 使用示例
    └── example_usage.py

```

## 性能和限制 (Performance and Limitations)

### 性能指标
- **准确率**: 在标准数据集上约99%
- **处理速度**: 单张照片识别约0.5-2秒（取决于硬件）
- **支持人脸数**: 建议100人以内效果最佳

### 限制
1. 对光照条件敏感，建议使用光照均匀的照片
2. 人脸角度不宜过大（±45度以内）
3. 遮挡过多会影响识别效果
4. 需要清晰的人脸图片（建议分辨率大于200x200像素）

## 技术细节 (Technical Details)

### 人脸编码
- 使用ResNet深度学习模型
- 输出128维特征向量
- 向量经过归一化处理

### 相似度判断
- 欧氏距离阈值: 0.6（可调整）
- 距离 < 0.6: 同一人
- 距离 >= 0.6: 不同人

### 优化建议
1. **提高准确率**: 
   - 每人录入多张不同角度的照片
   - 使用高质量照片
   - 统一照片规格和光照条件

2. **提高速度**:
   - 使用GPU加速（安装dlib GPU版本）
   - 降低图片分辨率
   - 使用HOG而非CNN进行人脸检测

3. **扩展功能**:
   - 添加实时摄像头识别
   - 添加GUI界面
   - 集成到Web应用

## 故障排除 (Troubleshooting)

### 问题1: 安装dlib失败
**解决方案**: 
- 确保安装了cmake
- 使用预编译的wheel文件
- 在Anaconda环境中安装

### 问题2: 无法检测到人脸
**解决方案**:
- 检查图片质量和分辨率
- 尝试使用CNN模型: `model='cnn'`
- 确保人脸清晰可见

### 问题3: 识别准确率低
**解决方案**:
- 增加每人的训练照片数量
- 使用高质量、正面照片
- 调整相似度阈值

## 许可证 (License)

MIT License

## 贡献 (Contributing)

欢迎提交Issue和Pull Request！

## 参考资料 (References)

- [face_recognition官方文档](https://github.com/ageitgey/face_recognition)
- [dlib官方网站](http://dlib.net/)
- [OpenCV官方文档](https://opencv.org/)
