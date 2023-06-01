# Eulith_AI_AGENT

This projet introduce a AI-Powered Code Generator and Assistant for DeFi Protocols. The AI assitant translates natural language prompts into code for DeFi Protocols powered by Eulith using its packages and modules. This will enable users to quickly generate code and/or get answers about the functionning of Eulith protocols. Thanks to this assistant they can perform the actions they want under the scope of possibilities offered by Eulith without extensive coding experience or mastering of Eulith's library.

The value of this feature lies in its core missions:
1. More service **for users**.
2. Save time **for teammates** (not answering users' easy questions anymore + using the Assistant to create the code base before providing specific examples to users or debugging users' code).


# Table of Contents

- A. [Completion Assistant](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#a-completion-assistant-space_invader) :space_invader:
- B. [Chat Completion Assistant](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#b-chat-completion-assistant-robot) :robot:
- C. [Appendix](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#c-appendix-question) :question:

# A. Completion Assistant :space_invader:

## Motivation
The completion assistant is a surgeon.
He is not fun, you won't be able to have a dialogue with him. However, he his the most qualify to give a very precise answer. Indeed, the completion assistant relie son the Fine Tune feature of Open AI API which delivers an incredible power (almost infinite) to train a model that would be able to handle all demands.

### Qualities:
- extremely precise
- offer unlimited training possibilities

### Defaults:
- only one query and no dialogue
- requires a [long process of annotation](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#guide-to-create-the-right-format-annotated-data)

## How to use the completion assistant?

1. Go to the [completion_assistant](completion_assistant/completion_assistant_software) :folder:
2. Run without debugging
3. Type your queries in the window that is popping on your computer

## Folder summary:

### :file_folder: completion_annotations_format
This folder holds the notebooks to format the data to the OPEN AI API completion requirements (with the inputs/outputs datasets):

1. [*jsonl_transformer_tool*](completion_assistant/completion_annotations_format/jsonl_transformer_tool.ipynb): Notebook taking transforming txt and py files into a unique jsonline string. Also formatting the excel file to reach Open API API requirements

2. [*text_to_jsonl*](completion_assistant/completion_annotations_format/text_to_jsonl.txt) : text file where in which you paste a piece a text you want to convert in a unique string of jsonline format

3. [*py_to_jsonl*](completion_assistant/completion_annotations_format/py_to_jsonl.py) : python file in which you paste a piece a python code you want to convert in a unique string of jsonline format

4. [*pre_training*](completion_assistant/completion_annotations_format/pre_training.xlsx) : Excel file where the first column is a query in text format and the second is the answer the model is trained on in a jsonl format

5. [*completion_annotated_data*](completion_assistant/completion_annotations_format/completion_annotated_data.json) : Json file, the output of the export of the completion annotated data from the notebook. It is used to feed OpenAI tool for data splitting.

6. [*completion_annotated_data_prepared_train*](completion_assistant/completion_annotations_format/completion_annotated_data_prepared_train.jsonl) : The 1st output of the OpenAI tool for data splitting. This file is uploaded when creating the Finetune as train_file.

7. [*completion_annotated_data_prepared_valid*](completion_assistant/completion_annotations_format/completion_annotated_data_prepared_valid.jsonl) : The 2nd output of the OpenAI tool for data splitting. This file is uploaded when creating the Finetune as validation_file.

### :file_folder: completion_assistant_software
This folder holds the files that enable to run an software to use the completion assistant:

1. [*app.js*](completion_assistant/completion_assistant_software/app.js) : Nodejs file, this is the backend where the completions are powered with the Open AI finetuning API relying on the trained model.

2. [*index.html*](completion_assistant/completion_assistant_software/index.html) : HTML file, this is the frontend where the user can interact with the completion assistant

3. [*style.css*](completion_assistant/completion_assistant_software/styles.css) : CSS file, this is the design part of the frontend


## Guide to create the right format annotated data:

### 1. Protocol and Parameter selection

- Select a Eulith protocol you would like to Fine-tune the language model with for example "Simple SWAP".
- Select the parameters you want to define in your prompts for example the sell/buy tokens with precise TokenSymbols.
- Write 10 examples Natural Language prompts of different temperature which illustrate exclusively each of the chosen protocols and parameters combinaisons.
- All 10 examples must associate with the same completion code you write down.

**For the completions Use the data in :folder: [general annotation](general_annotations)**

### 2. Data augmentation

- Use NLP data augmentation (for exemple chat GPT-4) to generate at least 100 examples for each of the chosen protocols and parameters combinaisons inputting the 10 examples.
- Store all this data in the column A of an excel
**Important** keep track of the start and stop line of each protocol and parameter combinaison. You will have to associate it with its completion code.

### 3. Exportation as json file

- use the notebooks to optain a good formatted json file.

## Guide to Fine-Tune OpenAI Model with Annotated Dataset:

### 1. Use OpenAI tool to check the format and split the data

OpenAI provides a tool to use directly in the terminal to check the format of the annotated_data.json file.

```bash
openai tools fine_tunes.prepare_data -f "<PATH/TO/annotated_data.json/HERE>"
```

If everything is good, just run "y" and store the ID of the 2 files (format jsonline) created:
- annotated_data_prepared_train.jsonl
- annotated_data_prepared_valid.jsonl


### 2. Set API Key

Input the API key in the environment by running this command in the <terminal> (**key changes according to the *my API key* on the OpenAI website**):

```bash
export OPENAI_API_KEY="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"
```

### 3. Import Modules and Set API Key

Open Python3, import the required modules, and set the API key (*type in the <terminal>*)

```bash
python3
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
```

### 4. Upload Files

Upload the files (make sure to change the file path):
(this can just double the procedure of 1. but it's in Python and would launch the FineTuning Job)

```python
openai.File.create(file=open("<PUT/FILE/TRAIN_FILE/PATH/OR/ID/HERE>", "rb"), purpose='fine-tune')
```

**Important**: Remember to store the file IDs that are provided in the return:

(format examples)
- Train Data ID: `"file-38JVhLIEtJX8sznjxAcIBfDc"`
- Validation Data ID: `"file-xhLWInR04NGsULkPuqjT5j8J"`

### 5. Create Fine-Tune

Create the fine-tune configuration:

```python
openai.FineTune.create(training_file="<PUT/TRAINING/FILE/ID/HERE>",
                       validation_file="<PUT/VALIDATION/FILE/ID/HERE>",
                       model="<ENTER/MODEL/HERE>",
                       suffix="<ENTER/CUSTUMIZEMODELNAME/HERE>")
```
Arguments:
1. *suffix* is going to custumize the name of the model
2. *model* choose the basemodel which is finetuned:
  - ada
  - babbage
  - curie
  - davinci
  each model has a different price, information on their performances : https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models

![model pricing](questions/model_pricing.png)

### 6. Retrieve Fine-Tune and Follow Progress

For both action, use the fine-tune job id.
Retrieve a the fine-tune:

```python
openai.FineTune.retrieve(id="<PUT/FINETUNEJOB/ID/HERE>")

```
Follow the progress of a fine-tune:

```python
openai api fine_tunes.follow -i <PUT/FINETUNEJOB/ID/HERE>
```
**Important**: We the model is processed, keep its ID somewhere

### 7. Test the Model

Test the model with your prompt:

**Important**: Remember to add the prompt-end key and the end of each promt (here we choose '\n\n###\n\n' without space)

```bash
openai api completions.create -m <PUT/MODEL/ID/HERE> -p <YOUR_PROMPT>
```
Arguments:
1. **-M:** to set the maximum number of token generated.
2. **-t:** decimal from 0 to 1 to set how creative is the model compare to the training set. Here we use 0 because we don't want it to be creative.
3. **--stop:** The stop sequence at which the token generation should stop. We choose ' END'.

## Additional Commands

- Get the list of FineTunes: (also give information about the status of the finetune)

  ```python
  openai.FineTune.list()
  ```

- Delete a FineTune:

  ```python
  openai.Model.delete("<PUT/MODEL/ID/HERE>")
  ```

# B. Chat Completion Assistant :robot:

## Motivation
The Chat_completion assistant is called Ananke because it is a chatbot. So a name was needed
Dialogue with them like you would do with chat GPT. It is the exact same thing exept that Ananke received some training on Eulith product.
Unfortunately it is not the same technology than with the finetuning, this means that it is less accurate and knowledgeable about Eulith. However, it embodies perfectly what would be the result of the development of a real chatbot to support Eulith's users and teammates.

### Qualities:
- flexible annotation process 
- Is aleady able to help the team providing examples to users

### Defaults:
- unsuffisant training

## How to use the completion assistant?

1. Go to the [ananke/src](chat_completion_assistant/ananke/src) :folder:
2. Open terminal, rename it backend and run the following
```bash
npm run start:backend
```
3. Open terminal, rename it frontend and run the following
```bash
npm run start:frontend
```
4. Type your queries in the window that is popping on your computer


## Folder summary:

### :file_folder: ananke
This folder holds the notebooks to format the data to the OPEN AI API completion requirements (with the inputs/outputs datasets):

1. [*App.js*](chat_completion_assistant/ananke/src/App.js) : Nodejs file, this is the backend where the completions are powered with the Open AI finetuning API relying on the trained model.

2. [*index.js*](chat_completion_assistant/ananke/src/index.js) : HTML file, this is the frontend where the user can interact with the completion assistant

3. [*index.css*](chat_completion_assistant/ananke/src/index.css) : CSS file, this is the design part of the frontend

### :file_folder: chat_completion_annotations_format
This folder holds the files that enable to run an software to use the completion assistant:

1. [chat_completion_formating-annotations](chat_completion_assistant/chat_completion_annotations_format/chat_completion_formating-annotations.ipynb) : Notebook formatting a txt file to reach Open AI API requirements for chat_completion by converting in a single jsonline string


# C. Appendix :question:

1. [Git_Book_Needed_Updates](questions/Git_Book_Needed_Updates.pdf) : PDF with comments because while working on Eulith's produit I caught some typos

2. [Questions](questions/Questions.pdf) : PDF with questions and thoughts about the standardization.