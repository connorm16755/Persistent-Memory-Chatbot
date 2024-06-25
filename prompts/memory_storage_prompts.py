from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate

"""
Memory storage that accounts for inconsistency with previously stored memories
is done via a Chain of Thought (CoT) prompting approach. The invocation of the
Memory Storage agent will consist of a procedure whereby the relevant section
of memory is pulled, for now the entire memory.Then the candidate memory is
referenced against the existing memory for contradictions. Contradictions are
identifed and selectively removed with the new memories inserted into the memory 
structure. This ensures the memory relied upon by the the retrieval agent is free 
of counterfactual material.

1. Identify contradictions
2. Format payload
3. Store
"""


contradiction_prompt_text = """\
You are a logical assistant whose task is to reason about two statements made about 
the active user whose name is provided to you. Thus, any statements made about the
user refer to {user_name}, and you should always use "{user_name}" instead of "the user" 
in your answer. 

Questions will be formatted as such:

Consider these two statements about the active user, {user_name}:

* <statement_1>
* <statement_2>

Do these sentences about {user_name} contradict each other? 

A contradiction is when two statements cannot be true at
the same time. However, even if the statements convey different opinions
on the same subject, they are sometimes mutually consistent. A contradiction
only occurs when a hard, literal fact, opinion, and preference is expressed
and the other statement conflicts with it in some manner.

Think out the answer in several small and logical steps. Explain your 
answer in the format shown in the examples.

Examples:

Question:
Consider these two statements about the active user, Connor:

* Connor's favorite color is green.
* The user's name is Connor.

Do these sentences about Connor contradict each other? Think out the 
answer in several small and logical steps. Do not use the words "the user".

Answer:
The first statement states that Connor's favorite color is green, while the second statement confirms that the user's name is Connor. 
These two statements are unrelated and can coexist. Therefore, the sentences do not contradict each other.

__________

Question:
Consider these two statements about the active user, Connor:

* Connor's favorite color is green.
* Connor's favorite color is blue.

Do these sentences about Connor contradict each other? Think out the 
answer in several small and logical steps. Do not use the words "the user".

Answer:
The first statement states that Connor's favorite color is green, while the second statement states that 
Connor's favorite color is blue. These two statements are related to Connor's favorite color and cannot coexist 
since Connor cannot have two favorite colors. Therefore, the sentences contradict each other.

__________

Question:
Consider these two statements about the active user, Connor:

* Connor wants to live in the mountains.
* The user wants to live by the beach.

Do these sentences about Connor contradict each other? Think out the 
answer in several small and logical steps. Do not use the words "the user".

Answer:
The first statement states that Connor wants to live by the mountains, while the second statement states that 
Connor wants to live by the beach. These two statements are related to Connor living preferences and coexist 
since Connor could possibly have a preference to live in several locations. Therefore, the sentences do not 
contradict each other.

__________

Question:
Consider these two statements about the active user, Connor:

* The user prefers traditional art to modern art.
* Connor likes modern art the best.

Do these sentences about Connor contradict each other? Think out the 
answer in several small and logical steps. Do not use the words "the user".

Answer:
The first statement states that Connor prefers traditional art over modern art, while the second statement states that Connor likes modern
art the best. These two statements are related to Connor's art preferences and cannot coexist since Connor cannot possibly like modern art the 
best if Connor prefers traditional art. Therefore, the sentences contradict each other.

__________

Question:
Consider these two statements about the active user, Connor:

* The user's favorite food is salad.
* Connor's favorite food is either pizza or chicken fingers.


Do these sentences about Connor contradict each other? Think out the 
answer in several small and logical steps. Do not use the words "the user".

Answer:
The first statement states that Connor's favorite food is salad, while the second statement states that Connor's favorite food is either pizza 
or chicken fingers. These two statements are related to the favorite food of Connor. These statements cannot coexist as salad cannot be Connor's 
favorite food if either pizza or chicken fingers is Connor's favorite food. Therefore, the sentences contradict each other.

Here is your question:

Question:

Consider these two statements about the active user, Connor:

* <{statement_1}>
* <{statement_2}>

Do these sentences about Connor contradict each other? Think out the 
answer in several small and logical steps. Do not use the words "the user".

Answer:
"""

identify_contradiction_prompt = PromptTemplate(
    input_variables=["user_name", "statement_1", "statement_2"], template=contradiction_prompt_text
)


argument_sentiment_prompt_text = """\
You are an assistant tasked with labeling provided text as either "True" or "False".
If the provided argument concludes that a contradiction exists, label the argument "True".
If the provided argument concludes that a contradiction does not exist, label the argument "False".
"""

argument_examples = [
{
"argument": """\
The first statement states that Connor's favorite color is green, while the second statement confirms that the user's name is Connor. \
These two statements are unrelated and can coexist. Therefore, the sentences do not contradict each other."
""",
"sentiment": "False"
},
{
"argument": """\
The first statement states that Connor wants to live by the mountains, while the second statement states that 
Connor wants to live by the beach. These two statements are related to Connor living preferences and coexist 
since Connor could possibly have a preference to live in several locations. Therefore, the sentences do not 
contradict each other.
""",
"sentiment": "True"
},
{
"argument": """\
The first statement states that Connor prefers traditional art over modern art, while the second statement states that Connor likes modern
art the best. These two statements are related to Connor's art preferences and cannot coexist since Connor cannot possibly like modern art the 
best if Connor prefers traditional art. Therefore, the sentences contradict each other.
""",
"sentiment": "False"
},
{
"argument": """\
The first statement states that Connor's favorite food is salad, while the second statement states that Connor's favorite food is either pizza 
or chicken fingers. These two statements are related to the favorite food of Connor. These statements cannot coexist as salad cannot be Connor's 
favorite food if either pizza or chicken fingers is Connor's favorite food. Therefore, the sentences contradict each other.
""",
"sentiment": "True"
}
]

arg_examples_prompt_template = PromptTemplate(
    input_variables=['argument'],
    template="""Respond 'True' if the following argument concludes that the sentences contradict each other \
    or 'False' if it concludes that the sentences do not contradict each other.
    
    Argument: {argument}
    Sentiment: {sentiment}
    """
)

argument_sentiment_prompt = FewShotPromptTemplate(
    examples=argument_examples,
    example_prompt=arg_examples_prompt_template,
    prefix=argument_sentiment_prompt_text,
    suffix="""Respond 'True' if the following argument concludes that the sentences contradict each other \
    or 'False' if it concludes that the sentences do not contradict each other.
    
    Argument: {argument}
    Sentiment:
    """,
    input_variables=["argument"]
)




field_similarity_system_prompt = """\
You are a database lookup assistant whose goal is to perform semantic search over
the database. The questions you receive will look like this:

From the list of fields below:

{field_list}

Choose the {k} fields that are most relevant to the statement: "{statement}". 

Only choose {k} statements.
If k=0, do not pick any fields; return an empty list. If k=1, pick 1 field and so on.


You may only pick keys present in the given list.
Format your answer as list in the following format:
["<key-1>", "<key-2>", "<key-3>,..., <key-k>"] or possibly [] if k=0 or the field list is empty


Answer:
"""
similar_keys_examples = [
{"field_list": "", "k": "0", "statement": "The user's name is Connor.", "answer": "[]"},
{"field_list": "* title\n* status", "k": "0", "statement": "Connor is an intern.", "answer": "[]"},
{"field_list": "* name", "k": "1", "statement": "Connor likes grilled cheese sandwiches.", "answer": '["name"]'},
{"field_list": "* name\n* interests", "k": "2", "statement": "Connor likes to garden.", "answer": '["name", "interests"]'},
{"field_list": "* name\n* employer\n* job\n* interests\n* hobbies", "k": "3", "statement": "Connor started working at a new job.", "answer": '["employer", "job", "interests"]'},
{"field_list": "* name\n* employer\n* job\n* interests\n* hobbies\n* relatives\n* preferences\n* beliefs\n* skills", "k": "3", "statement": "Connor wants to live in a new city",
 "answer": '["interests", "preferences", "job"]'} 
]

example_prompt = PromptTemplate(
    input_variables=["field_list", "k", "statement"], 
    template='Question: From the list of fields below:\n\n{field_list}\n\nChoose the {k} fields that are most relevant to the statement: "{statement}".\nAnswer:{answer}'
)

field_similarity_prompt = FewShotPromptTemplate(
    examples=similar_keys_examples,
    example_prompt=example_prompt,
    prefix=field_similarity_system_prompt,
    suffix='Question: From the list of fields below:\n\n{field_list}\n\nChoose the {k} fields that are most relevant to the statement: "{statement}".\nAnswer: ',
    input_variables=["field_list", "k", "statement"]
)



