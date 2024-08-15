import streamlit as st

def getData(testing=False):
    """Collects answers to main questions from the user.

    The conversation flow is stored in the msgs variable (which acts as the persistent langchain-streamlit memory for the bot). The prompt for LLM must be set up to return "FINISHED" when all data is collected.

    Parameters:
    testing: bool variable that will insert a dummy conversation instead of engaging with the user

    Returns:
    Nothing returned as all data is stored in msgs.
    """

    ## if this is the first run, set up the intro
    if len(msgs.messages) == 0:
        msgs.add_ai_message(
            "Hi there -- I'm collecting stories about challenging experiences on social media to better understand and support our students. I'd appreciate if you could share your experience with me by answering a few questions. \n\n I'll start with a general question and then we'll move to a specific situation you remember. \n\n  Let me know when you're ready! ")

    # as Streamlit refreshes page after each input, we have to refresh all messages.
    # in our case, we are just interested in showing the last AI-Human turn of the conversation for simplicity

    if len(msgs.messages) >= 2:
        last_two_messages = msgs.messages[-1:]
    else:
        last_two_messages = msgs.messages

    for msg in last_two_messages:
        if msg.type == "ai":
            with entry_messages:
                st.chat_message(msg.type).write(msg.content)

    # If user inputs a new answer to the chatbot, generate a new response and add into msgs
    if prompt:
        # Note: new messages are saved to history automatically by Langchain during run
        with entry_messages:
            # show that the message was accepted
            st.chat_message("human").write(prompt)

            # generate the reply using langchain
            response = conversation.invoke(input=prompt)

            # the prompt must be set up to return "FINISHED" once all questions have been answered
            # If finished, move the flow to summarisation, otherwise continue.
            if "FINISHED" in response['response']:
                st.divider()
                st.chat_message("ai").write("Great, I think I got all I need -- but let me double check!")

                # call the summarisation  agent
                st.session_state.agentState = "summarise"
                summariseData(testing)
            else:
                st.chat_message("ai").write(response["response"])

        # st.text(st.write(response))

