from django.test import TestCase

# Create your tests here.

""" 

[Base64 Image] --> [Convert to OpenCV Array]
        |
        v
[Face Detection] --> [Crop Face] --> [Normalize / Resize]
        |                          |
        |                          v
        |                    [Embedding Vector]
        |                          |
        v                          v
[Enrollment]                [Verification / Cosine Similarity]
        |                          |
        v                          v
[Store embedding]           [Attendance verified?]


#Working of the algorithms

Detection: Finds the face in the image.

Feature Extraction (Embedding): Converts face pixels into a vector representing that face.

Matching: Compares embeddings to see if it’s the same person.

Liveness Check: Ensures the face is real, not a photo/video.

Database Storage: Only embeddings (vectors) and images for reference are stored.


#Technology and Roles,

OpenCV (cv2) =>	Image processing, cropping, resizing, converting between formats
PIL / BytesIO =>	Handle base64 image conversion
MediaPipe =>	Real-time face detection
NumPy =>	Vector math, cosine similarity
Face Embeddings =>	Vector representation of a face for verification
Cosine Similarity =>	Measures how close two embeddings are (face match)




"""