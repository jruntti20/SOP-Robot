#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
import speech_recognition as sr
import threading

from chatbot_speech_recognizer_interface.srv import Speechrec  


class SpeechRecognizerNode(Node):

    def __init__(self):
        super().__init__('mt_speech_recognizer')
        self.publisher_ = self.create_publisher(String, 'mt_recognized_speech', 10)
        #self.service_ = self.create_service(Speechrec, "Speechrec_service", self.callback)
        self.service_ = self.create_service(Speechrec, "Speechrec_service", self.start_recognizing)
        self.recognizer_ = sr.Recognizer()

    def callback(self, request, response):
        if (request):
            recognized_speech = self.start_recognizing()
            if (recognized_speech is not None):
                response.success = True
                response.recognized_speech = recognized_speech

    def start_recognizing(self, request, response):
        request = request
        def recognize(response):
            with sr.Microphone() as source:
                self.recognizer_.adjust_for_ambient_noise(source)
                self.get_logger().info('Listening...')
                while rclpy.ok():
                    try:
                        #audio = self.recognizer_.listen(source, timeout=5)
                        audio = self.recognizer_.listen(source)
                        text = self.recognizer_.recognize_google(audio)
                        #msg = String()
                        #msg.data = text

                        #self.publisher_.publish(msg)
                        self.get_logger().info(f'Recognized speech: {text}')

                        response.success = True
                        response.recognized_speech = text
                        return response

                    except sr.UnknownValueError:
                        self.get_logger().warning('Speech not recognized')
                        response.success = False
                        response.recognized_speech = ""
                        return response
                    except sr.RequestError as e:
                        self.get_logger().error(f'Recognition request failed: {e}')
                        response.success = False
                        response.recognized_speech = ""
                        return response

        thread = threading.Thread(target=recognize, args=(response,))
        thread.start()


def main(args=None):
    rclpy.init(args=args)
    node = SpeechRecognizerNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

