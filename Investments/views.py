from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class BuyCoinView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BuyCoinSerializer(data = request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.create(serializer.validated_data)
        return Response(data, status=status.HTTP_202_ACCEPTED)


class SellCoinView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = SellCoinSerializer(data = request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.update(serializer.validated_data)
        return Response(data, status=status.HTTP_202_ACCEPTED)


class GETMyHoldingsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyHoldingsSerializer
    
    def get_object(self):
        try : 
            return MyHoldings.objects.get(user = self.request.user)
        except : 
            raise CustomError("Verify yourself with PAN to trade", code=status.HTTP_406_NOT_ACCEPTABLE)


class MyWatchlistView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyWatchlistSerializer

    def get_object(self):
        obj, created = MyWatchlist.objects.get_or_create(user = self.request.user)
        if created:
            obj.watchlist = []
            obj.save()
        return obj