#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@author RenMeng
@since 2022/4/24
'''

from atomic_writer import AtomicWriter
import pytest

@AtomicWriter
def write_normal(target_path, data):
    with open(target_path, 'w') as f:
        f.write(data)

@AtomicWriter
def write_error(target_path, data):
    with open(target_path, 'w') as f:
        f.write(data)
        raise OSError


def test_atomic_write(tmpdir):
    fname = tmpdir.join('ha')
    with write_normal(str(fname), 'hoho'):
        pass

    assert fname.read() == 'hoho'
    assert len(tmpdir.listdir()) == 1


def test_teardown(tmpdir):
    fname = tmpdir.join('ha')
    with pytest.raises(OSError):
        with write_error(fname, 'hoho'):
            pass

    assert not tmpdir.listdir()



def test_atomic_write_simultaneous(tmpdir):
    fname = tmpdir.join('ha')
    with write_normal(str(fname), 'hoho'):
        fname.write('harhar')
        assert fname.read() == 'harhar'
    assert fname.read() == 'hoho'
    assert len(tmpdir.listdir()) == 1

