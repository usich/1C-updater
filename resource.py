import os
import subprocess
import time

from flask import request
from flask_restful import Resource


class CheckIsOnline(Resource):
    """Пустой запрос, для понимания онлайн ли торговая точка"""

    def get(self):
        return {}, 201


class SendMessage(Resource):
    """Отправка системного уведомления в Windows"""

    def get(self):
        text_message = request.args.get('text_message')
        if text_message is None:
            return {'msg': 'Не передан текст сообщения'}
        print(text_message)
        os.system(f'msg */localhost "{text_message}"')
        os.system("Taskkill /f /im 1cv8.exe")
        return {}, 201


class CheckFileCfUpdate(Resource):
    """Проверка файла для обновления .dt"""

    def get(self):
        data = request.args
        filename = data.get('filename')

        check_file_update = os.path.isfile(f"C:/ftp/{filename}.cf")  # test TXT
        check_file_xml = os.path.isfile(f"C:/ftp/{filename}.xml")

        return {
            'file_update': check_file_update,
            'file_xml': check_file_xml
        }, 201


class Run1CMerge(Resource):
    """Запуск "сравнения/объединения с информационной базой" """

    def get(self):
        data = request.args
        server_name = data.get('server_name')
        file_name = data.get('file_name')
        version_1c = data.get('version_1c')
        is_fast_update = data.get('is_fast_update')
        user_name = data.get('user_name')
        password = data.get('password')
        full_merge = data.get('full_merge')
        if password is None:
            password = ''
        else:
            password = f'/P{password}'
        if server_name is None or file_name is None or version_1c is None or is_fast_update is None \
                or user_name is None or full_merge is None:
            return {'msg': 'Переданы не все обязательные параметры'}, 401
        setting_file_name = f'{file_name}.xml'
        if full_merge == 'true':
            setting_file_name = 'full_merge.xml'
        command = rf'"C:\Program Files (x86)\1cv8\{version_1c}\bin\1cv8.exe" CONFIG /S{server_name} /N{user_name} {password} /DisableStartupMessages /MergeCfg C:\ftp\{file_name}.cf -Settings C:\ftp\{setting_file_name} -force /UCПакетноеОбновлениеКонфигурацииИБ /Out C:\ftp\log-merge.txt'
        try:
            subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL)
        except Exception as ex:
            return {
                'msg': 'Error',
                'text': ex}, 401
        return {'msg': 'success'}, 201


class CheckMerge1C(Resource):
    """Проверка закончено ли объединение"""

    def get(self):
        if os.path.exists('C:/ftp/log-merge.txt'):
            with open('C:/ftp/log-merge.txt', 'r', encoding='ANSI') as f:
                logs_merge = f.read()
                if len(logs_merge) == 0:
                    return {'msg': 'Error',
                            'logs': 'file empty'}
                success = False
                for i in logs_merge.split('\n'):
                    if i.strip() == 'Объединение конфигураций успешно завершено':
                        success = True
                if not success:
                    return {'msg': 'Error',
                            'logs': logs_merge}, 401
            open('C:/ftp/log-merge.txt', 'w', encoding='ANSI').close()

            return {'msg': 'success',
                    'logs': logs_merge}, 201


class Run1CUpdate(Resource):
    """Запуск "Обновления конфигурации баз данных" """

    def get(self):
        data = request.args
        server_name = data.get('server_name')
        file_name = data.get('file_name')
        version_1c = data.get('version_1c')
        is_fast_update = data.get('is_fast_update')
        user_name = data.get('user_name')
        password = data.get('password')
        full_merge = data.get('full_merge')
        if password is None:
            password = ''
        else:
            password = f'/P{password}'
        if server_name is None or file_name is None or version_1c is None or is_fast_update is None \
                or user_name is None or full_merge is None:
            return {'msg': 'Переданы не все обязательные параметры'}, 401
        try:
            if is_fast_update != 'true':
                command = fr'"C:\Program Files (x86)\1cv8\{version_1c}\bin\1cv8.exe" ENTERPRISE /S{server_name} /N{user_name} {password} /WA- /AU- /DisableStartupMessages -force /CЗавершитьРаботуПользователей'
                subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL)
                time.sleep(15)
                os.system("Taskkill /f /im 1cv8.exe")
            command = rf'"C:\Program Files (x86)\1cv8\{version_1c}\bin\1cv8.exe" CONFIG /S{server_name} /N{user_name} {password} /DisableStartupMessages /UpdateDBCfg /UCКодРазрешения /Out C:\ftp\log-update-db.txt'
            subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL)

        except Exception as ex:
            return {
                'msg': 'Error',
                'logs': ex
            }
        return {'msg': 'success'}, 201


class CheckUpdate1C(Resource):
    """Проверка выполнено ли обновление """

    def get(self):
        data = request.args
        server_name = data.get('server_name')
        version_1c = data.get('version_1c')
        is_fast_update = data.get('is_fast_update')
        user_name = data.get('user_name')
        password = data.get('password')
        if password is None:
            password = ''
        else:
            password = f'/P{password}'

        if os.path.exists('C:/ftp/log-update-db.txt'):
            with open('C:/ftp/log-update-db.txt', 'r', encoding='ANSI') as f:
                logs_update = f.read()
                if len(logs_update) == 0:
                    return {'msg': 'Error',
                            'logs': 'File empty'}, 401
                success = False
                for i in logs_update.split('\n'):
                    if i.strip() == 'Обновление конфигурации успешно завершено':
                        success = True
                if not success:
                    return {'msg': 'Error',
                            'logs': logs_update}, 401

        if is_fast_update != 'true':
            command = fr'"C:\Program Files (x86)\1cv8\{version_1c}\bin\1cv8.exe" ENTERPRISE /S{server_name} /N{user_name} {password} /DisableStartupMessages -force /CРазрешитьРаботуПользователей /UCКодРазрешения'
            subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL)
        open('C:/ftp/log-update-db.txt', 'w', encoding='ANSI').close()
        return {'msg': 'success',
                'logs': logs_update}, 201
