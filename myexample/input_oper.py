#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/14 10:37
# @File  : input_oper.py
# @Author: 
# @Desc  :

import asyncio
from dbgpt.core.awel import DAG, MapOperator, InputOperator, SimpleInputSource

with DAG("awel_input_operator") as dag:
    input_source = SimpleInputSource(data="Hello, World!")
    input_task = InputOperator(input_source=input_source)
    print_task = MapOperator(map_function=lambda x: print(x))
    input_task >> print_task

asyncio.run(print_task.call())