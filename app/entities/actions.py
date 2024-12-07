from enum import Enum


class ActionName(str, Enum):
    FETCH_CONVERSATION_HISTORY = 'FetchConversationHistory'
    PREPARE_PROMPT = 'PreparePrompt'
    CALL_OPENAI = 'CallOpenAI'
    RESPONSE_HAS_FUNCTION_CALL = 'ResponseHasFunctionCall'
    EXECUTE_FUNCTION = 'ExecuteFunction'
    ADD_FUNCTION_RESULT_TO_MESSAGE = 'AddFunctionResultToMessage'
    USE_RESPONSE = 'UseResponse'
    SAVE_CONVERSATION_HISTORY = 'SaveConversationHistory'
