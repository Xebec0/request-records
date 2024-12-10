from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from ..models import Document, Requirement, Purpose, Course

def index(request):
    selected_table = request.GET.get('table_type', 'Requirement')
    
    if request.method == "POST":
        table_name = request.POST.get("table_name")
        description = request.POST.get("description")
        code = request.POST.get("code")

        try:
            if table_name == "Requirement":
                requirement = Requirement(code=code, description=description)
                requirement.save()
            elif table_name == "Document":
                document = Document(code=code, description=description)
                document.save()
            elif table_name == "Purpose":
                purpose = Purpose(description=description, active=True)
                purpose.save()
            elif table_name == "Course":
                course = Course(code=code, description=description)
                course.save()

            return JsonResponse({'status': True, 'message': "Codetable populated"})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
        
    else:
        data = None
        
        if selected_table == 'Requirement':
            data = Requirement.objects.all()
        elif selected_table == 'Document':
            data = Document.objects.all()
        elif selected_table == 'Purpose':
            data = Purpose.objects.all()
        elif selected_table == 'Course':
            data = Course.objects.all()
            
        context = {
            'selected_table': selected_table,
            'data': data
        }
        return render(request, 'code_table/index.html', context)
    
def get_table_data(request):
    table_type = request.GET.get('table_type', 'Requirement')
    
    if table_type == 'Requirement':
        data = list(Requirement.objects.values('id', 'code', 'description'))
    elif table_type == 'Document':
        data = list(Document.objects.values('id', 'code', 'description', 'active'))
    elif table_type == 'Purpose':
        data = list(Purpose.objects.values('id', 'description', 'active'))
    elif table_type == 'Course':
        data = list(Course.objects.values('id', 'code', 'description'))
        
    return JsonResponse({'data': data})

def check_duplicate(request):
    table_name = request.GET.get('table_name')
    code = request.GET.get('code')
    item_id = request.GET.get('id')
    
    model = None
    if table_name == "Requirement":
        model = Requirement
    elif table_name == "Document":
        model = Document
    elif table_name == "Course":
        model = Course
        
    if model:
        query = model.objects.filter(code=code)
        if item_id:  # Exclude current item when editing
            query = query.exclude(id=item_id)
        exists = query.exists()
        return JsonResponse({'exists': exists})
    
    return JsonResponse({'exists': False})

@require_POST
def edit(request):
    try:
        table_name = request.POST.get('table_name')
        item_id = request.POST.get('id')
        description = request.POST.get('description')
        code = request.POST.get('code')
        
        if table_name == "Requirement":
            item = get_object_or_404(Requirement, id=item_id)
            item.description = description
            item.code = code
        elif table_name == "Document":
            item = get_object_or_404(Document, id=item_id)
            item.description = description
            item.code = code
        elif table_name == "Purpose":
            item = get_object_or_404(Purpose, id=item_id)
            item.description = description
        elif table_name == "Course":
            item = get_object_or_404(Course, id=item_id)
            item.description = description
            item.code = code
            
        item.save()
        return JsonResponse({'status': True, 'message': 'Item updated successfully'})
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)})

@require_POST
def delete(request):
    try:
        table_name = request.POST.get('table_name')
        item_id = request.POST.get('id')
        
        if table_name == "Requirement":
            item = get_object_or_404(Requirement, id=item_id)
        elif table_name == "Document":
            item = get_object_or_404(Document, id=item_id)
        elif table_name == "Purpose":
            item = get_object_or_404(Purpose, id=item_id)
        elif table_name == "Course":
            item = get_object_or_404(Course, id=item_id)
            
        item.delete()
        return JsonResponse({'status': True, 'message': 'Item deleted successfully'})
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)})
