from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from ..models import Document, Requirement, Purpose

def index(request):
    selected_table = request.GET.get('table_type', 'Requirement')
    
    if request.method == "POST":
        table_name = request.POST.get("table_name")
        description = request.POST.get("description")

        try:
            if table_name == "Requirement":
                code = "REQ" + create_acronym(description)
                requirement = Requirement(code=code, description=description)
                requirement.save()
            elif table_name == "Document":
                code = "REQ" + create_acronym(description)
                document = Document(code=code, description=description)
                document.save()
            elif table_name == "Purpose":
                purpose = Purpose(description=description, active=True)
                purpose.save()

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
        
        if table_name == "Requirement":
            item = get_object_or_404(Requirement, id=item_id)
            item.description = description
            item.code = "REQ" + create_acronym(description)
        elif table_name == "Document":
            item = get_object_or_404(Document, id=item_id)
            item.description = description
            item.code = "REQ" + create_acronym(description)
        elif table_name == "Purpose":
            item = get_object_or_404(Purpose, id=item_id)
            item.description = description
            
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
            
        item.delete()
        return JsonResponse({'status': True, 'message': 'Item deleted successfully'})
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)})
    
def create_acronym(description):
    # Split the description into words
    words = description.split()
    
    # Get the first letter of each word and convert it to uppercase
    acronym = ''.join(word[0].upper() for word in words)
    
    return acronym
