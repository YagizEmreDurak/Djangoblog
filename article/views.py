from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .form import articleform
from django.contrib import messages
from .models import article,Yorumlar
from django.contrib.auth.decorators import login_required

# Create your views here.
def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles": articles})

    articles = article.objects.all()
    return render(request,"articles.html",{"articles" : articles})



def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

@login_required(login_url = "user:login")
def dashboard(request):
    articles = article.objects.filter(author = request.user)
    context = {"articles" : articles}
    return render(request,"dashboard.html",context)

@login_required(login_url = "user:login")
def addarticle(request):
    form = articleform(request.POST or None,request.FILES or None)
    if form.is_valid():
        articles = form.save(commit=False)
        articles.author = request.user
        articles.save()
        messages.success(request,"Makale Kaydedildi...")
        return redirect("article:dashboard")

    return render(request,"addarticle.html",{"form" : form})

def addcomment(request,id):
    makale = get_object_or_404(article,id = id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newcomment = Yorumlar(comment_author = comment_author,comment_content = comment_content)
        newcomment.makale = makale
        newcomment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))







def detail(request,id):
    #articles = article.objects.filter(id = id).first()
    articles = get_object_or_404(article,id = id)
    
    comments = articles.comments.all()

    
    return render(request,"detail.html",{"articles" : articles,"comments" : comments})

@login_required(login_url = "user:login")
def updatearticle(request,id):
    articles = get_object_or_404(article,id = id)
    form = articleform(request.POST or None,request.FILES or None,instance = articles)
    if form.is_valid():
        articles = form.save(commit=False)
        article.author = request.user
        articles.save()
        messages.success(request,"Makale Güncellendi...")
        return redirect("article:dashboard")
    return render(request,"update.html",{"form" : form})

@login_required(login_url = "user:login")
def deletearticle(request,id):
    articles = get_object_or_404(article,id = id)
    articles.delete()
    messages.success(request,"Makale Silindi...")
    return redirect("article:dashboard")





