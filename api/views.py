from rest_framework import generics,viewsets,permissions
from .models import Profile,LogTraining, Challenge
from .serializers import ProfileSerializer,LogTrainingSerializer, ChallengeSerializer,ContactSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny
from dj_rest_auth.registration.views import RegisterView
from django.conf import settings

class CustomRegisterView(RegisterView):
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        # Perform any additional actions here (e.g., log the registration, update user profile, etc.)

        # Send the registration email
        subject = 'Welcome to Swimtrack'
        message = 'Thank you for registering. Welcome to our platform!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        

        send_mail(subject, message, from_email, recipient_list)



class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile


class LogTrainingView(APIView):
    def get(self, request, format=None):
        # Filter log trainings based on the current user
        log_trainings = LogTraining.objects.filter(user=request.user)
        serializer = LogTrainingSerializer(log_trainings, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = LogTrainingSerializer(data=request.data)
        if serializer.is_valid():
            # Set the user of the log training to the current user
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class ChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'challenge_id'

    def get_queryset(self):
        return Challenge.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactFormView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Send email
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            subject = 'New Contact Form Submission'
            email_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            recipient_list = ['luismvg41@gmail.com']

            send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, recipient_list)

            return Response({'success': True, 'message': 'Form submitted successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)