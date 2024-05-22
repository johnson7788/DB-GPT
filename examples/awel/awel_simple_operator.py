#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/16 13:59
# @File  : awel_simple_operator.py
# @Author: 
# @Desc  : """awel-simple-operator operator package"""
import asyncio
from dbgpt.core.awel import MapOperator, DAG
from dbgpt.core.awel.flow import ViewMetadata, OperatorCategory, IOField, Parameter


class SimpleHelloWorldOperator(MapOperator[str, str]):
    # The metadata for AWEL flow
    metadata = ViewMetadata(
        label="Simple Hello World Operator",
        name="simple_hello_world_operator",
        category=OperatorCategory.COMMON,
        description="A example operator to say hello to someone.",
        parameters=[
            Parameter.build_from(
                "Name",
                "name",
                str,
                optional=True,
                default="World",
                description="The name to say hello",
            )
        ],
        inputs=[
            IOField.build_from(
                "Input value",
                "value",
                str,
                description="The input value to say hello",
            )
        ],
        outputs=[
            IOField.build_from(
                "Output value",
                "value",
                str,
                description="The output value after saying hello",
            )
        ]
    )

    def __init__(self, name: str = "World", **kwargs):
        super().__init__(**kwargs)
        self.name = name

    async def map(self, value: str) -> str:
        return f"Hello, {self.name}! {value}"

if __name__ == '__main__':
    with DAG("awel_hello_world") as dag:
        task = SimpleHelloWorldOperator()
    result = asyncio.run(task.call(call_data="world"))
    print(result)
