from rest_framework import generics,viewsets,permissions
from .models import Profile,LogTraining, Challenge
from .serializers import ProfileSerializer,LogTrainingSerializer, ChallengeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
