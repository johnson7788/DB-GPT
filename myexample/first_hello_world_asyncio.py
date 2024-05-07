#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/7 15:54
# @File  : first_hello_world_asyncio.py
# @Author: 
# @Desc  :


import asyncio

from dbgpt.core.awel import DAG, MapOperator

with DAG("awel_hello_world") as dag:
    task = MapOperator(map_function=lambda x: print(f"Hello, {x}!"))

asyncio.run(task.call(call_data="world"))