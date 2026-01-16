from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from graph.prompts import get_prompt

def build_llm_input(content: str, role: str):
    input : list[BaseMessage] = []

    # 메모리에서 캐싱된 프롬프트 가져오기 (File I/O 없음)
    prompt_content = get_prompt(role)
    input.append(SystemMessage(content=prompt_content))

    input.append(HumanMessage(content=f"""
<article>
{content}
</article>
"""))
    return input