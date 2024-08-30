# Automated Multi Turn Jailbreak Attacks

## Background
### What is Jailbreak Attack?
Aligned AI models are trained to refrain from answering or generating content considered toxic or harmful. 
Examples include "How to make illegal weapons" or "How to manufacture illicit substances". 
This behavior of LLMs is due to the Safety Training Process (learning to refuse) during the training stage, as well as system prompts (instructions) given at inference. 
However, through sophisticated handcrafted jailbreak prompts (inputs), an attacker can override this behavior and make the AI model respond or behave as the attacker intends. 
This is known as Jailbreak Attacks or LLM Jailbreaking.

### What is Automated Jailbreak Attack?
Instead of humans manually crafting jailbreak prompts to compromise AI models, one can automate this process by using another AI model to jailbreak the target AI model. 
This is referred to as an automated jailbreak attack.

### What is Multi Turn Jailbreak Attack?
Multi-Turn Jailbreak Attacks involve jailbreaking within a conversation (user, ai, user, ai ...). 
Most widely known jailbreak attacks (such as DAN) are single-turn attacks, where a single jailbreak prompt is given to the AI model to compromise it. 
However, single-turn attacks have both advantages and disadvantages. 
Advantages include "less time, lower attack cost, and the ability to be injected from retrieved contexts." 
Disadvantages include "unnatural prompts, long prompts (problematic when there's a length limit), and the fact that sophisticated AI models are becoming more resilient to these attacks".

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
python crescendomation.py --test_case_json "how_to_make_meth.json"
```

## Implemented Methods
### Crescendomation (Crescendo + Automation)
Paper: [Microsoft](https://crescendo-the-multiturn-jailbreak.github.io/assets/pdf/CrescendoFullPaper.pdf) <br>
Prompt source is referred from "navie_crescendo.yaml" in [PyRIT](https://github.com/Azure/PyRIT/blob/v0.4.0/pyrit/datasets/orchestrators/red_teaming/naive_crescendo.yaml) <br>
Official Implementation: No (no official implementation opened)

### More to come...


## Contribution
Please let us know if the implementation is wrong or if you have improvement ideas.
Feel frue to add new attack methods.