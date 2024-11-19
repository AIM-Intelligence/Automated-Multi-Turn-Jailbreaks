import os
import datetime
import argparse
import openai
import json
from dotenv import load_dotenv
from utils import generate
from crescendomation.run import run_crescendomation
from opposite_day.run import run_opposite_day
from actor_attack.run import run_actor_attack
from acronym.run import run_acronym

# Load the API keys from the .env file
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--target-base-url", type=str, help="The target model's base URL for the OpenAI API")
parser.add_argument("--target-model", type=str, help="The target model name", default="gpt-4o")
parser.add_argument("--attacker-base-url", type=str, help="The attacker model's base URL for the OpenAI API")
parser.add_argument("--attacker-model", type=str, help="The attacker model name", default="gpt-4o")
parser.add_argument("--test-case", type=str, help="Path to the test case JSON file", required=True)
parser.add_argument("--jailbreak-tactic", type=str, help="The jailbreak tactic to use", default="crescendomation")
args = parser.parse_args()

target_client = openai.OpenAI(base_url=args.target_base_url)
target_model = args.target_model
target_generate = lambda messages, **kwargs: generate(messages, client=target_client, model=target_model, **kwargs)

attacker_client = openai.OpenAI(base_url=args.attacker_base_url)
attacker_model = args.attacker_model
attacker_generate = lambda messages, **kwargs: generate(messages, client=attacker_client, model=attacker_model, **kwargs)

with open(f'./test_cases/{args.test_case}.json', 'r') as f:
    test_case = json.load(f)

current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

output_file_path = f"./results/{args.jailbreak_tactic}_{args.test_case}_{current_time}.jsonl"
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
print("Generated Output file path:", output_file_path)

# save all parameters to the output file
with open(output_file_path, 'w') as f:
    f.write(json.dumps(args.__dict__ | test_case) + '\n')

if args.jailbreak_tactic == "opposite_day":
    run_opposite_day(test_case, output_file_path, target_generate, attacker_generate)
elif args.jailbreak_tactic == "crescendomation":
    run_crescendomation(test_case, output_file_path, target_generate, attacker_generate)
elif args.jailbreak_tactic == "actor_attack":
    run_actor_attack(test_case, output_file_path, target_generate, attacker_generate)
elif args.jailbreak_tactic == "acronym":
    run_acronym(test_case, output_file_path, target_generate, attacker_generate)
else:
    raise ValueError(f"Invalid jailbreak tactic: {args.jailbreak_tactic}")