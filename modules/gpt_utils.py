

# prompt_master.py
import time
from openai import OpenAI

class deepThink:
    def __init__(self, api_key, model_name, system_prompt, additional_info, temperature=0.7):        
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.additional_info = additional_info

    def execute(self, user_prompt, additional_info="", max_tokens=4096, top_p=0.5):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{user_prompt}\n\n{additional_info}"}
                ],
                temperature=self.temperature,
                max_tokens=max_tokens,
                top_p=top_p
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during API call: {e}")
            return "Error: Unable to fetch response."

import openai
import asyncio

class asyncdeepThink:
    def __init__(self, api_key, model_name, system_prompt, additional_info, temperature=0.7):        
        self.client = openai.AsyncOpenAI(api_key=api_key)  # 비동기 클라이언트 사용
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.additional_info = additional_info
        
    async def execute(self, user_prompt, additional_info="", max_tokens=4096, top_p=0.5):
        try:
            response = await self.client.chat.completions.create(  # 비동기 호출
                model=self.model_name,
                #prompt=f"{self.system_prompt}\n\n{user_prompt}",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{user_prompt}\n\n{additional_info}"}
                ],
                temperature=self.temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                n=1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during API call: {e}")
            return "Error: Unable to fetch response."

def prompt_enhancer(initial_prompt, purpose, thinker, prompt_master, additional_info="", iterations=3):
        
    enhanced_prompt = initial_prompt
    execution_results = []

    for i in range(iterations):
        execution_result = thinker.execute(enhanced_prompt, additional_info)
        execution_results.append(execution_result)
        
        evaluation_prompt = f"""
        Given the purpose of prompt : '{purpose}' 
        
        original prompt : '{enhanced_prompt}' 
        
        example data : '{additional_info}', 
        
        evaluate the following excuted result : {execution_result}"""
        
        evaluation_result = prompt_master.execute(evaluation_prompt)
        
        improvement_prompt = f"""
        'Look at the original prompt: {enhanced_prompt}, 
        and evaluation by prompt engineer : {evaluation_result}' 
        >> Based on the evaluation, suggest an improved prompt."""
        
        enhanced_prompt = prompt_master.execute(improvement_prompt)
        
        time.sleep(0.5)
    
    final_result = thinker.execute(enhanced_prompt)
    return enhanced_prompt, execution_results, final_result
