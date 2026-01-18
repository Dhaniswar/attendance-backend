from django.test import TestCase

# Create your tests here.


""" 
to start redis server
sudo systemctl stop redis
redis-server





1. USER REGISTRATION:
   • Student/Teacher registers with email, name, student ID
   • For students: Face enrollment process captures 3-5 face images
   • System creates face embedding and stores in database

2. LOGIN PROCESS:
   • User enters email/password
   • JWT tokens generated for authentication
   • Redirect to role-based dashboard

3. ATTENDANCE MARKING (Student):
   • Student clicks "Mark Attendance"
   • Webcam opens for face capture
   • System detects face → Liveness check (anti-spoofing)
   • Face compared with stored embedding
   • If match → Attendance marked with timestamp
   • Record saved to database

4. ADMIN/TEACHER DASHBOARD:
   • View all students/attendance in real-time
   • Manual attendance override if needed
   • Generate reports (Excel/PDF)
   • Manage classes and users

5. ANALYTICS & REPORTING:
   • Daily/weekly/monthly attendance charts
   • Student-wise attendance percentage
   • Heat maps for attendance patterns
   • Export functionality

6. REAL-TIME FEATURES:
   • WebSocket notifications for new attendance
   • Live dashboard updates
   • Instant alerts for anomalies





PROJECT OVERVIEW

Problem: Manual attendance tracking is:
• Time-consuming 
• Error-prone (proxy attendance ~15%)
• No real-time monitoring
• Limited analytics

Solution: AI-powered automated system
• Face recognition for attendance marking
• Real-time tracking & monitoring
• Advanced analytics dashboard
• Anti-spoofing security

OBJECTIVES:
1. Reduce attendance marking time by 90%
2. Eliminate proxy attendance
3. Provide real-time insights
4. Generate automated reports
5. Ensure data privacy & security



=====================================================================================================
Technology Stack
text
FRONTEND:
• React.js with TypeScript - Modern UI
• Material-UI - Professional design
• Chart.js - Data visualization
• WebSocket - Real-time updates

BACKEND:
• Django REST Framework - API development
• PostgreSQL - Relational database
• Redis - Caching & WebSocket
• Celery - Background tasks

AI/COMPUTER VISION:
• MediaPipe (Google) - Face detection
• OpenCV - Image processing
• Custom algorithms - Liveness detection
• Scikit-learn - ML operations

================================================================================================



CORE FEATURES

1. SMART FACE RECOGNITION
   • 99.2% accuracy with MediaPipe
   • Real-time 30 FPS processing
   • Multi-face detection support

2. ADVANCED LIVENESS DETECTION
   • Eye blink verification
   • Head movement analysis
   • Texture-based anti-spoofing
   • Prevents photo/video replay attacks

3. REAL-TIME DASHBOARD
   • Live attendance monitoring
   • Instant notifications
   • WebSocket-based updates
   • Mobile-responsive design

4. COMPREHENSIVE ANALYTICS
   • Attendance trends & patterns
   • Heat maps & visualizations
   • Predictive analytics
   • Export to Excel/PDF

5. ROLE-BASED ACCESS CONTROL
   • Admin - Full system access
   • Teacher - Class management
   • Student - Self-attendance only
"""