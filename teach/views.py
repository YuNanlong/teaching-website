from django.shortcuts import render

# Create your views here.
def teach_home(request):
    '''For testing'''
    course = request.GET['course']
    if course == "SE":
        # render SE page
        return render(request, "teach_base.html")
    elif course == "SRE":
        # render
        return render(request, "teach_base.html")
    elif course == "SQTA":
        return render(request, "teach_base.html")
    else:
        return render(request, "teach_base.html")