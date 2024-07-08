import uuid
from django.contrib.auth import get_user_model, authenticate
from django.db import IntegrityError
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Organisation
from .serializers import UserSerializer, OrganisationSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                org_name = f"{user.firstName}'s Organisation"
                org = Organisation.objects.create(
                    orgId=str(uuid.uuid4()),
                    name=org_name,
                    description=""
                )
                org.users.add(user)
                org.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'success',
                    'message': 'Registration successful',
                    'data': {
                        'accessToken': str(refresh.access_token),
                        'user': {
                            'userId': user.userId,
                            'firstName': user.firstName,
                            'lastName': user.lastName,
                            'email': user.email,
                            'phone': user.phone
                        }
                    }
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    'status': 'Bad request',
                    'message': 'Registration unsuccessful. Duplicate email or userId.',
                    'statusCode': 422,
                    'errors': [{'field': 'email', 'message': 'Duplicate email or userId.'}]
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({
            'status': 'Bad request',
            'message': 'Registration unsuccessful',
            'statusCode': 422,
            'errors': serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"Attempting to authenticate user with email: {email}")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            print("Authentication successful")
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': {
                        'userId': user.userId,
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone
                    }
                }
            }, status=status.HTTP_200_OK)
        print("Authentication failed")
        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user or user.organisations.filter(users=request.user).exists():
            serializer = self.get_serializer(user)
            return Response({
                'status': 'success',
                'message': 'User retrieved successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Forbidden',
            'message': 'You do not have permission to view this user',
            'statusCode': 403
        }, status=status.HTTP_403_FORBIDDEN)

class OrganisationListView(generics.ListAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.organisations.all()

class OrganisationDetailView(generics.RetrieveAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'orgId'  # Correct the attribute name to 'lookup_field'

    def get(self, request, *args, **kwargs):
        try:
            org = self.get_object()
            if org.users.filter(pk=request.user.pk).exists():
                serializer = self.get_serializer(org)
                return Response({
                    'status': 'success',
                    'message': 'Organisation retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to view this organisation',
                'statusCode': 403
            }, status=status.HTTP_403_FORBIDDEN)
        except Organisation.DoesNotExist:
            return Response({
                'status': 'Not Found',
                'message': 'Organisation not found',
                'statusCode': 404
            }, status=status.HTTP_404_NOT_FOUND)



class OrganisationCreateView(generics.CreateAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            org = serializer.save()
            org.users.add(request.user)
            return Response({
                'status': 'success',
                'message': 'Organisation created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad Request',
            'message': 'Client error',
            'statusCode': 400,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AddUserToOrganisationView(generics.UpdateAPIView):
    queryset = Organisation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        org = self.get_object()
        userId = request.data.get('userId')
        try:
            user = User.objects.get(userId=userId)
            if org.users.filter(pk=request.user.pk).exists():
                org.users.add(user)
                return Response({
                    'status': 'success',
                    'message': 'User added to organisation successfully'
                }, status=status.HTTP_200_OK)
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to add users to this organisation',
                'statusCode': 403
            }, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({
                'status': 'Bad Request',
                'message': 'User not found',
                'statusCode': 400
            }, status=status.HTTP_400_BAD_REQUEST)
