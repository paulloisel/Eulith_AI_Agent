## Go to your terminal
## Run this the following in order
  ##export OPENAI_API_KEY="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"
  ##python3 
  ##import os
  ##import openai
  ##openai.api_key = os.getenv("OPENAI_API_KEY")
  ##openai.File.create(file=open("/Users/paul/Desktop/Eulith_AI_Agent/completion_assistant/completion_annotations_format/completion_annotated_data_prepared_train.jsonl", "rb"), purpose='fine-tune')
  ##openai.FineTune.create(training_file="file-w3r0zhrEVn6J18E2ryXyOYQe", model="davinci", suffix="completion_2")

##Keep the finetune ID
##Go to a new terminal and run "openai api fine_tunes.follow -i <ID-FInetune>"