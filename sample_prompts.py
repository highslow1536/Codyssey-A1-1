"""시연용 기본 프롬프트. 제출 전 자신의 이전 미션 프롬프트로 교체하세요."""


def load_sample_prompts():
    return [
        {
            "title": "블로그 글 작성 도우미",
            "content": "당신은 전문 블로거입니다. 주어진 주제로 서론, 본론, 결론을 갖춘 글과 제목 3개를 작성해주세요.",
            "category": "텍스트 생성",
            "favorite": False,
        },
        {
            "title": "제품 썸네일 이미지",
            "content": "제품의 특징을 살린 선명한 썸네일 이미지를 위한 프롬프트를 작성해주세요. 배경과 조명을 구체적으로 설명해주세요.",
            "category": "이미지 생성",
            "favorite": False,
        },
        {
            "title": "친절한 학습 코치",
            "content": "당신은 친절한 학습 코치입니다. 어려운 개념을 쉬운 예시와 단계별 설명으로 알려주세요.",
            "category": "페르소나",
            "favorite": False,
        },
    ]
