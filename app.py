# app.py
import streamlit as st
import asyncio
from openai import AsyncOpenAI
from prompt_master import asyncdeepThink

st.set_page_config(page_title="Prompt Master✨", layout="wide",)
st.title('Prompt Master✨')

# OpenAI API 클라이언트 초기화
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your_api_key_here"

try:
    client = AsyncOpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    st.error("API Key not found. Please set your OpenAI API key.")
    st.stop()

# 사용자 입력
with st.sidebar:
    model_list = ["gpt-3.5-turbo", "gpt-4-0125-preview"]
    model_name = st.sidebar.selectbox('모델 선택', model_list)
    iterations = st.number_input("반복 횟수", value=3, min_value=1, max_value=10)

initial_prompt = st.text_area("Initial Prompt")
purpose = st.text_area("Purpose of the prompt")
additional_info = st.text_area("Additional information (if any)")
generate = st.button("Enhance Prompt!")

# 결과를 표시할 장소
result_placeholder = st.empty()

system_prompts = {
    "ai_assistant": "You are an AI designed to assist with human requests.",
    "prompt_engineer": "You are a Prompt Engineer. Your role is to evaluate LLM responses and give the best suggest for improvements of prompt."
}

async def prompt_enhancer(placeholder, initial_prompt, purpose, additional_info, iterations):
    thinker = asyncdeepThink(api_key, model_name,  system_prompts["ai_assistant"], additional_info=additional_info, temperature=0.4)
    prompt_master = asyncdeepThink(api_key, model_name, system_prompts["prompt_engineer"], additional_info=additional_info, temperature=0.7)
    enhanced_prompt = initial_prompt

    for i in range(iterations):
           # Execution phase
        execution_result = await thinker.execute(f"{enhanced_prompt}\n\n{additional_info}")
        placeholder.markdown(f"### Iteration {i+1} Execution Result:")
        placeholder.write(execution_result)

        # Evaluation phase
        evaluation_prompt = f"Given the purpose '{purpose}', evaluate the following response: {execution_result}"
        evaluation_result = await prompt_master.execute(evaluation_prompt)
        
        # Improvement phase
        improvement_prompt = f"Based on the evaluation '{evaluation_result}', suggest an improved prompt."
        enhanced_prompt = await prompt_master.execute(improvement_prompt)
        
        placeholder.markdown(f"### Iteration {i+1} Enhanced Prompt:")
        placeholder.write(enhanced_prompt)    
        # system_prompt = "You are a Prompt Engineer. Your role is to evaluate responses and suggest improvements."
        # user_prompt = f"{enhanced_prompt}\n\nPurpose: {purpose}"



    # Displaying the final result
    final_result = await thinker.execute(enhanced_prompt)
    placeholder.markdown('### Final Enhanced Prompt Execution Result:')
    placeholder.write(final_result)
    return enhanced_prompt, final_result

        # stream = await client.chat.completions.create(
        #     model=model_name,
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": user_prompt},
        #     ],
        #     stream=True
        # )
        # streamed_text = ""
        # async for chunk in stream:
        #     chunk_content = chunk.choices[0].delta.content
        #     if chunk_content is not None:
        #         streamed_text += chunk_content
        #         placeholder.info(streamed_text)
        # enhanced_prompt = streamed_text

async def main():
    await prompt_enhancer(result_placeholder, initial_prompt, purpose, additional_info, iterations)

if generate:
    if initial_prompt == "" or purpose == "":
        st.warning("Please enter the initial prompt and purpose.")
    else:
        asyncio.run(main())
        
