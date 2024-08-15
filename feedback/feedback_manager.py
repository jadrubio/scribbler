import streamlit as st
from langchain.output_parsers.json import SimpleJsonOutputParser
from langsmith import Client
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree

smith_client = Client()

def collectFeedback(answer, column_id, scenario):
    """ Submits user's feedback on specific scenario to langsmith; called as on_submit function for the respective streamlit feedback object.

    The payload combines the text of the scenario, user output, and answers. This function is intended to be called as 'on_submit' for the streamlit_feedback component.

    Parameters:
    answer (dict): Returned by streamlit_feedback function, contains "the user response, with the feedback_type, score and text fields"
    column_id (str): marking which column this belong too
    scenario (str): the scenario that users submitted feedback on

    """

    st.session_state.temp_debug = "called collectFeedback"

    # allows us to pick between thumbs / faces, based on the streamlit_feedback response
    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
    }
    scores = score_mappings[answer['type']]

    # Get the score from the selected feedback option's score mapping
    score = scores.get(answer['score'])

    # store the Langsmith run_id so the feedback is attached to the right flow on Langchain side
    run_id = st.session_state['run_id']

    if DEBUG:
        st.write(run_id)
        st.write(answer)

    if score is not None:
        # Formulate feedback type string incorporating the feedback option
        # and score value
        feedback_type_str = f"{answer['type']} {score} {answer['text']} \n {scenario}"

        st.session_state.temp_debug = feedback_type_str

        ## combine all data that we want to store in Langsmith
        payload = f"{answer['score']} rating scenario: \n {scenario} \n Based on: \n {answer_set}"

        # Record the feedback with the formulated feedback type string
        # and optional comment
        smith_client.create_feedback(
            run_id=run_id,
            value=payload,
            key=column_id,
            score=score,
            comment=answer['text']
        )
    else:
        st.warning("Invalid feedback score.")


@traceable
def summariseData(testing=False):
    """Takes the extracted answers to questions and generates three scenarios, based on selected prompts.

    testing (bool): will insert a dummy data instead of user-generated content if set to True

    """

    # start by setting up the langchain chain from our template (defined in lc_prompts.py)
    prompt_template = PromptTemplate.from_template(prompt_one_shot)

    # add a json parser to make sure the output is a json object
    json_parser = SimpleJsonOutputParser()

    # connect the prompt with the llm call, and then ensure output is json with our new parser
    chain = prompt_template | chat | json_parser

    ## pick the prompt we want to use
    prompt_1 = prompts['prompt_1']
    prompt_2 = prompts['prompt_2']
    prompt_3 = prompts['prompt_3']

    end_prompt = end_prompt_core

    ### call extract choices on real data / stored test data based on value of testing
    if testing:
        answer_set = extractChoices(msgs, True)
    else:
        answer_set = extractChoices(msgs, False)

    ## debug shows the interrim steps of the extracted set
    if DEBUG:
        st.divider()
        st.chat_message("ai").write(
            "**DEBUGGING** *-- I think this is a good summary of what you told me ... check if this is correct!*")
        st.chat_message("ai").json(answer_set)

    # store the generated answers into streamlit session state
    st.session_state['answer_set'] = answer_set

    # let the user know the bot is starting to generate content
    with entry_messages:
        if testing:
            st.markdown(":red[DEBUG active -- using testing messages]")

        st.divider()
        st.chat_message("ai").write(
            "Seems I have everything! Let me try to summarise what you said in three scenarios. \n See you if you like any of these! ")

        ## can't be bothered to set up LLM stream here, so just showing progress bar for now
        ## this gets manually updated after each scenario
        progress_text = 'Processing your scenarios'
        bar = st.progress(0, text=progress_text)

    # create first scenario & store into st.session state
    st.session_state.response_1 = chain.invoke({
        "main_prompt": prompt_1,
        "end_prompt": end_prompt,
        "example_what": example_set['what'],
        "example_context": example_set['context'],
        "example_outcome": example_set['outcome'],
        "example_reaction": example_set['reaction'],
        "example_scenario": example_set['scenario'],
        "what": answer_set['what'],
        "context": answer_set['context'],
        "outcome": answer_set['outcome'],
        "reaction": answer_set['reaction']
    })
    run_1 = get_current_run_tree()

    ## update progress bar
    bar.progress(33, progress_text)

    st.session_state.response_2 = chain.invoke({
        "main_prompt": prompt_2,
        "end_prompt": end_prompt,
        "example_what": example_set['what'],
        "example_context": example_set['context'],
        "example_outcome": example_set['outcome'],
        "example_reaction": example_set['reaction'],
        "example_scenario": example_set['scenario'],
        "what": answer_set['what'],
        "context": answer_set['context'],
        "outcome": answer_set['outcome'],
        "reaction": answer_set['reaction']
    })
    run_2 = get_current_run_tree()

    ## update progress bar
    bar.progress(66, progress_text)

    st.session_state.response_3 = chain.invoke({
        "main_prompt": prompt_3,
        "end_prompt": end_prompt,
        "example_what": example_set['what'],
        "example_context": example_set['context'],
        "example_outcome": example_set['outcome'],
        "example_reaction": example_set['reaction'],
        "example_scenario": example_set['scenario'],
        "what": answer_set['what'],
        "context": answer_set['context'],
        "outcome": answer_set['outcome'],
        "reaction": answer_set['reaction']
    })
    run_3 = get_current_run_tree()

    ## update progress bar after the last scenario
    bar.progress(99, progress_text)

    # remove the progress bar
    # bar.empty()

    if DEBUG:
        st.session_state.run_collection = {
            "run1": run_1,
            "run2": run_2,
            "run3": run_3
        }

    ## update the correct run ID -- all three calls share the same one.
    st.session_state.run_id = run_1.id

    ## move the flow to the next state
    st.session_state["agentState"] = "review"

    # we need the user to do an action (e.g., button click) to generate a natural streamlit refresh (so we can show scenarios on a clear page). Other options like streamlit rerun() have been marked as 'failed runs' on Langsmith which is annoying.
    st.button("I'm ready -- show me!", key='progressButton')


def testing_reviewSetUp():
    """Simple function that just sets up dummy scenario data, used when testing later flows of the process.
    """

    ## setting up testing code -- will likely be pulled out into a different procedure
    text_scenarios = {
        "s1": "So, here's the deal. I've been really trying to get my head around this coding thing, specifically in langchain. I thought I'd share my struggle online, hoping for some support or advice. But guess what? My PhD students and postdocs, the very same people I've been telling how crucial it is to learn coding, just laughed at me! Can you believe it? It made me feel super ticked off and embarrassed. I mean, who needs that kind of negativity, right? So, I did what I had to do. I let all the postdocs go, re-advertised their positions, and had a serious chat with the PhDs about how uncool their reaction was to my coding struggles.",

        "s2": "So, here's the thing. I've been trying to learn this coding thing called langchain, right? It's been a real struggle, so I decided to share my troubles online. I thought my phd students and postdocs would understand, but instead, they just laughed at me! Can you believe that? After all the times I've told them how important it is to learn how to code. It made me feel really mad and embarrassed, you know? So, I did what I had to do. I told the postdocs they were out and had to re-advertise their positions. And I had a serious talk with the phds, telling them that laughing at my coding struggles was not cool at all.",

        "s3": "So, here's the deal. I've been trying to learn this coding language called langchain, right? And it's been a real struggle. So, I decided to post about it online, hoping for some support or advice. But guess what? My PhD students and postdocs, the same people I've been telling how important it is to learn coding, just laughed at me! Can you believe it? I was so ticked off and embarrassed. I mean, who does that? So, I did what any self-respecting person would do. I fired all the postdocs and re-advertised their positions. And for the PhDs? I had a serious talk with them about how uncool their reaction was to my coding struggles."
    }

    # insert the dummy text into the right st.sessionstate locations
    st.session_state.response_1 = {'output_scenario': text_scenarios['s1']}
    st.session_state.response_2 = {'output_scenario': text_scenarios['s2']}
    st.session_state.response_3 = {'output_scenario': text_scenarios['s3']}
