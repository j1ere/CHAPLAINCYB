from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import ContactMessageSerializer

from rest_framework.permissions import IsAdminUser

from .models import ContactMessage
from .serializers import ContactMessageSerializer
from rest_framework import status

class ContactMessageAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            email = EmailMessage(
                subject=f"New Contact Message: {data.get('category')}",
                body=f"""
From: {data.get('first_name')} {data.get('last_name')}
Email: {data.get('email')}
Phone: {data.get('phone')}

Message:
{data.get('message')}
                """,
                from_email='admin@stanneschaplaincy.com',  # uses DEFAULT_FROM_EMAIL
                to=["csa.maseno@stanneschaplaincy.com"],
                reply_to=[data.get("email")],  # ✅ NOW WORKS
            )

            email.send(fail_silently=False)

            serializer.save()

            return Response(
                {"message": "Message sent successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class AdminMessageListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        messages = ContactMessage.objects.all().order_by("-created_at")
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)
    




class AdminMarkAsReadAPIView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            message = ContactMessage.objects.get(pk=pk)
            message.is_read = True
            message.status = "read"
            message.save()

            return Response({"message": "Marked as read"}, status=status.HTTP_200_OK)

        except ContactMessage.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        

class AdminMarkAsRepliedAPIView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            message = ContactMessage.objects.get(pk=pk)
            message.status = "replied"
            message.is_read = True
            message.save()

            return Response({"message": "Marked as replied"}, status=status.HTTP_200_OK)

        except ContactMessage.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
class AdminDeleteMessageAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            message = ContactMessage.objects.get(pk=pk)
            message.delete()

            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except ContactMessage.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)