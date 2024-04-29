import json
import openai
import os
import random

# OpenAI API 키 설정
api_key = 'sk-proj-bCN28oQJRiUTZa8JfkO7T3BlbkFJ1y2CwHyX16gC7zj4Q3Gb'
openai.api_key = api_key

# 대화 기록을 저장할 경로
communication_path = os.path.join("conversationData", "communication.json")
update_status_path = os.path.join("conversationData", "update_status.json")

def save_to_json(data, file_path):
    """주어진 데이터를 JSON 파일에 저장합니다."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_conversation(user_ment, gpt_ment, file_path):
    """대화를 JSON 파일에 저장합니다."""
    with open(file_path, 'a', encoding='utf-8') as f:
        conversation = {"user_ment": user_ment, "gpt_ment": gpt_ment}
        json.dump(conversation, f, ensure_ascii=False)
        f.write('\n')  # 한 줄씩 저장하기 위해 줄 바꿈 문자 추가

def update_status(daughter_status_data, gpt_reply):
    """대화 응답에 따라 상태를 업데이트하고 update_status.json에 저장합니다."""
    # mood, moral_evaluation, stress, fatigue를 대화에 따라 랜덤하게 업데이트
    daughter_status_data["mood"] = random.choice(["happy", "sad", "angry", "depression"])
    daughter_status_data["moral_evaluation"] = random.randint(0, 100)
    daughter_status_data["stress"] = f"{random.randint(0, 100)}%"
    daughter_status_data["fatigue"] = f"{random.randint(0, 100)}%"

    # 수치 값을 순서대로 업데이트
    daughter_status_data["E"] = f"{random.randint(0, 100)}%"
    daughter_status_data["I"] = f"{100 - int(daughter_status_data['E'][:-1])}%"
    daughter_status_data["S"] = f"{random.randint(0, 100)}%"
    daughter_status_data["N"] = f"{100 - int(daughter_status_data['S'][:-1])}%"
    daughter_status_data["T"] = f"{random.randint(0, 100)}%"
    daughter_status_data["F"] = f"{100 - int(daughter_status_data['T'][:-1])}%"
    daughter_status_data["J"] = f"{random.randint(0, 100)}%"
    daughter_status_data["P"] = f"{100 - int(daughter_status_data['J'][:-1])}%"

    # daughter_status를 JSON 파일에 추가로 저장
    save_to_json(daughter_status_data, update_status_path)

def train_ai(daughter_status, user_ment, dad_ment):
    """AI를 훈련하고 응답을 반환합니다."""
    # 대화 메시지 생성
    messages = [
        {"role": "user", "content": user_ment},
        {"role": "assistant", "content": dad_ment}
    ]

    # AI 훈련
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )

    # 결과 출력
    gpt_reply = response['choices'][0]['message']['content']
    print("AI 대답:", gpt_reply)

    # 대화 기록
    save_conversation(user_ment, gpt_reply, communication_path)
    
    # 상태 업데이트
    update_status(daughter_status, gpt_reply)

    return gpt_reply

def show_status_update(daughter_status_data):
    """수치 변화를 보여줍니다."""
    print("Daughter Status Update:")
    for key, value in daughter_status_data.items():
        if key != "daughter":
            print(f"{key}: {value}")

def main():
    # 초기 상태 설정
    daughter_status_data = {
        "daughter": {
            "name": "더조은",
            "age": "20",
            "sex": "female",
            "mbti": "ISFJ",
            "hp": 70,
            "mp": 80,
            "mood": "happiness",
            "stress": "low",
            "fatigue": "energetic",
            "E": 50,
            "I": 50,
            "S": 50,
            "N": 50,
            "T": 50,
            "F": 50,
            "J": 50,
            "P": 50
        }
    }

    # 대화 테스트
    user_ment = "오늘은 행복한 날이다."
    dad_ment = "그래, 오늘 정말 기분이 좋아 보이는구나!"
    train_ai(daughter_status_data, user_ment, dad_ment)
    show_status_update(daughter_status_data)

if __name__ == "__main__":
    main()
