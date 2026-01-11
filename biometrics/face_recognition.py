import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from .models import FaceImage
from django.utils import timezone
import mediapipe as mp
from deepface import DeepFace
from insightface.app import FaceAnalysis
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class FaceRecognitionSystem:
    def __init__(self):
        self.model_name = settings.FACE_RECOGNITION_MODEL
        self.threshold = settings.FACE_CONFIDENCE_THRESHOLD
        
        if self.model_name == 'mediapipe':
            self.initialize_mediapipe()
        elif self.model_name == 'insightface':
            self.initialize_insightface()
        elif self.model_name == 'deepface':
            self.initialize_deepface()
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
    
    def initialize_mediapipe(self):
        """Initialize MediaPipe face detection and recognition"""
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,  # 0 for short-range, 1 for full-range
            min_detection_confidence=0.5
        )
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            min_detection_confidence=0.5
        )
    
    def initialize_insightface(self):
        """Initialize InsightFace model"""
        self.insightface_app = FaceAnalysis(name='buffalo_l')
        self.insightface_app.prepare(ctx_id=0, det_size=(640, 640))
    
    def initialize_deepface(self):
        """Initialize DeepFace models"""
        # DeepFace uses multiple models internally
        pass
    
    def base64_to_image(self, image_data):
        """Convert base64 image to OpenCV format"""
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            image_np = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            
            return image_cv
        except Exception as e:
            logger.error(f"Error converting base64 to image: {str(e)}")
            raise
    
    def image_to_base64(self, image_np):
        """Convert OpenCV image to base64"""
        try:
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            image_pil = Image.fromarray(image_rgb)
            
            # Save to bytes
            buffered = BytesIO()
            image_pil.save(buffered, format="JPEG", quality=85)
            
            # Encode to base64
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return f"data:image/jpeg;base64,{img_str}"
        except Exception as e:
            logger.error(f"Error converting image to base64: {str(e)}")
            raise
    
    def detect_faces_mediapipe(self, image):
        """Detect faces using MediaPipe"""
        results = self.face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        faces = []
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)
                
                confidence = detection.score[0]
                
                faces.append({
                    'bbox': (x, y, w, h),
                    'confidence': confidence,
                    'landmarks': None  # MediaPipe detection doesn't provide landmarks
                })
        
        return faces
    
    def detect_faces_insightface(self, image):
        """Detect faces using InsightFace"""
        faces = self.insightface_app.get(image)
        
        results = []
        for face in faces:
            bbox = face.bbox.astype(int)
            results.append({
                'bbox': (bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]),
                'confidence': face.det_score,
                'landmarks': face.kps.tolist() if hasattr(face, 'kps') else None,
                'embedding': face.embedding.tolist() if hasattr(face, 'embedding') else None
            })
        
        return results
    
    def detect_faces_deepface(self, image):
        """Detect faces using DeepFace"""
        try:
            from deepface import DeepFace
            
            faces = DeepFace.extract_faces(
                img_path=image,
                detector_backend='opencv',
                enforce_detection=False,
                align=True
            )
            
            results = []
            for face in faces:
                facial_area = face['facial_area']
                results.append({
                    'bbox': (
                        facial_area['x'], 
                        facial_area['y'], 
                        facial_area['w'], 
                        facial_area['h']
                    ),
                    'confidence': face['confidence'],
                    'landmarks': None,
                })
            
            return results
        except Exception as e:
            logger.error(f"DeepFace detection error: {str(e)}")
            return []
    
    def detect_faces(self, image_data):
        """Detect faces in an image"""
        image = self.base64_to_image(image_data)
        
        if self.model_name == 'mediapipe':
            faces = self.detect_faces_mediapipe(image)
        elif self.model_name == 'insightface':
            faces = self.detect_faces_insightface(image)
        elif self.model_name == 'deepface':
            faces = self.detect_faces_deepface(image)
        else:
            faces = []
        
        # Extract face embeddings
        for face in faces:
            if 'embedding' not in face or face['embedding'] is None:
                face['embedding'] = self.extract_embedding(image, face['bbox'])
        
        return {
            'face_detected': len(faces) > 0,
            'faces': faces,
            'image_size': image.shape[:2]
        }
    
    def extract_embedding(self, image, bbox):
        """Extract face embedding from detected face"""
        x, y, w, h = bbox
        
        # Extract face region
        face_region = image[y:y+h, x:x+w]
        
        if face_region.size == 0:
            return None
        
        # Resize to standard size
        face_resized = cv2.resize(face_region, (160, 160))
        
        # Convert to embedding (simplified - in production use proper model)
        # This is a placeholder - you should use a proper face recognition model
        face_normalized = face_resized / 255.0
        embedding = face_normalized.flatten()[:settings.FACE_EMBEDDING_SIZE].tolist()
        
        return embedding
    
    def compare_faces(self, embedding1, embedding2):
        """Compare two face embeddings"""
        if not embedding1 or not embedding2:
            return 0.0
        
        # Convert to numpy arrays
        emb1 = np.array(embedding1)
        emb2 = np.array(embedding2)
        
        # Ensure same length
        min_len = min(len(emb1), len(emb2))
        emb1 = emb1[:min_len]
        emb2 = emb2[:min_len]
        
        # Calculate cosine similarity
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = np.dot(emb1, emb2) / (norm1 * norm2)
        
        return float(similarity)
    
    def verify_face(self, image_data, stored_embedding):
        """Verify if face matches stored embedding"""
        result = self.detect_faces(image_data)
        
        if not result['face_detected']:
            return {
                'verified': False,
                'confidence': 0.0,
                'message': 'No face detected'
            }
        
        # Get the first face (assuming one face per attendance)
        face = result['faces'][0]
        current_embedding = face['embedding']
        
        # Compare embeddings
        similarity = self.compare_faces(current_embedding, stored_embedding)
        
        return {
            'verified': similarity >= self.threshold,
            'confidence': similarity,
            'similarity': similarity,
            'face_detected': True,
            'face_confidence': face['confidence']
        }
    
    def check_liveness(self, images_data):
        """Perform liveness check using multiple images"""
        if len(images_data) < 3:
            return {
                'is_live': False,
                'score': 0.0,
                'message': 'Insufficient images for liveness check'
            }
        
        try:
            # Convert images
            images = [self.base64_to_image(img) for img in images_data[:5]]  # Use first 5 images
            
            # Simple liveness check: detect eye blinks and head movement
            # This is a simplified version - in production use proper liveness detection
            
            # Check for variations in images (real faces move)
            variations = self.check_image_variations(images)
            
            # Check for eye blinks (simplified)
            eye_blink_detected = self.check_eye_blinks(images)
            
            # Calculate overall liveness score
            liveness_score = (variations * 0.6 + eye_blink_detected * 0.4)
            
            return {
                'is_live': liveness_score >= settings.LIVENESS_THRESHOLD,
                'score': liveness_score,
                'details': {
                    'variations_detected': variations > 0.5,
                    'eye_blink_detected': eye_blink_detected == 1.0,
                    'image_count': len(images)
                }
            }
        except Exception as e:
            logger.error(f"Liveness check error: {str(e)}")
            return {
                'is_live': False,
                'score': 0.0,
                'message': f'Liveness check failed: {str(e)}'
            }
    
    def check_image_variations(self, images):
        """Check for variations between images (movement detection)"""
        if len(images) < 2:
            return 0.0
        
        variations = []
        for i in range(len(images) - 1):
            # Calculate absolute difference
            diff = cv2.absdiff(images[i], images[i+1])
            diff_mean = np.mean(diff)
            variations.append(diff_mean)
        
        avg_variation = np.mean(variations)
        # Normalize to 0-1 range (assuming variation > 10 is significant)
        normalized = min(avg_variation / 10.0, 1.0)
        
        return normalized
    
    def check_eye_blinks(self, images):
        """Simple eye blink detection (placeholder)"""
        # In production, implement proper eye blink detection using facial landmarks
        # For now, return random result for demonstration
        import random
        return 1.0 if random.random() > 0.3 else 0.0
    
    def enroll_face(self, user, images_data):
        """Enroll user's face from multiple images"""
        embeddings = []
        
        for image_data in images_data[:10]:  # Use first 10 images max
            try:
                result = self.detect_faces(image_data)
                if result['face_detected']:
                    face = result['faces'][0]
                    embeddings.append(face['embedding'])
            except Exception as e:
                logger.error(f"Error processing image for enrollment: {str(e)}")
                continue
        
        if not embeddings:
            raise ValueError("No valid faces found in the provided images")
        
        # Calculate average embedding
        avg_embedding = np.mean(embeddings, axis=0).tolist()
        
        # Update user's face encoding
        user.face_encoding = avg_embedding
        user.face_encoding_version = self.model_name
        user.last_face_update = timezone.now()
        user.save()
        
        # Store individual face images
        for i, image_data in enumerate(images_data[:5]):
            try:
                face_image = FaceImage.objects.create(
                    user=user,
                    image=self.save_face_image(image_data, f"{user.id}_{i}"),
                    encoding=embeddings[i] if i < len(embeddings) else avg_embedding,
                    is_verified=True
                )
            except Exception as e:
                logger.error(f"Error saving face image {i}: {str(e)}")
        
        return {
            'success': True,
            'message': f'Face enrolled successfully with {len(embeddings)} images',
            'embedding_size': len(avg_embedding)
        }
    
    def save_face_image(self, image_data, filename):
        """Save face image to media storage"""
        from django.core.files.base import ContentFile
        import uuid
        
        # Convert base64 to image
        image = self.base64_to_image(image_data)
        
        # Convert to bytes
        success, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not success:
            raise ValueError("Failed to encode image")
        
        # Save to Django file field
        face_image = FaceImage()
        
        file_name = f"{filename}_{uuid.uuid4().hex[:8]}.jpg"
        file_content = ContentFile(buffer.tobytes())
        
        face_image.image.save(file_name, file_content, save=False)
        
        return face_image.image


# Global instance
face_recognition = FaceRecognitionSystem()