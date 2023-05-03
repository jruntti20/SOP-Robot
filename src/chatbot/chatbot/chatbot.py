#!/usr/bin/python3

import rclpy
from rclpy.service import Service
from rclpy.action import ActionClient
from rclpy.node import Node

#from ament_index_python.packages import get_package_share_directory

from std_msgs.msg import String
from chatbot_speech_recognizer_interface.srv import Speechrec

from chatterbot import ChatBot
import logging
#from chatterbot.trainers import ChatterBotCorpusTrainer

#from preprocessors import preprocess_text
#from preprocessors import clean_whitespace
#from spacyadapter import SpacyBestMatch
from chatbot.language_detector import detect_language
from chatbot.translate_text import translate_to_english
from chatbot.translate_text import translate_to_finnish
from chatbot.best_match_adapter import BestMatchAdapter

#from trainers import ChatterBotTXTTrainer
#from trainers import SQuADJSONTrainer
#from trainers import MSMARCOJSONTrainer
#from trainers import ChatterBotJSONTrainer
#from trainers import ChatterBotCorpusTrainer

logging.basicConfig(level=logging.INFO)


class ChatBotClientNode(Node):

    def __init__(self):
        super().__init__('chatbot_node')
        self.cli = self.create_client(Speechrec, "Speechrec_service")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.timer = self.create_timer(1.0, self.send_request)
        self.recognized_speech = ""
        #self.req = Speechrec.Request()
        #self.resp = self.send_request()
        self.chatbot = ChatBot("Helper", read_only=True, storage_adapter='chatterbot.storage.SQLStorageAdapter',
                            logic_adapters=[
                            {
                                #'import_path': '__main__.BestMatchAdapter',
                                'import_path': 'chatbot.best_match_adapter.BestMatchAdapter',
                                'default_response': 'I am sorry, but I do not understand.',
                                'maximum_similarity_threshold': 0.90,
                                'statement_comparison_function': 'chatterbot.comparisons.LevenshteinDistance',
                                #'response_selection_method': 'chatterbot.response_selection.get_most_frequent_response'
                            },
                            {
                                'import_path': 'chatterbot.logic.MathematicalEvaluation',
                            }
                            ]
                            )


    def send_request(self):
        request = Speechrec.Request()
        future = self.cli.call_async(request)
        #rclpy.spin_until_future_complete(self, future)
        future.add_done_callback(self.callback)
        #return self.future.result()
    
    def callback(self, future) -> bool:
        response = future.result()
        if (response.success):
            self.get_logger().info("Response:\n" + response.recognized_speech)
            responded = self.chatbot_worker_callback(response.recognized_speech)
            if (responded):
                return True
        else:
            self.get_logger().info("Response is not ready yet.")
            self_recognized_speech = ""
            return False

    def chatbot_train(self):
        pass
        # train with self-written data
        #    trainer = ChatterBotCorpusTrainer(chatbot)
        #
        #    trainer.train(
        #        "/workspace/src/chatbot/chatbot/trainingdata"
        #    )
        #
        #
        #    # train with ambignq data
        #    trainer = ChatterBotJSONTrainer(chatbot)
        #
        #    trainer.train(
        #        "/workspace/src/chatbot/chatbot/ambignq/train.json", input_language="en"
        #    )
        #
        #
        #    # train with qa dataset
        #    trainer = ChatterBotTXTTrainer(chatbot)
        #    trainer.train(
        #        "/workspace/src/chatbot/chatbot/Question_Answer_Dataset_v1.2/S08/question_answer_pairs.txt", input_language="en"
        #    )
        #    trainer.train(
        #        "/workspace/src/chatbot/chatbot/Question_Answer_Dataset_v1.2/S09/question_answer_pairs.txt", input_language="en"
        #    )
        #    trainer.train(
        #        "/workspace/src/chatbot/chatbot/Question_Answer_Dataset_v1.2/S10/question_answer_pairs.txt", input_language="en"
        #    )
        #
        #    # train with stanford training data
        #    trainer = SQuADJSONTrainer(chatbot)
        #    trainer.train(
        #        "/workspace/src/chatbot/chatbot/train_stanford/train-v2.0.json", input_language="en"
        #        )
    def chatbot_worker_callback(self, recognized_speech):
        #user_input = input("Sinä: ")

        #preprocessed_input = preprocess_text(user_input)
        # Get response for the original input
        original_response = self.chatbot.get_response(recognized_speech)
        original_confidence = original_response.confidence

        # Translate input to English
        translated_input = translate_to_english.translate(recognized_speech)
        #preprocessed_translated_input = preprocess_text(translated_input)

        # Get response for the translated input
        translated_response = self.chatbot.get_response(translated_input)
        translated_confidence = translated_response.confidence

        # Compare confidence levels and choose the higher one
        # Balance the translater confidence by lowering it
        balance_variable = 0.1
        if (translated_confidence - balance_variable) > original_confidence:
            # Translate the English response back to the input language
            final_response_text = translate_to_finnish.translate(translated_response)
        else:
            final_response_text = original_response.text

        print("Bot: ", final_response_text)
        return(final_response_text)

            
def main(args=None):
    rclpy.init(args=args)
    client = ChatBotClientNode()
    rclpy.spin(client)
    rclpy.shutdown()

    #response = client.send_request()
    #if (response.success):
    #    client.get_logger().info(response.recognized_speech)



if __name__ == '__main__':
    main()
