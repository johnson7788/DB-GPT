"""Agents: auto plan agents example?

    Examples:
     
        Execute the following command in the terminal:
        Set env params.
        .. code-block:: shell

            export OPENAI_API_KEY=sk-xx
            export OPENAI_API_BASE=https://xx:80/v1

        run example.
        ..code-block:: shell
            python examples/agents/auto_plan_agent_dialogue_example.py 
"""

import asyncio

from dbgpt.agent import (
    AgentContext,
    AgentMemory,
    AutoPlanChatManager,
    LLMConfig,
    UserProxyAgent,
)
from dbgpt.agent.expand.code_assistant_agent import CodeAssistantAgent
from dbgpt.util.tracer import initialize_tracer

initialize_tracer(
    "/tmp/agent_auto_plan_agent_dialogue_example_trace.jsonl", create_system_app=True
)


async def main():
    from dbgpt.model.proxy import OpenAILLMClient

    agent_memory = AgentMemory()

<<<<<<< HEAD
    llm_client = OpenAILLMClient(model_alias="gpt-3.5-turbo")
=======
    llm_client = OpenAILLMClient(model_alias="gpt-4o")
>>>>>>> main
    context: AgentContext = AgentContext(
        conv_id="test456", gpts_app_name="代码分析助手", max_new_tokens=2048
    )

    coder = (
        await CodeAssistantAgent()
        .bind(context)
        .bind(LLMConfig(llm_client=llm_client))
        .bind(agent_memory)
        .build()
    )

    manager = (
        await AutoPlanChatManager()
        .bind(context)
        .bind(agent_memory)
        .bind(LLMConfig(llm_client=llm_client))
        .build()
    )
    manager.hire([coder])

    user_proxy = await UserProxyAgent().bind(context).bind(agent_memory).build()
    # team manager 先设立计划, 然后按计划分步执行，执行后summary
    await user_proxy.initiate_chat(
        recipient=manager,
        reviewer=user_proxy,
        message="Obtain simple information about issues in the repository 'eosphoros-ai/DB-GPT' in the past three days and analyze the data. Create a Markdown table grouped by day and status.",
        # message="Find papers on gpt-4 in the past three weeks on arxiv, and organize their titles, authors, and links into a markdown table",
        # message="find papers on LLM applications from arxiv in the last month, create a markdown table of different domains.",
    )

    print(await agent_memory.gpts_memory.one_chat_completions("test456"))


if __name__ == "__main__":
    ## dbgpt-vis message infos
    asyncio.run(main())

'''
--------------------------------------------------------------------------------
User (to AutoPlanChatManager)-[]:
"Obtain simple information about issues in the repository 'eosphoros-ai/DB-GPT' in the past three days and analyze the data. Create a Markdown table grouped by day and status."
--------------------------------------------------------------------------------
un_stream ai response: [
  {
    "serial_number": "1",
    "agent": "CodeEngineer",
    "content": "Write and execute a Python script to use GitHub API to retrieve issues from the 'eosphoros-ai/DB-GPT' repository created in the past three days. The data should include issue title, creation date, and status (open/closed).",
    "rely": ""
  },
  {
    "serial_number": "2",
    "agent": "CodeEngineer",
    "content": "Analyze the retrieved issues data to group them by creation date and status. For each group, count the number of issues.",
    "rely": "1"
  },
  {
    "serial_number": "3",
    "agent": "CodeEngineer",
    "content": "Create a Markdown table summarizing the grouped issue data by day and status, including columns for Date, Status, and Count.",
    "rely": "2"
  }
]
--------------------------------------------------------------------------------
Planner (to AutoPlanChatManager)-[gpt-4]:
"[\n  {\n    \"serial_number\": \"1\",\n    \"agent\": \"CodeEngineer\",\n    \"content\": \"Write and execute a Python script to use GitHub API to retrieve issues from the 'eosphoros-ai/DB-GPT' repository created in the past three days. The data should include issue title, creation date, and status (open/closed).\",\n    \"rely\": \"\"\n  },\n  {\n    \"serial_number\": \"2\",\n    \"agent\": \"CodeEngineer\",\n    \"content\": \"Analyze the retrieved issues data to group them by creation date and status. For each group, count the number of issues.\",\n    \"rely\": \"1\"\n  },\n  {\n    \"serial_number\": \"3\",\n    \"agent\": \"CodeEngineer\",\n    \"content\": \"Create a Markdown table summarizing the grouped issue data by day and status, including columns for Date, Status, and Count.\",\n    \"rely\": \"2\"\n  }\n]"
>>>>>>>>Planner Review info: 
Pass(None)
>>>>>>>>Planner Action report: 
execution succeeded,
[
  {
    "serial_number": "1",
    "agent": "CodeEngineer",
    "content": "Write and execute a Python script to use GitHub API to retrieve issues from the 'eosphoros-ai/DB-GPT' repository created in the past three days. The data should include issue title, creation date, and status (open/closed).",
    "rely": ""
  },
  {
    "serial_number": "2",
    "agent": "CodeEngineer",
    "content": "Analyze the retrieved issues data to group them by creation date and status. For each group, count the number of issues.",
    "rely": "1"
  },
  {
    "serial_number": "3",
    "agent": "CodeEngineer",
    "content": "Create a Markdown table summarizing the grouped issue data by day and status, including columns for Date, Status, and Count.",
    "rely": "2"
  }
]
--------------------------------------------------------------------------------
GroupChat select_speaker failed to resolve the next speaker's name. This is because the speaker selection OAI call returned:
CodeEngineer
--------------------------------------------------------------------------------
AutoPlanChatManager (to Turing)-[]:
"Write and execute a Python script to use GitHub API to retrieve issues from the 'eosphoros-ai/DB-GPT' repository created in the past three days. The data should include issue title, creation date, and status (open/closed)."
--------------------------------------------------------------------------------
un_stream ai response: ```python
# filename: github_issues.py
import requests
from datetime import datetime, timedelta
# GitHub repository to query
owner = 'eosphoros-ai'
repo = 'DB-GPT'
# Calculate the date 3 days ago from today
date_since = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%SZ')
# GitHub API URL for issues
url = f'https://api.github.com/repos/{owner}/{repo}/issues?since={date_since}'
# Make a request to the GitHub API
response = requests.get(url)
issues = response.json()
# Check if issues were found
if issues:
    for issue in issues:
        # Extracting the necessary information
        title = issue['title']
        created_at = issue['created_at']
        state = issue['state']
        print(f'Title: {title}, Created At: {created_at}, State: {state}')
else:
    print('No issues found created in the past 3 days.')
```
This script will contact the GitHub API to retrieve issues from the specified repository that were created in the past three days. It will print the title, creation date, and status (open/closed) of each issue found.
>>>>>>>> EXECUTING CODE BLOCK 0 (inferred language is python)...
execute_code was called without specifying a value for use_docker. Since the python docker package is not available, code will be run natively. Note: this fallback behavior is subject to change
un_stream ai response: False. The execution results include issues created outside the specified time range of the past three days.
--------------------------------------------------------------------------------
Turing (to AutoPlanChatManager)-[gpt-4]:
"```python\n# filename: github_issues.py\nimport requests\nfrom datetime import datetime, timedelta\n\n# GitHub repository to query\nowner = 'eosphoros-ai'\nrepo = 'DB-GPT'\n# Calculate the date 3 days ago from today\ndate_since = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%SZ')\n\n# GitHub API URL for issues\nurl = f'https://api.github.com/repos/{owner}/{repo}/issues?since={date_since}'\n\n# Make a request to the GitHub API\nresponse = requests.get(url)\nissues = response.json()\n\n# Check if issues were found\nif issues:\n    for issue in issues:\n        # Extracting the necessary information\n        title = issue['title']\n        created_at = issue['created_at']\n        state = issue['state']\n        print(f'Title: {title}, Created At: {created_at}, State: {state}')\nelse:\n    print('No issues found created in the past 3 days.')\n```\n\nThis script will contact the GitHub API to retrieve issues from the specified repository that were created in the past three days. It will print the title, creation date, and status (open/closed) of each issue found."
>>>>>>>>Turing Review info: 
Pass(None)
>>>>>>>>Turing Action report: 
execution succeeded,
Title:  Is Qwen1.5-14B-Chat-GPTQ-Int4 not supported now?, Created At: 2024-05-11T03:23:24Z, State: open
Title: What is the relationship between the two projects DB-GPT and DB-GPT-HUB?, Created At: 2024-05-11T00:45:03Z, State: open
Title: When creating an APP, where can I find the required app_id?, Created At: 2024-05-10T09:16:32Z, State: open
Title: feat: add GraphRAG framework and integrate TuGraph, Created At: 2024-05-09T11:18:49Z, State: open
Title: [New Feature] ES VectorStore, Created At: 2024-05-08T16:31:20Z, State: open
Title:     if tokenizer.eos_token_id not in stop_token_ids: AttributeError: 'NoneType' object has no attribute 'eos_token_id', Created At: 2024-05-08T12:00:51Z, State: open
Title:  Expected all tensors to be on the same device, but found at least two devices, cpu and cuda:0! (when checking argument for argument mat2 in method wrapper_CUDA_addmm, Created At: 2024-04-22T08:56:41Z, State: open
Title: [Bug] [Module Name]  Automatically rewrite and continuously loop answers, Created At: 2024-04-15T09:06:42Z, State: open
Title: how to connect the knowledge, Created At: 2024-04-11T03:43:00Z, State: open
Title: [Bug] [chat_dashboard] Used all tables ddl as context to anwser question, Created At: 2024-04-10T10:54:19Z, State: open
Title: Customized an operator, how to display it on the interface, Created At: 2024-04-10T10:15:03Z, State: open
Title: [Bug]I connected my own db, why is the chat DB the default three tables?, Created At: 2024-04-10T09:04:13Z, State: open
Title: how to write AWEL when i should use HttpTrigger then i want to use branchOperator with it., Created At: 2024-04-10T06:54:09Z, State: open
Title: [Bug] [remote_worker] When using model-controller as the cluster mode, all models will be requested once when conducting knowledge base Q&A through the web., Created At: 2024-04-10T03:57:27Z, State: open
Title: [Bug] LLMServer Generate Error, Please CheckErrorInfo.: CUDA error, Created At: 2024-04-10T03:12:34Z, State: open
Title: [Bug] [datasource] Unable to modify database table structure after executing query, Created At: 2024-04-09T03:18:41Z, State: open

'''