# 快速开始指南 (Quick Start Guide)

这是一个完整的人脸识别系统快速开始教程。

## 第一步：安装依赖

### 方法1：使用pip（推荐）

```bash
pip install -r requirements.txt
```

### 方法2：逐个安装

```bash
pip install face_recognition==1.3.0
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
pip install Pillow==10.0.0
```

### 方法3：使用conda（推荐Windows用户）

```bash
conda create -n face_recognition python=3.8
conda activate face_recognition
conda install -c conda-forge dlib
pip install face_recognition opencv-python numpy Pillow
```

### 常见安装问题

#### 问题1: dlib安装失败

**Ubuntu/Debian系统**:
```bash
sudo apt-get update
sudo apt-get install cmake
sudo apt-get install libboost-all-dev
pip install dlib
```

**Windows系统**:
1. 使用Anaconda环境
2. 或下载预编译的wheel文件：
   ```bash
   pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp38-cp38-win_amd64.whl
   ```

**macOS系统**:
```bash
brew install cmake
pip install dlib
```

## 第二步：准备人脸数据库

1. 在项目根目录，人脸图片已经放在 `face_database/` 目录中
2. 图片命名规则：人名.jpg（如：张三.jpg、李四.png）
3. 支持的格式：.jpg、.jpeg、.png、.bmp、.gif

示例目录结构：
```
face_database/
├── 张三.jpg       # 张三的照片
├── 李四.jpg       # 李四的照片
├── 王五.png       # 王五的照片
└── 赵六.jpeg      # 赵六的照片
```

**照片要求**：
- ✅ 清晰的正面照片
- ✅ 光照均匀
- ✅ 人脸占比合适（建议人脸占图片1/3以上）
- ✅ 分辨率建议 ≥ 300x300 像素
- ❌ 避免过度模糊
- ❌ 避免严重遮挡
- ❌ 避免侧脸或背面

## 第三步：录入人脸

运行以下命令从 `face_database/` 目录录入所有人脸：

```bash
python main.py --mode enroll --database face_database
```

**输出示例**：
```
    ╔════════════════════════════════════════════╗
    ║     人脸识别系统 (Face Recognition System)  ║
    ║              Version 1.0.0                 ║
    ╚════════════════════════════════════════════╝

【人脸录入模式】

开始扫描文件夹: face_database
处理: 张三.jpg -> 张三
  ✓  成功编码
处理: 李四.jpg -> 李四
  ✓  成功编码
处理: 王五.png -> 王五
  ✓  成功编码

✓ 已保存 3 个人脸编码到 encodings/face_encodings.pkl

==================================================
录入统计:
  处理图片: 3
  成功录入: 3
  未检测到人脸: 0
  失败: 0
==================================================

✓ 人脸录入完成！
现在可以使用识别功能了
```

## 第四步：识别人脸

### 4.1 识别单张图片

```bash
python main.py --mode recognize --image test.jpg
```

**输出示例**：
```
【人脸识别模式】

✓ 已加载 3 个人脸编码
图片: test.jpg
检测到 1 个人脸

人脸 #1:
  姓名: 张三
  置信度: 95.23%
  距离: 0.0477
  位置: (150, 400, 350, 200)
```

### 4.2 识别并生成标注图片

```bash
python main.py --mode recognize --image test.jpg --visualize
```

这会生成一个标注了识别结果的图片（recognized_test.jpg）。

### 4.3 批量识别多张图片

```bash
python main.py --mode batch_recognize --folder test_images
```

## 第五步：高级功能

### 5.1 查看数据库统计

```bash
python main.py --mode stats
```

**输出示例**：
```
【数据库统计】

编码文件: encodings/face_encodings.pkl
总人脸数: 5
不同人数: 3

已录入人员:
  - 张三 (2 张照片)
  - 李四 (1 张照片)
  - 王五 (2 张照片)
```

### 5.2 添加单个人脸

```bash
python main.py --mode add --image new_person.jpg --name "新员工"
```

### 5.3 查看相似度分析

```bash
python main.py --mode match --image test.jpg --top-n 5
```

**输出示例**：
```
【相似度分析】

图片: test.jpg
前 5 个最相似的匹配:

1. 张三
   相似度: 95.23%
   距离: 0.0477
   状态: ✓ 匹配

2. 李四
   相似度: 42.18%
   距离: 0.5782
   状态: ✓ 匹配

3. 王五
   相似度: 15.67%
   距离: 0.8433
   状态: ✗ 不匹配
```

### 5.4 使用CNN模型（更准确）

```bash
python main.py --mode recognize --image test.jpg --model cnn
```

注意：CNN模型更准确但速度较慢，建议有GPU时使用。

### 5.5 调整识别阈值

```bash
python main.py --mode recognize --image test.jpg --tolerance 0.5
```

- tolerance值越小，识别越严格（默认0.6）
- 0.4-0.5：严格模式，减少误识别
- 0.6：标准模式（推荐）
- 0.7-0.8：宽松模式，提高识别率但可能误识别

## 常用命令速查表

| 功能 | 命令 |
|------|------|
| 录入人脸 | `python main.py --mode enroll --database face_database` |
| 识别人脸 | `python main.py --mode recognize --image test.jpg` |
| 可视化识别 | `python main.py --mode recognize --image test.jpg --visualize` |
| 批量识别 | `python main.py --mode batch_recognize --folder test_images` |
| 查看统计 | `python main.py --mode stats` |
| 添加人脸 | `python main.py --mode add --image photo.jpg --name "姓名"` |
| 相似度分析 | `python main.py --mode match --image test.jpg` |
| 使用CNN模型 | `python main.py --mode recognize --image test.jpg --model cnn` |
| 调整阈值 | `python main.py --mode recognize --image test.jpg --tolerance 0.5` |

## 在Python代码中使用

除了命令行，你也可以在Python代码中直接使用：

```python
from src.face_encoder import FaceEncoder
from src.face_recognizer import FaceRecognizer

# 录入人脸
encoder = FaceEncoder()
encoder.encode_faces_from_folder("face_database")

# 识别人脸
recognizer = FaceRecognizer()
results = recognizer.recognize_faces("test.jpg")

for result in results:
    print(f"识别为: {result['name']}, 置信度: {result['confidence']:.2%}")
```

更多使用示例请查看 `examples/example_usage.py`。

## 性能优化建议

### 提高准确率
1. 每人录入3-5张不同角度的照片
2. 使用高质量、光照均匀的照片
3. 使用CNN模型：`--model cnn`
4. 调整阈值：`--tolerance 0.5`

### 提高速度
1. 使用HOG模型（默认）
2. 降低图片分辨率
3. 使用GPU版本的dlib：`pip install dlib-gpu`
4. 批量处理而非逐个处理

## 故障排除

### 问题1：未检测到人脸
- 检查图片质量和分辨率
- 确保人脸清晰可见
- 尝试使用CNN模型：`--model cnn`
- 检查图片是否正确加载

### 问题2：识别错误
- 增加训练样本（每人多张照片）
- 使用高质量照片
- 调整阈值：`--tolerance 0.5`（更严格）
- 检查光照条件

### 问题3：处理速度慢
- 使用HOG模型而非CNN
- 降低图片分辨率
- 考虑使用GPU加速

### 问题4：内存占用高
- 分批处理图片
- 减少数据库中的人脸数量
- 优化图片分辨率

## 下一步

- 查看 `README.md` 了解系统架构和技术原理
- 查看 `TECHNICAL_GUIDE.md` 了解详细技术细节
- 查看 `examples/example_usage.py` 学习更多使用方法
- 尝试实现实时摄像头识别
- 添加Web界面或GUI

## 获取帮助

如有问题，请：
1. 查看项目文档
2. 检查常见问题部分
3. 提交Issue到GitHub仓库
