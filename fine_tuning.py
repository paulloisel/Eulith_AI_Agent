#Document to FineTune from an annotated dataset:

##1## input the key in the env by writing this in the terminal (the key may change)

    # export OPENAI_API_KEY="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"

##2## Opening Python3, importing modules and providing access with the key to work in the terminal

    # python3
    #import os
    #import openai
    #openai.api_key = os.getenv("OPENAI_API_KEY")

##3## Upload the files (the file path should change)

    #openai.File.create(file=open("/Users/paul/Desktop/Eulith_AI_Agent/annotated_data_prepared_train.jsonl", "rb"), purpose='fine-tune', filename = 'first_train')

# //ATTENTION// think about storing the file IDs
    #Train Data ID : "file-38JVhLIEtJX8sznjxAcIBfDc"
    #Validation Data ID : "file-xhLWInR04NGsULkPuqjT5j8J"

##4## create the fineTune
    #openai.FineTune.create(training_file="file-G9iRttjrOYn6JgakFFWIBOxT", validation_file = "file-LuK597k2hlLom5zy58kh4c9y", model = "curie", suffix = "first")


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


# Get the list of FineTune:
    # openai.FineTune.list()

# Delete FineTune:
    # openai.Model.delete("curie:ft-acmeco-2021-03-03-21-44-20")


train_1 =  "file-G9iRttjrOYn6JgakFFWIBOxT"
validation_1 = "file-LuK597k2hlLom5zy58kh4c9y"
finetune_1_2 = "ft-sflpFiRj7trZHUCQV4lL6Wec"


openai api completions.create -m curie:ft-personal:first2-2023-05-07-02-53-45 -p <YOUR_PROMPT>