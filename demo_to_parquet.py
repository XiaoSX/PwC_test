#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@author RenMeng
@since 2022/4/24
'''

from atomic_writer import AtomicWriter
import pandas as pd
import io

"""
实现写入parquet文件
    AtmoicWriter支持写入为一般文件格式, 待文件写入完成后, 手动完成转换
"""

@AtomicWriter
def write(path, data):
    with open(path, 'w') as f:
        f.write(data)

if __name__ == '__main__':
    # 准备data
    df = pd.DataFrame({'name': ['张三', '李四'], 'age': [10, 20]})
    s = io.StringIO()
    df.to_csv(s, index=False)
    data = s.getvalue()
    # 调用装饰器
    with write('demo.txt', data):
        pass
    # 格式转换
    df = pd.read_csv('demo.txt')
    df.to_parquet('demo.parq')