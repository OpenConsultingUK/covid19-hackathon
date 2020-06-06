import torch
from transformers import BertTokenizer
from transformers import BertForQuestionAnswering

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

BERT_SQUAD = 'bert-large-uncased-whole-word-masking-finetuned-squad'

model = BertForQuestionAnswering.from_pretrained(BERT_SQUAD)
tokenizer = BertTokenizer.from_pretrained(BERT_SQUAD)

model = model.to(torch_device)
model.eval()

print()

def answer_question(question, context):
    # anser question given question and context
    encoded_dict = tokenizer.encode_plus(
                        question, context,
                        add_special_tokens = True,
                        max_length = 256,
                        pad_to_max_length = True,
                        return_tensors = 'pt'
                   )
    
    input_ids = encoded_dict['input_ids'].to(torch_device)
    token_type_ids = encoded_dict['token_type_ids'].to(torch_device)
    
    start_scores, end_scores = model(input_ids, token_type_ids=token_type_ids)

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)
    
    answer = tokenizer.convert_tokens_to_string(all_tokens[start_index:end_index+1])
    answer = answer.replace('[CLS]', '')
    return answer

def qna(query):
    """
    This function uses NLP technique to give response to user queries.
    """
    f = open("../data/covidinfo.txt", "r")
    context = f.read() 
    question = query
    answer = answer_question(question, context)
    return answer

print(qna('Is covid and coronavirus the same'))