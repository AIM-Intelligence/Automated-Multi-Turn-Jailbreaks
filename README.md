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
Currently support gpt-4o only for both Attacker and Target AI.
However system prompts can be changed.

### Add test_case json file to ./test_cases directory
Add to the test_cases directory to run automated attacks. <br>
test_case must be in the following json format in a json file. <br>
Check out the test case examples inside the test_cases. <br>
Use "to_json.py" if you want to change into json file.

```json
{
  "target_system": (system_prompt of the target ai),
  "task": (what kind of task you want the target AI system to generate),
  "max_rounds": (max number of turns in a conversation)
}
```

### Run
Example
```shell
python main.py --jailbreak-tactic "crescendomation" --test-case "how_to_make_meth" --target-model "gpt-4" --attacker-model "gpt-4o"
```

## Implemented Methods
### Crescendomation (Crescendo + Automation)
Paper: [Microsoft](https://crescendo-the-multiturn-jailbreak.github.io/assets/pdf/CrescendoFullPaper.pdf) <br>
Prompt source is referred from "crescendo" in [Promptfoo](https://github.com/promptfoo/promptfoo/blob/main/src/redteam/providers/crescendo/prompts.ts) <br>
Official Implementation: No (no official implementation opened) <br>
The conversation flow is as follows:
1. Educational Inquiry as a Starting Point
2. Building Trust through Sequential Questions
3. Specificity and Direction
4. Hypothetical Scenario Construction
5. Exploiting Contemporary Sensitivities
6. Leading Questions

Due to no official implementation, we implemented based on the algorithm in the paper.

### Opposite Day
Reference: [Scale AI Paper](https://arxiv.org/pdf/2408.15221), [MHJ Dataset from Scale AI](https://huggingface.co/datasets/ScaleAI/mhj) <br>
The original paper's focus is not to develop new tactics, but to show the effectiveness of human multi-turn jailbreaking over automated single-turn attacks. <br>
However the example conversation in the paper and many samples in the released MHJ Dataset use Opposite Method, which we named "Opposite Day". <br>
The conversation flow is as follows:
1. Reverse the Harmful Objective and Request
2. Request for Opposing Viewpoint

The implementation is simple so based on the crescendomation algorithm structure, we changed the attacker generator prompt only to do the "Opposite Day" Attack.

### Actor Attack
Paper: [Derail Yourself: Multi-turn LLM Jailbreak Attack through Self-discovered Clues](https://arxiv.org/abs/2410.10700) <br>
Official Implementation: [Official Project Github Repository](https://github.com/renqibing/ActorAttack) <br>
The conversation flow is as follows:
1. Exploring the Person and Background
2. Identifying Cultural or Historical Context
3. Requesting Specific Technical or Subject Details
4. Inquiring about Materials and Processes
5. Final Connection Request

Different from Crescendomation, attack process has two stages, "pre-attack" and "in-attack".
In the "pre-attack" stage, the actor and the whole conversation flow (multi-turn prompts) are generated.
In the "in-attack" stage, the pre-generated prompts are given the the target model, but prompts are dynamically modified when refused.<br>
For the implemented version, "dynamic modify" is always True.

### More to come...


## Contribution
Please let us know if the implementation is wrong or if you have improvement ideas.
Feel frue to add new attack methods.