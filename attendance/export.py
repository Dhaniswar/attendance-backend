import logging
from django.utils import timezone


logger = logging.getLogger(__name__)



def export_attendance_to_excel(start_date, end_date):
    """Export attendance data to Excel"""
    import pandas as pd
    from io import BytesIO
    from attendance.models import Attendance
    
    # Get attendance data
    attendance_qs = Attendance.objects.filter(
        date__range=[start_date, end_date]
    ).select_related('student').order_by('date', 'student__student_id')
    
    # Convert to DataFrame
    data = []
    for att in attendance_qs:
        data.append({
            'Student ID': att.student.student_id,
            'Student Name': att.student.get_full_name(),
            'Date': att.date,
            'Time In': att.time_in,
            'Time Out': att.time_out,
            'Status': att.get_status_display(),
            'Location': att.location or '',
            'Verified by Face': 'Yes' if att.verified_by_face else 'No',
            'Face Confidence': att.face_confidence or 0,
            'Liveness Score': att.liveness_score or 0,
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Attendance', index=False)
        
        # Add summary sheet
        summary_data = {
            'Metric': ['Total Records', 'Start Date', 'End Date', 'Export Date'],
            'Value': [
                len(df),
                start_date,
                end_date,
                timezone.now().date()
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    output.seek(0)
    return output

