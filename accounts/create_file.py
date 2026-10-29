import os

# تحديد المسار بدقة
base_dir = r"D:\studend platform"
dir_path = os.path.join(base_dir, "accounts", "templates", "accounts")
file_path = os.path.join(dir_path, "link_student.html")

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(dir_path, exist_ok=True)

# محتوى ملف HTML
html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ربط الطالب</title>
    <style>
        body { font-family: 'Cairo', sans-serif; background: #0D1614; color: #EEF4F1; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; width: 400px; text-align: center; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); }
        h2 { margin-top: 0; color: #33D6A6; }
        input { width: 100%; padding: 12px; margin: 15px 0; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.08); color: white; font-family: inherit; box-sizing: border-box;}
        input:focus { outline: none; border-color: #33D6A6; }
        button { width: 100%; padding: 12px; background: linear-gradient(135deg, #33D6A6, #1F9E7A); color: #08251C; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; font-family: inherit; font-size: 1.1em; }
        button:hover { opacity: 0.9; }
        .message { margin-top: 15px; padding: 12px; border-radius: 10px; font-size: 0.9em; }
        .error { background: rgba(242,104,92,0.15); color: #F2685C; border: 1px solid rgba(242,104,92,0.3); }
        .success { background: rgba(51,214,166,0.15); color: #33D6A6; border: 1px solid rgba(51,214,166,0.3); }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔗 ربط الطالب</h2>
        <p style="color: #8DA098; margin-bottom: 25px;">أدخل كود الطالب لربطه بحسابك</p>
        <form method="POST">
            {% csrf_token %}
            <input type="text" name="student_code" placeholder="مثال: ST1511" required>
            <button type="submit">ربط الطالب</button>
        </form>
        {% if messages %}
            {% for message in messages %}
                <div class="message {% if message.tags == 'error' %}error{% else %}success{% endif %}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    </div>
</body>
</html>"""

# كتابة الملف
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ تم إنشاء الملف بنجاح!")
print(f"📁 المسار: {file_path}")
print(f"🔍 هل الملف موجود فعلياً؟ {os.path.exists(file_path)}")