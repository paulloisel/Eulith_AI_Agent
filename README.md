# Eulith_AI_Agent

The files:

1. *pre_prompts* : excel file where all the generated pre_prompts are in columns A. 
    Attention: keep track of the operation they are linked to to annotate correctly

2. *formating_inputs* : Notebook taking the *pre_prompts* as an input, it annotates this data and format it to result in the export of a Json file required by the OpenAI API

3. *annotated_data* : export of the annotated data from the notebook. This feed OpenAI model directly 


# Fine-Tuning OpenAI Model with Annotated Dataset

This README file provides a step-by-step guide on how to use OpenAI for fine-tuning using an annotated dataset.

## 1. Set API Key

Input the API key in the environment by running this command in the <terminal> (**key changes according to the *my API key* on the OpenAI website**):

```bash
export OPENAI_API_KEY="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"
```

## 2. Import Modules and Set API Key

Open Python3, import the required modules, and set the API key (*type in the <terminal>*)

```bash
python3
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
```

## 3. Upload Files

Upload the files (make sure to change the file path):

```python
openai.File.create(file=open("<PUT/FILE/PATH/HERE>", "rb"), purpose='fine-tune')
```

**Important**: Remember to store the file IDs that are provided in the return:

(format examples)
- Train Data ID: `"file-38JVhLIEtJX8sznjxAcIBfDc"`
- Validation Data ID: `"file-xhLWInR04NGsULkPuqjT5j8J"`

## 4. Create Fine-Tune

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

## 5. Retrieve Fine-Tune and Follow Progress

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

## 6. Test the Model

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