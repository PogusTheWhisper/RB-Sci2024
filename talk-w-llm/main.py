import streamlit as st
from openai import OpenAI
import os
import numpy as np

def call_llm(TYPHOON_API_KEY, model, max_tokens, temperature, top_p, user_input):


    client = OpenAI(
        api_key=TYPHOON_API_KEY,
        base_url="https://api.opentyphoon.ai/v1",
    )
    try:

        stream = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """"คุณคือแชทบอทที่คอยให้ข้อมูลภายในโรงเรียนวัดราชบพิธ ถ้าไม่มีข้อมูลให้ตอบกลับว่า "ไม่มีข้อมูลครับ" """,
                },
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=True,
        )
    except:
        return '<API_KEY_ERROR>'

    else:
        respond=[]
        for chunk in stream:
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                choice = chunk.choices[0]
                if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                    if choice.delta.content is not None:
                        respond.append(choice.delta.content)

        return "".join(respond)

# Sidebar configuration
with st.sidebar:
    # logo, credits = st.columns(2)
    # with logo:
    #     st.image('./RB_logo.png', width=75)
    
    left, center, right = st.columns(3)
    with center:
        # st.image('RB_logo.png', width=75)
        st.write(os.getcwd())
            
    # with credits: # ไปทำ canva
    #     st.markdown('')
    #     st.markdown('จัดทำโดย ม.6 แผนการเรียนเตรียมวิศวะหุ่นยนต์')
        
    # st.markdown('แชทบอทสำหรับการสอบถามข้อมูลทั่วไปต่างๆภายในโรงเรียนวัดราชบพิธ')
    st.title("Config")
    
    # Input fields
    typhoon_api_key = st.text_input(
        label='TYPHOON API KEY', 
        placeholder='Place key here', 
        value=st.session_state.get('typhoon_api_key', '')
    )
    
    model = st.selectbox(
        label="Model", 
        options=( "typhoon-instruct", "typhoon-v1.5x-70b-instruct"),
        index=st.session_state.get('model_index', 0)
    )
    
    max_token = st.slider(
        label='Max Token', 
        min_value=50, 
        max_value=512, 
        step=10, 
        value=st.session_state.get('max_token', 300)
    )
    
    temperature = st.slider(
        label='Temperature', 
        min_value=0.0, 
        max_value=1.0, 
        step=0.05, 
        value=st.session_state.get('temperature', 0.6)
    )
    
    top_p = st.slider(
        label='Top P', 
        min_value=0.0, 
        max_value=1.0, 
        step=0.05, 
        value=st.session_state.get('top_p', 0.95)
    )

    # Save button
    if st.button('Save Config'):
        st.session_state['typhoon_api_key'] = typhoon_api_key
        st.session_state['model'] = model
        st.session_state['max_token'] = max_token
        st.session_state['temperature'] = temperature
        st.session_state['top_p'] = top_p
        st.success("Configuration saved!")

# with st.empty():
#     with st.chat_message("assistant"):
#         st.write("Hello human")
            
#     prompt = st.chat_input("Say something")
#     if prompt:
#         with st.chat_message("user"):
#             st.write(prompt)
            
#         with st.chat_message("assistant"):
#             st.write(call_llm(st.session_state['typhoon_api_key'], st.session_state['model'], st.session_state['max_token'], st.session_state['temperature'], st.session_state['top_p'], prompt))
     
st.title('RB Information ChatBot')

with st.chat_message("assistant"):
    st.write("สวัสดีครับ มีข้อสงสัยเรื่องอะไรครับ")
               
prompt = st.chat_input("พิมพ์คำถามตรงนี้!!")
         
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        st.write(call_llm(st.session_state['typhoon_api_key'], st.session_state['model'], st.session_state['max_token'], st.session_state['temperature'], st.session_state['top_p'], prompt))
        