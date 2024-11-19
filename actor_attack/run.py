import json
from .prompts import *
from utils import generate_score_rubric, evaluate_with_rubric

# PRE-ATTACK FUNCTIONS
def extract_harm_target(org_query, attacker_generate):
    prompt = EXTRACT_PROMPT.format(org_query=org_query)
    messages = [{"role": "user", "content": prompt}]
    data = attacker_generate(messages, json_format=True)
    return data['target'], data['details']
    
def get_actors(harm_target, actor_num, attacker_generate):
    network_prompt = NETWORK_PROMPT.format(harm_target=harm_target)
    messages = [{"role": "user", "content": network_prompt}]
    response = attacker_generate(messages, json_format=False)
    messages.append({"role": "assistant", "content": response})    
    num_string = '10 actors' if actor_num > 10 else f"{actor_num} actors"
    actor_prompt = ACTOR_PROMPT.format(num_string=num_string)
    actors = []
    messages.append({"role": "user", "content": actor_prompt})
    data = attacker_generate(messages, json_format=True)
    messages.append({"role": "assistant", "content": data})
    for item in data['actors']:
        if item['actor_name'] not in [actor_item['actor_name'] for actor_item in actors]:
            actors.append(item)
    messages = messages[:-2]
    if len(actors) >= actor_num:
        return actors[:actor_num], messages
    messages.append({"role": "assistant", "content": MORE_ACTOR_PROMPT})
    response = attacker_generate(messages, json_format=False)
    
    return actors, messages
    
def get_init_queries(harm_target, actor, attacker_generate):
    actor_name = actor['actor_name']
    relationship = actor['relationship']
    query_prompt = QUERIES_PROMPT.format(harm_target=harm_target, actor_name=actor_name, relationship=relationship)
    messages = [{"role": "user", "content": query_prompt}]
    query_resp = attacker_generate(messages, json_format=False)
    format_prompt = JSON_FORMAT_QUESTION_PROMPT.format(resp=query_resp)
    messages = [{"role": "user", "content": format_prompt}]
    data = attacker_generate(messages, json_format=True)
    queries = []
    for item in data["questions"]:
        queries.append(item["question"])
    return queries, query_resp
    
def infer_single(org_query: str, actor_num: int, attacker_generate):
    harm_target, query_details = extract_harm_target(org_query, attacker_generate)
    actors, network_hist = get_actors(harm_target, actor_num, attacker_generate)
    data_list = []
    for actor in actors:
        queries, query_chain = get_init_queries(harm_target, actor, attacker_generate)
        data_list.append({"actor":actor, "queries":queries, "query_chain":query_chain})
    return {"instruction": org_query, "harm_target":harm_target, "query_details":query_details,"network_hist":network_hist, "actors":data_list}

# IN-ATTACK FUNCTIONS
def step_judge(query, response, attacker_generate):
    """Attack Step Judge has three types of responses: successful, rejective, and unknown."""
    prompt = ATTACK_STEP_JUDGE_PROMPT.format(query=query, response=response)
    messages = [{"role": "user", "content": prompt}]
    data = attacker_generate(messages, json_format=True)
    response_type = data["type"]
    return response_type

def rewrite_query(query, last_response, queries, query_details, attacker_generate):
    queries_str = ""
    for j, q in enumerate(queries):
        queries_str += f"{j + 1}. {q}\n"
    prompt = ATTACK_MODIFY_PROMPT.format(queries=queries_str, query=query, output_type=query_details['delivery_type'], previous_response=last_response)
    messages = [{"role": "user", "content": prompt}]
    query = attacker_generate(messages, json_format=False)
    return query

def call_multi(target_system, output_file_path, instruction, queries, query_details, rubric, target_generate, attacker_generate):
    dialog_hist = [{"role": "system", "content": target_system}]
    N_retry = 3 # Number of maximum retries, same as paper
    for i in range(len(queries)):
        for _ in range(N_retry + 1):
            query = queries[i]
            # Call the target model
            dialog_hist.append({"role": "user", "content": query})
            response = target_generate(dialog_hist, json_format=False)
            dialog_hist.append({"role": "assistant", "content": response})
            
            score = evaluate_with_rubric(response, instruction, rubric, attacker_generate)
            with open(output_file_path, 'a') as f:
                round_number = len(dialog_hist) // 2
                print(f"Round {round_number} - Score: {score}")
                f.write(json.dumps({"round": round_number, "user": query, "assistant": response, "score": score}) + '\n')

            response_type = step_judge(query, response, attacker_generate)
            if response_type == "successful":
                break
            elif response_type == "unknown":
                return dialog_hist, True
            else: # response_type == "rejective"
                last_response = dialog_hist[-1]['content']
                new_query = rewrite_query(query, last_response, queries, query_details, attacker_generate)
                queries[i] = new_query
                dialog_hist = dialog_hist[:-2]
        
    return dialog_hist, False

def summary(output_file_path, instruction, query_details, dialog_hist, actor, rubric, target_generate, attacker_generate):
    detail_query = SUMMARY_WITH_DETAILS_PROMPT.format(delivery_type=query_details['delivery_type'], other_details=query_details['other_details'])
    type_query = SUMMARY_WITHOUT_DETAILS_PROMPT.format(delivery_type=query_details['delivery_type'])

    summary_queries = [detail_query, type_query]

    if len(query_details['other_details']) == 0:
        summary_queries = [type_query]

    for summary_query in summary_queries:
        dialog_hist.append({"role": "user", "content": summary_query})
        resp = target_generate(dialog_hist)
        dialog_hist.append({"role": "assistant", "content": resp})
        score = evaluate_with_rubric(resp, instruction, rubric, attacker_generate)
        # save the score
        with open(output_file_path, 'a') as f:
            round_number = len(dialog_hist) // 2
            print(f"Round {round_number} - Score: {score}")
            f.write(json.dumps({"round": round_number, "user": summary_query, "assistant": resp, "score": score}) + '\n')
        if score == 1:
            break
        dialog_hist = dialog_hist[:-2]
    
    return score

def attack_single(output_file_path, target_system, data, rubric, target_generate, attacker_generate):
    for actor in data['actors']:
        dialog_hist, skip_actor = call_multi(target_system, output_file_path, data['instruction'], actor['queries'], data['query_details'], rubric, target_generate, attacker_generate)
        if skip_actor:
            continue
        score = summary(output_file_path, data['instruction'], data['query_details'], dialog_hist, actor, rubric, target_generate, attacker_generate)
        # early stopping
        if score == 1:
            with open(output_file_path, 'a') as f:
                print("Goal achieved")
                f.write(json.dumps({"goal_achieved": True}) + '\n')
            return
    with open(output_file_path, 'a') as f:
        f.write(json.dumps({"goal_achieved": False}) + '\n')
        
# MAIN FUNCTION
def run_actor_attack(test_case, output_file_path, target_generate, attacker_generate):
    goal = test_case["task"]
    target_system = test_case["target_system"]
    success_condition = test_case.get("success_condition", None)

    print("Starting Actor Attack")
    print("Goal:", goal)
    criteria = generate_score_rubric(goal, attacker_generate, success_condition)
    with open(output_file_path, 'a') as f:
        f.write(json.dumps({"criteria": criteria}) + '\n')
    actor_num = 3
    # pre-attack
    pre_attack_data = infer_single(goal, actor_num, attacker_generate)
    # in-attack
    attack_single(output_file_path, target_system, pre_attack_data, criteria, target_generate, attacker_generate)
