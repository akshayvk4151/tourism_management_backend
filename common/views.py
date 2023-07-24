from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


from admin_app.models import Blog, Destination
from admin_app.serializers import Destination_serializer, blogserializer
from .serializers import Adminserializer, BookingSerializer, ContactSerializer, Cuserializer
from .models import Admin, Booking, Customer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your views here.


@api_view(['GET'])
def destination_index(request):
    destination = Destination.objects.all()
    serializer = Destination_serializer(destination, many = True)
    return JsonResponse({'destination_list':serializer.data})


@api_view(['POST'])
def customer_register(request):
    try:
        customer_data = request.data
        email_exist = Customer.objects.filter(customer_email=customer_data['customer_email']).exists()
        msg1 = ''
        msg = ''
        status = False  # Define status variable
        
        if not email_exist:
            serialized_data = Cuserializer(data=customer_data)
            msg1 = 'Email available'
            if serialized_data.is_valid():
                serialized_data.save()
                msg = 'Customer registered successfully'
                status = True  # Set status to True if registration is successful
            else:
                msg = 'Registration failed'
        else:
            msg1 = 'Email already exists'
            msg = 'Customer registration failed: email already exists'
        
        # Return response outside the else block
        return JsonResponse({'msg': msg, 'msg1': msg1, 'email_exist': status})

    except:
        msg = 'Something went wrong'
        return JsonResponse({'msg': msg, 'msg1': msg1, 'email_exist': status})





@api_view(['POST'])
def customer_login(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username,password)
    try:
        customer = Customer.objects.get(customer_email = username, customer_password = password)
        status = True
         # Generate or retrieve a token for the authenticated customer user
        user, _ = User.objects.get_or_create(username=customer.customer_email)  # Create or retrieve User based on customer_email
        token, _ = Token.objects.get_or_create(user=user)
        customer_id = customer.id  # Retrieve the customer ID
        # Serialize the customer data
        serializer = Cuserializer(customer)
        customer_data = serializer.data
        return JsonResponse ({'status':status,'token': token.key,'customer_data': customer_data, 'customer_id': customer_id})
    except Customer.DoesNotExist:
        status = False
    return JsonResponse ({'status':status, 'customer_id':None})   



@api_view(['GET']) #Customer loggedin to his accound
def customer_accound(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    serializer = Cuserializer(customer)
    # print(serializer)
    customer_data = serializer.data
    # print(admin_data)
    return JsonResponse({'customer_data':customer_data})


@api_view(['PUT'])
def change_password(request):  #Customer password changing
    customer_data = request.data
    try:
        customer = Customer.objects.get(id = customer_data['customer_id'])
        if customer.customer_password != customer_data['old_password']:
            return JsonResponse({'message':'Invalid old password'})
        if customer.customer_password == customer_data['new_password']:
            return JsonResponse({'message':'New password should be different from the old password'})
        customer.customer_password = customer_data['new_password']
        customer.save()
        return JsonResponse({'message':'Passord updated successfully'})
    except Customer.DoesNotExist:
        return JsonResponse({'message': 'Customer not found'})
    
@api_view(['GET']) #Customer can view his profile
def view_profile(request, customer_id):
    try:
        customer = Customer.objects.get(id = customer_id)
        serialized_data = Cuserializer(customer)
        return JsonResponse({'data':serialized_data.data})
    except Customer.DoesNotExist:
        return JsonResponse({'message':'Customer data doesnot found.'})

@api_view(['GET','PUT'])  #Customer can edit his profile
def edit_profile(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        if request.method == 'GET':
            serializer_data = Cuserializer(customer)
            return JsonResponse({'data': serializer_data.data})
        elif request.method == 'PUT':
            edited_serializer_data = Cuserializer(customer, data=request.data, partial=True)
            if edited_serializer_data.is_valid():
                if 'profile_pic' in request.FILES:
                    customer.profile_pic = request.FILES['profile_pic']
                edited_serializer_data.save()
                return JsonResponse({'message': 'Customer updated successfully'})
            else:
                return JsonResponse({'message': 'Update Error, Not updated.'})
    except Customer.DoesNotExist:
        return JsonResponse({'message': 'Customer not found'})




@api_view(['GET'])
def blog(request):
    admin_blog = Blog.objects.all()
    serialize = blogserializer(admin_blog, many = True)

    return JsonResponse({'blog_data':serialize.data})

@api_view(['GET'])
def view_blog(request, post_id):
    try:
        # Get the blog post from the database
        post = Blog.objects.get(id=post_id)
        
        # Create a dictionary with the post data
        post_data = {
            'id': post.id,
            'Blog_topic': post.Blog_topic,
            'post_date': post.post_date,
            'blog_content': post.blog_description,
        }
        
        if post.blog_image: # check if blog_image exists before adding to post_data
            post_data['blog_image'] = post.blog_image.url
            print(post.blog_image.url)
        else:
            post_data['blog_image'] = None

        # Return the post data as JSON
        return JsonResponse({'post': post_data})
    except Blog.DoesNotExist:
        # Return a 404 response if the post does not exist
        return JsonResponse({'error': 'Post not found'}, status=404)


@api_view(['GET'])
def view_destinations(request, destination_id):
    try:
        destination = Destination.objects.get(id=destination_id)
        serializer = Destination_serializer(destination)
        return JsonResponse(serializer.data)
    except Destination.DoesNotExist:
        # Return a 404 response if the destination does not exist
        return JsonResponse({'error': 'Destination not found'}, status=404)



@api_view(['POST'])
def book_destination(request, destination_id, customer_id):
    try:
        destination = Destination.objects.get(id=destination_id)
    except Destination.DoesNotExist:
        return Response({'error': 'Destination not found'})

    booking_serializer = BookingSerializer(data=request.data)
    print(booking_serializer)
    if booking_serializer.is_valid():
        print(request.data)  # Debug statement to check the data received by the server
        booking = booking_serializer.save(destination=destination, customer_id=customer_id)
        
        # Update the status of the customer to "booked"
        customer = booking.customer
        customer.status = 'booked'
        customer.save()
        
        return JsonResponse({'success': 'Booking created'})
    else:
        print(booking_serializer.errors)  # Debug statement to check any validation errors
        return JsonResponse(booking_serializer.errors)
  


@api_view(['POST'])
def contact_us(request):
    contact_data  = request.data
    serializer_data = ContactSerializer(data = contact_data)
    if serializer_data.is_valid():
        serializer_data.save()
        return JsonResponse({'message':'Your message was send successfully!'})
    else:
        return JsonResponse({'message':'Message not send'})

from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def customer_logout(request):
    # Delete the authentication token associated with the user
    Token.objects.filter(user=request.user).delete()
    return Response({'success': 'Logged out successfully'})




# ///////////////////////////// Admin Section //////////////////////////////////////


@api_view(['POST'])

def admin_register(request):
    try:
        admin_data = request.data
        email_exist =  Admin.objects.filter(admin_email = admin_data['admin_email']).exists()
        msg = ''
        msg1 = ''
        
        if not email_exist:
            adminserialized_data = Adminserializer(data = admin_data)
            status = False
            
            msg1 = 'Email available'
            
            if adminserialized_data.is_valid():
                adminserialized_data.save()
                msg = 'Admin registered successfully'
            else:
                msg = 'Registration failed'
        else:
            status = True
            msg1 = 'Email already exist'
            return JsonResponse({'msg1':msg1})
    except:
        msg = 'Something went wrong'
        return JsonResponse({'msg': msg})
    return JsonResponse({'msg':msg, 'msg1':msg1,'email_exist': status})





@api_view(['POST'])
def admin_login(request):
    username = request.POST['username']
    password = request.POST['password']
    
    try:
        admin = Admin.objects.get(admin_email=username, admin_password=password)
        status = True
        
        # Generate or retrieve a token for the authenticated admin user
        user, _ = User.objects.get_or_create(username=admin.admin_email)  # Create or retrieve User based on admin_email
        # print(user,'00000000000')
        token, _ = Token.objects.get_or_create(user=user)
        # print(token,'111111111111111')
        admin_id = admin.id  # Retrieve the admin ID
        # print(admin_id,'22222222222222222')
        # Serialize the admin data
        serializer = Adminserializer(admin)
        admin_data = serializer.data
        
        return JsonResponse({'status': status, 'token': token.key,'admin_data': admin_data, 'admin_id': admin_id})
    
    except Admin.DoesNotExist:
        status = False
    
    return JsonResponse({'status': status, 'admin_id': None})



# /////////////////////////////////////////////////////////////////////////////////////////////
