from unicodedata import category

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .serializers import CustomerSerializer, CategorySerializer, FoodSerializer, OrderSerializer
from .models import Customer, Category, Food, Order
from .permissions import IsAdminUser, IsAuth


class CustomerListView(APIView):
    permission_classes = [IsAuth, IsAdminUser]

    def get(self, request):
        customers = Customer.objects.all()
        customers_serializer = CustomerSerializer(customers, many=True, context={'request': request})
        return Response(customers_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        customer_serializer = CustomerSerializer(data=request.data, context={'request': request})
        if customer_serializer.is_valid():
            customer = customer_serializer.save()
            context = {
                'message': "Mijoz muvaffaqiyatli qo'shildi",
                'data': CustomerSerializer(customer, context={'request': request}).data
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    permission_classes = [IsAuth, IsAdminUser]
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            customer_serializer = CustomerSerializer(customer, context={'request': request})
            return Response(customer_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            update_customer = serializer.update(customer, serializer.validated_data)
            context = {
                'message': "Mijoz ma'lumotlari muvaffaqiyatli yangilandi",
                'data': CustomerSerializer(update_customer, context={'request': request}).data
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            Customer.objects.get(pk=pk).delete()
            return Response({"Mijoz muvafaqqiyatli o'chirildi"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class CategoryListView(APIView):
    permission_classes = [IsAuth, IsAdminUser]
    def get(self, request):
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(categories_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        category_serializer = CategorySerializer(data=request.data, context={'request': request})
        if category_serializer.is_valid():
            category = category_serializer.save()
            context = {
                'message': "Ma'lumot muvaffaqiyatli qo'shildi",
                'data': CategorySerializer(category, context={'request': request}).data
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [IsAuth, IsAdminUser]
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
            category_serializer = CategorySerializer(category, context={'request': request})
            return Response(category_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            update_category = serializer.update(category, serializer.validated_data)
            context = {
                'message': "Kategoriya muvaffaqiyatli yangilandi",
                'data': CategorySerializer(update_category, context={'request': request}).data
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        try:
            Category.objects.get(slug=slug).delete()
            return Response({'message': "Ma'lumot muvaffaqiyatli o'chirildi"})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class FoodListView(APIView):
    permission_classes = [IsAuth, IsAdminUser]
    def get(self, request):
        foods = Food.objects.filter(available=True)
        foods_serializer = FoodSerializer(foods, many=True, context={'request': request})
        return Response(foods_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        category_id = request.data.get('category_id', None)
        if category_id:
            try:
                category_url = reverse('api:category_detail',
                                       kwargs={'slug': Category.objects.get(id=category_id).slug}, request=request)
                request.data['category'] = category_url
            except Category.DoesNotExist:
                return Response({'error': 'Category not found.'}, status=status.HTTP_400_BAD_REQUEST)

        food_serializer = FoodSerializer(data=request.data, context={'request': request})
        if food_serializer.is_valid():
            food = food_serializer.save()
            context = {
                'message': "Ma'lumot muvaffaqiyatli qo'shildi",
                'data': FoodSerializer(food, context={'request': request}).data
            }
            return Response(context, status=status.HTTP_200_OK)

        return Response(food_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodDetailView(APIView):
    permission_classes = [IsAuth, IsAdminUser]

    def get(self, request, slug):
        try:
            food = Food.objects.get(slug=slug, available=True)
            food_serializer = FoodSerializer(food, context={'request': request})
            return Response(food_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug):
        try:
            food = Food.objects.get(slug=slug)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

        category_id = request.data.get('category_id', None)
        if category_id:
            try:
                category_url = reverse('api:category_detail',
                                       kwargs={'slug': Category.objects.get(id=category_id).slug}, request=request)
                request.data['category'] = category_url
            except Category.DoesNotExist:
                return Response({'error': 'Category not found.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FoodSerializer(data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            update_food = serializer.update(food, serializer.validated_data)
            context = {
                'message': "Ma'lumot muvaffaqiyatli yangilandi",
                'data': FoodSerializer(update_food, context={'request': request}).data
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        try:
            Food.objects.get(slug=slug).delete()
            return Response({'message': "Ma'lumot muvaffaqiyatli o'chirildi"})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class OrderListView(APIView):
    permission_classes = [IsAuth, IsAdminUser]

    def get(self, request):
        orders = Order.objects.all()
        orders_serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(orders_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        customer_id = request.data.get('customer_id', None)
        if customer_id:
            try:
                customer_url = reverse('api:customer_detail',
                                       kwargs={'pk': Customer.objects.get(id=customer_id).pk}, request=request)
                request.data['customer'] = customer_url
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found.'}, status=status.HTTP_400_BAD_REQUEST)

        items = request.data.get('items', None)
        if items:
            foods_url = []
            for item in items:
                if item:
                    try:
                        food_url = reverse('api:food_detail',
                                               kwargs={'slug': Food.objects.get(id=item).slug}, request=request)
                        foods_url.append(food_url)
                    except Food.DoesNotExist:
                        return Response({'error': 'Food not found.'}, status=status.HTTP_400_BAD_REQUEST)
            request.data['items'] = foods_url

        order_serializer = OrderSerializer(data=request.data, context={'request': request})
        if order_serializer.is_valid():
            order = order_serializer.save()
            context = {
                'message': "Buyurtma muvaffaqiyatli qo'shildi",
                'data': OrderSerializer(order, context={'request': request}).data
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = [IsAuth, IsAdminUser]

    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        order_serializer = OrderSerializer(order, context={'request': request})
        return Response(order_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        customer_id = request.data.get('customer_id', None)
        if customer_id:
            try:
                customer_url = reverse('api:customer_detail',
                                       kwargs={'pk': Customer.objects.get(id=customer_id).pk}, request=request)
                request.data['customer'] = customer_url
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found.'}, status=status.HTTP_400_BAD_REQUEST)

        items = request.data.get('items', None)
        if items:
            foods_url = []
            for item in items:
                if item:
                    try:
                        food_url = reverse('api:food_detail',
                                           kwargs={'slug': Food.objects.get(id=item).slug}, request=request)
                        foods_url.append(food_url)
                    except Food.DoesNotExist:
                        return Response({'error': 'Food not found.'}, status=status.HTTP_400_BAD_REQUEST)
            request.data['items'] = foods_url

        order = get_object_or_404(Order, id=id)
        order_serializer = OrderSerializer(data=request.data, partial=True, context={'request': request})
        if order_serializer.is_valid():
            order = order_serializer.update(order, order_serializer.validated_data)
            context = {
                'message': "Buyurtma muvaffaqiyatli yangilandi",
                'data': OrderSerializer(order, context={'request': request}).data
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        order = get_object_or_404(Order, id=id)
        order.delete()
        return Response({'message': "Buyurtma muvaffaqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)
