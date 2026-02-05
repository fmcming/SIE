"""
人脸编码器模块 (Face Encoder Module)
用于提取人脸特征向量并保存到数据库
"""

import face_recognition
import pickle
import os
from pathlib import Path
from typing import List, Tuple, Dict
import cv2
import numpy as np


class FaceEncoder:
    """
    人脸编码器类
    负责从图片中提取人脸特征并保存
    """
    
    def __init__(self, encodings_file: str = "encodings/face_encodings.pkl"):
        """
        初始化人脸编码器
        
        Args:
            encodings_file: 编码文件保存路径
        """
        self.encodings_file = encodings_file
        self.known_encodings = []
        self.known_names = []
        
        # 确保编码文件目录存在
        os.makedirs(os.path.dirname(encodings_file), exist_ok=True)
        
        # 如果编码文件存在，加载已有数据
        if os.path.exists(encodings_file):
            self.load_encodings()
    
    def encode_face(self, image_path: str, model: str = "hog") -> List[np.ndarray]:
        """
        从图片中提取人脸编码
        
        Args:
            image_path: 图片路径
            model: 人脸检测模型，'hog' 或 'cnn'
                   hog更快但不够准确，cnn更准确但需要GPU
        
        Returns:
            人脸编码列表（一张图片可能包含多个人脸）
        """
        # 读取图片
        image = face_recognition.load_image_file(image_path)
        
        # 检测人脸位置
        face_locations = face_recognition.face_locations(image, model=model)
        
        # 提取人脸编码
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        return face_encodings
    
    def encode_faces_from_folder(self, folder_path: str, model: str = "hog") -> Dict[str, int]:
        """
        从文件夹中批量编码人脸
        
        Args:
            folder_path: 包含人脸图片的文件夹路径
            model: 人脸检测模型
        
        Returns:
            处理统计信息
        """
        folder = Path(folder_path)
        stats = {
            "processed": 0,
            "success": 0,
            "failed": 0,
            "no_face": 0
        }
        
        # 支持的图片格式
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
        
        print(f"开始扫描文件夹: {folder_path}")
        
        for image_path in folder.iterdir():
            if not image_path.is_file():
                continue
            
            if image_path.suffix.lower() not in image_extensions:
                continue
            
            stats["processed"] += 1
            
            # 使用文件名（不含扩展名）作为人名
            person_name = image_path.stem
            
            try:
                print(f"处理: {image_path.name} -> {person_name}")
                
                # 提取人脸编码
                encodings = self.encode_face(str(image_path), model=model)
                
                if len(encodings) == 0:
                    print(f"  ⚠️  未检测到人脸")
                    stats["no_face"] += 1
                    continue
                
                if len(encodings) > 1:
                    print(f"  ⚠️  检测到 {len(encodings)} 个人脸，使用第一个")
                
                # 保存第一个检测到的人脸编码
                self.known_encodings.append(encodings[0])
                self.known_names.append(person_name)
                
                print(f"  ✓  成功编码")
                stats["success"] += 1
                
            except Exception as e:
                print(f"  ✗  处理失败: {str(e)}")
                stats["failed"] += 1
        
        # 保存编码
        if stats["success"] > 0:
            self.save_encodings()
            print(f"\n✓ 已保存 {stats['success']} 个人脸编码到 {self.encodings_file}")
        
        return stats
    
    def save_encodings(self):
        """保存编码到文件"""
        data = {
            "encodings": self.known_encodings,
            "names": self.known_names
        }
        
        with open(self.encodings_file, "wb") as f:
            pickle.dump(data, f)
    
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
    
    def add_face(self, image_path: str, name: str, model: str = "hog") -> bool:
        """
        添加单个人脸到数据库
        
        Args:
            image_path: 图片路径
            name: 人员姓名
            model: 人脸检测模型
        
        Returns:
            是否成功添加
        """
        try:
            encodings = self.encode_face(image_path, model=model)
            
            if len(encodings) == 0:
                print(f"未检测到人脸")
                return False
            
            # 添加第一个检测到的人脸
            self.known_encodings.append(encodings[0])
            self.known_names.append(name)
            
            # 保存
            self.save_encodings()
            
            print(f"✓ 成功添加 {name} 的人脸编码")
            return True
            
        except Exception as e:
            print(f"添加失败: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict[str, int]:
        """
        获取数据库统计信息
        
        Returns:
            统计信息字典
        """
        return {
            "total_faces": len(self.known_names),
            "unique_names": len(set(self.known_names))
        }
