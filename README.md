Скрипт для Леши 

Чтобы запустить скрипт нужно перейти в директорию скрипта и прописать:
python3 название_скрипта.py  путь_к_списку_emailов
Cписок email должен  быть в формате:
         логин:пароль
         логин:пароль

Тестовый файл с учетками прилагается.

Также если надо загрузить файлы прикрепленные к email то надо передать с
cо скрипто м ключ get_file

Пример:  python3 script.py email.txt  get_file

Для того чтобы можно было качать email c гугла  нужно разрешить
небезопансные приложения