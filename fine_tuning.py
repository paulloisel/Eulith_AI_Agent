#Document to FineTune from an annotated dataset:

##1## input the key in the env by writing this in the terminal (the key may change)

    # export OPENAI_API_KEY="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"

##2## Opening Python3, importing modules and providing access with the key to work in the terminal

    # python3
    #import os
    #import openai
    #openai.api_key = os.getenv("OPENAI_API_KEY")

##3## Upload the files (the file path should change)

    #openai.File.create(
    #  file=open("/Users/paul/Desktop/Eulith_AI_Agent/annotated_data_prepared_valid.jsonl", "rb"),
    #  purpose='fine-tune'
    #)

# //ATTENTION// think about storing the file IDs
    #Train Data ID : "file-38JVhLIEtJX8sznjxAcIBfDc"
    #Validation Data ID : "file-xhLWInR04NGsULkPuqjT5j8J"

##4## create the fineTune
    #openai.FineTune.create(training_file="file-38JVhLIEtJX8sznjxAcIBfDc", 
    #                       validation_file = "file-xhLWInR04NGsULkPuqjT5j8J", 
    #                       model = "curie", 
    #                       suffix = "first_test")


openai.FineTune.create(training_file="file-38JVhLIEtJX8sznjxAcIBfDc", 
                       validation_file = "file-xhLWInR04NGsULkPuqjT5j8J",
                       model = "curie", 
                       suffix = "first_test")

#To delete a file from OpenAI
    #openai.File.delete("file-uaCPZnQDTZA731tewLT7uIdu")




# good fine tune id =ft-7pwAVKCj8yrBCQEhklsbjPCb

openai.Completion.create(
    model="curie",
    prompt="Swap ETH to UNI")

openai.FineTune.retrieve(id="ft-7pwAVKCj8yrBCQEhklsbjPCb")

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

openai api fine_tunes.follow -i ft-7pwAVKCj8yrBCQEhklsbjPCb

####

# test the model 

openai api completions.create -m curie:ft-personal:first-test-2023-05-05-01-50-58 -p <YOUR_PROMPT>