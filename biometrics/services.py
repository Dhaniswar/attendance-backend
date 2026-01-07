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


face_recognition = FaceRecognitionService()
