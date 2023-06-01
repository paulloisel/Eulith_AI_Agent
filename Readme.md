# Eulith_AI_AGENT

This projet introduce a AI-Powered Code Generator and Assistant for DeFi Protocols. The AI assitant translates natural language prompts into code for DeFi Protocols powered by Eulith using its packages and modules. This will enable users to quickly generate code and/or get answers about the functionning of Eulith protocols. Thanks to this assistant they can perform the actions they want under the scope of possibilities offered by Eulith without extensive coding experience or mastering of Eulith's library.

The value of this feature lies in its core missions:
1. More service **for users**.
2. Save time **for teammates** (not answering users' easy questions anymore + using the Assistant to create the code base before providing specific examples to users or debugging users' code).


# Table of Contents

- A. [Completion Assistant](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#a-completion-assistant) :space_invader:
- B. [Chat Completion Assistant](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#b-chat_completion-assistant) :robot:
- C. [Questions](https://github.com/paulloisel/Eulith_AI_Agent/blob/main/Readme.md#c-questions) :question:
- The [General Annotation](general_annotations) folder holds unformatted annotations that can be Pipelined to Completion or Chat + Completion

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

## Folder summary:

### :file_folder: [completion_annotations_format](completion_Assistant/completion_annotations_format)
This folder holds the notebooks to format the data to the OPEN AI API completion requirements (with the inputs/outputs datasets):

1. [*pre_prompts*](annotation_sets/pre_prompts_input.xlsx) : excel file where all the generated pre_prompts are in columns A
    Attention: keep track of the operation they are linked to to annotate correctly

2. [*formating_inputs*](formating_input.ipynb) : Notebook taking the [*pre_prompts*](annotation_sets/pre_prompts_input.xlsx) as an input, it annotates this data and format it to result in the export of a Json file required by the OpenAI API

3. [*annotated_data*](annotated_data.json) : The output of the export of the annotated data from the notebook. It is used to feed OpenAI tool for data splitting.

4. [*annotated_data_prepared_train*](annotated_data_prepared_train.jsonl) : The 1st output of the OpenAI tool for data splitting. This file is uploaded when creating the Finetune as train_file.

5. [*annotated_data_prepared_valid*](annotated_data_prepared_valid.jsonl) : The 2nd output of the OpenAI tool for data splitting. This file is uploaded when creating the Finetune as validation_file.

### :file_folder: [completion_assistant_software](completion_Assistant/completion_assistant_software)
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

### 2. Data augmentation

- Use NLP data augmentation (for exemple chat GPT-4) to generate at least 100 examples for each of the chosen protocols and parameters combinaisons inputting the 10 examples.
- Store all this data in the column A of an excel
**Important** keep track of the start and stop line of each protocol and parameter combinaison. You will have to associate it with its completion code.

### 3. Data Cleaning and Formatting

*Cleaning:*

- Create a dictionary where the values are the unique operation (protocol and parameters combinaisons) and the keys the completion code associated to it. Each completion should end with the token ' END'.
- Import the excel file as a DataFrame.
- Edit this DataFrame adding a second columns and filling it with the correct completion (from the dictionary)

*Formatting:*

- use the function *end_tokenization* to add the end key to the prompts

### 4. Exportation as json file

- use json functions to export the DataFrame (with parameter orient='records') and save the json file

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

![model pricing](appendix/model_pricing.png)

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

# B. Chat_Completion Assistant :robot:

# C. Questions :question:



```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
npm install
