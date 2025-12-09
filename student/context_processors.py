from student.models import OJTPlacement

def user_placement(request):
    if request.user.is_authenticated and request.user.role == "student":
        try:
            placement = OJTPlacement.objects.get(student=request.user)
            return {"student_placement_id": placement.id}
        except OJTPlacement.DoesNotExist:
            return {"student_placement_id": None}
    return {"student_placement_id": None}