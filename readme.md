Python实现文件的原子写

## 思路
- 实现平台为Linux.
- 原子写入, 创建临时文件, 并写入, 待文件成功写入磁盘后, 直接将文件rename为目标文件.
- 为实现简单, 没有考虑追加写入方式, 且所有写入均为覆盖写, 且写入文件格式为行存储格式(按行写入方式). 

## 结构
```
atomic_writer.py: 文件的原子写装饰器
test_case.py: 测试用例
demo_to_parquet.py 写入parquet文件格式
```

## Example
```
为了测试 原子写与其他写进程的同步执行, 将函数包装成上下文管理器, 原子写完成时, 退出上下文环境.
    用法:
    @AtomicWriter
    def fun(path, data):
        write_info_file

    with fun(path, data):
        pass
```

## test
```
test_atomic_write: 正常写入case
test_teardown: 写入异常case
test_atomic_write_simultaneous: 原子写结束前, 同步写入case测试
```

## refer
[node.js](https://github.com/mcollina/fast-write-atomic)
[python-atomicwrites](https://github.com/untitaker/python-atomicwrites)