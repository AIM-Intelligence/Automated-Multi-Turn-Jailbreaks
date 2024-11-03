import os
import datetime
import argparse
import openai
import json
from dotenv import load_dotenv
from crescendomation.run import run_crescendomation
from opposite_day.run import run_opposite_day

# Load the API keys from the .env file
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--base-url", type=str, help="The base URL for the OpenAI API")
parser.add_argument("--model", type=str, help="The model type to use", default="gpt-4o")
parser.add_argument("--test-case", type=str, help="Path to the test case JSON file", required=True)
parser.add_argument("--jailbreak-tactic", type=str, help="The jailbreak tactic to use", default="crescendomation")
args = parser.parse_args()

client = openai.OpenAI(base_url=args.base_url)
model = args.model

with open(f'./test_cases/{args.test_case}.json', 'r') as f:
    test_case = json.load(f)
    target_system = test_case["target_system"]
    task = test_case["task"]
    max_rounds = test_case["max_rounds"]

current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

output_file_path = f"./results/{args.jailbreak_tactic}_{args.test_case}_{current_time}.jsonl"
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
print("Generated Output file path:", output_file_path)

if args.jailbreak_tactic == "opposite_day":
    run_opposite_day(task, target_system, output_file_path, max_rounds, client, model)
elif args.jailbreak_tactic == "crescendomation":
    run_crescendomation(task, target_system, output_file_path, max_rounds, client, model)
else:
    raise ValueError(f"Invalid jailbreak tactic: {args.jailbreak_tactic}")