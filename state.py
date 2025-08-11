from typing_extensions import TypedDict
from typing import List

class ConversationState(TypedDict):
    messages: List[str]