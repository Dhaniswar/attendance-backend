from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

from attendance_backend.pagination import CustomPagination
from .export import export_attendance_to_excel
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from biometrics import face_recognition
from .models import Attendance
from .serializers import AttendanceSerializer
from biometrics.serializers import FaceDetectionSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'status', 'verified_by_face']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_teacher:
            return Attendance.objects.select_related('student')
        return Attendance.objects.filter(student=user)

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        queryset = self.get_queryset().filter(date=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_with_face(self, request):
        serializer = FaceDetectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        today = timezone.now().date()

        if Attendance.objects.filter(student=user, date=today).exists():
            return Response(
                {"error": "Attendance already marked today"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.face_encoding:
            return Response(
                {"error": "Face not enrolled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = face_recognition.verify_face(
            serializer.validated_data['image'],
            user.face_encoding
        )

        if not result['verified']:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        attendance = Attendance.objects.create(
            student=user,
            date=today,
            time_in=timezone.now().time(),
            verified_by_face=True,
            face_confidence=result['confidence'],
            created_by=user
        )

        return Response(
            AttendanceSerializer(attendance).data,
            status=status.HTTP_201_CREATED
        )







@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_attendance(request):
    """
    Export attendance between start and end date to Excel
    """
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    file_format = request.GET.get('format', 'excel')

    if not start_date or not end_date:
        return Response({"detail": "start_date and end_date are required"}, status=400)

    output = export_attendance_to_excel(start_date, end_date)

    filename = f"attendance_{start_date}_to_{end_date}.{ 'xlsx' if file_format=='excel' else 'csv'}"

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
