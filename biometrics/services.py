class FaceRecognitionService:
    threshold = 0.6

    def detect_faces(self, image):
        # implement detection
        return {"faces": 1}

    def verify_face(self, image, stored_encoding):
        # implement verification
        return {
            "verified": True,
            "confidence": 0.85
        }

    def check_liveness(self, images):
        return {
            "is_live": True,
            "score": 0.9
        }
    # ADD THIS METHOD
    def enroll_face(self, user, images):
        """Enroll user's face - delegates to actual implementation"""
        # Import the real implementation to avoid circular imports
        from .face_recognition import face_recognition as fr_system
        return fr_system.enroll_face(user, images)


face_recognition = FaceRecognitionService()
