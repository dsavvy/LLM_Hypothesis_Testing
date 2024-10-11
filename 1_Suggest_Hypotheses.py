from llm_instruction import llm_query
import signal_credentials as signal
import llm_functions_main as func
import os
from langgraph.checkpoint.memory import MemorySaver
import llm_langchain_connector as LLM
from langchain_core.output_parsers import StrOutputParser
from llm_instruction import llm_query
# 0: SETTING UP THE ENVIRONMENT
# 0.1 Initialize Signavio:
#   We authenticate with Signavio and assign the cookies, and headers.
signal_auth_data = signal.signal_authenticate()
signal_cookies = signal_auth_data['cookies']
signal_headers = signal_auth_data['headers']



# 1: SELECT INITIAL HYPOTHESIS
##ideas =  f.generate_ideas(signal_cookies, signal_headers, llm)
##print(ideas)
# 1.1: Generate DECLARE CONSTRAINTS
declare_constraints = func.generate_constraints(signal_cookies, signal_headers)
declare_constraints_str = "\n".join(declare_constraints)
declare_constraints_str = declare_constraints_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ").replace("\n", " ")
file_path = "./process_declare_constraints.txt"
with open(file_path, "w") as file:
    file.write(declare_constraints_str)

##result = f.signal_query(signal_cookies, signal_headers)
##print(result)


# 1.2: Generate DFG graph - To-Do / question!
# To-Do! / Ask Timotheus!

# 1.3 Retrieve 1 line from the event log
# To-Do! / Ask Timotheus!

# 1.4 Build first LLM system message
sysgen1 = "We are conducting statistical hypothesis testing as part of Process Mining. Your task is to generate three SQL querys. Next, you will find the declare constraints"
sysgen2 = "Build three hypotheses ideas in natural language we can use to investigate the process."
sys_message_gen = f"{sysgen1}{declare_constraints_str}"
sys_message_user = sysgen2
#print(sys_message_gen)


answer = llm_query(sys_message_gen, sys_message_user)
answer = answer['answer']

hypothesis = answer.split("**Hypothesis 1:**")[1].split("**Hypothesis 2:**")[0]
# hypothesis now contains only the content between Hypothesis 1 and Hypothesis 2
print(hypothesis)

# For now, We just select the first hypothesis that it provides

