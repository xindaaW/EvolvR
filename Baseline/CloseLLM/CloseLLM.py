import json
import random
import time
import httpx

instruction="""
    # Role:
    Story Evaluation Expert

    # Background:
    The user needs to evaluate a given story segment, combined with reviews from the {aspect} perspective.

    # Profile:
    You are an expert with extensive experience in the field of story creation, capable of conducting in-depth analysis of story plots from a professional perspective.

    # Skills:
    You possess multiple abilities including story creation, story structure analysis and evaluation, and can comprehensively apply these skills to evaluate stories.

    # Goals:
    Combining the story content, conduct a detailed evaluation of the story focusing on the {aspect} aspect, and provide an analysis process.

    # Input Section
    ## Story Demand
    {prompt}
    ## Story Content
    {context}
    ## Evaluation Aspect
    {aspect}

    
    # Workflow:
    Understand the **Story Content** and analyze the story's existing issues.
    *Note: The score should be a number between 1 and 5.
    *Note: Give me score in <ANSWER> score </ANSWER>.
    </end>
"""

other_instruction="""
    # Role:
    Story Evaluation Expert

    # Background:
    The user needs to evaluate a given story segment, combined with reviews from the {aspect} perspective.

    # Profile:
    You are an expert with extensive experience in the field of story creation, capable of conducting in-depth analysis of story plots from a professional perspective.

    # Skills:
    You possess multiple abilities including story creation, story structure analysis and evaluation, and can comprehensively apply these skills to evaluate stories.

    # Goals:
    Combining the story content, conduct a detailed evaluation of the story focusing on the {aspect} aspect, and provide an analysis process.

    # Input Section
    ## Story Demand
    {prompt}
    ## Story Content
    {context}
    ## Evaluation Aspect
    {aspect}

    # Output Format:
    【Content Analysis】
    【Evaluation and Scoring Process】

    # Workflow:
    1. Output 【Content Analysis】: Carefully read the **Story Content** 、**Story Demand** and **Comment Aspect** from the **Input Section**. Understand the **Story Content** and analyze the story's existing issues.
    2. Output 【Evaluation and Scoring Process】: Provide a detailed analysis process for the existing 【Story Content】, and ultimately give a score. You should give me score in <ANSWER> score </ANSWER>
    *Note: There should be a detailed thinking process regarding the story, preferably with specific examples.
    *Note: The score should be a number between 1 and 5.
    *Note: Give me score in <ANSWER> score </ANSWER>.
    </end>
"""

def call_llm_stream(system_input, messages_input, temperature=0.6, top_p=0.95, model_type="claude37_sonnet"):
    messages_input_final = []
    if system_input:
        messages_input_final.append({'role': 'system', 'content': system_input})
    messages_input_final.extend(messages_input)
    
    url = "your-api"
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'your key'
    }
    
    req_data = {
        "messages": messages_input_final,
        "stream": True,
        "temperature": temperature,
        "top_p": top_p,
        "model": model_type,
        "max_tokens": 65536
    }

    is_success, try_time = False, 0
    stream_list = []
    timeout = 700
    
    while not is_success and try_time <= 5:
        try:
            try_time += 1
            with httpx.stream("POST", url=url, json=req_data, headers=header, timeout=timeout) as responses:
                for chunk in responses.iter_text():
                    stream_content = chunk.strip()
                    if stream_content.startswith("data: "):
                        data_part = stream_content[6:].strip()
                        if data_part == "[DONE]":
                            continue
                        try:
                            struct_stream_content = json.loads(data_part)
                            content = struct_stream_content['choices'][0]['delta'].get('content', '')
                            if content:
                                stream_list.append(content)
                                yield content
                        except Exception as e:
                            # print(f"Error parsing chunk: {e}")
                            continue
            if len(stream_list) > 0:
                is_success = True
            else:
                time.sleep(1)
        except Exception as e:
            print(f"Stream request failed: {e}")
            continue
    return


import json
import time
import os
from datetime import datetime


if __name__ == "__main__":
    
    system_input = "you are a helpful assistant."
    file_path = "../HANNA_test.json"
    

    output_base_dir = "../HANNA"
    
    model_type = "gemini-2.5-flash-06-17"  
    temperature = 0.6
    top_p = 0.95
    
    # 创建模型专用目录
    model_output_dir = os.path.join(output_base_dir, model_type)
    os.makedirs(model_output_dir, exist_ok=True)
    
    # 生成输出文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_filename = os.path.basename(file_path).replace(".json", "")
    output_filename = f"{input_filename}_{model_type}_{timestamp}.json"
    output_file = os.path.join(model_output_dir, output_filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 检查数据格式是否正确
        if not data or not isinstance(data[0], dict):
            print("Data format does not meet expectations, please check JSON file structure")
            exit(1)
            
        # 统计总数
        total_samples = len(data)
        print(f"Loaded {total_samples} samples")
        
        # Store all results
        all_results = []
        data = data[:300]
        for idx, sample in enumerate(data):
            print(f"\nProcessing sample {idx + 1}/{total_samples}")
            
            try:
                context = sample["context"]
                aspect = sample["aspect"] 
                score = sample["score"]
                prompt = sample["prompt"]
                
  
                try:
                    input_content = instruction.format(context=context, aspect=aspect, prompt=prompt)
                except NameError:
                    # 如果instruction未定义，使用简单的格式
                    input_content = f"Context: {context}\nAspect: {aspect}\nPrompt: {prompt}"
                
                messages_inputs = [{"role": "user", "content": input_content}]
                
                print(f"Input content preview: {input_content[:100]}...")
                
                response_chunks = []
                try:
                    for chunk in call_llm_stream(
                        system_input, 
                        messages_inputs, 
                        temperature=temperature, 
                        top_p=top_p, 
                        model_type=model_type
                    ):
                        print(chunk, end='', flush=True)  
                        response_chunks.append(chunk)
                    
                    full_response = ''.join(response_chunks)
                    
                except Exception as api_error:
                    print(f"\nAPI call failed: {api_error}")
                    full_response = f"ERROR: {str(api_error)}"
                
                # Save result
                result = {
                    "index": idx,
                    "input": {
                        "context": context,
                        "aspect": aspect,
                        "score": score,
                        "prompt": prompt,
                        "formatted_input": input_content
                    },
                    "output": {
                        "response": full_response,
                        "timestamp": datetime.now().isoformat(),
                        "model_type": model_type,
                        "temperature": temperature,
                        "top_p": top_p
                    }
                }
                
                all_results.append(result)
                print(f"\n✓ Sample {idx + 1} processed")

                if (idx + 1) % 10 == 0:
                    with open(output_file, 'w', encoding='utf-8') as out_f:
                        json.dump(all_results, out_f, ensure_ascii=False, indent=2)
                    print(f"Intermediate results saved to: {output_file}")
                
 
                time.sleep(1)
                
            except Exception as sample_error:
                print(f"Error processing sample {idx + 1}: {sample_error}")
                # Even if there is an error, save error information
                error_result = {
                    "index": idx,
                    "input": sample,
                    "output": {
                        "response": f"PROCESSING_ERROR: {str(sample_error)}",
                        "timestamp": datetime.now().isoformat(),
                        "model_type": model_type,
                        "temperature": temperature,
                        "top_p": top_p
                    }
                }
                all_results.append(error_result)
                continue
        
        # 最终保存所有结果
        with open(output_file, 'w', encoding='utf-8') as out_f:
            json.dump(all_results, out_f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*50}")
        print(f"All samples processed!")
        print(f"Model: {model_type}")
        print(f"Total samples: {total_samples}")
        print(f"Successfully processed: {len([r for r in all_results if not r['output']['response'].startswith('ERROR')])}")
        print(f"Failed to process: {len([r for r in all_results if r['output']['response'].startswith('ERROR')])}")
        print(f"Results saved to: {output_file}")
        
        # Display some statistics
        successful_results = [r for r in all_results if not r['output']['response'].startswith('ERROR')]
        if successful_results:
            avg_response_length = sum(len(r['output']['response']) for r in successful_results) / len(successful_results)
            print(f"Average response length: {avg_response_length:.1f} characters")
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"JSON file format error: {e}")
    except Exception as e:
        print(f"Program running error: {e}")
