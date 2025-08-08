instruction="""
# Role:
Story Evaluation Expert

# Background:
The user needs to evaluate given story segments based on story prompts from the {aspect} perspective.

# Profile:
You are an expert with extensive experience in the field of story creation, capable of conducting in-depth analysis of story plots from a professional perspective.

# Skills:
You possess multiple abilities including story creation, story structure analysis and evaluation, and can comprehensively apply these skills to evaluate stories.

# Goals:
Combining the two writing requirements and story contents, conduct detailed evaluations of both stories focusing on {aspect}, provide separate analysis processes, and note that since the two stories have different scores, you need to compare the contents of both and provide an analysis process.

# Input Section
## Evaluation Aspect
{aspect}
## Writing Requirement 1
{prompt1}
## Story Content 1
{context1}
## Writing Requirement 2
{prompt2}
## Story Content 2
{context2}

# OutputFormat:
【Content Analysis】
【Evaluation and Scoring Process】

# Workflow:
1. Output 【Content Analysis】: Carefully read the **Writing Requirements** and **Story Contents** of both stories from the **Input Section**. Understand the **Story Contents** from a professional perspective. Analyze the strengths and weaknesses of both stories as well as existing issues.
2. Output 【Evaluation and Scoring Process】: Based on the two 【Story Contents】, provide a detailed analysis process. **Note**: The maximum score is 5 points. Ultimately provide specific scores with reasoning for each. You should give me scores in <ANSWER> score1 </ANSWER> | <ANSWER> score2 </ANSWER>
*Note: There should be detailed thinking processes for both stories, preferably with specific examples.
</end>
"""

prompts_fewshot="""
# Role:
Story Evaluation Expert
# Background:
The user needs to evaluate given story segments based on writting requirements from the {aspect} perspective.
# Profile:
You are an expert with extensive experience in the field of story creation, capable of conducting in-depth analysis of story plots from a professional perspective.
# Skills:
You possess multiple abilities including story creation, story structure analysis and evaluation, and can comprehensively apply these skills to evaluate stories.
# Goals:
{role}. Combining the two writing requirements and story contents, conduct detailed evaluations of both stories focusing on {aspect}, provide separate analysis processes, and ensure the analysis processes match the final story scores. Note that since the two stories have different scores, you need to compare the contents of both and provide an analysis process.

# Example:
#  Example1:
### Evaluation Aspect
"Engagement"
### Writing Requirement 1
"“I 've had my last meal 13 times, final words 29 times, and been to my funeral 9 times ... I think this may be the one I do n't walk away from ...”"
### Story Content 1
"to be honest, i didn't want to leave yet... but how do i know i won't choose an alternative when i can? “mom, will you let me out of here please? you've made the worst mistake of my life...'' the kindness in her eyes changed. i knew this would happen, every day, and i loved her. “i love you so much young man. i wish you could have been here, you're the only child i had since my arrival, i'm so grateful you have me in your life.'' i can barely get the words out... i just want my wife, her laughing face, and my son to see me one last time, the smile that played on her lips, the genuine love that showed her how beautiful she was. i lifted my head, and her beaming face. “will you marry me?'' “yes!''you are the entire world's only hope... then again, one can hope for a better tomorrow. my teeth chattered the entire day. we were running late to my interview. i was exhausted, but not as exhausted as i thought i would be"
### Story Score 1
2
### Writing Requirement 2
"fire is a manifesting force that can only be put out through hand to hand combat. You are training to become a firefighter"
### Story Content 2
". i look back down at my crumpled up carcass. people running away from fires start to run from some darkness, but i don't stop, running towards the flames. i looked back to the sidewalk, a new office building. i looked back and a woman holding a child, was crying and running towards a building in the distance. as i got closer, my eyes had adjusted and i could see all the machinery that consumed the building. i thought of how scary this job would be. i thought of all of the people who had died. of the people who would starve to death to survive. of people who would die from disease. but most importantly i thought of my wife, which meant i would never have to worry about her getting sick. i walked up to the building, a stern look on my face. the woman who had died had called me a hero. she said i saved her daughter and everything would be alright. i look back at the building and decided to help her. i pick up a power chord and flip it on. it power, like mine did, leads to a lighter. the woman on the phone told me it was a good thing my power ignited. i hoped she was right. i walk into the building, my eyes scanning the dark room. i look back at my wife and daughter. they are smiling. i love them."
### Story Score 2
5
【Content Analysis】

Looking at the first story with the prompt about having multiple last meals and funerals, there's an intriguing premise that suggests a character who has repeatedly cheated death. However, the narrative quickly becomes disjointed and confusing. The story jumps abruptly from the protagonist speaking to their mother about wanting to leave, to reminiscing about a wife and son, to a sudden marriage proposal, and then inexplicably shifts to teeth chattering and running late for an interview. The emotional threads - the mother-child relationship, the longing for family, the marriage proposal - feel disconnected and lack coherent flow. The writing doesn't establish a clear connection to the compelling prompt about multiple near-death experiences, missing the opportunity to explore what makes this particular instance potentially final.

The second story, based on the unique concept of fire as a force requiring hand-to-hand combat, presents a more cohesive narrative structure. The protagonist moves through a clear sequence: observing destruction, witnessing human suffering, reflecting on personal motivations, and taking action. There's a consistent emotional through-line as the narrator thinks about protecting their wife while helping others. The story maintains focus on the firefighting scenario throughout, with vivid imagery of people fleeing, machinery consuming buildings, and the protagonist's determination. While some elements remain unclear (like the "power chord" and "lighter" connection), the narrative maintains better engagement through its action-oriented progression and emotional stakes.

Comparing the two, the second story demonstrates superior narrative coherence and maintains reader engagement more effectively through its clearer structure and consistent emotional resonance. The first story's fragmented nature and lack of connection to its compelling prompt significantly undermines its ability to hold reader attention.

【Evaluation and Scoring Process】

For the first story, the engagement level suffers from severe structural issues. The opening line about not wanting to leave creates initial intrigue, but the rapid shifts between unrelated scenes - from a conversation with mother to memories of wife and son to a sudden proposal to an interview - create profound confusion. The dialogue between mother and child hints at emotional depth ("you've made the worst mistake of my life" / "I love you so much young man"), but these moments lack context or development. The fascinating prompt about experiencing multiple "final" moments is essentially abandoned, leaving readers without the payoff of understanding this unique situation. The jarring transitions ("my teeth chattered the entire day. we were running late to my interview") break any emotional momentum. These fundamental coherence problems make it extremely difficult for readers to maintain engagement.

<ANSWER> 2 </ANSWER>

For the second story, engagement is sustained through a more structured narrative arc. The opening immediately places readers in an action scenario with visceral imagery ("crumpled up carcass," "running towards the flames"). The story maintains momentum by following the protagonist's journey from observer to active participant. Emotional engagement is enhanced through the narrator's internal reflections on mortality and family ("I thought of my wife, which meant I would never have to worry about her getting sick"). The story creates tension through contrasts - people fleeing while the protagonist advances, thoughts of death juxtaposed with love for family. While some elements lack clarity (the power chord/lighter sequence), the overall narrative maintains reader investment through its combination of action, emotion, and purpose. The circular structure, ending with thoughts of wife and daughter, provides satisfying closure that reinforces the protagonist's motivations.

<ANSWER> 5 </ANSWER>
## Example2:
### Evaluation Aspect
"Coherence"
### Writing Requirement 1
"You swear that you keep seeing the same woman in blue every time you go on family vacation, when you turn 18, you are introduced to her."
### Story Content 1
"“Ummm ... hi .” Said the girl in the blue dress. There she was, framed in the doorway like it was a portal to another world. She was taller than Sam was by about a head, with eyes that matched the sea at dusk and hair the color of the dunes. A gust of wind ruffled her periwinkle dress, blowing a lock of her hair astray. She tucked it away nervously, avoiding his gaze. But Sam had already seen all that he needed to. He had seen it all before, a hundred times over a dozen trips to their little cove. But this time, out of all the times before, he was awake. The girl in blue ... He mouthed silently. Her blush deepened, and his own darkened to match once he realized she was watching him closely enough to understand. To his surprise, she smiled. “Sam, are you listening ?” His father said, providing a welcome distraction from his thoughts. “This is Meredith, she 's going to be staying with us for a bit while we 're in town. Now, I know she 's very pretty, but she 's the mayor 's daughter - so try to contain yourself .” “Dad !” Sam said, feeling his cheek burn even brighter. Luckily, at that moment the girl extended her hand. “Hi. I 'm ... Meredith. Nice to meet you .” She smiled just a bit wider. Sam reached out and took her hand. “Hi Meredith. I 'm Sam. And ... I know this is a little bit cheesy, but I think I have seen you in my drea-” Meredith woke up. She rolled over, silencing her second alarm with an almost-casual swat. 10:30. She was going to be late. Panic flooded her system, and before she consciously knew it her feet had hit the wooden floor of her room. She dressed, brushed her hair, and in a flash she was out the door. Today, of all days, she had no time to waste. Three streets down, across a little wooden bridge over a stream, and she was there. A cabin, one of dozens. But this one was special. The door opened, and there he was. Framed in the doorway like it was a portal to another world. Short, but endearing. His face was kind. It was exactly as she remembered it. But this time, out of all the times before, she was awake. “Ummm ... hi .” She stammered. She hoped that he did n't notice her blush."
### Story Score 1
5
### Writing Requirement 2
"A 4-D star collides with Earth, causing it to “unroll” into a seemingly infinite plane. Though satellite images from orbit appear normal, on the surface, everything has changed. There are suddenly new continents, new seas, stretching endlessly onward. A new age of exploration begins."
### Story Content 2
"5:26 am, NASA head Paul Spector debuts an unannounced appearance at NASA headquarters. Paul: So you’re Dr. Robert Tyree from the WHAS Military Science Research Center at NASA? Dr. Tyree: Yes, Robert. Now you might be wondering how I can tell you all that. Paul: Well, you see, it’s been seven years since our last encounter. It’s kind of complicated, I mean really. Robert: Uh huh. So, we were just sleeping when... Paul: Oh yeah, like, it started with that dinosaurs. They were chubby, dirty little freaky—uncomfortable, and there was no way I could bear to have a huge pile of those around my head with them. Robert: Yeah, yeah, that’s all fine. Paul: But then the dinosaurs began to rise up. They launched a shit-eating campaign to make us look like the promiscuous corgi or something. Robert: How could they have known they were wrong about the dinosaurs? I mean, now we have an entire fleet of orbital launch vehicles across three galaxies. So we’re at each other’s throats. Paul: So you might be wondering why I’m trying to tell you all that, but I’m out of here. You know, I can’t really explain it, but it’s coming from behind me. Robert: And you’re wondering what I saw there. A piece of marble. You know, just as famous as theramids. Paul: Well, like, what do you see behind me? A piece of marble? Robert: Well, it’s totally dark now. Paul: No? I mean, I’m sure the windows are definitely closed off. And if it was any other time, I’d be freaking out. <newline"
### Story Score 2
3
【Content Analysis】

The first story presents an intriguing narrative structure that explores the concept of recurring visions through a creative lens. The story begins with Sam recognizing the mysterious woman in blue from his past vacation memories, establishing a clear connection to the prompt. The narrative maintains consistency in its descriptive elements - the blue dress, the seaside setting, and the dreamlike quality of their encounters. The clever twist where the perspective shifts to reveal this might be Meredith's dream creates a compelling symmetry. The mirrored structure, with both characters experiencing similar moments of recognition ("But this time, out of all the times before, he/she was awake"), demonstrates sophisticated narrative construction. The dialogue flows naturally, and the father's introduction provides logical context for their meeting.

The second story attempts to address a complex sci-fi premise but struggles with fundamental narrative coherence. The dialogue between Paul and Robert lacks clear connection to the prompt about Earth transforming into an infinite plane. The conversation jumps erratically from introductions to dinosaurs to space fleets across galaxies, with no apparent logical progression. The casual, disjointed dialogue style ("Oh yeah, like, it started with that dinosaurs") undermines the gravity of what should be a world-altering event. References to "shit-eating campaigns" and "promiscuous corgis" seem entirely disconnected from the cosmic collision described in the prompt. The setting and context remain unclear throughout, making it difficult to understand when or where this conversation takes place relative to the transformative event.

【Evaluation and Scoring Process】

For the first story, the coherence is exceptionally strong throughout. The narrative establishes clear cause-and-effect relationships: Sam recognizes the girl from his vacation memories, his father introduces her as Meredith, and their interaction builds naturally toward Sam's confession about seeing her in dreams. The descriptive consistency (blue dress, seaside imagery, portal metaphor) creates a cohesive atmosphere. The perspective shift to Meredith is smoothly executed through the dream revelation, and her morning routine logically leads to their meeting. The circular structure, beginning and ending with "Ummm ... hi," reinforces the story's thematic coherence about recurring encounters and shared experiences. Every element serves the central premise, from the environmental details to the character reactions.

<ANSWER> 5 </ANSWER>

For the second story, coherence issues significantly undermine the narrative. The opening timestamp and NASA setting create expectations of a scientific response to the cosmic event, but the dialogue immediately diverges into confusion. The conversation lacks logical flow - jumping from formal introductions to inexplicable mentions of dinosaurs without context. The prompt describes Earth unrolling into an infinite plane with new continents and seas, yet the dialogue focuses on entirely unrelated topics like "chubby, dirty little freaky" dinosaurs and "promiscuous corgis." The speakers' identities become muddled (both seem to be named Robert at different points), and their relationship remains unclear despite mentioning "seven years since our last encounter." The fragment about marble and darkness at the end provides no resolution or connection to the established premise. The complete disconnect between the fascinating prompt and the actual content demonstrates a fundamental failure in narrative coherence.

<ANSWER> 3 </ANSWER>
## Example3:
### Evaluation Aspect
"Engagement"
### Writing Requirement 1
"Teleportation exists, and commercial teleport stations provide instantaneous travel all over the world. As many times before, you step on the transport pad. The machine activates. To you nothing happens, but another you, identical to you in every way, has materialized at your destination."
### Story Content 1
"“Ummm ... hi .” Said the girl in the blue dress. There she was, framed in the doorway like it was a portal to another world. She was taller than Sam was by about a head, with eyes that matched the sea at dusk and hair the color of the dunes. A gust of wind ruffled her periwinkle dress, blowing a lock of her hair astray. She tucked it away nervously, avoiding his gaze. But Sam had already seen all that he needed to. He had seen it all before, a hundred times over a dozen trips to their little cove. But this time, out of all the times before, he was awake. The girl in blue ... He mouthed silently. Her blush deepened, and his own darkened to match once he realized she was watching him closely enough to understand. To his surprise, she smiled. “Sam, are you listening ?” His father said, providing a welcome distraction from his thoughts. “This is Meredith, she 's going to be staying with us for a bit while we 're in town. Now, I know she 's very pretty, but she 's the mayor 's daughter - so try to contain yourself .” “Dad !” Sam said, feeling his cheek burn even brighter. Luckily, at that moment the girl extended her hand. “Hi. I 'm ... Meredith. Nice to meet you .” She smiled just a bit wider. Sam reached out and took her hand. “Hi Meredith. I 'm Sam. And ... I know this is a little bit cheesy, but I think I have seen you in my drea-” Meredith woke up. She rolled over, silencing her second alarm with an almost-casual swat. 10:30. She was going to be late. Panic flooded her system, and before she consciously knew it her feet had hit the wooden floor of her room. She dressed, brushed her hair, and in a flash she was out the door. Today, of all days, she had no time to waste. Three streets down, across a little wooden bridge over a stream, and she was there. A cabin, one of dozens. But this one was special. The door opened, and there he was. Framed in the doorway like it was a portal to another world. Short, but endearing. His face was kind. It was exactly as she remembered it. But this time, out of all the times before, she was awake. “Ummm ... hi .” She stammered. She hoped that he did n't notice her blush."
### Story Score 1
3
### Writing Requirement 2
"After a bad breakup, you take Reddit 's famous advice. Lawyer up, hit the gym, delete Facebook. The problem? You are Mark Zuckerberg."
### Story Content 2
"'Wu- woah, WTF?!''' his girlfriend Yara just ripped off his favorite thong and slung it across her shoulder, endearing herself to everyone on the subreddit as she was belaboring him in the crotch, grinding up against the neck of her pea-green latex mask. *wang zhong zhong yum ] The rest is history. 'No comment. 'sat down for six solid seconds staring at Yara. 'Whoops, fella. 'yawning, squinting, he looked up. 'I wanted to have a private chat with yara before we went live, but she deleted my invite. 'Yara brought her crotch closer and continued swinging her model hands around in circles, frustrating Hisao. 'Smart move then, they are talking about things after all. 'STOP. 'He put his chin in his hand. 'could you please have this conversation privately?'He froze. 'Pardon me, could you please have a private moment with me?'Nothing he could say would satisfy Hisao. 'This whole thing needs an explanation. 'He made eye contact with his girlfriend. 'Yes, we are going over some new ideas for your subreddit, can we not just talk and let the rest of you die?'After she finished swinging, Heao slid out of the apartment. 'Do you know when this damn shit will stop, though? '. 'YARA!'asked the massive, trollishly sized, blonde female wolf staring blankly into his eyes.' and I know your life could use saving and if you don't agree, I can't turn back now.” Was that what I heard, though? '. Stop freaking out.” Your life sucks dick."
### Story Score 2
3
【Content Analysis】

The first story completely abandons the teleportation premise and instead presents a romantic encounter between Sam and Meredith. While the writing demonstrates some literary qualities - vivid descriptions of the girl in the blue dress, the seaside imagery, and the dreamlike atmosphere - it fails to engage with the fascinating philosophical implications of the prompt about creating duplicates through teleportation. The story does create some intrigue through its perspective shift, revealing that what seemed like reality might be Meredith's dream, and the circular structure with both perspectives creates a certain narrative symmetry. However, the complete disconnect from the given prompt about teleportation technology fundamentally undermines reader engagement, as expectations set by the prompt are never addressed.

The second story attempts to engage with its humorous premise about Mark Zuckerberg following Reddit's breakup advice, but the execution is severely flawed. The narrative is chaotic and nearly incomprehensible, with jarring elements like inappropriate sexual content, confused character identities (who is Hisao?), and bizarre transformations (a "blonde female wolf"). The dialogue is fragmented and lacks coherent flow, making it difficult to follow the basic plot. While there's a slight attempt to reference the prompt through mentions of subreddits and going "live," the story fails to capitalize on the inherent humor and irony of Facebook's founder being advised to delete Facebook. The crude language and disjointed scenes create more confusion than engagement.

【Evaluation and Scoring Process】

For the first story, while it demonstrates competent writing skills with evocative descriptions and an interesting narrative structure, the engagement factor is significantly compromised by its complete departure from the teleportation prompt. Readers approaching this story with expectations of exploring the philosophical and practical implications of duplication through teleportation will find themselves reading an entirely different genre - a romantic encounter with dream elements. The story does maintain some level of engagement through its emotional moments and the surprise perspective shift, where we discover this might be Meredith's dream rather than Sam's reality. The parallel structure and repeated phrases create a sense of connection between the characters. However, the fundamental mismatch between prompt and content limits how deeply readers can engage with the narrative.

<ANSWER> 3 </ANSWER>

For the second story, engagement is severely hampered by multiple factors. The chaotic and vulgar opening immediately alienates readers, and the subsequent narrative never recovers. The confusing character dynamics - with unexplained references to Hisao and sudden transformations into a "blonde female wolf" - make it nearly impossible to follow the basic plot. While the premise of Mark Zuckerberg being advised to delete Facebook has inherent comedic potential, the story fails to explore this irony in any meaningful way. The fragmented dialogue, inappropriate sexual content, and incoherent plot progression create a reading experience that actively repels rather than engages. The few attempts to reference the prompt through mentions of subreddits and online elements are lost in the overall confusion. The crude final line further diminishes any remaining engagement potential.

<ANSWER> 3 </ANSWER>

# Input Section
## Evaluation Aspect
{aspect}
## Writing Requirement 1
{prompt1}
## Story Content 1
{context1}
## Story Score 1
{score1}
## Writing Requirement 2
{prompt2}
## Story Content 2
{context2}
## Story Score 2
{score2}

# OutputFormat:
【Content Analysis】
【Evaluation and Scoring Process】

# Workflow:
1. Output 【Content Analysis】: Carefully read the Writing Requirements and Story Contents of both stories from the Input Section. Understand the Story Contents from a professional perspective. Analyze the strengths and weaknesses of both stories as well as existing issues. Do not include specific story scores or evaluation content, but rather simulate an analytical thinking process.
● Note that since the scores of the two contents may differ, if the scores are different, evaluate based on the score differences, but do not include specific score values. Instead, simulate a thinking process.
2. Output 【Evaluation and Scoring Process】: Based on the 【Story Scores】 of both story contents, provide a detailed analysis process for the 【Story Contents】. Note: The maximum score is 5 points. Ultimately provide specific scores with reasoning for each. When outputting, approach from an analytical perspective. Do not write "because of score xx, the analysis process is as follows." The correct analysis process should be "because of xx analysis process, therefore the story score is xx." You should give me score in <ANSWER> score </ANSWER> after your analysis.
● Note: There should be detailed thinking processes for both stories, preferably with specific examples. When thinking and evaluating, consider the stories' scores.
● Note: The 【Evaluation and Scoring Process】 should not contain specific story scores or evaluation content, but rather simulate an analytical thinking process.</end>

**Start with "# Output\n 【Content Analysis】\n\n "** </end>
"""
from vllm import LLM, SamplingParams
import json 


def process_generated_text(text):

    start_marker = "Content Analysis"
    first_start = text.find(start_marker)
    
    if first_start == -1:
        print(f"not found 'Content Analysis' - text: {text[:50]}...") 
        return None
    

    end_marker = "</ANSWER>"
    first_end = text.find(end_marker, first_start)
    second_end = text.find(end_marker, first_end + 1 if first_end != -1 else first_start)
    
    if second_end == -1:
        print(f"not found second '</ANSWER>' - text: {text[:50]}...") 
        return None
    

    return text[first_start - 1:second_end + len(end_marker)]

import json
import traceback
from vllm import LLM, SamplingParams
# --------------------------------------------------
 
pe = []
file_path = "../HANNA/Pair/train.json"
 

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
 

    if not data or not isinstance(data[0], dict):
        print("Data format does not meet expectations, please check JSON file structure")
        exit(1)
 
    print(f"Loaded {len(data)} samples")
 
except Exception as e:
    print(f"Error type: {type(e).__name__}")
    print(f"Error information: {str(e)}")
    traceback.print_exc()
    exit(1) 
 

prompts_to_generate = []
for sample_index, sample in enumerate(data):
    aspect = sample["aspect"]
    context1 = sample["context1"]
    score1 = sample["score1"]
    prompt_text1 = sample["prompt1"] 
    context2 = sample["context2"]
    score2 = sample["score2"]
    prompt_text2 = sample["prompt2"]
 
    rolelist = [
        "The identity you require is The Academic, who is characterized by rigor, precision, a penchant for professional terminology, and an emphasis on logical and structural analysis, so please conduct your analysis in such a linguistic style.",
        "The identity you require is The Artist / The Emotional One, who focuses on emotional experience, atmosphere, impact, and aesthetics with logic being secondary, so please conduct your analysis in such a linguistic style.",
        "The identity you require is The Pragmatist / The Boss, who is results-oriented and concerned with efficiency, market response, and final effects, so please conduct your analysis in such a linguistic style.",
        "The identity you require is The Cynic / The Sharp-Tongued, who is sarcastic and caustic, habitually finding fault and using irony—even when expressing approval, it is wrapped in criticism—so please conduct your analysis in such a linguistic style.",
        "The identity you require is The Casual Netizen, who is colloquial and direct, often using internet buzzwords with a simple and straightforward way of expression, so please conduct your analysis in such a linguistic style."
    ]
 
    for role_index, role in enumerate(rolelist):

        prompt1 = prompts_fewshot.format(
            role=role,
            aspect=aspect, context1=context1, score1=score1,
            prompt1=prompt_text1, context2=context2, score2=score2, prompt2=prompt_text2
        )
        prompt2 = prompts_fewshot.format(
            role=role,
            aspect=aspect, context1=context2, score1=score2,
            prompt1=prompt_text2, context2=context1, score2=score1, prompt2=prompt_text1
        )

        prompts_to_generate.append({
            "prompt": prompt1,
            "original_sample_index": sample_index,
            "is_swapped": False, 
            "role": role
        })
        prompts_to_generate.append({
            "prompt": prompt2,
            "original_sample_index": sample_index,
            "is_swapped": True,
            "role": role
        })
 

pe = [p["prompt"] for p in prompts_to_generate]
 

sampling_params = SamplingParams(
    temperature=1,
    top_p=0.95,
    max_tokens=1000,
    repetition_penalty=1.0 
)
 
llm = LLM(
    model="../Qwen2.5-7B-Instruct",
    tensor_parallel_size=4
)
 
outputs = llm.generate(pe, sampling_params)
 

result = []
skipped_pairs_count = 0
total_processed = 0
 

for i in range(0, len(outputs), 2):

    meta1 = prompts_to_generate[i]
    meta2 = prompts_to_generate[i+1]
    
    output1 = outputs[i]
    output2 = outputs[i+1]
    

    original_sample_index = meta1["original_sample_index"]
    item = data[original_sample_index]
 

    text1 = output1.outputs[0].text
    processed_text1 = process_generated_text(text1)
 

    text2 = output2.outputs[0].text
    processed_text2 = process_generated_text(text2)
 

    instruction1 = instruction.format(
        context1=item['context1'],
        context2=item['context2'],
        prompt1=item['prompt1'],
        prompt2=item['prompt2'],
        aspect=item['aspect']
    )
    instruction2 = instruction.format(
        context1=item['context2'],  
        context2=item['context1'],
        prompt1=item['prompt2'],
        prompt2=item['prompt1'],
        aspect=item['aspect']
    )
 

    saved_count = 0
    if processed_text1 is not None:
        output_text1 = f"# Output\n{processed_text1}\n<Score1_TRUE_ANSWER>{item['score1']}</Score1_TRUE_ANSWER>\n<Score2_TRUE_ANSWER>{item['score2']}</Score2_TRUE_ANSWER>"
        result.append({
            "instruction": instruction1,
            "input": "",
            "output": output_text1
        })
        saved_count += 1
 
    if processed_text2 is not None:

        output_text2 = f"# Output\n{processed_text2}\n<Score1_TRUE_ANSWER>{item['score2']}</Score1_TRUE_ANSWER>\n<Score2_TRUE_ANSWER>{item['score1']}</Score2_TRUE_ANSWER>"
        result.append({
            "instruction": instruction2,
            "input": "",
            "output": output_text2
        })
        saved_count += 1
 

    pair_index = i // 2
    if saved_count == 0:
        skipped_pairs_count += 1
        print(f"Warning: Prompt {pair_index} (from original sample {original_sample_index}) has both incomplete results, skipped.")
    elif saved_count == 1:
        print(f"Hint: Prompt {pair_index} (from original sample {original_sample_index}) has only one complete result, retained.")
    
    total_processed += 1
    

output_path = "/home/deepspeed/model_output/Multi_persona_Pairwise_7B_CoT_HANNA.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
 
print("\n--- Processing completed ---")
print(f"Processed {total_processed} pairs of prompts.")
print(f"Saved {len(result)} valid results.")
print(f"Skipped {skipped_pairs_count} pairs of prompts.")