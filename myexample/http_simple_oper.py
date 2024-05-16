#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/14 10:43
# @File  : http_simple_oper.py
# @Author: 
# @Desc  :

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator, setup_dev_environment

with DAG("awel_hello_world") as dag:
    trigger_task = HttpTrigger(endpoint="/awel_tutorial/hello_world")
    task = MapOperator(map_function=lambda x: f"Hello, world!")
    trigger_task >> task

setup_dev_environment([dag], port=5555)