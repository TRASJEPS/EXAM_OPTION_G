from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Wall_Message, Comment, Book
import bcrypt

def index(request):
    if 'userid' in request.session:
        user = User.objects.filter(id=request.session['userid'])
        if user:
            return redirect('/login_page')
    return render(request, 'index.html')
    
def official_user_page(request):
    if 'userid' in request.session:
        user = User.objects.filter(id=request.session['userid'])
        if user:
            context = {
                "user":user[0],
                "wall_messages": Wall_Message.objects.all()    ##ADDED
            }
            return render(request, 'official_user_page.html', context)
    return redirect('/')

def register(request):
    if request.method == "POST":
        results = User.objects.basic_validator(request.POST)  ##TAKES THE STRINGS FROM THE basic_validator DICTIONARY!
        if len(results) > 0:
            request.session['user_validation_results'] = True
            if len(results['success']) > 0:
                totalSuccesses = results['success'] 
                for key, value in totalSuccesses.items():
                    messages.success(request, value)  
            if len(results['errors']) > 0:
                totalErrors = results['errors']
                for key, value in totalErrors.items():
                    messages.error(request, value)
                for key, value in request.POST.items():
                    request.session[key] = value
                return redirect('/')
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                user_name = request.POST['user_name'],
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email_address = request.POST['email_address'],
                password = pw_hash
            )
            request.session['userid'] = new_user.id  ##MAKE SURE TO USE ['userid']
            messages.success(request, "User successfully created!")
            return redirect('/official_user_page')
        return redirect('/')

def login(request):
    if request.method == "GET":   ## CHANGE TO POST  //FROM GET
        return redirect('/')
    if not User.objects.authenticate(request.POST['email_address'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email_address=request.POST['email_address'])
    request.session['userid'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/login_page')   

def login_page(request): 
    user = User.objects.get(id=request.session['userid'])
    context = {
                "user":user,
                "wall_messages": Wall_Message.objects.all(),  
                'all_books' : Book.objects.all()    
            } 
    return render(request,'login.html', context)


def post_message(request):
    if request.method == "POST":
        if 'userid' in request.session:
            user = User.objects.get(id=request.session['userid'])
            Wall_Message.objects.create(
                message=request.POST["post_message"],
                poster=user    
            )   
    return redirect('/login_page')

def post_comment(request,wall_comment_id):
    if request.method == "POST":
        if 'userid' in request.session:
            user = User.objects.get(id=request.session['userid'])
            wall_message = Wall_Message.objects.get(id=wall_comment_id)
            Comment.objects.create(
                message=request.POST["post_comment"],
                poster=user,
                wall_message=wall_message
            )   
    return redirect('/login_page')

def favorite(request, post_book_id):
    user = User.objects.get(id=request.session["userid"])
    post_book = Book.objects.get(id=post_book_id)
    user.favorited_books.add(post_book)
    return redirect('/login_page')

def unfavorite(request, post_book_id):
    user = User.objects.get(id=request.session["userid"])
    post_book = Book.objects.get(id=post_book_id)
    user.favorited_books.remove(post_book)
    return redirect('/login_page')

def favorite_in_solo_view(request, post_book_id):
    user = User.objects.get(id=request.session["userid"])
    post_book = Book.objects.get(id=post_book_id)
    user.favorited_books.add(post_book)
    return redirect('/view_book/{{book.id}}')

def unfavorite_in_solo_view(request, post_book_id):
    user = User.objects.get(id=request.session["userid"])
    post_book = Book.objects.get(id=post_book_id)
    user.favorited_books.remove(post_book)
    return redirect('/view_book/{{book.id}}')

def logout(request):
    request.session.clear()
    return redirect('/')

def delete_comment(request, post_comment_id):
    post_comment = Comment.objects.get(id=post_comment_id)
    post_comment.delete()
    return redirect('/login_page')

def delete_message(request, post_message_id):
    post_message = Wall_Message.objects.get(id=post_message_id)
    post_message.delete()
    return redirect('/login_page')

def delete_book(request, post_book_id):
    post_book = Book.objects.get(id=post_book_id)
    post_book.delete()
    return redirect('/login_page')

def edit_comment(request, post_comment_id):
    x = Comment.objects.get(id=post_comment_id)
    context = {
        'comment' : x
    }
    return render(request,'edit_comment.html', context)

def edit_message(request, post_message_id):
    x = Wall_Message.objects.get(id=post_message_id)
    context = {
        'message' : x
    }
    return render(request,'edit_message.html', context)

def edit_book(request, post_book_id):
    x = Book.objects.get(id=post_book_id)
    context = {
        'book' : x
    }
    return render(request,'edit_book.html', context)

def view_book(request, post_book_id):
    x = Book.objects.get(id=post_book_id)
    context = {
        'book' : x,
        'current_user': User.objects.get(id=request.session['userid'])
    }
    return render(request,'view_book.html', context)

def process_edit_comment(request, post_comment_id):
    x = Comment.objects.get(id=post_comment_id)
    x.message = request.POST['process_edit_comment']
    x.save()
    return redirect('/login_page')

def process_edit_message(request, post_message_id):
    x = Wall_Message.objects.get(id=post_message_id)
    x.message = request.POST['process_edit_message']
    x.save()
    return redirect('/login_page')

def process_edit_book(request, post_book_id):
    x = Book.objects.get(id=post_book_id)
    x.book_title = request.POST['book_title_edit']
    x.book_description = request.POST['book_description_edit']
    x.save()
    return redirect('/login_page')

def create_new_book(request):
    if request.method == "POST":
        results = Book.objects.book_validator(request.POST)  ##CONNECTS to book_validator DICTIONARY
        if len(results) > 0:
            request.session['book_validation_results'] = True
            if len(results['success']) > 0:
                totalSuccesses = results['success'] 
                for key, value in totalSuccesses.items():
                    messages.success(request, value)  
            if len(results['errors']) > 0:
                totalErrors = results['errors']
                for key, value in totalErrors.items():
                    messages.error(request, value)
                for key, value in request.POST.items():
                    request.session[key] = value
                return redirect('/login_page')
            user = User.objects.get(id=request.session['userid'])
            book = Book.objects.create(
                book_title = request.POST['book_title'],
                book_description = request.POST['book_description'],
                book_uploaded_by = user
            )
            messages.success(request, "New quote has been successfully created!")
            return redirect('/login_page')
        return redirect('/')

def edit_profile(request):
    if 'userid' in request.session:
            user = User.objects.filter(id=request.session['userid'])
            if user:
                context = {
                    "user":user[0]
                }
                return render(request, 'edit_my_profile.html', context)
    return redirect('/')

#LINKED TO LIKES

def book_like(request, post_book_id):
    user = User.objects.get(id=request.session["userid"])
    x = Book.objects.get(id=post_book_id)  ##post_message_like is the VAR or in this case x
    user.book_likes.add(x)
    return redirect('/login_page')  ##fix in ajax later

def book_unlike(request, post_book_id):
    user = User.objects.get(id=request.session["userid"])
    x = Book.objects.get(id=post_book_id)
    user.book_likes.remove(x)
    return redirect('/login_page')  ##fix in ajax later


    # book_likes = models.ManyToManyField(Book, related_name="user_books_likes")         #book.likes.all
    # message_likes = models.ManyToManyField(Wall_Message, related_name="user_message_likes")
    # comment_likes = models.ManyToManyField(Comment, related_name="user_comment_likes")

#     def unfavorite(request, post_book_id):
#     user = User.objects.get(id=request.session["userid"])
#     post_book = Book.objects.get(id=post_book_id)
#     user.favorited_books.remove(post_book)
#     return redirect('/login_page')

# def favorite_in_solo_view(request, post_book_id):
#     user = User.objects.get(id=request.session["userid"])
#     post_book = Book.objects.get(id=post_book_id)
#     user.favorited_books.add(post_book)
#     return redirect('/view_book/{{book.id}}')