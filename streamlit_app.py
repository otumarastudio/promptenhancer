# streamlit_app.py
import streamlit as st
from prompt_master import deepThink, prompt_enhancer

st.title('Prompt Master✨')

api_key = st.sidebar.text_input('API 키를 입력하세요', type="password")
model_list = ["gpt-3.5-turbo", "gpt-4-0125-preview"]
model_name = st.sidebar.selectbox('모델을 선택하세요', model_list)
iterations = st.sidebar.number_input('반복 횟수를 선택하세요', min_value=1, max_value=10, value=3)

initial_prompt = st.text_area('🧠 초기 프롬프트를 입력하세요')
additional_info = st.text_area('프롬프트에 추가할 예시 데이터가 있다면 입력해주세요.')
purpose = st.text_area('🎯 프롬프트의 명확한 목적을 입력하세요. 원하는 이상적인 결과나 기대효과가 뭔지, 피하고 싶은 결과는 무엇인지 작성해주세요.')

# 역할별 시스템 프롬프트 설정
system_prompts = {
    "ai_assistant": "You are an AI designed to assist with human requests.",
    "prompt_engineer": "You are a Prompt Engineer. Your role is to evaluate LLM responses and give the best suggest for improvements of prompt."
}
if st.button('프롬프트 실행'):
    if not api_key:
        st.error('API 키가 필요합니다.')
    else:
        with st.spinner('프롬프트를 개선하는 중...'):
            thinker = deepThink(api_key, model_name, system_prompts["ai_assistant"], additional_info=additional_info, temperature=0.4)
            prompt_master = deepThink(api_key, model_name, system_prompts["prompt_engineer"], additional_info=additional_info, temperature=0.7)
            
            result_placeholder = st.empty()            
            enhanced_prompt, execution_results, final_result = prompt_enhancer(initial_prompt, purpose, thinker, prompt_master, iterations)
                                    
        # st.write('### 초기 프롬프트 실행 결과')
        # for i, result in enumerate(execution_results, start=1):
        #     st.markdown(f"### Iteration {i}: ")
        #     st.write(result)
            
        # 개선된 프롬프트 표시
        st.markdown('### 개선된 프롬프트:')
        st.write(enhanced_prompt) # 최종적으로 만들어진 프롬프트를 보여줌

        st.info('### 개선된 프롬프트 실행 결과')        
        st.write(final_result)

