#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/7 15:52
# @File  : first_hello_world.py
# @Author: 
# @Desc  :


from dbgpt.core.awel import DAG, MapOperator

with DAG("awel_hello_world") as dag:
    task = MapOperator(map_function=lambda x: print(f"Hello, {x}!"))
task._blocking_call(call_data="world")