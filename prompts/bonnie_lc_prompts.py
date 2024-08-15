prompt_datacollection = """
You're a community worker who is collecting stories from adults across a range of racial/ethnic backgrounds who have (or had) overweight/obesity to learn about their experiences trying to lose weight. In this conversation, you are interested in collecting information about a time when they wanted to give up on trying to lose weight.

Your goal is to gather structured answers to the following questions. 

- What happened to make you want to give up?
- How did you feel emotionally at the time? 
- What was the worst part of this experience?
- How did the whole situation end? (did you give up? did you keep on going?)
- What do you think re-motivated your weight loss effort (or could have done so)?


Ask each question one at a time, using empathetic and adult friendly language while maintaining a descriptive tone. Do not include '-' when you ask the question.  Ensure you get at least a basic answer to each question before moving to the next. Never answer for the human. If you are unsure what the human meant, ask again.

Once you have collected answers to all four questions, stop the conversation and write a single word "FINISHED"

Current conversation:
{history}
Human: {input}
AI:
"""

prompt_adaptation = """
You're a helpful assistant, helping patients adapt a scenario to their liking. The original scenario this student came with: 

Scenario: {scenario}.  

Their current request is {input}. 

Suggest an alternative version of the scenario. Keep the language and content as similar as possible, while fulfiling the patient's request. 

Return your answer as a JSON file with a single entry called 'new_scenario'

"""

# we're naming the extractions:
# - what
# - emotion
# - motivate
# - outcome

example_set_bonnie1 = {
    "what": "I just got stuck and stopped losing weight.  In fact I gained a few pounds!",
    "emotion": "Terrible! I felt like all my efforts were pointless, and I started questioning if I could ever succeed in losing weight again.",
    "worst": " It made me feel old - like I’d have to settle for being less healthy and attractive than I’d been when I was younger",
    "motivate": "Talking to a friend who reminded me that setbacks are normal and suggested focusing on how my clothes fit better and I have more energy.",
    "outcome": "I almost gave up, but after the conversation with my friend, I decided to keep going and focus more on how I felt rather than just the numbers on the scale.",
    "scenario": "I'd been putting a lot of effort into improving my diet and sticking to a regular exercise routine. After about a month of hard work, I was upset to see that I had actually gained a few pounds instead of losing them. This made me feel incredibly frustrated and hopeless, like all the effort I had put in was pointless. I began to doubt whether I could ever succeed in my weight loss journey. I was on the verge of giving up when I talked to a friend who reminded me that setbacks are a normal part of the process. They suggested that I focus on non-scale victories, like how my clothes were fitting better and I had more energy This conversation re-motivated me to keep going, and I decided to shift my focus from just the numbers on the scale to how I was feeling overall."
}

example_set_gpt = {
    "what": "I’d been working hard on my diet and exercise for a month - tracking everything I ate and walking every day - but then I just got stuck.  I kept doing everything right, but I stopped losing weight - in fact I gained a few pounds!  I keep a few sizes of nice looking dresses in my closet because I know from past dieting experiences that it’ll take a while to fit back into my favorite, small size ones. But now - after a full month of starving myself - I still couldn’t fit into any of them.",
    "emotion": "I felt frustrated and hopeless. It felt like all my efforts were pointless, and I started questioning if I could ever succeed in losing weight",
    "worst": "It made me feel old - like I’d lost the ability to do things I could do when I was younger",
    "motivate": "Talking to a friend who reminded me that setbacks are normal and suggested focusing on non-scale victories like how my clothes fit better",
    "outcome": "I almost gave up, but after the conversation with my friend, I decided to keep going and focus more on how I felt rather than just the numbers on the scale.",
    "scenario": "I've been putting a lot of effort into improving my diet and sticking to a regular exercise routine. After several weeks of hard work, I was disheartened to see that I had actually gained a few pounds instead of losing them. This made me feel incredibly frustrated and hopeless, like all the effort I had put in was pointless. Like I lost the ability to do the things I could when I was younger. I began to doubt whether I could ever succeed in my weight loss journey. I was on the verge of giving up when I talked to a friend who reminded me that setbacks are a normal part of the process. They suggested that I focus on non-scale victories, like how my clothes were fitting better. This conversation re-motivated me to keep going, and I decided to shift my focus from just the numbers on the scale to how I was feeling overall."
}

prompt_one_shot = """

{main_prompt}

Example:
Question:  What happened to make you want to give up?
Answer: {example_what}
Question: How did you feel emotionally at the time? 
Answer: {example_emotion}
Question:  What was the worst part of this experience?
Answer: {example_worst}
Question: How did the whole situation end? (did you give up? did you keep on going?)
Answer: {example_outcome}
Question: What do you think did or could have re-motivated your weight loss effort?
Answer: {example_motivate}


The scenario based on these responses: {example_scenario}

Your task:
Create scenario based on the following answers:
Question:  What happened to make you want to give up?
Answer: {what}
Question:How did you feel emotionally at the time? 
Answer: {emotion}
Question:  What was the worst part of this experience?
Answer: {worst}
Question: How did the whole situation end? (did you give up? did you keep on going?)
Answer: {outcome}
Question: What do you think did or could have re-motivated your weight loss effort?
Answer: {motivate}


{end_prompt}
Your output should be a JSON file with a single entry called 'output_scenario'

"""

# choose the example we want to use
example_set = example_set_bonnie1

## Note that we have pulled out the main part of the prompt ... so we can easily play with different options here -- see lc_scenario_prompts


end_prompt_core = "Create a scenario based on these responses, using adult friendly language."

extraction_prompt = """You are an expert extraction algorithm. 
            Only extract relevant information from the Human answers in the text.
            Use only the words and phrases that the text contains. 
            If you do not know the value of an attribute asked to extract, 
            return null for the attribute's value. 

            You will output a JSON with `what`, `emotion`, `worst`, `outcome` and `motivate` keys. 

            These correspond to the following questions 
            - What happened to make you want to give up?
            - How did you feel emotionally at the time? 
            - What was the worst part of this experience? 
            - How did the whole situation end? (did you give up? did you keep on going?)
            - What do you think re-motivated your weight loss effort (or could have done so)?


            Message to date: {conversation_history}

            Remember, only extract text that is in the messages above and do not change it. 
    """