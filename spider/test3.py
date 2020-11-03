import os
import time

date_time_str = str(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))

root_file = 'files'
if os.path.exists(root_file):
    root_dirs = os.listdir(root_file)
    if len(root_dirs) > 0:
        line_uniq = []
        for file in root_dirs:
            if 'detail' in file:
                need_file = os.path.join(root_file, file)
                if os.path.isfile(need_file):
                    with open(need_file, 'r', encoding='utf-8') as f_his:
                        for line in f_his.readlines():
                            if line not in line_uniq:
                                line_uniq.append(line)

        with open('files/51job_detail_uniq_company_' + date_time_str + '.txt', 'a', encoding='utf-8') as f_new:
            if line_uniq.__len__() > 0:
                for line in line_uniq:
                    f_new.write(line)

        for file in root_dirs:
            if 'detail' in file:
                os.remove(os.path.join(root_file, file))

