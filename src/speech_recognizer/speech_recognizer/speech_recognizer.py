#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import speech_recognition as sr
import os
#import pocketsphinx as spx

from chatbot_speech_recognizer_interface.srv import Speechrec  

class SpeechRecognizerNode(Node):
    def __init__(self):
        super().__init__('speech_recognizer_node')
        self.publisher_ = self.create_publisher(String, 'recognized_speech', 10)
        self.service_ = self.create_service(Speechrec, "Speechrec_service", self.start_listening)

    def start_listening(self, request, response):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            #self.get_logger().info('Listening...')

            while rclpy.ok():
                try:
                    #text = self.r.recognize_google_cloud(audio, credentials_json=None, language="fi" )
                    audio = r.listen(source)
                    text = r.recognize_google(audio, language="fi" )
                    #text = self.r.recognize_sphinx(audio)
                    #credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS_JSON)
                    print(f"You said: {text}")
                    #msg = String()
                    #msg.data = text
                    #self.publisher_.publish(msg)
                    response.success = True
                    response.recognized_speech = text
                    return response

                except sr.UnknownValueError:
                    #print("Google Cloud Speech-to-Text could not understand audio")
                    print("Could not understand audio")
                    response.success = False
                    response.recognized_speech = ""
                    return response
                except sr.RequestError as e:
                    #print(f"Could not request results from Google Cloud Speech-to-Text service; {e}")
                    print(f"Could not request results from service; {e}")
                    response.success = False
                    response.recognized_speech = ""
                    return response

def main(args=None):
    rclpy.init(args=args)

    node = SpeechRecognizerNode()
    rclpy.spin(node)

    #while rclpy.ok():
    #    node.start_listening()

    #node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

