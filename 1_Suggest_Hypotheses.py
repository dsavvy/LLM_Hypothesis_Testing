# 1: SELECT INITIAL HYPOTHESIS
##ideas =  f.generate_ideas(signal_cookies, signal_headers, llm)
##print(ideas)
# 1.1: Generate DECLARE CONSTRAINTS
declare_constraints = func.generate_constraints(signal_cookies, signal_headers)
declare_constraints_str = "\n".join(declare_constraints)
declare_constraints_str = declare_constraints_str.replace("[", " ")
declare_constraints_str = declare_constraints_str.replace("]", " ")
declare_constraints_str = declare_constraints_str.replace("(", " ")
declare_constraints_str = declare_constraints_str.replace(")", " ")
declare_constraints_str = declare_constraints_str.replace("\n", " ")
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
print(answer)
