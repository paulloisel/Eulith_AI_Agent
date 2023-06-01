import os
import openai
ROOT_DIR = '/Users/paul/Desktop/Eulith_AI_Agent'
openai.api_key = os.getenv("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")
openai.File.create(
  file=open(os.path.join(ROOT_DIR, 'completion_assistant/completion_annotations_format','completion_annotated_data.json'), "rb"),
  purpose='fine-tune'
)

openai.File.create(file=open("/Users/paul/Desktop/Eulith_AI_Agent/completion_assistant/completion_annotations_format/completion_annotated_data_prepared_train.jsonl", "rb"), purpose='fine-tune')

openai.FineTune.create(training_file="file-w3r0zhrEVn6J18E2ryXyOYQe",
                       model="ada",
                       suffix="completion_1")
