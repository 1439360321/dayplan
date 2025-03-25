from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import Task
from .serializer import TaskSerializer
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
import io
# Create your views here.


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        return TaskSerializer  # 可以在这里动态返回不同的序列化器

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return TaskSerializer  # 可以在这里动态返回不同的序列化器


class ExportTasksPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        html_string = render_to_string('tasks_pdf_template.html', {'tasks': tasks, 'user': request.user})

        # 生成 PDF
        result = io.BytesIO()
        with io.BytesIO() as temp_file:
            pisa_status = pisa.CreatePDF(html_string, dest=temp_file)
            if pisa_status.err:
                return Response({"error": "PDF 导出失败"}, status=500)

            temp_file.seek(0)  # 读取内容
            response = HttpResponse(temp_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="tasks.pdf"'
            return response
