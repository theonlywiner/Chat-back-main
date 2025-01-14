from zhipuai import ZhipuAI
import time

class ZhiPu():
    def __init__(self, api_key, model_index):
        self.model_map = {
            1: "GLM-4-0520",
            2: "GLM-4-Plus",
            3: "GLM-4-Air",
            4: "glm-4v-plus",
            5: "glm-4v",
        }
        self.api_key = api_key
        self.index = model_index

    def zhipuai_chat(self, question, enable_tool=False):
        print("此次使用的模型是{}".format(self.model_map[self.index]))

        tools = [{
            "type": "web_search",
            "web_search": {
                "enable": enable_tool,  # 禁用：False，启用：True。
                "search_query": "自定义搜索的关键词"
            }
        }] if enable_tool else None

        try:
            client = ZhipuAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model_map[self.index],
                messages=[
                    {"role": "user", "content": question},
                ],
                stream=False,
                tools=tools,
                timeout=15  # 添加10秒超时
            )
            return response
        except Exception as e:
            print(f"API调用错误: {str(e)}")
            return None

if __name__ == "__main__":
    api_key = "c94b92b94a1d46db867ef57d77187c89.ZlF2AlE53yfMd8Pv"  # 替换为你的API Key
    question = "帮忙给这句话解析人之初，性本善"

    start = time.time()  # 注意：strat 应该是 start

    zhipu_instance = ZhiPu(api_key, 1)
    zhipu_instance.zhipuai_chat(question, enable_tool=False)  # 启用工具
    end = time.time()

    print(f"此次调用花费时间为：{(end - start):.4f}秒")
