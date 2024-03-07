In this file, I tried to edit OpenAIGPTModel class (as well as Block and OpenAIGPTLMHeadModel) to make it possible to replace hidden states of the chosen layers with the brain activations.
The edits are marked by the "edit" comment.

The file is taken from transformers repository: https://github.com/huggingface/transformers
The path to the file is: "transformers\src\transformers\models\openai\modeling_openai.py"