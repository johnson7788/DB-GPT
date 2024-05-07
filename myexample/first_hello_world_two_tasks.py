#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/7 15:55
# @File  : first_hello_world_two_tasks.py
# @Author: 
# @Desc  : 有两个任务的Hello World程序
import asyncio

from dbgpt.core.awel import DAG, MapOperator, InputOperator, SimpleCallDataInputSource

with DAG("awel_hello_world") as dag:
    input_task = InputOperator(
        input_source=SimpleCallDataInputSource()
    )
    task = MapOperator(map_function=lambda x: print(f"Hello, {x}!"))
    input_task >> task

asyncio.run(task.call(call_data="world"))