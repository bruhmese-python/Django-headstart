cd "D:/Image-Editor-Environment"
call "D:/Image-Editor-Environment/Scripts/activate"
call django-admin startproject Image-Editor-Project
cd Image-Editor-Project
start http://127.0.0.1:8000/
call python manage.py runserver
exit