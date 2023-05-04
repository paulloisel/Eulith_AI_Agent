# Eulith_AI_Agent

The files:

1. *pre_prompts* : excel file where all the generated pre_prompts are in columns A. 
    Attention: keep track of the operation they are linked to to annotate correctly

2. *formating_inputs* : Notebook taking the *pre_prompts* as an input, it annotates this data and format it to result in the export of a Json file required by the OpenAI API

3. *annotated_data* : export of the annotated data from the notebook. This feed OpenAI model directly 