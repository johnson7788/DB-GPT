"""Indicator Assistant Agent."""

import logging

from ..core.base_agent import ConversableAgent
from ..core.profile import DynConfig, ProfileConfig
from .actions.indicator_action import IndicatorAction

logger = logging.getLogger(__name__)
'''
"优先从改进后的资源文本中总结用户问题的答案。如果找不到相关信息，则从给定的历史对话记忆中进行总结。严禁凭空捏造。"

"您需要首先检测您需要用总结回答的用户问题。"

"提取用于总结的提供的文本内容。"

"然后，您需要总结提取的文本内容。"

"仅输出与用户问题相关的总结内容。输出语言必须与用户问题的语言相同。"

"如果您认为提供的文本内容与用户问题毫不相关，请仅输出 '未找到您想要的信息。'！！"
'''

class IndicatorAssistantAgent(ConversableAgent):
    """Indicator Assistant Agent."""

    profile: ProfileConfig = ProfileConfig(
        name=DynConfig(
            "Indicator",
            category="agent",
            key="dbgpt_agent_expand_indicator_assistant_agent_profile_name",
        ),
        role=DynConfig(
            "Indicator",
            category="agent",
            key="dbgpt_agent_expand_indicator_assistant_agent_profile_role",
        ),
        goal=DynConfig(
            "Summarize answer summaries based on user questions from provided "
            "resource information or from historical conversation memories.",
            category="agent",
            key="dbgpt_agent_expand_indicator_assistant_agent_profile_goal",
        ),
        constraints=DynConfig(
            [
                "Prioritize the summary of answers to user questions from the "
                "improved resource text. If no relevant information is found, "
                "summarize it from the historical dialogue memory given. It is "
                "forbidden to make up your own.",
                "You need to first detect user's question that you need to answer "
                "with your summarization.",
                "Extract the provided text content used for summarization.",
                "Then you need to summarize the extracted text content.",
                "Output the content of summarization ONLY related to user's question. "
                "The output language must be the same to user's question language.",
                "If you think the provided text content is not related to user "
                "questions at all, ONLY output 'Did not find the information you "
                "want.'!!.",
            ],
            category="agent",
            key="dbgpt_agent_expand_indicator_assistant_agent_profile_constraints",
        ),
        desc=DynConfig(
            "You can summarize provided text content according to user's questions "
            "and output the summarization.",
            category="agent",
            key="dbgpt_agent_expand_indicator_assistant_agent_profile_desc",
        ),
    )

    def __init__(self, **kwargs):
        """Create a new instance."""
        super().__init__(**kwargs)
        self._init_actions([IndicatorAction])
