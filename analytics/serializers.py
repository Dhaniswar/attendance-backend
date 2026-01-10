from rest_framework import serializers



class StatisticsSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
    total_teachers = serializers.IntegerField()
    total_attendance_today = serializers.IntegerField()
    attendance_rate_today = serializers.FloatField()
    average_attendance_rate = serializers.FloatField()
    recent_activity = serializers.ListField(child=serializers.DictField())
    
    



class ExportSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    format = serializers.ChoiceField(choices=['excel', 'csv', 'pdf'], default='excel')
    include_details = serializers.BooleanField(default=False)

