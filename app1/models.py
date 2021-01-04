from django.db import models
import re	
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):            
        results = {"errors":{}, "success":{}}
        if len(postData['user_name']) < 2:
            results["errors"]["user_name"]= "Please make your user name longer than two characters."
        else: #len(postData['user_name']) < 2:
            results["success"]["user_name"]= "User name is valid!"
        if len(postData['first_name']) < 2:
            results["errors"]["first_name"]= "Please make your first name longer than two characters."
        if len(postData['last_name']) < 2:
            results["errors"]["last_name"]= "Please make your last name longer than two characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')    
        if not EMAIL_REGEX.match(postData['email_address']):           
            results["errors"]['email_address'] = "Please enter a valid email address."
        if len(postData['password']) < 10:
            results["errors"]["password"]= "Please make your password longer than ten characters.  Protect your account from hackers!"
        if postData['password'] != postData['confirm_password']:
            results["errors"]["password"]= "Please make sure your passwords match.  Protect your account from hackers!"
        else:                                                                       
            results["success"]["password"]= "Passwords match!"
        return results 

    def authenticate(self, email_address, password):
        users = self.filter(email_address=email_address)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email_address = form['email_address'],
            password = pw,
        )

class User(models.Model):
    ##ID IS AUTOMATICALLY ADDED.  called (id)    #CHANGED required=True
    user_name = models.CharField(max_length=55, blank=False)        
    first_name = models.CharField(max_length=55, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email_address = models.CharField(max_length=255, blank=False)
    password = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User: {self.first_name} ({self.id}) >"

class BookManager(models.Manager):
    def book_validator(self, postData):            
        results = {"errors":{}, "success":{}}
        if len(postData['book_title']) <= 1:
            results["errors"]["book_title"]= "Please enter your author."
        else: 
            results["success"]["user_name"]= "Author submitted!"
        if len(postData['book_description']) < 5:
            results["errors"]["book_description"]= "Please make your quote is at least 5 characters."
        else: 
            results["success"]["book_description"]= "Your quote was accepted!"
        return results #THIS STORES BOTH [errors] AND [success]

class Book(models.Model):
    ##ID IS AUTOMATICALLY ADDED.  called (id)    #CHANGED required=True
    book_title = models.CharField(max_length=200, blank=False)   
    book_description = models.TextField(max_length=5000, blank=False)
    book_uploaded_by = models.ForeignKey(User, related_name="uploaded_books", on_delete = models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_books")
    user_books_likes = models.ManyToManyField(User, related_name="book_likes")   #PAY ATTN TO RELATION dont ref before dec      #book.likes.all
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Wall_Message(models.Model):
    ##ID IS AUTOMATICALLY ADDED.  called (id)    #CHANGED required=True
    message = models.TextField(max_length=1000, blank=False)        
    poster = models.ForeignKey(User, related_name="wall_messages", on_delete = models.CASCADE) #POSTER!@!!
    user_message_likes = models.ManyToManyField(User, related_name="message_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = UserManager()
    
class Comment(models.Model):
    ##ID IS AUTOMATICALLY ADDED.  called (id)    #CHANGED required=True
    message = models.TextField(max_length=1000, blank=False)        
    poster = models.ForeignKey(User, related_name="wall_comments", on_delete = models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete = models.CASCADE)
    user_comment_likes = models.ManyToManyField(User, related_name="comment_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = UserManager()