"""
人脸识别系统 - 主程序
Face Recognition System - Main Program

使用说明:
1. 录入人脸: python main.py --mode enroll --database face_database
2. 识别人脸: python main.py --mode recognize --image test.jpg
3. 批量识别: python main.py --mode batch_recognize --folder test_images
4. 查看统计: python main.py --mode stats
5. 显示帮助: python main.py --help
"""

import argparse
import os
import sys
from src.face_encoder import FaceEncoder
from src.face_recognizer import FaceRecognizer


def print_banner():
    """打印程序横幅"""
    banner = """
    ╔════════════════════════════════════════════╗
    ║     人脸识别系统 (Face Recognition System)  ║
    ║              Version 1.0.0                 ║
    ╚════════════════════════════════════════════╝
    """
    print(banner)


def enroll_faces(args):
    """录入人脸模式"""
    print("\n【人脸录入模式】\n")
    
    if not os.path.exists(args.database):
        print(f"✗ 数据库目录不存在: {args.database}")
        print(f"请创建目录并放入人脸图片")
        return
    
    # 创建编码器
    encoder = FaceEncoder(encodings_file=args.encodings)
    
    # 批量编码
    stats = encoder.encode_faces_from_folder(args.database, model=args.model)
    
    # 打印统计信息
    print("\n" + "="*50)
    print("录入统计:")
    print(f"  处理图片: {stats['processed']}")
    print(f"  成功录入: {stats['success']}")
    print(f"  未检测到人脸: {stats['no_face']}")
    print(f"  失败: {stats['failed']}")
    print("="*50)
    
    if stats['success'] > 0:
        print(f"\n✓ 人脸录入完成！")
        print(f"现在可以使用识别功能了")
    else:
        print(f"\n⚠️  未成功录入任何人脸")


def recognize_face(args):
    """识别单张图片"""
    print("\n【人脸识别模式】\n")
    
    if not os.path.exists(args.image):
        print(f"✗ 图片不存在: {args.image}")
        return
    
    # 创建识别器
    recognizer = FaceRecognizer(
        encodings_file=args.encodings,
        tolerance=args.tolerance
    )
    
    # 识别人脸
    results = recognizer.recognize_faces(args.image, model=args.model)
    
    # 打印结果
    print(f"图片: {args.image}")
    print(f"检测到 {len(results)} 个人脸\n")
    
    if len(results) == 0:
        print("未检测到人脸")
        return
    
    for i, result in enumerate(results, 1):
        print(f"人脸 #{i}:")
        print(f"  姓名: {result['name']}")
        print(f"  置信度: {result['confidence']:.2%}")
        print(f"  距离: {result['distance']:.4f}")
        print(f"  位置: {result['location']}")
        print()
    
    # 如果需要可视化
    if args.visualize:
        output_path = recognizer.visualize_recognition(
            args.image, 
            model=args.model
        )
        print(f"✓ 已生成标注图片: {output_path}")


def batch_recognize(args):
    """批量识别模式"""
    print("\n【批量识别模式】\n")
    
    if not os.path.exists(args.folder):
        print(f"✗ 文件夹不存在: {args.folder}")
        return
    
    # 创建识别器
    recognizer = FaceRecognizer(
        encodings_file=args.encodings,
        tolerance=args.tolerance
    )
    
    # 批量识别
    results = recognizer.batch_recognize(args.folder, model=args.model)
    
    # 统计信息
    total_images = len(results)
    total_faces = sum(r['faces_detected'] for r in results)
    recognized = sum(
        len([f for f in r['faces'] if f['name'] != 'Unknown']) 
        for r in results
    )
    
    print("\n" + "="*50)
    print("识别统计:")
    print(f"  处理图片: {total_images}")
    print(f"  检测人脸: {total_faces}")
    print(f"  识别成功: {recognized}")
    print(f"  未识别: {total_faces - recognized}")
    print("="*50)


def show_stats(args):
    """显示统计信息"""
    print("\n【数据库统计】\n")
    
    if not os.path.exists(args.encodings):
        print(f"✗ 编码文件不存在: {args.encodings}")
        print("请先运行人脸录入流程")
        return
    
    # 加载编码器
    encoder = FaceEncoder(encodings_file=args.encodings)
    stats = encoder.get_statistics()
    
    print(f"编码文件: {args.encodings}")
    print(f"总人脸数: {stats['total_faces']}")
    print(f"不同人数: {stats['unique_names']}")
    
    # 显示所有人名
    if stats['total_faces'] > 0:
        print(f"\n已录入人员:")
        unique_names = set(encoder.known_names)
        for name in sorted(unique_names):
            count = encoder.known_names.count(name)
            print(f"  - {name} ({count} 张照片)")


def add_face(args):
    """添加单个人脸"""
    print("\n【添加人脸】\n")
    
    if not os.path.exists(args.image):
        print(f"✗ 图片不存在: {args.image}")
        return
    
    if not args.name:
        print(f"✗ 请指定人员姓名 (--name)")
        return
    
    # 创建编码器
    encoder = FaceEncoder(encodings_file=args.encodings)
    
    # 添加人脸
    success = encoder.add_face(args.image, args.name, model=args.model)
    
    if success:
        print(f"\n✓ 成功添加 {args.name} 的人脸")
    else:
        print(f"\n✗ 添加失败")


def get_top_matches(args):
    """获取最相似的匹配"""
    print("\n【相似度分析】\n")
    
    if not os.path.exists(args.image):
        print(f"✗ 图片不存在: {args.image}")
        return
    
    # 创建识别器
    recognizer = FaceRecognizer(
        encodings_file=args.encodings,
        tolerance=args.tolerance
    )
    
    # 获取匹配
    matches = recognizer.get_match_info(
        args.image, 
        top_n=args.top_n, 
        model=args.model
    )
    
    if len(matches) == 0:
        print("未检测到人脸或数据库为空")
        return
    
    print(f"图片: {args.image}")
    print(f"前 {args.top_n} 个最相似的匹配:\n")
    
    for i, match in enumerate(matches, 1):
        status = "✓ 匹配" if match['is_match'] else "✗ 不匹配"
        print(f"{i}. {match['name']}")
        print(f"   相似度: {match['confidence']:.2%}")
        print(f"   距离: {match['distance']:.4f}")
        print(f"   状态: {status}")
        print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="人脸识别系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 录入人脸
  python main.py --mode enroll --database face_database
  
  # 识别人脸
  python main.py --mode recognize --image test.jpg
  
  # 批量识别
  python main.py --mode batch_recognize --folder test_images
  
  # 查看统计
  python main.py --mode stats
  
  # 添加单个人脸
  python main.py --mode add --image photo.jpg --name "张三"
  
  # 获取相似度分析
  python main.py --mode match --image test.jpg --top-n 5
        """
    )
    
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        choices=["enroll", "recognize", "batch_recognize", "stats", "add", "match"],
        help="运行模式"
    )
    
    parser.add_argument(
        "--database",
        type=str,
        default="face_database",
        help="人脸数据库目录 (默认: face_database)"
    )
    
    parser.add_argument(
        "--image",
        type=str,
        help="图片路径"
    )
    
    parser.add_argument(
        "--folder",
        type=str,
        help="图片文件夹路径"
    )
    
    parser.add_argument(
        "--name",
        type=str,
        help="人员姓名"
    )
    
    parser.add_argument(
        "--encodings",
        type=str,
        default="encodings/face_encodings.pkl",
        help="编码文件路径 (默认: encodings/face_encodings.pkl)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="hog",
        choices=["hog", "cnn"],
        help="人脸检测模型 (默认: hog, 更快但不够准确; cnn: 更准确但需要GPU)"
    )
    
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.6,
        help="人脸匹配容差，越小越严格 (默认: 0.6)"
    )
    
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="生成标注图片"
    )
    
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="显示前N个最相似的匹配 (默认: 5)"
    )
    
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    
    # 根据模式执行相应功能
    if args.mode == "enroll":
        enroll_faces(args)
    elif args.mode == "recognize":
        recognize_face(args)
    elif args.mode == "batch_recognize":
        batch_recognize(args)
    elif args.mode == "stats":
        show_stats(args)
    elif args.mode == "add":
        add_face(args)
    elif args.mode == "match":
        get_top_matches(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ 发生错误: {str(e)}")
        sys.exit(1)
