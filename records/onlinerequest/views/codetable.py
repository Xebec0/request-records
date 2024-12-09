from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import Document, Requirement, Purpose

def index(request):
    selected_table = request.GET.get('table_type', 'Requirement')
    
    if request.method == "POST":
        table_name = request.POST.get("table_name")
        description = request.POST.get("description")

        try:
            if table_name == "Requirement":
                code = "REQ" + create_acronym(description)
                requirement = Requirement(code = code, description = description)
                requirement.save()
            elif table_name == "Document":
                code = "REQ" + create_acronym(description)
                document = Document(code = code, description = description)
                document.save()
            elif table_name == "Purpose":
                purpose = Purpose(description = description, active = True)
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
    
def create_acronym(description):
    # Split the description into words
    words = description.split()
    
    # Get the first letter of each word and convert it to uppercase
    acronym = ''.join(word[0].upper() for word in words)
    
    return acronym

# Example usage
description = "1x1 Picture"
acronym = create_acronym(description)
print("Acronym:", acronym)  # Output: "1XP"

    
