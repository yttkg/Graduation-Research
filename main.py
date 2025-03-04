import sys
import openai
import json

openai.api_key = "OPENAI_API_KEY"

def add_prompt(chat, flag, key):
    if flag == True and key == 0:
        f1 = open('welcome.txt', 'r', encoding='UTF-8') #設定
        prompt = f1.read()
        chat.insert(-1, {'role': 'system', 'content': prompt})
        f1.close()
        print("<追加>", flag)
        flag = False

    return chat, flag

def finish(total_tokens, f):
    print("終了　総トークン：" , total_tokens)
    f.close()
    sys.exit()

functions_list_a = [
    {
        "name": "add_prompt",
        "description": "歓迎会の話題になったら歓迎会についてのプロンプトを追加。",
        "parameters": {
            "type": "object",
            "properties": {
                "chat": {
                    "type": "string",
                    "description": "プロンプトを追加する対象"
                    },
                "flag": {
                    "type": "boolean",
                    "description": "関数が実行されたか判定する、True＝未、False＝済",
                    },
                "key":{
                    "type": "number",
                    "description": "キー"
                }
                },
            }
    }
]
functions_list_b = [
    {
        "name": "add_prompt",
        "description": "歓迎会の話題になったら実行。",
        "parameters": {
            "type": "object",
            "properties": {
                "chat": {
                    "type": "string",
                    "description": "プロンプトを追加する対象"
                    },
                "flag": {
                    "type": "boolean",
                    "description": "関数が実行されたか判定する、True＝未、False＝済",
                    },
                "key":{
                    "type": "number",
                    "description": "キー"
                }
                },
            }
    },
    {
        "name": "finish",
        "description": "歓迎会について話しおわったら実行",
        "parameters": {
            "type": "object",
            "properties": {
                "total_tokens": {
                    "type": "number",
                    "description": "総トークン数"
                    },
                "f":{
                    "type":"string"
                }
                },
            }
    },
]

def main():
    flag = True
    functions_list = functions_list_a
    f = open('sizuka.txt', 'r', encoding='UTF-8') #設定
    situ = f.read()
    total_tokens = 0
    chat = []
    chat.append({'role': 'system', 'content': situ})

    while(True):
        print("ユウキ:", end="")
        user_msg = input()

        if user_msg == "終了":
            print("終了　総トークン：" , total_tokens)
            f.close()
            sys.exit()

        else :
            chat.append({"role": "user", "content":user_msg})
            # 判定
            judge_response = openai.ChatCompletion.create(
                model = 'gpt-3.5-turbo',
                messages = chat,
                functions = functions_list,
                function_call = 'auto',
                temperature = 0.1
            )
            judge_msg = judge_response["choices"][0]["message"]
            # print(judge_msg)
            # 関数を実行するか確認
            if judge_msg.get("function_call"):
                function_name = judge_msg["function_call"]["name"]
                arguments = json.loads(judge_msg["function_call"]["arguments"])
                # print(arguments)
                if function_name == "add_prompt":
                    chat, flag = add_prompt(chat, flag, 0)
                    functions_list = functions_list_b
                elif function_name  == "finish":
                    finish(total_tokens, f)
            # 会話
            chat_response = openai.ChatCompletion.create(
                model='gpt-4',
                messages=chat,
                #temperature=1.5,
                #max_tokens=50
            )
            gpt_msg = chat_response["choices"][0]["message"]["content"]    #返答
            gpt_token = chat_response["usage"]["total_tokens"]       #トークン数
            total_tokens += gpt_token
            print("シズカ:" + gpt_msg)

            chat.append({"role": "assistant", "content": gpt_msg})
            # 判定
            judge_response = openai.ChatCompletion.create(
                model = 'gpt-4',
                messages = chat,
                functions = functions_list,
                function_call = 'auto',
                temperature = 0.5
            )
            judge_msg = judge_response["choices"][0]["message"]
            # print(judge_msg)
            # 関数を実行するか確認
            if judge_msg.get("function_call"):
                function_name = judge_msg["function_call"]["name"]
                arguments = json.loads(judge_msg["function_call"]["arguments"])
                # print(arguments)
                if function_name == "add_prompt":
                    chat, flag = add_prompt(chat, flag, 1)
                elif function_name  == "finish":
                    finish(total_tokens, f)
            #chat.append({"role": "assistant", "content": gpt_msg})

if __name__ == "__main__":
    main()
