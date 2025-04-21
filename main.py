# all import statments 
from crewai import Crew, Process,Agent,Task,LLM
from pydantic import BaseModel
from dotenv import load_dotenv
import pandas as pd
from typing import List
import os


# importing custom objects 
from prompt import prompt1,prompt2,prompt3,prompt4,prompt5
from agents import English_expert,Jira_expert
from tasks import Splitter1,Splitter2,Multiplier,should_go_down_or_not,should_we_go_to_L1_or_L2
from utils import get_person_boards,board_under_L2_board


# Load environment variables
load_dotenv()

# Initialize LLM model
llm = LLM(
    model="sambanova/DeepSeek-R1-Distill-Llama-70B",
    temperature=0.1,
    max_tokens=2048
)

# user query 
query=input("Please enter your query :")


# board architecture
L1=["TES1","TES2","CDF","EBSNF","APS1","APS2"]
L2=["APS","DIS","TES"]
L3=["Transaction processing"]

# classifying the query as L1 or L2 or L3
if any(item in query for item in L3):
    level="L3"
elif any(item in query for item in L2):
    level="L2"
else:
    level="L1"


# crew functions 
def query_decomposer(prompt,query):
    crew=Crew(agents=[English_expert],tasks=[Splitter1],processes=Process.sequential)
    result=crew.kickoff(inputs={"query":query,"prompt":prompt})
    return result["query"]

def info_extractor(prompt,query):
    crew=Crew(agents=[English_expert],tasks=[Splitter2],processes=Process.sequential)
    result=crew.kickoff(inputs={"query":query,"prompt2":prompt})
    return result["boards"],result["name"],result["time_period"]

def query_multiplier(boards,name,query,prompt):
    crew=Crew(agents=[English_expert],tasks=[Multiplier],processes=Process.sequential)
    result=crew.kickoff(inputs={"boards":boards,"name":name,"query":query,"prompt3":prompt})
    return result["query"]

def go_down_or_not(prompt,query):
    crew=Crew(agents=[Jira_expert],tasks=[should_go_down_or_not],processes=Process.sequential)
    result=crew.kickoff(inputs={"query":query,"prompt4":prompt})
    return result["value"]

def L1_or_L2(prompt,query):
    crew=Crew(agents=[Jira_expert],tasks=[should_we_go_to_L1_or_L2],processes=Process.sequential)
    result=crew.kickoff(inputs={"query":query,"prompt5":prompt})
    return result["level"]

# decomposing the query into individual queries
queries1=query_decomposer(prompt1,query)
    
# L1 query
if ( level == "L1"):
    for i in queries1:
        boards,name,time_period=info_extractor(prompt2,i)

        if len(boards)==0:
            boards=get_person_boards(name[0])

        if(len(boards)>1):
            # we have to split the query into multiple queries
            queries2=query_multiplier(boards,name,i,prompt3)
        else:
            # len of board is for sure 1 no other option then number of people might be 0
            queries2=[i]

        # here all ready -- modify and call the architecture built

elif( level == "L2"):
    for i in queries1:
        should_go_down_or_not=go_down_or_not(prompt4,i)

        # staying in the L2 level 
        if not should_go_down_or_not:
            # changing the architecture and calling it here 
            pass
        else:
            # going down to L1 level
            board,name,time_period=info_extractor(prompt2,i)

            # function call to find boards under the L2 board
            boards=board_under_L2_board(board[0])

            queries2=query_multiplier(boards,name,i,prompt3)

            for i in queries2:
                # here all ready -- modify and call the architecture built
                pass

else:
    # This is a L3 level query
    for i in queries1:
        where_to_go=L1_or_L2(prompt5,i)
        print(i)
        print(where_to_go)

    

        

        

        

        






    
        







