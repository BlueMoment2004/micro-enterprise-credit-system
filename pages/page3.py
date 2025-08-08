import streamlit as st
import openai
import requests
import json
from datetime import datetime

# 设置页面标题
st.title("🤖 AI智能助手")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    # 选择AI提供商
    provider = st.selectbox(
        "选择AI提供商",
        ["OpenAI", "DeepSeek"],
        index=0
    )
    
    # API密钥输入
    if provider == "OpenAI":
        api_key = st.text_input(
            "OpenAI API Key", 
            type="password",
            help="请输入您的OpenAI API密钥"
        )
        base_url = "https://api.openai.com/v1"
    else:  # DeepSeek
        api_key = st.text_input(
            "DeepSeek API Key", 
            type="password",
            help="请输入您的DeepSeek API密钥"
        )
        base_url = "https://api.deepseek.com/v1"
    
    # 模型选择
    if provider == "OpenAI":
        model = st.selectbox(
            "选择OpenAI模型",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
            index=0
        )
    else:  # DeepSeek
        model = st.selectbox(
            "选择DeepSeek模型",
            ["deepseek-chat", "deepseek-coder"],
            index=0
        )
    
    # 温度设置
    temperature = st.slider(
        "创造性 (Temperature)", 
        min_value=0.0, 
        max_value=2.0, 
        value=0.7, 
        step=0.1,
        help="控制回答的创造性，0=保守，2=非常创造性"
    )
    
    # 清除聊天记录
    if st.button("🗑️ 清除聊天记录"):
        st.session_state.messages = []
        st.rerun()

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 检查API密钥
    if not api_key:
        st.error("⚠️ 请在侧边栏输入OpenAI API密钥")
        st.stop()
    
    # 添加用户消息到聊天历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 显示AI正在思考
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 正在思考...")
        
        try:
            # 构建消息列表
            messages = [
                {"role": "system", "content": "你是一个专业的小微企业信贷风险评估助手。请根据用户的问题提供准确、专业的回答。"}
            ]
            messages.extend(st.session_state.messages)
            
            if provider == "OpenAI":
                # 使用OpenAI API
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    stream=True
                )
                
                # 流式显示回答
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
            else:  # DeepSeek
                # 使用DeepSeek API
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "stream": True
                }
                
                # 发送请求
                response = requests.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    stream=True
                )
                
                if response.status_code != 200:
                    raise Exception(f"API请求失败: {response.status_code} - {response.text}")
                
                # 流式显示回答
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data_str = line[6:]  # 移除 'data: ' 前缀
                            if data_str == '[DONE]':
                                break
                            try:
                                chunk_data = json.loads(data_str)
                                if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                    delta = chunk_data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        full_response += delta['content']
                                        message_placeholder.markdown(full_response + "▌")
                            except json.JSONDecodeError:
                                continue
            
            # 显示完整回答
            message_placeholder.markdown(full_response)
            
            # 添加AI回答到聊天历史
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"❌ 发生错误: {str(e)}")
            # 从聊天历史中移除用户消息
            st.session_state.messages.pop()

# 页面底部信息
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("💡 提示：您可以询问关于小微企业信贷评估的问题")
with col2:
    st.info("🔒 您的API密钥仅用于本次会话，不会被保存")
with col3:
    st.info("🤖 支持OpenAI和DeepSeek两种AI模型")

# DeepSeek API密钥获取说明
if provider == "DeepSeek":
    st.markdown("---")
    st.info("""
    **🔑 DeepSeek API密钥获取步骤：**
    1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
    2. 注册并登录账户
    3. 进入API管理页面
    4. 创建新的API密钥
    5. 复制密钥到上方输入框
    """)

# 退出按钮
if st.button("退出系统"):
    st.switch_page("pages/page1.py")
