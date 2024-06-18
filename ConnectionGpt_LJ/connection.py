import json
import openai
import os

# 현재 스크립트의 경로
current_directory = os.path.dirname(__file__)

# conversation.json 상대경로
relative_path = "conversationData/conversation.json"
# 절대경로 변환
absolute_path = os.path.join(current_directory, relative_path)

# OpenAI API 키 설정
openai.api_key = "sk-proj-3ZLbBHwylhtASxE4BIaMT3BlbkFJh6cUB6QhPVKBieezTqSg"
# 이전 대화 결과 초기화
previous_completion = None

# 전체 대화 내용 저장용 리스트
conversation = []

# 현재 대화 내용 저장용 리스트 파일이 초기화 되도록 설계
communication_ = []

# communication.json 파일 읽고 덮어쓰기
def read_comm_file(question, response):
    commu = {"user_ment": question, "gpt_ment": response}
    communication_path = os.path.join(current_directory, "conversationData", "communication.json")

    # communication.json 파일을 저장할 폴더가 없을 경우 폴더를 생성합니다.
    if not os.path.exists(os.path.dirname(communication_path)):
        os.makedirs(os.path.dirname(communication_path))

    # 파일이 존재하지 않는 경우 새로운 파일을 생성하여 데이터를 저장
    if not os.path.exists(communication_path):
        communication_.append(commu)
        with open(communication_path, 'w') as f:
            json.dump(communication_, f, indent=4)
    else:
        # 파일이 존재하는 경우 기존 파일을 열어서 데이터를 읽고 덮어쓰기
        communication_.append(commu)
        with open(communication_path, 'r') as f:
            current_communication = json.load(f)
        current_communication.append(commu)
        with open(communication_path, 'w') as f:
            json.dump(current_communication, f, indent=4)

# gpt 대화
while (True):
    question = input("user: ")

    # 이전 대화 결과를 다음 대화의 입력으로 사용
    messages = [{"role": "user", "content": question}]
    if previous_completion:
        messages.append({"role": "assistant", "content": previous_completion.choices[0].message.content})

    # OpenAI API를 사용하여 대화 생성 요청 보내기
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",  # 사용할 모델
        messages=messages
    )
    response = completion.choices[0].message.content.strip()
    print("gpt:", response)

    previous_completion = completion

    # 대화 내용을 전체파일로 저장할때 사용 parameter 값 추가될 예정.
    message = {"data": 
               {"user_ment": question,
                 "gpt_ment": response}
                 }

    read_comm_file(question, response)
    
    conversation.append("{data}")
    conversation.append(message)

    # 대화 종료 이벤트
    if question.lower() == "close":
        break

# 전체 대화 내용 json파일 저장
with open(absolute_path, 'w', encoding='UTF-8') as file:
    json.dump(conversation, file, ensure_ascii=False, indent=4)


# 1. parameter値が全体的に入る: Parameter.json
# 2. quesとrespだけが入る: Conversation.json


# 全体的なロジック
# 1.ユーザーがプロンプト入力
# 2. プロンプト値jsonに保存 -> ユニティで
# 3. Pythonでjsonファイルを読み、ユーザーが入力したプロンプト値のキー値を読む
# 4.読んだキー値を変数に保存してから飛ばす
# 5. 飛んでくる時、すべてのパラメータ値の変更と、答えを持ってくる
# 6。 データ定在
# 6.1 飛んできたデータからパラメータ値を除いた答案を別途のjsonファイルに保存
# 6.2 先に飛んできたquestionを別のjsonに入れて responseだけまた別のjsonに入れて
# 6.3 ユニティに返還
# ユニティでゲームが終了したり、ゲームを保存または四半期が終わった時、すべてのプロンプト値が含まれたjsonファイルをユニティに渡す
# ユニティでdb管理
# ゲームが再起動すると、全体的なパラメータおよびデータが入ったjsonファイルを渡すメソッドを開始。


# 作成方法リスト
# parameter読み書き関数、conversation読み書き、データ定在関数