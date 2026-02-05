"""
人脸识别系统使用示例 (Face Recognition System Usage Examples)

本文件展示了如何在Python代码中使用人脸识别系统的各个模块
"""

from src.face_encoder import FaceEncoder
from src.face_recognizer import FaceRecognizer


def example_1_basic_enrollment():
    """示例1: 基本的人脸录入"""
    print("="*60)
    print("示例1: 基本的人脸录入")
    print("="*60)
    
    # 创建编码器
    encoder = FaceEncoder(encodings_file="encodings/face_encodings.pkl")
    
    # 从文件夹批量录入人脸
    stats = encoder.encode_faces_from_folder("face_database", model="hog")
    
    print(f"\n录入结果:")
    print(f"  成功: {stats['success']}")
    print(f"  失败: {stats['failed']}")
    print(f"  未检测到人脸: {stats['no_face']}")


def example_2_single_face_addition():
    """示例2: 添加单个人脸"""
    print("\n" + "="*60)
    print("示例2: 添加单个人脸")
    print("="*60)
    
    # 创建编码器
    encoder = FaceEncoder(encodings_file="encodings/face_encodings.pkl")
    
    # 添加单个人脸
    success = encoder.add_face(
        image_path="face_database/张三.jpg",
        name="张三",
        model="hog"
    )
    
    if success:
        print("\n✓ 人脸添加成功")
    else:
        print("\n✗ 人脸添加失败")


def example_3_basic_recognition():
    """示例3: 基本的人脸识别"""
    print("\n" + "="*60)
    print("示例3: 基本的人脸识别")
    print("="*60)
    
    # 创建识别器
    recognizer = FaceRecognizer(
        encodings_file="encodings/face_encodings.pkl",
        tolerance=0.6
    )
    
    # 识别图片中的人脸
    results = recognizer.recognize_faces("test.jpg", model="hog")
    
    # 打印结果
    print(f"\n检测到 {len(results)} 个人脸:")
    for i, result in enumerate(results, 1):
        print(f"\n人脸 #{i}:")
        print(f"  姓名: {result['name']}")
        print(f"  置信度: {result['confidence']:.2%}")
        print(f"  距离: {result['distance']:.4f}")


def example_4_detailed_recognition():
    """示例4: 详细的人脸识别信息"""
    print("\n" + "="*60)
    print("示例4: 详细的人脸识别信息")
    print("="*60)
    
    # 创建识别器
    recognizer = FaceRecognizer(encodings_file="encodings/face_encodings.pkl")
    
    # 获取详细识别结果
    result = recognizer.recognize_face_detailed("test.jpg", model="hog")
    
    print(f"\n图片: {result['image_path']}")
    print(f"检测到人脸数: {result['faces_detected']}")
    
    for face in result['faces']:
        print(f"\n  姓名: {face['name']}")
        print(f"  置信度: {face['confidence']:.2%}")
        print(f"  距离: {face['distance']:.4f}")
        print(f"  位置: {face['location']}")


def example_5_visualize_recognition():
    """示例5: 可视化识别结果"""
    print("\n" + "="*60)
    print("示例5: 可视化识别结果")
    print("="*60)
    
    # 创建识别器
    recognizer = FaceRecognizer(encodings_file="encodings/face_encodings.pkl")
    
    # 识别并在图片上标注结果
    output_path = recognizer.visualize_recognition(
        image_path="test.jpg",
        output_path="result.jpg",
        model="hog"
    )
    
    print(f"\n✓ 标注图片已保存到: {output_path}")


def example_6_batch_recognition():
    """示例6: 批量识别"""
    print("\n" + "="*60)
    print("示例6: 批量识别")
    print("="*60)
    
    # 创建识别器
    recognizer = FaceRecognizer(encodings_file="encodings/face_encodings.pkl")
    
    # 批量识别文件夹中的所有图片
    results = recognizer.batch_recognize("test_images", model="hog")
    
    # 统计
    total_images = len(results)
    total_faces = sum(r['faces_detected'] for r in results)
    
    print(f"\n统计:")
    print(f"  处理图片: {total_images}")
    print(f"  检测人脸: {total_faces}")


def example_7_top_matches():
    """示例7: 获取最相似的匹配"""
    print("\n" + "="*60)
    print("示例7: 获取最相似的匹配")
    print("="*60)
    
    # 创建识别器
    recognizer = FaceRecognizer(encodings_file="encodings/face_encodings.pkl")
    
    # 获取前5个最相似的匹配
    matches = recognizer.get_match_info("test.jpg", top_n=5, model="hog")
    
    print(f"\n前5个最相似的匹配:")
    for i, match in enumerate(matches, 1):
        status = "✓" if match['is_match'] else "✗"
        print(f"\n{i}. {match['name']} {status}")
        print(f"   相似度: {match['confidence']:.2%}")
        print(f"   距离: {match['distance']:.4f}")


def example_8_custom_tolerance():
    """示例8: 自定义容差"""
    print("\n" + "="*60)
    print("示例8: 自定义容差")
    print("="*60)
    
    # 创建识别器，使用更严格的容差
    recognizer = FaceRecognizer(
        encodings_file="encodings/face_encodings.pkl",
        tolerance=0.5  # 更小的值意味着更严格的匹配
    )
    
    results = recognizer.recognize_faces("test.jpg", model="hog")
    
    print(f"\n使用容差 0.5 (更严格):")
    for result in results:
        print(f"  {result['name']} - 置信度: {result['confidence']:.2%}")


def example_9_statistics():
    """示例9: 获取数据库统计信息"""
    print("\n" + "="*60)
    print("示例9: 获取数据库统计信息")
    print("="*60)
    
    # 创建编码器
    encoder = FaceEncoder(encodings_file="encodings/face_encodings.pkl")
    
    # 获取统计信息
    stats = encoder.get_statistics()
    
    print(f"\n数据库统计:")
    print(f"  总人脸数: {stats['total_faces']}")
    print(f"  不同人数: {stats['unique_names']}")


def example_10_using_cnn_model():
    """示例10: 使用CNN模型（更准确但需要GPU）"""
    print("\n" + "="*60)
    print("示例10: 使用CNN模型")
    print("="*60)
    
    # 创建识别器
    recognizer = FaceRecognizer(encodings_file="encodings/face_encodings.pkl")
    
    # 使用CNN模型进行识别（更准确但更慢）
    results = recognizer.recognize_faces("test.jpg", model="cnn")
    
    print(f"\n使用CNN模型识别:")
    for result in results:
        print(f"  {result['name']} - 置信度: {result['confidence']:.2%}")


def main():
    """运行所有示例（需要相应的图片文件）"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*10 + "人脸识别系统 - 使用示例" + " "*22 + "║")
    print("╚" + "="*58 + "╝\n")
    
    print("注意: 运行这些示例前，请确保:")
    print("1. 已安装所有依赖 (pip install -r requirements.txt)")
    print("2. face_database/ 目录中有人脸图片")
    print("3. 已运行人脸录入流程")
    print("\n" + "-"*60 + "\n")
    
    # 取消注释你想运行的示例
    # example_1_basic_enrollment()
    # example_2_single_face_addition()
    # example_3_basic_recognition()
    # example_4_detailed_recognition()
    # example_5_visualize_recognition()
    # example_6_batch_recognition()
    # example_7_top_matches()
    # example_8_custom_tolerance()
    # example_9_statistics()
    # example_10_using_cnn_model()
    
    print("\n取消注释想要运行的示例函数")


if __name__ == "__main__":
    main()
