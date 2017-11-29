from django.shortcuts import render

# Create your views here.
def teach_detail(request):
    '''For testing'''
    course = request.GET['course']
    if course == "SE":
        # render SE page
        return render(request, "teach_detail.html")
    elif course == "SRE":
        # render
        return render(request, "teach_detail.html")
    elif course == "SQTA":
        return render(request, "teach_detail.html")
    else:
        return render(request, "teach_detail.html")