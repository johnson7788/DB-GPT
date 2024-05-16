#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/14 10:04
# @File  : awe_dag_start_end_hook.py
# @Author: 
# @Desc  : 钩子函数

import asyncio
from dbgpt.core.awel import DAG, MapOperator

class MyLifecycleTask(MapOperator[str, str]):
    async def before_dag_run(self):
        print("Before DAG run")

    async def after_dag_end(self,task_id):
        print(f"After DAG end, {task_id}")

    async def map(self, x: str) -> str:
        return f"Hello, {x}!"

with DAG("awel_lifecycle_hooks") as dag:
    task = MyLifecycleTask()

print(asyncio.run(task.call("world")))