from django.shortcuts import render,redirect
#สอบถามข้อมูลบทความ
from blogs.models import Blogs
#function ทางคณิตศาสตร์
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from category.models import Category
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
# Create your views here.
@login_required(login_url="member")
def panel(request):
    try :
        writer = auth.get_user(request)
        blogs = Blogs.objects.filter(writer=writer)
        blogCount = blogs.count()
        #sum('views') ,views ชื่อ column
        total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
        return render(request, "backend/index.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total})
    except :
         return render(request, "backend/index.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total})

@login_required(login_url="member")
def displayForm(request):
    try :
        writer = auth.get_user(request)
        blogs = Blogs.objects.filter(writer=writer)
        blogCount = blogs.count()
        #sum('views') ,views ชื่อ column
        total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
        categories = Category.objects.all()
        return render(request, "backend/blogForm.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total,"categories":categories})
    except :
        return render(request, "backend/blogForm.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total,"categories":categories})

@login_required(login_url="member")
def insertData(request):

    try :
            if  request.method == "POST" and request.FILES["image"]: #check       
                datafile = request.FILES["image"]    # รับค่า
                #รับค่าจากform
                name = request.POST["name"]
                category = request.POST["category"]
                description = request.POST["description"]
                content = request.POST["content"]
                writer = auth.get_user(request)
                if str(datafile.content_type).startswith("image"):
                    #upload
                    fs = FileSystemStorage()
                    img_url = "blogImages/"+datafile.name
                    filename = fs.save(img_url, datafile)
                    #บันทึกข้อมูลบทความ
                    blog = Blogs(name=name,category_id=category,description=description,content=content,writer=writer,image = img_url)
                    blog.save()
                messages.info(request, "Save successfully")
                return redirect("displayForm")
            else:
                messages.info(request, "Can't upload this file ,Please try again")
                return redirect("displayForm")
    except :
        return redirect("displayForm")
                
@login_required(login_url="member")
def deleteData(request,id):
    try :
            blog = Blogs.objects.get(id=id)
            fs=FileSystemStorage()
            #ลบภาพปกของบทความ
            fs.delete(str(blog.image))
            #ลบข้อมูลจากฐานข้อมูล
            blog.delete()
            return redirect('panel')
    except :
        return redirect('panel')

@login_required(login_url="member")
def editData(request,id):
    try :
        writer = auth.get_user(request)
        blogs = Blogs.objects.filter(writer=writer)
        blogCount = blogs.count()
        total = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
        categories = Category.objects.all()
        blogEdit = Blogs.objects.get(id=id)
        return render(request, "backend/editForm.html",{"blogEdit":blogEdit,"writer":writer,"blogCount":blogCount,"total":total,"categories":categories})
    except :
        return render(request, "backend/editForm.html",{"blogEdit":blogEdit,"writer":writer,"blogCount":blogCount,"total":total,"categories":categories})
    
@login_required(login_url="member")
def updateData(request,id):
    try:
        if request.method == "POST":
            #ดึงข้อมูลบทความที่ต้องการแก้ไขมาใช้งาน
            blog = Blogs.objects.get(id=id)
            #รับค่่าจากform
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]

            #อัพเดต
            blog.name = name
            blog.category_id = category
            blog.description = description
            blog.content = content
            blog.save()

        #อัพเดตหน้าปก
        if request.FILES["image"]:
            datafile = request.FILES["image"]
            if str(datafile.content_type).startswith("image"):
                #ลบภาพจริงของบทความออกไปก่อน
                fs=FileSystemStorage()
                fs.delete(str(blog.image))

                #แทนที่ภาพใหม่ลงไป
                img_url = "blogImages/"+datafile.name
                filename = fs.save(img_url, datafile)
                blog.image = img_url
                blog.save()
                
        
        #messages.info(request, "Update Successfully")
        return redirect("panel")
    

    except :
        return redirect("panel")