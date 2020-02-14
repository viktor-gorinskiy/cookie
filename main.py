#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tarfile
import zipfile
import time
import json
import sys

try:
    tar = sys.argv[1]
except:
    print('А где .tar.gz архив???')
    sys.exit(1)
#
js = ["domain", "flag", "path", "secure", "expiration", "name", "value"]
#
try:
    tarf = tarfile.open(tar, 'r:gz')
except IsADirectoryError as error:
    print(error)
    sys.exit(1)
except tarfile.ReadError as error:
    print(error)
    sys.exit(1)

# tar = '/home/viktor/PycharmProjects/cookie/2020_02_06_13_28-lr4R6C.tar.gz'
# tarf = tarfile.open(tar, 'r:gz')
try:
    result = {}
    result['count_zip'] = len(tarf.getmembers())
    for zip_ar in tarf.getmembers():
        data = []
        # print('zip_ar.name', zip_ar.name)
        result[zip_ar.name] = {}
        contentfobj = tarf.extractfile(zip_ar)
        z = zipfile.ZipFile(contentfobj, 'r')
        w = 0
        cookie_dict = []
        for file in z.filelist:
            if 'pass' in file.filename.lower():
                # print('\tfile.filename',file.filename)
                f = z.open(file.filename)
                # print(f.readlines())
                mega_line = ''
                for line in f:
                    mega_line = mega_line + line.decode()
                mega_line = mega_line.split('\r\n\r\n')
                # account_pair = {}
                account_pair = ''
                for d in mega_line:
                    d = d.split('\r\n')
                    if len(d) >= 3:
                        if 'facebook.com' in d[1]:
                            login = d[2].split('Login: ')[1]
                            password = d[3].split('Pass: ')[1]
                            account_pair = login + ' ' + password

                            data.append(account_pair)

            if 'cookies' in file.filename.lower():
            #     # print('\tcook',file.filename)
                coo = z.open(file.filename)
            #     # print(file.filename,coo.readlines())
            #     # w = 0
                for line_cook in coo.readlines():
            #         w += 1
            #         time.sleep(0.001)
            #         print(file.filename,line_cook.decode().replace('\r\n','').split('\t'))
                    line_cook = list(line_cook.decode().replace('\r\n','').split('\t'))
                    # print(line_cook)
                    # if line_cook.isspace():
                    #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    cookie = dict(zip(js, line_cook))
                    # print('\t\t',w,cookie)
                    cookie_dict.append(cookie)
    # print(data)
        unique_user_pass = list(set(data))
        account = []
        for user_dat in unique_user_pass:
            # number_of_accounts = len(user_dat)
            user_pass = {}

            user_pass['login'] = user_dat.split(' ')[0]
            user_pass['pass'] = user_dat.split(' ')[1]
            account.append(user_pass)

        # print('account', account,'\n')
        # number_of_accounts = len(account)
        result[zip_ar.name]['count_accounts'] = len(account)
        result[zip_ar.name]['accounts'] = account
        result[zip_ar.name]['cookies'] = cookie_dict

        # print('\t',account, cookie_dict,'\n')

    print(json.dumps(result))
except Exception as error:
    print('Что-то тут не так!')
    print(error)
    sys.exit(1)