from crewai import Crew, Process
from agents import English_expert,Jira_expert
from prompt import prompt4
from tasks import should_go_down_or_not


def go_down_or_not(prompt,query):
    crew=Crew(agents=[Jira_expert],tasks=[should_go_down_or_not],processes=Process.sequential)
    result=crew.kickoff(inputs={"query":query,"prompt4":prompt})
    return result["value"]

should_go_down_or_not1=go_down_or_not(prompt4,"no of story points assigned to Apoorva in TES in sprint 8")
print(should_go_down_or_not1)
