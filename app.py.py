import streamlit as st
import requests
import os  # 新增：用于读取系统环境变量

# 页面配置
st.set_page_config(page_title="山东农产品AI营销文案助手", page_icon="🌾")

st.title("🌾 山东农产品AI营销文案助手")
st.write("输入你的农产品，一键生成小红书/抖音爆款文案！")

st.divider()

product = st.text_input("请输入农产品名称（例如：烟台苹果、章丘大葱）：")
platform = st.selectbox("选择发布平台：", ["小红书", "抖音", "微信视频号", "朋友圈"])

# 核心提示词
system_prompt = f"""
你是一个精通山东本土文化的资深营销专家。
现在你需要为【{product}】写一篇【{platform}】的营销文案。
要求：
1. 必须结合山东地域特色（比如实在、好客、产地优势）。
2. 如果是小红书，语气要活泼，带emoji表情；如果是抖音，要有吸引人的开头，节奏快。
3. 不要用空洞的词汇，要突出卖点，并且字数在300字以内。
"""

if st.button("🚀 一键生成文案"):
    if not product:
        st.warning("请先输入农产品名称！")
    else:
        # 从系统环境变量中获取 API Key
        api_key = os.getenv(DEEPSEEK_API_KEY)
        
        if not api_key:
            st.error("未读取到 API Key！请检查是否在电脑系统环境变量中配置了 DEEPSEEK_API_KEY。")
        else:
            with st.spinner('AI正在思考中...'):
                api_url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"请帮我写一篇关于{product}的营销文案。"}
                    ]
                }
                
                try:
                    response = requests.post(api_url, headers=headers, json=data)
                    result = response.json()
                    
                    if 'choices' in result:
                        ai_text = result['choices'][0]['message']['content']
                        st.success("生成成功！")
                        # 强制呈现可编辑文本框，体现人机协同
                        st.text_area("AI生成的初稿（你可以在这里进行人工修改）：", ai_text, height=300)
                    else:
                        st.error(f"调用失败，请检查 API Key 是否正确或账户余额。错误信息：{result}")
                        
                except Exception as e:
                    st.error(f"网络或代码出错了。错误信息：{e}")
