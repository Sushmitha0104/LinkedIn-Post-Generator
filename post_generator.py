from llm_helper import llm
from few_shots import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def get_prompt(length, language, topic):
    length_str = get_length_str(length)
    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {topic}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    examples = few_shot.get_filtered_posts(length, language, topic)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."
        for i, post in enumerate(examples):
            post_text = post['text']
            prompt += f'\n\n Example {i+1}: \n\n {post_text}'
        
            if i == 2:
                break
    return prompt


   

def generate_post(length, language, topic):
    prompt = get_prompt(length, language, topic)
    response = llm.invoke(prompt)
    return response.content
    

if __name__ == "__main__":
    post = generate_post("Short", "English", "Job Search")
    print(post)