#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/14 10:31
# @File  : unstreamify_ope.py
# @Author: 
# @Desc  :

import asyncio
from typing import AsyncIterator
from dbgpt.core.awel import DAG, UnstreamifyAbsOperator, StreamifyAbsOperator

class NumberProducerOperator(StreamifyAbsOperator[int, int]):
    """Create a stream of numbers from 0 to `n-1`"""
    async def streamify(self, n: int) -> AsyncIterator[int]:
        for i in range(n):
            yield i

class SumOperator(UnstreamifyAbsOperator[int, int]):
    """Unstreamify the stream of numbers"""
    async def unstreamify(self, it: AsyncIterator[int]) -> int:
        return sum([i async for i in it])

with DAG("sum_dag") as dag:
    task = NumberProducerOperator()
    sum_task = SumOperator()
    task >> sum_task

print(asyncio.run(sum_task.call(call_data=5)))
print(asyncio.run(sum_task.call(call_data=10)))