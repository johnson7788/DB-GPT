#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/14 10:46
# @File  : http_get_oper.py
# @Author: 
# @Desc  :

from dbgpt._private.pydantic import BaseModel, Field
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator, setup_dev_environment

class TriggerReqBody(BaseModel):
    name: str = Field(..., description="User name")
    age: int = Field(18, description="User age")

with DAG("awel_say_hello") as dag:
    trigger_task = HttpTrigger(
        endpoint="/awel_tutorial/say_hello",
        methods="GET",
        request_body=TriggerReqBody,
        status_code=200
    )
    task = MapOperator(
        map_function=lambda x: f"Hello, {x.name}! You are {x.age} years old."
    )
    trigger_task >> task

setup_dev_environment([dag], port=5555)