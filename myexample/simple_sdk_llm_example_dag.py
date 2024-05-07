#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2024/5/7 15:50
# @File  : simple_sdk_llm_example_dag.py
# @Author: 
# @Desc  :


from dbgpt.core import BaseOutputParser
from dbgpt.core.awel import DAG
from dbgpt.core.operators import (
    PromptBuilderOperator,
    RequestBuilderOperator
)

from dbgpt.model.proxy import OpenAILLMClient
from dbgpt.model.operators import LLMOperator

with DAG("simple_sdk_llm_example_dag") as dag:
    prompt_task = PromptBuilderOperator(
        "Write a SQL of {dialect} to query all data of {table_name}"
    )

    model_pre_handle_task = RequestBuilderOperator(model="gpt-3.5-turbo")
    llm_task = LLMOperator(OpenAILLMClient())
    out_parse_task = BaseOutputParser()

    print(out_parse_task)

    prompt_task >> model_pre_handle_task >> llm_task >> out_parse_task
