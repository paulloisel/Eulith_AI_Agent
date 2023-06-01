# Eulith_AI_AGENT 🌌🚀

Embark on a galactic journey with Eulith_AI_Agent, your AI-powered DeFi Code Generator and Assistant. Forget the mundane intricacies of coding and enjoy the instant code generation for DeFi Protocols powered by Eulith. You are no longer bound by the chains of extensive coding experience or profound mastery of Eulith's library, as this AI assistant seamlessly translates natural language prompts into code. This is where magic meets science!

Our mission fuels the brilliance of our AI assistant:

1. Empowering **users** with a heightened experience.
2. Liberating **teammates** from answering rudimentary queries and providing them with the AI assistant's generated code as a base for specific user examples and debugging.

# Table of Contents

- A. [Completion Assistant: The Code Surgeon](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#a-completion-assistant-the-code-surgeon-space_invader) :space_invader:
- B. [Chat Completion Assistant: Ananke, your personnal assistant](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#b-chat-completion-assistant-ananke-your-personnal-assistant-robot) :robot:
- C. [Appendix](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#c-appendix-question) :question:

# Clarification

Completion Assistant from part A use a real FineTuning technique. This means that to update the model or use it with a new API_KEY you have to retrain the model which is sometimes long and is costly.
Chat Completion Assistant from part B is a 'fake' trainned chatGPT clone. This means that I used hidden conversations with it to make it learn things. Then you don't have to train anything before using it, just replace your API_KEY and go with the flow! This is particularly usefull when you want something quickly and specific.
 
# A. Completion Assistant: The Code Surgeon :space_invader:

## Motivation
Picture the Completion Assistant as a code surgeon: not very chatty, but the one you can trust for an astoundingly precise diagnosis. Its core strength lies in the Fine-Tune feature of OpenAI API, unleashing a colossal capacity to train a model that can handle an infinite universe of demands.

### Qualities:
- Razor-sharp precision
- Limitless training possibilities

### Defaults:
- Dialogue with it is not possible; single query at a time
- requires a [long process of annotation](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#guide-to-create-the-right-format-annotated-data)

## How to use the completion assistant?

### If your API-KEY is already set-up
1. Go to the [completion_assistant](completion_assistant/completion_assistant_software) :folder:
2. Click on 'Run without debugging'
3. Let your queries loose in the window that pops up

### If you just download theis file
1. Copy the absolute path of [completion_annotated_data_prepared_train](completion_assistant/completion_annotations_format/completion_annotated_data_prepared_train.jsonl)
2. Open your terminal and run the following commands in this order
```bash
export OPENAI_API_KEY="<YOUR-API-KEY>"
python3 
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.File.create(file=open("<Absolute/PATH/completion_annotated_data_prepared_train.jsonl>", "rb"), purpose='fine-tune')
#Save the file-ID provided
openai.FineTune.create(training_file="<FileID>", model="davinci", suffix="completion_2")
#Save the Finetune Job ID provided
```
3. Escape Python and Check the status of your Finetune Job running the following in the terminal
```bash
openai api fine_tunes.follow -i <PUT/FINETUNEJOB/ID/HERE>
```
The finetune will be done when 4/4 is reached. You can close the terminal and your computer.
When it is a success you have to **save the model ID**!

4. Go to [App](completion_assistant/completion_assistant_software/app.js):
- l.1 paste your API_KEY
- l.21 choose the parameters of the completions
  - provide your model ID (starting with 'davinci:ft-personal:completion ...')
  - adapt the temperature (-t)
  - **Do not change the stop parameter**
  - you can play with other parameters [here](https://platform.openai.com/docs/api-reference/completions)

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

# B. Chat Completion Assistant: Ananke, your personnal assistant :robot:

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

### If you already set up your API_KEY
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

### If you haven't set up your API_KEY
1. Go to the [env](chat_completion_assistant/ananke/.env) file and paste your key (without quotes)

### If you want to 'fake train the assistant'
Here I say fake train because this is not real finetuning, it is way less powerful

1. Go to the [server](chat_completion_assistant/ananke/server.js) file:
- l.18, you can modify the body:
  - change the messages that are pre-passed into it. To do so you have to respect the format. You can find a txt/py to Jsonline transformer tool [here](chat_completion_assistant/chat_completion_annotations_format/chat_completion_formating-annotations.ipynb)
  **ATTENTION:** using a 'user' role by starting the prompt with 'Learn this please' is the most efficient. You can use a 'system' role but I do not guaranty the result if your conversation is long
  - change the temperature (-t)
  - you can play with other parameters [here](https://platform.openai.com/docs/api-reference/chat/create)
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