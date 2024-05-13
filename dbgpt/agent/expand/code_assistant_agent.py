"""Code Assistant Agent."""

from typing import Optional, Tuple

from dbgpt.core import ModelMessageRoleType
from dbgpt.util.string_utils import str_to_bool

from ..core.agent import AgentMessage
from ..core.base_agent import ConversableAgent
from ..core.profile import DynConfig, ProfileConfig
from .actions.code_action import CodeAction

"""
你是任务执行结果分析的专家。你的责任是分析用户提供的任务目标和执行结果，然后做出判断。你需要按照以下规则回答：

规则 1：确定聚焦执行结果的内容是否与任务目标内容相关，并且是否可用作目标问题的答案。对于不理解内容的人来说，只要需要执行结果类型，就可以判断为正确。

规则 2：不需要注意答案内容的边界、时间范围和值是否正确。

只要任务目标和执行结果符合以上规则，就会返回 True；否则，将返回 False，并提供失败原因。

例如：

如果判断为成功，只会返回 true，例如：True。

如果判断为失败，返回 false 和原因，例如：False。执行结果中没有回答任务的计算目标的数字。

你可以参考以下示例：

用户：请理解以下任务目标和结果，并给出你的判断：
任务目标：使用 Python 代码计算 1 + 2 的结果。
执行结果：3
助手：True

用户：请理解以下任务目标和结果，并给出你的判断：
任务目标：使用 Python 代码计算 100 * 10 的结果。
执行结果：“你可以通过将 100 乘以 10 来获得结果”
助手：False。执行结果中没有回答任务计算目标的数字。
"""

CHECK_RESULT_SYSTEM_MESSAGE = (
    "You are an expert in analyzing the results of task execution. Your responsibility "
    "is to analyze the task goals and execution results provided by the user, and "
    "then make a judgment. You need to answer according to the following rules:\n"
    "          Rule 1: Determine whether the content of the focused execution results "
    "is related to the task target content and whether it can be used as the answer to "
    "the target question. For those who do not understand the content, as long as the "
    "execution result type is required, it can be judged as correct.\n"
    "          Rule 2: There is no need to pay attention to whether the boundaries, "
    "time range, and values of the answer content are correct.\n"
    "As long as the task goal and execution result meet the above rules, True will be "
    "returned; otherwise, False will be returned and the failure reason will be given."
    "\nFor example:\n"
    "        If it is determined to be successful, only true will be returned, "
    "such as: True.\n"
    "        If it is determined to be a failure, return false and the reason, "
    "such as: False. There are no numbers in the execution results that answer the "
    "computational goals of the mission.\n"
    "You can refer to the following examples:\n"
    "user: Please understand the following task objectives and results and give your "
    "judgment:\nTask goal: Calculate the result of 1 + 2 using Python code.\n"
    "Execution Result: 3\n"
    "assistant: True\n\n"
    "user: Please understand the following task objectives and results and give your "
    "judgment:\nTask goal: Calculate the result of 100 * 10 using Python code.\n"
    "Execution Result: 'you can get the result by multiplying 100 by 10'\n"
    "assistant: False. There are no numbers in the execution results that answer the "
    "computational goals of the mission.\n"
)

"""
goal:
使用你的编码和语言技能解决任务。
在以下情况下，建议用户执行 Python 代码（在 Python 代码块中）或 shell 脚本（在 sh 代码块中）。

当你需要收集信息时，请使用代码输出所需的信息，例如浏览或搜索网页，下载/读取文件，打印网页或文件的内容，获取当前日期/时间，检查操作系统。在打印了足够的信息并且基于你的语言技能准备好解决任务后，你可以自行解决任务。
当你需要使用代码执行某些任务时，请使用代码执行任务并输出结果。聪明地完成任务。

限制：
用户不能提供除执行你建议的代码之外的任何其他反馈或执行其他操作。用户不能修改你的代码。因此，请不要建议需要用户修改的不完整代码。如果不打算由用户执行，请不要使用代码块。不要要求用户复制粘贴结果。相反，当相关时必须使用 'Print' 函数进行输出。
使用代码时，必须在代码块中指明脚本类型。请不要在一个回复中包含多个代码块。
如果希望用户在执行代码之前将代码保存到文件中，请在代码块的第一行放置 # filename: <filename>。
如果收到用户输入表明代码执行中存在错误，请修复错误并重新输出完整代码。建议使用完整的代码而不是部分代码或代码更改。如果错误无法修复，或者即使代码成功执行后任务仍未解决，请分析问题，重新审视假设，从历史对话记录中收集所需的附加信息，并考虑尝试不同的方法。
除非必要，应优先使用 Python 代码解决问题。如果涉及下载文件或本地存储数据，请使用 'Print' 输出存储数据的完整文件路径和数据的简要介绍。
'print' 函数的输出内容将作为依赖数据传递给其他 LLM 代理。请控制 'print' 函数输出内容的长度。'print' 函数只输出依赖数据信息的一部分，并尽可能简洁。
代码在没有用户参与的情况下执行。禁止使用会阻塞进程或需要关闭的方法，例如 matplotlib.pyplot 的 plt.show() 方法。
禁止虚构不存在的数据以实现目标。
"""

class CodeAssistantAgent(ConversableAgent):
    """Code Assistant Agent."""

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig(
            "Turing",
            category="agent",
            key="dbgpt_agent_expand_code_assistant_agent_profile_name",
        ),
        role=DynConfig(
            "CodeEngineer",
            category="agent",
            key="dbgpt_agent_expand_code_assistant_agent_profile_role",
        ),
        goal=DynConfig(
            "Solve tasks using your coding and language skills.\n"
            "In the following cases, suggest python code (in a python coding block) or "
            "shell script (in a sh coding block) for the user to execute.\n"
            "    1. When you need to collect info, use the code to output the info you "
            "need, for example, browse or search the web, download/read a file, print "
            "the content of a webpage or a file, get the current date/time, check the "
            "operating system. After sufficient info is printed and the task is ready "
            "to be solved based on your language skill, you can solve the task by "
            "yourself.\n"
            "    2. When you need to perform some task with code, use the code to "
            "perform the task and output the result. Finish the task smartly.",
            category="agent",
            key="dbgpt_agent_expand_code_assistant_agent_profile_goal",
        ),
        constraints=DynConfig(
            [
                "The user cannot provide any other feedback or perform any other "
                "action beyond executing the code you suggest. The user can't modify "
                "your code. So do not suggest incomplete code which requires users to "
                "modify. Don't use a code block if it's not intended to be executed "
                "by the user.Don't ask users to copy and paste results. Instead, "
                "the 'Print' function must be used for output when relevant.",
                "When using code, you must indicate the script type in the code block. "
                "Please don't include multiple code blocks in one response.",
                "If you want the user to save the code in a file before executing it, "
                "put # filename: <filename> inside the code block as the first line.",
                "If you receive user input that indicates an error in the code "
                "execution, fix the error and output the complete code again. It is "
                "recommended to use the complete code rather than partial code or "
                "code changes. If the error cannot be fixed, or the task is not "
                "resolved even after the code executes successfully, analyze the "
                "problem, revisit your assumptions, gather additional information you "
                "need from historical conversation records, and consider trying a "
                "different approach.",
                "Unless necessary, give priority to solving problems with python "
                "code. If it involves downloading files or storing data locally, "
                "please use 'Print' to output the full file path of the stored data "
                "and a brief introduction to the data.",
                "The output content of the 'print' function will be passed to other "
                "LLM agents as dependent data. Please control the length of the "
                "output content of the 'print' function. The 'print' function only "
                "outputs part of the key data information that is relied on, "
                "and is as concise as possible.",
                "The code is executed without user participation. It is forbidden to "
                "use methods that will block the process or need to be shut down, "
                "such as the plt.show() method of matplotlib.pyplot as plt.",
                "It is prohibited to fabricate non-existent data to achieve goals.",
            ],
            category="agent",
            key="dbgpt_agent_expand_code_assistant_agent_profile_constraints",
        ),
        desc=DynConfig(
            "Can independently write and execute python/shell code to solve various"
            " problems",
            category="agent",
            key="dbgpt_agent_expand_code_assistant_agent_profile_desc",
        ),
    )

    def __init__(self, **kwargs):
        """Create a new CodeAssistantAgent instance."""
        super().__init__(**kwargs)
        self._init_actions([CodeAction])

    async def correctness_check(
        self, message: AgentMessage
    ) -> Tuple[bool, Optional[str]]:
        """Verify whether the current execution results meet the target expectations."""
        task_goal = message.current_goal
        action_report = message.action_report
        task_result = ""
        if action_report:
            task_result = action_report.get("content", "")

        check_result, model = await self.thinking(
            messages=[
                AgentMessage(
                    role=ModelMessageRoleType.HUMAN,
                    content="Please understand the following task objectives and "
                    f"results and give your judgment:\n"
                    f"Task goal: {task_goal}\n"
                    f"Execution Result: {task_result}",
                )
            ],
            prompt=CHECK_RESULT_SYSTEM_MESSAGE,
        )
        success = str_to_bool(check_result)
        fail_reason = None
        if not success:
            fail_reason = (
                f"Your answer was successfully executed by the agent, but "
                f"the goal cannot be completed yet. Please regenerate based on the "
                f"failure reason:{check_result}"
            )
        return success, fail_reason
