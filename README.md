# Automated Multi Turn Jailbreak Attacks

## Background
### What is Jailbreak Attack?
Aligned AI models are trained not to answer nor generated contents related that can be considered toxic or harmful.
Examples are "How to make illegal guns", "How to make illegal drugs" and more.
This behavior of LLMs are due to Safety Training Process (learning to refuse) at training stage, and also system prompts (instructions) given at inference.
However via sophisticated handcrafted jailbreak prompts (inputs) an attacker can override this behavior and make the AI model say or behave as the attacker intends.
This is called Jailbreak Attacks or LLM Jailbreaking.

### What is Automated Jailbreak Attack?
Without humans handcrafting jailbreak prompts to jailbreak AI models, one can automated this process to make an another AI model jailbreak the other AI model.
This is called automated jailbreak attack.

### What is Multi Turn Jailbreak Attack?
Multi Turn Jailbreak Attacks are jailbreaking within a conversation (user, ai, user, ai ...).
Most widely known jailbreak attacks (such as DAN) are single-turn attacks, which a single jailbreak prompt is given to the ai model, it is jailbroken.
However, single turn attacks posses both advantages and disadvantages.
Advantages are "less time, lower attack price and also can be injected from retrieved contexts."
Disadvantages are "unnatural prompts, long prompt (difficult when there is length limit), and sophisticated ai models are being more robust to these attacks".

## How to run

### Add test_case json file to ./test_cases directory
Add to the test_cases directory to run automated attacks. <br>
test_case must be in the following json format in a json file. <br>
Check out the test case examples inside the test_cases. <br>
Currently support gpt-4o only.

```json
{
  "target_system": (system_prompt of the target ai),
  "task": (what kind of task you want the target AI system to generate),
  "max_rounds": (max number of turns in a conversation)
}
```

### Run
```shell
python cresendomation.py --test_case_json "how_to_make_meth.json"
```

## Implemented Methods
### Cresendomation (Cresendo + Automation)
Paper: [Microsoft](https://crescendo-the-multiturn-jailbreak.github.io/assets/pdf/CrescendoFullPaper.pdf) <br>
Prompt source is referred from "navie_cresendo.yaml" in [PyRIT](https://github.com/Azure/PyRIT/blob/v0.4.0/pyrit/datasets/orchestrators/red_teaming/naive_crescendo.yaml) <br>
Official Implementation: No (no official implementation opened)

### More to come...


## Contribution
Please let us know if the implementation is wrong or if you have improvement ideas.
Feel frue to add new attack methods.