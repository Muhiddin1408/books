from django.contrib.auth import authenticate, user_logged_in
from rest_framework import status, generics, authentication, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from shop.serializers import (
    UserSerializer,
    RegisterSerializer,
    ProductSerializer,
    HistorySerializer,
    ProductDetailSerializerMine,
    CartSerializer,
    OrderSerializer,
    ProfilSerializer)
from .paginations import LargeResultsSetPagination
from account.models import User
from .models import Book, Cart, Order, Report
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    try:
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user:
            try:
                poyload = jwt_payload_handler(user)
                token = jwt_encode_handler(poyload)
                user_detail = {}
                user_detail['status'] = 1
                user_detail['msg'] = 'User sign'
                user_detail['username'] = UserSerializer(user, many=False).data
                user_detail['token'] = token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(user_detail, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'status': 0,
                'msg': 'Can not authenticate with the given credentials or the account has been deactivated'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please provide a login and a password'
        }
        return Response(res)


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProductView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    search_fields = ['name', 'author', 'category']

    def get_queryset(self):
        return Book.objects.filter(category=self.kwargs['category'])


class ProductViewSet(RetrieveAPIView):
    serializer_class = ProductDetailSerializerMine
    queryset = Book.objects.all()


class AaaCartView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        snippets = Cart.objects.all()
        serializer = CartSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)

        product = Book.objects.get(id=self.kwargs['id'])
        if serializer.is_valid():
            cart = Cart.objects.create(
                user=request.user,
                product=product,
                quantity=request.data['quantity'],
                subtotel=product.price*request.data['quantity']

            )
            print(serializer)
            cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        carts = Cart.objects.all()
        serializer = OrderSerializer(data=request.data)
        text = ''
        buy = 0
        if serializer.is_valid():
            for i in carts:
                Book.objects.filter(product=i.product).update(residue=Book.objects.get(product=i.product).residue-1)
                text += f'{i.product.name}--{i.quantity}ta--{i.quantity * i.product.price}so\'m\n  '
                buy += i.quantity * i.product.price
            buy = str(buy)
            order = Order.objects.create(
                user=request.user,
                products=text,
                quantity=buy,
            )
            order.save()
            for i in carts:
                if Report.objects.filter(book=i.product):
                    report = Report.objects.filter(book=i.product).first()
                    report.quantity += i.quantity
                    report.save()
                else:
                    report = Report.objects.create(
                        book=i.product,
                        quantity=i.quantity
                    )
                    report.save()
            Cart.objects.filter(user=request.user).delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilView(generics.ListAPIView):
    serializer_class = ProfilSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['id'])


class History(generics.ListAPIView):
    serializer_class = HistorySerializer

    def get_queryset(self):
        return Order.objects.filter(id=self.kwargs['id'])
