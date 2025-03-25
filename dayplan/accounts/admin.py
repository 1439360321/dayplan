from django.contrib import admin
from .models import CustomUser  # 导入你的模型

# 注册 Blog 让它出现在 Django Admin
admin.site.register(CustomUser)
