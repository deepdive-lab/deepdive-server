"""
프롬프트 파일들을 관리하는 모듈.
FastAPI Lifespan 이벤트에서 load_prompts()를 호출하여 서버 시작 시 한 번만 로드합니다.
"""
from pathlib import Path
from typing import Dict

# 전역 변수로 프롬프트 저장 (서버 시작 시 한 번만 로드됨)
PROMPTS: Dict[str, str] = {}

def load_prompts():
    """
    프롬프트 파일들을 로드하여 전역 변수 PROMPTS에 저장합니다.
    FastAPI lifespan 이벤트에서 서버 시작 시 한 번만 호출됩니다.
    
    Raises:
        FileNotFoundError: 프롬프트 파일을 찾을 수 없을 때
    """
    prompts_dir = Path(__file__).parent / "prompts"
    
    prompt_files = {
        "translator": "translator.md",
        "summarizer": "summarizer.md",
        "enhancer": "enhancer.md",
        "explanator": "explanator.md",
    }
    
    for role, filename in prompt_files.items():
        file_path = prompts_dir / filename
        if file_path.exists():
            PROMPTS[role] = file_path.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError(f"프롬프트 파일을 찾을 수 없습니다: {file_path}")


def get_prompt(role: str) -> str:
    """
    캐싱된 프롬프트를 반환합니다 (File I/O 없음).
    
    Args:
        role: 프롬프트 역할 ("translator", "summarizer", "enhancer", "explanator")
    
    Returns:
        프롬프트 문자열
    
    Raises:
        ValueError: 알 수 없는 role이거나 프롬프트가 로드되지 않았을 때
    """
    if not PROMPTS:
        raise ValueError("프롬프트가 아직 로드되지 않았습니다. load_prompts()를 먼저 호출하세요.")
    
    prompt = PROMPTS.get(role)
    if prompt is None:
        raise ValueError(f"존재하지 않는 role입니다: {role}")
    
    return prompt
