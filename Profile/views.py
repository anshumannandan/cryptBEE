from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class VerifyPANView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = VerifyPANSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({ **{'message' : ['Verified']}, **serializer.data}, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


# class EnableTwoFactorView(CreateAPIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = EnableTwoFactorSerializer(data = request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.create(serializer.validated_data)
#         return Response({'message' : ['Two Factor Verification Enabled']}, status=status.HTTP_202_ACCEPTED)


class DisableTwoFactorView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DisableTwoFactorSerializer

    def get_object(self):
        try:
            return self.request.user.twofactor
        except:
            pass


class ProfilePictureView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePictureSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        picture = self.request.user.profile_picture
        if picture != 'profile.jpg':
            picture.delete()
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if user.profile_picture != 'profile.jpg':
            user.profile_picture.delete()
        user.profile_picture = 'profile.jpg'
        user.save()
        return Response({'message' : 'Profile Picture Deleted'})


class UserDetailsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer

    def get_object(self):
        return self.request.user