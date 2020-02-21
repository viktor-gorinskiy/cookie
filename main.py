#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tarfile
import zipfile
import json
import sys
import fleep
import rarfile


debug = True
debug = False

filter_cook = True
# filter_cook = False

js = ["domain", "flag", "path", "secure", "expiration", "name", "value"]

def type_file(file):
    with open(file, "rb") as file:
        info = fleep.get(file.read(128))
    # print('111',info.extension)
    return info.extension

def tar_file(tar_file):
    js = ["domain", "flag", "path", "secure", "expiration", "name", "value"]
    tarf = tarfile.open(tar_file, 'r:gz')
    result = {}
    result['count_zip'] = len(tarf.getmembers())
    for zip_ar in tarf.getmembers():
        data = []
        # print('zip_ar.name', zip_ar.name)
        result[zip_ar.name] = {}
        contentfobj = tarf.extractfile(zip_ar)
        z = zipfile.ZipFile(contentfobj, 'r')
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
                for line_cook in coo.readlines():
                    if filter_cook:
                        if 'facebook' in str(line_cook):
                            line_cook = list(line_cook.decode().replace('\r\n','').split('\t'))
                            cookie = dict(zip(js, line_cook))
                            cookie_dict.append(cookie)
                    else:
                        line_cook = list(line_cook.decode().replace('\r\n','').split('\t'))
                        cookie = dict(zip(js, line_cook))
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

def zip_file(file):
    result = {}
    # data = []
    z = zipfile.ZipFile(file, 'r')
    # cookie_dict = []
    # print(z.filelist)
    for file in z.filelist:
        # result = {}
        data = []
        # cookie_dict = []
        f_name = file.filename.split('/')[0].replace('(', '').replace(')', '')
        # f_name = file.filename
        if not f_name in result:
            result[f_name] = {}
            cookie_dict = []

        if 'pass' in file.filename.lower():
            # print('\tfile.filename',file.filename)
            f = z.open(file.filename)
            # print(f.readlines())
            mega_line = ''
            for line in f:
                try:
                    mega_line = mega_line + line.decode()
                except:
                    pass
            mega_line = mega_line.split('\r\n\r\n')
            account_pair = ''
            for d in mega_line:
                d = d.split('\r\n')
                if len(d) >= 3:
                    if 'facebook.com' in d[1]:
                        login = d[2].split('USER:')[1].replace('\t','')
                        password = d[3].split('PASS:')[1].replace('\t','')
                        account_pair = login + ' ' + password
                        data.append(account_pair)
            unique_user_pass = list(set(data))
            account = []
            for user_dat in unique_user_pass:
                # number_of_accounts = len(user_dat)
                user_pass = {}

                user_pass['login'] = user_dat.split(' ')[0]
                user_pass['pass'] = user_dat.split(' ')[1]
                account.append(user_pass)
                # print(user_pass)
                # print(account)
            # print(f_name, 'account', account,'\n')
        # result['count_files'] = len(result)
            result[f_name]['count_accounts'] = len(account)
            result[f_name]['accounts'] = account
        # result[f_name]['cookies'] = cookie_dict

        # if 'cookies' in file.filename.lower():
        # #     # print('\tcook',file.filename)
        #     coo = z.open(file.filename)
        # #     # print(file.filename,coo.readlines())
        #     for line_cook in coo.readlines():
        #         if 'facebook' in str(line_cook):
        # #         print(file.filename,line_cook.decode().replace('\r\n','').split('\t'))
        #             try:
        #                 line_cook = list(line_cook.decode().replace('\r\n','').split('\t'))
        #             except:
        #                 pass
        #             cookie = dict(zip(js, line_cook))
        #             cookie_dict.append(cookie)
        #             result[f_name]['cookies'] = cookie_dict
        if 'cook' in file.filename.lower():
            with z.open(file.filename) as cook_file:
                for line_cook in cook_file:
                    if filter_cook:
                        if 'facebook' in str(line_cook):
                            try:
                                line_cook = list(line_cook.decode().replace('\r\n', '').split('\t'))
                            except:
                                pass
                            cookie = dict(zip(js, line_cook))
                            cookie_dict.append(cookie)
                            # print(f_name, cookie_dict)
                    # else:
                    #     try:
                    #         line_cook = list(line_cook.decode().replace('\r\n', '').split('\t'))
                    #     except:
                    #         pass
                    #     cookie = dict(zip(js, line_cook))
                    #     cookie_dict.append(cookie)
                # print(f_name, cookie_dict)
                result[f_name]['cookies'] = cookie_dict

    result['count_files'] = len(result)
    print(json.dumps(result))

def rar_file(archive):
    result = {}
    rf = rarfile.RarFile(archive)
    for file_in_rar in rf.infolist():
        data = []
        if file_in_rar.file_size > 0:
            file_name = file_in_rar.filename.replace('[facebook] Europe, Poland ','').split('/')[0].replace('(', '').replace(')', '')
            if not file_name in result:
                result[file_name] = {}

            if 'pass' in file_in_rar.filename.lower():
                with rf.open(file_in_rar.filename) as file:
                    mega_line = ''
                    for line in file:
                        try:
                            mega_line = mega_line + line.decode()
                        except: pass
                mega_line = mega_line.split('\r\n\r\n')
                # print(mega_line)
                for d in mega_line:
                    d = d.split('\r\n')
                    # print(d)
                    if len(d) >= 3:
                        if d[0]:
                            if 'facebook.com' in d[1]:
                                login = d[2].split('Login: ')[1]
                                password = d[3].split('Password: ')[1]
                                account_pair = login + ' ' + password
                                data.append(account_pair)
                        else:
                            if 'facebook.com' in d[2]:
                                login = d[3].split('Login: ')[1]
                                password = d[4].split('Password: ')[1]
                                account_pair = login + ' ' + password
                                # account_pair = password
                                data.append(account_pair)

                account = []
                unique_user_pass = list(set(data))

                user_pass = {}
                for user_dat in unique_user_pass:
                    user_pass['login'] = user_dat.split(' ')[0]
                    user_pass['pass'] = user_dat.split(' ')[1]

                    account.append(user_pass)
                # print(file_name, account)
                result[file_name]['count_accounts'] = len(account)
                result[file_name]['accounts'] = account
    # print(len(result), result[file_name])
    result['count_files'] = len(result)
    # print(json.dumps(result))

    rf = rarfile.RarFile(archive)
    for file_in_rar in rf.infolist():
        cookie_dict = []
        if file_in_rar.file_size > 0:
            file_name = file_in_rar.filename.replace('[facebook] Europe, Poland ','').split('/')[0].replace('(', '').replace(')', '')
            if not file_name in result:
                result[file_name] = {}

            if 'cookies' in file_in_rar.filename.lower():
                with rf.open(file_in_rar.filename) as cook_file:
                    for line_cook in cook_file:
                        if filter_cook:
                            if 'facebook' in str(line_cook):
                                try:
                                    line_cook = list(line_cook.decode().replace('\r\n','').split('\t'))
                                except:
                                    pass
                                cookie = dict(zip(js, line_cook))
                                cookie_dict.append(cookie)
                        else:
                            try:
                                line_cook = list(line_cook.decode().replace('\r\n','').split('\t'))
                            except:
                                pass
                            cookie = dict(zip(js, line_cook))
                            cookie_dict.append(cookie)
                result[file_name]['cookies'] = cookie_dict

    print(json.dumps(result))

if not debug:
    try:
        if sys.argv[1] == '-h':
            print('to disable the filter, add a third parameter: filter_cook_off')
        else:
            file = sys.argv[1]

    except:
        print('Where\'s the archive???\n should I remind you about -h?')
        sys.exit(1)

    try:
        if sys.argv[2] == 'filter_cook_off':
            filter_cook = False
            print('False')
        elif sys.argv[2] == '-h':
            print('to disable the filter, add a third parameter: filter_cook_off')
            sys.exit(0)
    except:
        pass
else:
    # file = '2020_02_06_13_28-lr4R6C.tar.gz'
    # file = 'Facebook PL good 40.rar'
    file = ''


try:
    for t_file in type_file(file):
        if t_file == 'rar':
            rar_file(file)
            # print('rar')
        elif t_file == 'gz':
            tar_file(file)
            # print('gz')
        elif t_file == 'zip':
            # print('ZIP')
            zip_file(file)
        else:
            pass
        # print('eeeeeeeeeee')
        #     archives_type =  type_file(file)
        #     print('So far I can only work with RAR and GZ archives!')
        #     sys.exit(1)
        #     # print('gz')
except Exception as error:
    print(error)
