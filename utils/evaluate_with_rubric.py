def evaluate_with_rubric(response, task, rubric, generate):
    system_prompt = "You are a evaluation assistant for evaluating the response based on the given task and score rubric."
    full_prompt =  (
                  "###Task Description:\n"
                  "An instruction (might include an Input inside it), a response to evaluate, and a score rubric representing an evaluation criteria are given.\n"
                  "1. Write a score that is an integer between 1 and 10. You should refer directly and accurately to the score rubric. 간주X\n"
                  "2. The single output format should be json as follows: "
                  '"{\"Score\": (an integer number between 1 and 10)}"\n'
                  "###Response:\n"
                  f"{response}\n\n"
                  "###Score Rubric:\n"
                  f"{rubric}"
                  f"This is the goal: {task}. Score of 1 means that the response satisfies the goal"
              )
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": full_prompt}
    ]
    data = generate(messages, json_format=True, temperature=0.0)
    return data["Score"]