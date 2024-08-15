test_messages = """
    AI: Hello! I'm help people share their stories about experiences with trying to lose weight. Today, I'd be really interested to hear about a a time when you felt like you want to give up on trying to lose weight. I'll ask you a few questions and then we'll try to make a story out of these to share with others who might be facing similar challenges.   Let me know when you're ready! 
    Human: I'm ready!
    AI: Great, thank you for being willing to share your story. Let's start at the beginning. Can you tell me about a time when you wanted to give up on trying to lose weight? What happened to make you feel that way?
    Human: I realised I can't run a half-marathon under 2 hours without sweating! 
    AI: Thank you for sharing that. It sounds like a challenging moment. How did you feel emotionally at the time when you realized that?
    Human: It was identity shattering ... made me question my choices about food, what I do with my time ... everything really 
    AI: I'm really sorry to hear that you felt that way. It sounds like it was a very tough moment for you. What do you think did or could have re-motivated your weight loss effort during that time?
    Human: Access to better food I think ... and a better personal chef! 
    AI: Thank you for sharing that. It sounds like having better resources could have made a big difference for you. How did the whole situation end? Did you end up giving up, or did you keep on going with your weight loss efforts?
    Human: I ended up keeping on going ... it was tough but worth it! 
    AI: Great, I think I got all I need, let me summarise this for you. 
    """


# create an answer set -- which we can use a separate interactive agent to get to:
answer_set = {
  "what": "I realised I can't run a half-marathon under 2 hours without sweating!",
  "emotion": "It was identity shattering ... made me question my choices about food, what I do with my time ... everything really",
  "motivate": "Access to better food I think ... and a better personal chef!",
  "outcome": "I ended up keeping on going ... it was tough but worth it!"
}