import rclpy
from rclpy.node import Node
<<<<<<< Updated upstream

import speech_recognition as sr

from msg_interface.srv import SpeechRec

class SpeechRecServer(Node):

    def __init__(self):
        super().__init__('speech_rec_server')
        self.server = self.create_service(SpeechRec, "speech_rec_server", self.callback_speech_rec)
        self.get_logger().info("SpeechRecServer started...")

    def callback_speech_rec(self, request, response):

        r = sr.Recognizer()
        
        with sr.Microphone(device_index=0, sample_rate=16000) as source:

            self.get_logger().info("Say something!")
            audio = r.listen(source)
            
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                self.recognized_data = r.recognize_google(audio, language="fi")
                self.all_data = r.recognize_google(audio, language="fi", show_all=True)

                self.get_logger().info("Google Speech Recognition thinks you said " + self.recognized_data)
            except sr.UnknownValueError:
                self.get_logger().info("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                self.get_logger().info("Could not request results from Google Speech Recognition service; {0}".format(e))     
        return response

def main(args=None):
    rclpy.init(args=args)
    node = SpeechRecServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
=======
from rclpy.task import Future

import speech_recognition as sr
from threading import Thread, Event
from queue import Queue

from msg_interface.msg import SpeechRecognitionCandidates, SetParametersResult
from msg_interface.srv import Get_speech_msg, Speech_msg_ready

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli_speech_msg_ready = self.create_client(Speech_msg_ready, 'speech_msg_ready')
        self.cli_speech_msg = self.create_client(Speech_msg, 'speech_msg_ready')

        while not self.cli_speech_msg_ready.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req_speech_msg_ready = Speech_msg_ready.Request()
        self.req_speech_msg = Speech_msg.Request()

    def send_request(self, msg):
        self.future = self.cli.call_async(self.req)

class Publish(Thread):
    def __init__(self, name, quit_event):
        Thread.__init__(self)
        self.name = name
        self.event = quit_event
        self.future = Future()

        self.logger().info("Speech recognizer has been started...")

    def run(self, in_q):

        self.publisher = MinimalPublisher(in_q)
        
        #rclpy.spin(self.publisher)
        while not self.event.is_set():
            #rclpy.spin_until_future_complete(self.publisher, self.future)
            rclpy.spin_once(self.publisher)

        self.publisher.destroy_node()
        rclpy.shutdown()
>>>>>>> Stashed changes
