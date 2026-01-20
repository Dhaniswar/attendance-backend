from .face_recognition import face_recognition as fr_system

class FaceRecognitionService:
    def detect_faces(self, image):
        return fr_system.detect_faces(image)

    def verify_face(self, image, stored_encoding):
        return fr_system.verify_face(image, stored_encoding)

    def check_liveness(self, images):
        return fr_system.check_liveness(images)

    def enroll_face(self, user, images):
        return fr_system.enroll_face(user, images)


face_recognition = FaceRecognitionService()
