#!/usr/bin/python3
# -*- coding: utf-8

#    ___   __ _              _____               ___                        _ _
#   / _ \ /__\ |_            \_   \/\/\   __ _  / _ \   ___ _ __ ___   __ _(_) |
#  / /_\//_\ | __|            / /\/    \ / _` |/ /_)/  / _ \ '_ ` _ \ / _` | | |
# / /_\\//__ | |_          /\/ /_/ /\/\ \ (_| / ___/  |  __/ | | | | | (_| | | |
# \____/\__/  \__|  _____  \____/\/    \/\__,_\/       \___|_| |_| |_|\__,_|_|_|
#                  |_____|
#
#  Чтобы запустить скрипт нужно перейти в директорию скрипта и прописать:
#  python3 название_скрипта.py  путь_к_списку_emailов
#
#  Cписок email должен  быть в формате:
#           логин:пароль
#           логин:пароль
#
#  Тестовый файл с учетками прилагается.
#
#  Также если надо загрузить файлы прикрепленные к email то надо передать с
#  cо скрипто м ключ get_file
#
#  Пример:  python3 script.py email.txt  get_file
#
#  Для того чтобы можно было качать email c гугла  нужно разрешить
#  небезопансные приложения




import sys, imaplib, email, pprint, os, re, traceback, datetime


def get_imap_server(str):
    '''

    :mailru: массив для доменов в mail почте
    :gmail: массив для доменов в gmail почте
    :yandex: массив для доменов в yandex почте
    :param str:  получает адрес(логин) почты
    :return: возвращает название imap сервера для почты

    '''
    mailru = ["bk", "mail", "inbox", "list"]
    gmail = ["gmail"]
    yandex = ["yandex"]
    str = str.split(".")[-2].split("@")[-1]
    if str in mailru:
        return "imap.mail.ru"
    if str in gmail:
        return "imap.gmail.com"
    if str in yandex:
        return "imap.yandex.ru"
    else:
        print("В базе нет данного imap сервера")



def correct_aray_mail(file, sss=":"):
    '''

    :param file: получает путь к файлу из текущей дирректории
    :param sss: получает символы разделяющие логин и пароль (default=":")
    :return: возвращает коректный для дальнейшей обработки массив login:password

    '''
    with open(file, 'r') as mail_file_list:
        e = mail_file_list.readlines()
    result_email = {}
    for i in e:
        b = i.split(sss)
        result_email[b[0]] = b[1]
    return result_email;



def decode_words(string):
    '''

    :param string: получает строку
    :return:  декодирует заголовок

    '''
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(string))


def good_file_name(string):
    '''

    :param string: строка которую надо изменить
    :return: возрощает строку разрешеную для использования в именование попок

    '''
    # получает строку и уберает символы не разрешеные для именования папок
    name_file_email = string[:30].replace(" ", "_") + "..."
    name_file_email = re.sub(r"[#%!:*?”<>|\\/]", "", name_file_email)
    return name_file_email


def change_directories(main_dir, path):
    '''

    :param main_dir: деректория от которй начинается отсчет
    :param path: папка в  которую надо создать и перейти
    :return: создает деректорию и меняет текущую на созданную

    '''
    if os.path.exists(main_dir + "/" + path):
        os.chdir(main_dir + "/" + path)
    else:
        os.mkdir(main_dir + "/" + path)
        os.chdir(main_dir + "/" + path)
    return;


if __name__ == '__main__':
    MAIN_DIR = os.getcwd()



    try:

        result_email = correct_aray_mail(sys.argv[1])


        for login, pawssword in result_email.items():

            print("\n\r \n\r")

            change_directories(MAIN_DIR, login)

            imap_server=get_imap_server(login)

            # Я сделал для Yandex потому-что у меня были готовые почты yandex,
            #  но можно сделать проверку или указывать призапуске скрипта
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(login,re.sub("^\s+|\n|\r|\s+$", '', pawssword))

            mail.list()

            # Выводит список папок в почтовом ящике.
            mail.select("inbox")
            result, data = mail.uid('search', None, "ALL")
            latest_email_uid = data[0].split()

            for email_uid in latest_email_uid:
                result, data = mail.uid('fetch', email_uid, '(RFC822)')
                mail_data = data[0][1]
                mail_data = mail_data
                mail_message = email.message_from_bytes(mail_data)

                # Получаем:
                # mail_subject: заголовок  сообщения
                # mail_from: от кого отправленно сообшение
                # mail_date: Дата когла пришел email

                mail_subject = decode_words(mail_message.get('Subject'))  # ~~~
                mail_from = decode_words(mail_message.get('From'))  # ~~~
                mail_date = mail_message.get('Date')  # ~~~

                name_file_email = good_file_name(mail_subject[:30])
                change_directories(".", name_file_email)


                #
                # Создаем и записываем в файл html письма
                if mail_message.is_multipart():
                    for part in mail_message.walk():
                        content_type = part.get_content_type()
                        pprint.pprint(content_type)
                        filename = part.get_filename()
                        if part.get_content_type() == 'text/html':
                            body = part.get_payload(decode=True).decode("utf-8")
                            with open("./email.html", 'w') as new_file:
                                new_file.write(body)

                        if "get_file" in sys.argv:
                            if filename:
                                #
                                # здесь я создаю   все изображения, файлы прикрепленые к письму
                                with open(part.get_filename(), 'wb') as new_file:
                                    new_file.write(part.get_payload(decode=True))
                else:
                    for part in mail_message.walk():
                        body = part.get_payload(decode=True).decode("utf-8")
                        with open("./email.html", 'w') as new_file:
                            new_file.write(body)
                        #
                        # здесь я создаю   все изображения, файлы прикрепленые к письму

                        if "get_file" in sys.argv:
                            if filename:
                                #
                                # здесь создаю я  все изображения, файлы прикрепленые к письму
                                with open(part.get_filename(), 'wb') as new_file:
                                    new_file.write(part.get_payload(decode=True))

                print("\n\r \n\r")
                os.chdir("../")
            os.chdir("../")

            # закрываем работу с почтой
            mail.close()
            mail.logout()

    except Exception as e:
        #
        # Пишем в логи ошибку
        print('Произошла ошибка логи можно посмотреть в папке ./log: \n')
        # pprint.pprint(traceback.format_exc())
        change_directories(MAIN_DIR, "log")
        now = datetime.datetime.now()
        with open("./error_" + str(now), 'w') as new_file:
            new_file.write(traceback.format_exc())
