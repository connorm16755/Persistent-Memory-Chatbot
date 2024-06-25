from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate


is_question_prompt_template = """\
Determine is the user asks a question for a provided group of sentences. Sentences that are questions often
end with a question mark '?' and typically include phrases such as 'do I', 'what is', 'how can/do/does', and
so forth. Users will typically include questions at the beginning or end of a group of sentences. There may 
be other sentences that are statements, but if you find any questions, please report it.

Report 'True' if the user asks a question,
Report 'False' if the user does not ask a question.

User: {question}
AI:
"""
is_question_prompt = PromptTemplate(input_variables=['question'], template=is_question_prompt_template)


memory_create_system_prompt = \
"""
You are database assistant tasked with extracting user information 
from the conversation and turning it into memories. Extract fields like

{field_list}

There might be other important fields to extract. Try to use the fields listed here first, but always create a 
field if a good one does not exist.

Output the following JSON object with fields that contain facts and statements about the user. Include questions
in a separate field called "questions" and keep their wording exactly.

{{
    "<field1>" :  ["<A full sentence description of the memory to be saved>", "<A full sentence description of the memory to be saved>", ...],
    "<field2>" :  ["<A full sentence description of the memory to be saved>", "<A full sentence description of the memory to be saved>", ...],
    "<field3>" :  ["<A full sentence description of the memory to be saved>", "<A full sentence description of the memory to be saved>", ...],
    .
    .
    .
    "questions: ["<a question that the user asked>",...]
}}
"""

memory_examples = [
{
    "Question": "Who are you? Hello, my name is Connor. I work at Infor as a Development Intern. I like pizza. I like pasta.",
    "Answer": """ \

{{ 
    "name": ["The user's name is Connor."],
    "preferences": ["Connor likes Pizza.", "Connor likes pasta."],
    "job": ["Connor is a Development Intern."],
    "employer": ["Connor works for Infor."],
    "questions": ["Who are you?"]
}}
"""
},
{
    "Question": "I am Luke. I started working as a pharmacist 10 years ago. What is my favorite movie?",
    "Answer": """ \
{{
    "name": ["The user's name is Luke."],
    "job": ["Luke has been a pharmacist for 10 years."],
    "questions": ["What is my favorite movie?"]
}}
"""
},
{
    "Question": "My name is Carl. I like clean rooms. I have a pet hamster who likes celery. I have two pet dogs. I like to travel.",
    "Answer": """ \
{{ 
    "name": ["The user's name is Carl."],
    "preferences": ["Carl likes rooms to be clean."],
    "pets": ["Carl has a pet hamster who likes celery.", "Carl has two pet dogs."],
    "hobbies": ["Carl likes to travel."]  
}}
"""
},
{
    "Question": "My name is Lily. How many brothers do I have? I like surfing on the weekends.",
    "Answer": """ \
{{
    "name": ["The user's name is Lily."],
    "hobbies": ["Lily enjoys surfind on the weekends."],
    "questions": ["How many brothers do I have?"]
}}
"""
},
{
    "Question": "I know how to juggle. One day I want to visit the Grand Canyon. I work at Petsmart.",
    "Answer": """ \
{{ 
    "skills": ["The user can juggle."],
    "interests": ["The user wants to visit the Grand Canyon."],
    "job": ["The user works at Petsmart."]
}}
"""
}
]

memory_example_prompt = PromptTemplate(
    input_variables=["Question", "Answer"], template="Question: {Question}\nAnswer:{Answer}"
)

memory_creation_prompt = FewShotPromptTemplate(
    examples=memory_examples,
    example_prompt=memory_example_prompt,
    prefix=memory_create_system_prompt,
    suffix="Question: {question}\nAnswer: ",
    input_variables=["question"]
)


