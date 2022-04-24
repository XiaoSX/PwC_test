#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@author RenMeng
@since 2022/4/24
'''

import tempfile
import os
import io
import contextlib

class AtomicWriter:
    """
    原子写装饰器, 使写函数具有原子写特性.
        为了测试 原子写与其他写进程的同步执行, 将函数包装成上下文管理器, 原子写完成时, 退出上下文环境.
        用法:
        @AtomicWriter
        def fun(path, data):
            write_info_file

        with fun(path, data):
            pass

        为简单处理:
            (1) 假设默认写函数为覆盖写模式(即mode='w'),不支持追加写操作.
            (2) 所有写操作均为覆盖写
    :param fun: 被装饰的写函数
    """
    def __init__(self, func):
        self.func = func

    @contextlib.contextmanager
    def __call__(self, path, data=''):
        """

        :param args:
        :param kwargs:
        :return:
        """
        f = None
        try:
            success = False
            with self.get_fileobject(path) as f:
                self.func(f.name, data)
                yield
                # 若正常写入, 刷新缓存并写入磁盘
                self.sync(f)
            # 原子替换
            self.commit(f, path)
            success = True
        finally:
            if not success:
                try:
                    self.rollback(f)
                except:
                    pass


    def get_fileobject(self, path):
        '''返回临时文件'''
        dir = os.path.normpath(os.path.dirname(path))
        descriptor, name = tempfile.mkstemp(dir=dir)
        os.close(descriptor)
        return io.open(file=name, mode='w')

    def sync(self, f):
        f.flush()
        os.fsync(f.fileno())

    def commit(self, f, dst):
        os.rename(f.name, dst)
        dir_path = os.path.normpath(os.path.dirname(dst))
        fd = os.open(dir_path, 0)
        os.fsync(fd)
        os.close(fd)


    def rollback(self, f):
        os.unlink(f.name)


