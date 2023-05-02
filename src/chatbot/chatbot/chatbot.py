from chatterbot import ChatBot
import logging
#from chatterbot.trainers import ChatterBotCorpusTrainer
from trainers import ChatterBotJSONTrainer
from trainers import ChatterBotCorpusTrainer
from preprocessors import preprocess_text
from preprocessors import clean_whitespace
from spacyadapter import SpacyBestMatch
from chatterbot.storage import MongoDatabaseAdapter
from language_detector import detect_language
from translate_text import translate_to_english
from best_match_adapter import BestMatchAdapter
from trainers import ChatterBotTXTTrainer
from trainers import SQuADJSONTrainer
from trainers import MSMARCOJSONTrainer

logging.basicConfig(level=logging.INFO)


chatbot = ChatBot("Helper",
                  read_only=True,
                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  #storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                  #storage_adapter='chatterbot.storage.django_storage',
                  #database_uri='mongodb://localhost:27017',
                  

                  logic_adapters=[
                    {
                'import_path': '__main__.BestMatchAdapter',
                'default_response': 'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.90,
                'statement_comparison_function': 'chatterbot.comparisons.LevenshteinDistance',
                #'response_selection_method': 'chatterbot.response_selection.get_most_frequent_response'
                    },
                    {
                'import_path': 'chatterbot.logic.MathematicalEvaluation',
                    }
                    ]
                  #preprocessors=['__main__.preprocess_text']
                  )

#chatbot.storage.create(text='Ok, here is a link: http://chatterbot.rtfd.org', in_response_to='Help me!')


# train with self-written data
trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
    "src\chatbot\chatbot\trainingdata"
    
)


# train with ambignq data
""" trainer = ChatterBotJSONTrainer(chatbot)

trainer.train(
    "src\chatbot\chatbot\ambignq\train.json", input_language="en"
) """


# train with qa dataset
""" trainer = ChatterBotTXTTrainer(chatbot)
trainer.train(
    "src\chatbot\chatbot\Question_Answer_Dataset_v1.2\S08\question_answer_pairs.txt", input_language="en"
)
trainer.train(
    "src\chatbot\chatbot\Question_Answer_Dataset_v1.2\S09\question_answer_pairs.txt", input_language="en"
)
trainer.train(
    "src\chatbot\chatbot\Question_Answer_Dataset_v1.2\S10\question_answer_pairs.txt", input_language="en"
) """

# train with stanford training data
""" trainer = SQuADJSONTrainer(chatbot)
trainer.train(
    "src\chatbot\chatbot\train_stanford\train-v2.0.json", input_language="en"
    ) """

# train with msmarco data
# not working
""" trainer = MSMARCOJSONTrainer(chatbot)
trainer.train(
    "SOP-Robot/src/chatbot/chatbot/train_msmarco/train_v2.1.json", input_language="en", chunk_size=500
) """



while True:
    try:
        user_input = input("You: ")
        preprocessed_input = preprocess_text(user_input)

        input_language = detect_language.detect(user_input)
        #if input_language == 'fi':
            #input_english = translate_to_english.translate(user_input)
            #print("käännetty input: ", input_english)
            #bot_input = chatbot.get_response(input_english)
        bot_input = chatbot.get_response(preprocessed_input)

        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break