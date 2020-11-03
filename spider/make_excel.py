# coding:utf-8
import os
import time
import platform
import pandas as pd
import uuid
from pandas import DataFrame


def make_excel(jobs_data):
    # 增加行数据，在第5行新增
    #     # for i in range(10):
    #     #     data.loc[i + 4] = [1, '韩小顺', '男', '152224199101105555', '初级', '否', 33.5, '17099887654', '1999-01-01',
    #     #                        '青峰白羽软件技术工作室',
    #     #                        '韩小顺', '电（高）, 钳（中）']
    try:
        # 生成将要保存的文件路径
        day_string = str(time.strftime('%Y/%m/%d', time.localtime(time.time())))
        file_root = "files"
        if os.path.exists(file_root):
            pass
        else:
            os.makedirs(file_root)
        files_path = file_root + "51job_day.xlsx"
        data = pd.DataFrame(jobs_data)
        # 保存数据
        with pd.ExcelWriter(files_path) as writer:  # doctest: +SKIP
            data.to_excel(writer, sheet_name='51job', index=False, header=0, na_rep='')
    except Exception as e:
        print(e)
        raise e


if __name__ == '__main__':
    jobs_datas = [[1111, 2222, 444444, 5555, 6666, 7777777],
        [1111, 2222, 444444, 5555, 6666, 7777777],
        [1111, 2222, 444444, 5555, 6666, 7777777]
    ]
    make_excel(jobs_datas)
