from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from admin_app.models import Blog, Destination
from admin_app.serializers import Destination_serializer, blogserializer
from common.models import Admin, ContactUs, Customer
from common.serializers import Adminserializer, ContactSerializer, Cuserializer
from rest_framework.authtoken.models import Token


# Create your views here.

@api_view(['GET'])
def admin_name(request, name_id):
    admin = Admin.objects.get(id=name_id)
    serializer = Adminserializer(admin)
    # print(serializer,'000000000000')
    admin_data = serializer.data
    # print(admin_data,'11111111111')
    return JsonResponse({'admin_data':admin_data})





@api_view(['GET'])
def dashboard(request):
   
    total_destination = Destination.objects.all().count()
    total_customer = Customer.objects.all().count()
    data = {
        'total_destination':total_destination,
        'total_customer':total_customer
    }
    return JsonResponse({'data':data})





@api_view(['GET'])
def view_customer(request):
    customers = Customer.objects.all()
    serialize = Cuserializer(customers, many = True)
    return JsonResponse({'customer_data':serialize.data})

@api_view(['DELETE'])
def delete_customer(request,id):
    try:
        customer = Customer.objects.get(id = id)
        customer.delete()
        return JsonResponse({'status_code':200, 'message':'Delete successfully'})
    except:
        return JsonResponse({'message':'Id not found'})
    

@api_view(['POST'])
def add_blog(request):
    blog_data = request.data
    serialized_data = blogserializer(data=blog_data)
    if serialized_data.is_valid():
        # blog_image_file = request.FILES.get('blog_image')
        serialized_data.save()
        return JsonResponse({'status_code': 201, 'message': 'Blog added successfully!!!'})
    else:
        print(serialized_data.errors)
        return JsonResponse({'status_code': 402, 'message': 'Form error'})



@api_view(['GET'])
def adminView_blog(request):
    blog = Blog.objects.all()
    serialized_data = blogserializer(blog, many = True)
    return JsonResponse({'blog_data':serialized_data.data})

@api_view(['GET', 'PUT'])
def update_blog(request, id):
    try:
        blog = Blog.objects.get(id = id)
        if request.method == 'GET':
            blog_serializer = blogserializer(blog)
            print(blog_serializer)
            return JsonResponse(blog_serializer.data)
        elif request.method == 'PUT':
            serialized_data = blogserializer(blog, data=request.data, partial=True)
            if serialized_data.is_valid():
                if 'blog_image' in request.FILES:
                    blog.blog_image = request.FILES['blog_image']
                serialized_data.save()
                return JsonResponse({'status_code':200,'message':'Upadted Successfully'})
            else:
                return JsonResponse({'status_code':400, 'message':'Not updated'})
    except Blog.DoesNotExist:
        return JsonResponse({'status_code':400,'message':'Blog not found'})



 

@api_view(['DELETE'])
def delete_blog(request, id):
    try:
        blog = Blog.objects.get(id = id)
        blog.delete()
        return JsonResponse({'message':'Delete successfully'})
    except:
        return JsonResponse({'message':'Id not found'})


@api_view(['POST'])
def add_destination(request):
    destination_data = request.data
    serialized_data = Destination_serializer(data = destination_data)
    if serialized_data.is_valid():
        serialized_data.save()
        return JsonResponse({'message':'Destination added successfully'})
    else:
        return JsonResponse({'message':'Form error'})

@api_view(['GET'])
def view_destination(request):
    destination = Destination.objects.all()
    serializer_data = Destination_serializer(destination, many = True)
    return JsonResponse({'detination_data':serializer_data.data})

@api_view(['DELETE'])
def delete_destination(request, id):
    try:
        destination = Destination.objects.get(id = id)
        destination.delete()
        return JsonResponse({'message':'Delete successfully'})
    except:
        return JsonResponse({'message':'Id not found'})

@api_view(['GET', 'PUT'])
def edit_destination(request, destination_id):
    try:
        destination = Destination.objects.get(id=destination_id)
        if request.method == 'GET':
            destin_serializer = Destination_serializer(destination)
            print('get')
            return JsonResponse(destin_serializer.data)
        elif request.method == 'PUT':
            print('put')
            serialized_data = Destination_serializer(destination, data=request.data,partial=True)
            print(serialized_data)
            if serialized_data.is_valid():
                serialized_data.save()
                print('Valid')
                return JsonResponse({'status_code': 200, 'message': 'Destination updated successfully'})
            else:
                return JsonResponse({'status_code': 400, 'message': serialized_data.errors})
    except Destination.DoesNotExist:
        return JsonResponse({'status_code': 404, 'message': 'Destination not found'})


@api_view(['GET'])
def view_queries(request):
    queries = ContactUs.objects.all()
    serialized_data = ContactSerializer(queries, many = True)
    return JsonResponse({'query_data':serialized_data.data})
    
@api_view(['DELETE'])
def delete_queries(request, query_id):
    try:
        query = ContactUs.objects.get(id = query_id)
        query.delete()
        return JsonResponse({'message':'Delete successfully'})
    except:
        return JsonResponse({'message':'Id not found'})

@api_view(['PUT'])
def change_password(request):
    data = request.data
    try:
        admin = Admin.objects.get(id=data['admin_id'])
        
        if admin.admin_password != data['old_password']:
            return JsonResponse({'message': 'Invalid old password'})
        if admin.admin_password == data['new_password']:
            return JsonResponse({'message': 'New password should be different from the old password'})
        admin.admin_password = data['new_password']
        admin.save()

        return JsonResponse({'message': 'Password changed successfully'})
    except Admin.DoesNotExist:
        return JsonResponse({'message': 'Admin not found'})


@api_view(['POST'])
def admin_logout(request):
    # Get the token from the request headers or any other means
    token_key = request.POST.get('token')

    try:
        # Find the token in the database
        token = Token.objects.get(key=token_key)
        admin = token.user  # Assuming Admin model has a foreign key to User model

        # Delete the token
        token.delete()

        return JsonResponse({'status': True, 'message': 'Logout successful.'})

    except Token.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Invalid token.'})
