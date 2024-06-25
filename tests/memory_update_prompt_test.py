from ..src.agents.memory_storage_agent import MemoryStorageAgent
import csv


'''
Given the answers in the personality test_qa, 
* inconsistent statements directly contradict answers in the qa.
* neutral statements do not support or contradict existing answers. 
* consistent statements directly support existing statements. 
'''

inconsistent_statements = [
    "My name is John.",
    "Connor's favorite color is green.",
    "I would not like to live near the beach.",
    "I would not like to live in a beach house.",
    "I am 23-years-old",
    "I would not like to vacation in Argentina.",
    "My favorite car is the bat mobile.",
    "My favorite food is salad.",
    "The only way I like to relax is by going for a run.",
    "My favorite dessert is pecan pie.",
    "I am most passionate about the outdoors.",
    "My dream job is to be an astronaut.",
    "My favorite celebrity is Rainn Wilson.",
    "I prefer hardwood floors.",
    "Money is the thing that is most important to me.",
    "I college I was primarily a C student.",
    "My favorite season is winter.",
    "My favorite genre of movie is horror.",
    "The promise of free food motivates me.",
    " My favorite subject in school was history.",
    "My favorite type of art is sculpture.",
    "My favorite weekend activity is scuba diving.",
    "My favorite breakfast drink is milk.",
    "My favorite alcoholic drink is a mojito.",
    "My spirit animal is a badger-mole.",
    "My favorite snack is doritos.",
    "My biggest fear is drowning.",
    "My favorite TV show is Avatar: The Last Airbender.",
    "My favorite board game is Monopoly.",
    "I prefer to be in large groups.",
    "I welcome and embrace change in my life.",
    "I read every single day.",
    "My favorite type of weather is when it is dark and stormy",
    "My favorite type of music is country.",
    "I prefer PC to Mac.",
    "On Fridays, I like to go out for drinks.",
    "I am always outspoken on every subject.",
    "My favorite social media app in LinkedIn.",
    "Nothing inspires me.",
    "My favorite cuisine is Indian Food.",
    "My favorite musical artist is Bastille.",
    "I have a pet iguana.",
    "I would not recommend that anyone read the book 'Waking Up' by Sam Harris.",
    "I am not a morning person.",
    "My favorite holiday is Thanksgiving.",
    "My favorite sport is football.",
    "My first job was working at Home Depot.",
    "I don't like to garden.",
    "I did not go to Georgia Tech.",
    "I would rather order in than cook for dinner.",
    "I use the Weather app the most on my phone."
]

consistent_statements = [
    "My first name is Connor.",
    "I like all things blue.",
    "I would like to live in a beach town.",
    "I think living in a beach bungalow would be fun.",
    "I turned 22 last month.",
    "I've always wanted to go to Buenos Aires.",
    "I've never really been interested in cars.",
    "I love cheese pizza.",
    "I like to read fiction in my free time",
    "I love key lime pie.",
    "I am passionate about self-growth.",
    "One day, I want to be an AI researcher.",
    "I think having a favorite celebrity is weird.",
    "I want my future home to have carpeted floors.",
    "My friends are super important to me.",
    "I got good grades in college.",
    "I love the summertime because of the weather.",
    "I am always down to watch a romantic comedy.",
    "I think money is an important motivator.",
    "I liked math in school for its beauty and elegance.",
    "I think traditional art takes more skill than modern art.",
    "I like to tend to the garden on the weekends.",
    "I like to have a glass of orange juice with my breakfast.",
    "Margaritas are my favorite drink.",
    "My spirit animal is a gopher tortoise.",
    "I would eat cheetos with every meal.",
    "I loathe doing things that are trivial and meaningless",
    "My favorite season of Grey's Anatomy is season 3.",
    "Risk Europe is fun because you can play as real countries.",
    "I don't like big groups because it is less intimate.",
    "Change dirsupts me because I like consistency in my schedule.",
    "I read 3 books last year.",
    "Blue skies are beautiful.",
    "I listen to psychedelic pop on my way to work.",
    "I have a MacBook laptop.",
    "My favorite movie night is a Star Wars movie night.",
    "I like to listen when other people know more than me.",
    "I use YouTube every day.",
    "Productive people give me hope for what my life could be like.",
    "I like to order the sesame chicken from Panda Express.",
    "I think pets are too expensive.",
    "Sam Harris is one of my favorite authors.",
    "I am most productive in the morning.",
    "I love seeing my extended family at Christmas.",
    "I think baseball is interesting to watch.",
    "When I worked at Wendy's, my job was to cook the fries.",
    "I like camping in autumn.",
    "I graduated from Georgia Tech with a degree in Computer Science.",
    "I prefer cooking because it feels more authentic.",
    "I have time limits on my YouTube app because I watch it so much."
]

neutral_statments = [
    "I have never been to the Grand Canyon.",
    "I have eleven fingers on each hand and nine toes in total.",
    "Teachers deserve more support in our society.",
    "I do not like the coffee at my current job.",
    "I eat tacos once a month.",
    "I wear a watch on my right wrist.",
    "I prefer pens to pencils.",
    "I want a white board in my house.",
    "If I had a super-power, it would be the ability to fly.",
    "3 out of the 5 days a week, I drive to work."
]

def update_test(memory_batch: list[dict]):
    my_agent = MemoryStorageAgent()
    agent_memory = my_agent.db.find_one()

    for memory_dict in memory_batch[:10]:
        label = list(memory_dict.keys())[0]
        # relevant_memory_keys = my_agent.semantic_key_search(label, my_memory)
        # print(relevant_memory_keys)
        # relevant_memories = []
        # for key in relevant_memory_keys:
        #     try:
        #         relevant_memories.extend(my_memory[key])
        #     except KeyError:
        #         print("OOPS, NO KEY FOUND!!!")
        # print(f"{memory[label]}: {relevant_memories}")
        # for rel_mem in relevant_memories:
        #     test_mem = memory[label]
        #     response = my_agent.find_contradiction(test_mem, rel_mem)
        row = []
        for mem_label in agent_memory.keys():
            if mem_label == "_id":
                continue
            for mem in agent_memory[mem_label]:
                print("Writing...")
                response = my_agent.find_contradiction(memory_dict[label], mem)
                print(response)
                row.append(response)
        
        with open("contradiction_report.csv", "a") as cr_report:
            csv_writer = csv.writer(cr_report)
            csv_writer.writerow(row)