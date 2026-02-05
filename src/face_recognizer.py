"""
人脸识别器模块 (Face Recognizer Module)
用于识别图片中的人脸并与数据库匹配
"""

import face_recognition
import pickle
import os
from typing import List, Tuple, Dict, Optional
import cv2
import numpy as np


class FaceRecognizer:
    """
    人脸识别器类
    负责识别图片中的人脸并与数据库中的人脸进行匹配
    """
    
    def __init__(self, encodings_file: str = "encodings/face_encodings.pkl", 
                 tolerance: float = 0.6):
        """
        初始化人脸识别器
        
        Args:
            encodings_file: 编码文件路径
            tolerance: 人脸匹配容差，越小越严格（默认0.6）
        """
        self.encodings_file = encodings_file
        self.tolerance = tolerance
        self.known_encodings = []
        self.known_names = []
        
        # 加载已有编码
        if os.path.exists(encodings_file):
            self.load_encodings()
        else:
            print(f"⚠️  编码文件不存在: {encodings_file}")
            print("请先运行人脸录入流程")
    
    def load_encodings(self):
        """从文件加载编码"""
        try:
            with open(self.encodings_file, "rb") as f:
                data = pickle.load(f)
                self.known_encodings = data["encodings"]
                self.known_names = data["names"]
            print(f"✓ 已加载 {len(self.known_names)} 个人脸编码")
        except Exception as e:
            print(f"⚠️  加载编码失败: {str(e)}")
            self.known_encodings = []
            self.known_names = []
    
    def recognize_faces(self, image_path: str, model: str = "hog") -> List[Dict]:
        """
        识别图片中的所有人脸
        
        Args:
            image_path: 图片路径
            model: 人脸检测模型，'hog' 或 'cnn'
        
        Returns:
            识别结果列表，每个结果包含：
            - name: 识别到的姓名（未知则为"Unknown"）
            - confidence: 置信度（距离的倒数）
            - distance: 与数据库中最接近人脸的距离
            - location: 人脸位置 (top, right, bottom, left)
        """
        if len(self.known_encodings) == 0:
            print("⚠️  数据库为空，请先录入人脸")
            return []
        
        # 读取图片
        image = face_recognition.load_image_file(image_path)
        
        # 检测人脸位置
        face_locations = face_recognition.face_locations(image, model=model)
        
        # 提取人脸编码
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        results = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # 计算与所有已知人脸的距离
            distances = face_recognition.face_distance(
                self.known_encodings, face_encoding
            )
            
            # 找到最小距离
            min_distance = np.min(distances)
            min_index = np.argmin(distances)
            
            # 判断是否匹配
            if min_distance <= self.tolerance:
                name = self.known_names[min_index]
                confidence = 1.0 - min_distance  # 转换为置信度
            else:
                name = "Unknown"
                confidence = 0.0
            
            results.append({
                "name": name,
                "confidence": float(confidence),
                "distance": float(min_distance),
                "location": face_location
            })
        
        return results
    
    def recognize_face_detailed(self, image_path: str, model: str = "hog") -> Dict:
        """
        识别图片中的人脸（详细信息）
        
        Args:
            image_path: 图片路径
            model: 人脸检测模型
        
        Returns:
            详细识别结果
        """
        results = self.recognize_faces(image_path, model=model)
        
        return {
            "image_path": image_path,
            "faces_detected": len(results),
            "faces": results
        }
    
    def visualize_recognition(self, image_path: str, output_path: str = None, 
                            model: str = "hog") -> str:
        """
        识别人脸并在图片上标注结果
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径（为None则自动生成）
            model: 人脸检测模型
        
        Returns:
            输出图片路径
        """
        # 读取图片
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 识别人脸
        results = self.recognize_faces(image_path, model=model)
        
        # 在图片上绘制结果
        for result in results:
            top, right, bottom, left = result["location"]
            
            # 绘制人脸框
            color = (0, 255, 0) if result["name"] != "Unknown" else (0, 0, 255)
            cv2.rectangle(image, (left, top), (right, bottom), color, 2)
            
            # 绘制标签背景
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            
            # 绘制文字
            font = cv2.FONT_HERSHEY_DUPLEX
            text = f"{result['name']} ({result['confidence']:.2f})"
            cv2.putText(image, text, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
        
        # 保存输出图片
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = f"recognized_{base_name}.jpg"
        
        cv2.imwrite(output_path, image)
        print(f"✓ 已保存标注结果到: {output_path}")
        
        return output_path
    
    def batch_recognize(self, folder_path: str, model: str = "hog") -> List[Dict]:
        """
        批量识别文件夹中的所有图片
        
        Args:
            folder_path: 图片文件夹路径
            model: 人脸检测模型
        
        Returns:
            所有图片的识别结果列表
        """
        from pathlib import Path
        
        folder = Path(folder_path)
        results = []
        
        # 支持的图片格式
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
        
        print(f"开始批量识别文件夹: {folder_path}")
        
        for image_path in folder.iterdir():
            if not image_path.is_file():
                continue
            
            if image_path.suffix.lower() not in image_extensions:
                continue
            
            print(f"\n处理: {image_path.name}")
            
            try:
                result = self.recognize_face_detailed(str(image_path), model=model)
                results.append(result)
                
                # 打印识别结果
                for face in result["faces"]:
                    print(f"  - 识别为: {face['name']} (置信度: {face['confidence']:.2%})")
                
            except Exception as e:
                print(f"  ✗  处理失败: {str(e)}")
        
        return results
    
    def get_match_info(self, image_path: str, top_n: int = 5, 
                      model: str = "hog") -> List[Dict]:
        """
        获取最相似的前N个匹配
        
        Args:
            image_path: 图片路径
            top_n: 返回前N个匹配
            model: 人脸检测模型
        
        Returns:
            匹配结果列表
        """
        if len(self.known_encodings) == 0:
            return []
        
        # 读取图片
        image = face_recognition.load_image_file(image_path)
        
        # 检测人脸
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        if len(face_encodings) == 0:
            print("未检测到人脸")
            return []
        
        # 使用第一个检测到的人脸
        face_encoding = face_encodings[0]
        
        # 计算与所有已知人脸的距离
        distances = face_recognition.face_distance(
            self.known_encodings, face_encoding
        )
        
        # 获取前N个最小距离的索引
        top_indices = np.argsort(distances)[:top_n]
        
        matches = []
        for idx in top_indices:
            matches.append({
                "name": self.known_names[idx],
                "distance": float(distances[idx]),
                "confidence": float(1.0 - distances[idx]),
                "is_match": distances[idx] <= self.tolerance
            })
        
        return matches
