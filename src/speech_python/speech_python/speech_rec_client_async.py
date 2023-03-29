#!/usr/bin/env python3

<<<<<<< Updated upstream
import rclpy
from rclpy.node import Node
from rclpy import Future

from msg_interface.srv import SpeechRec
from msg_interface.msg import SpeechRecognitionCandidates

class SpeechRecClient(Node):
    
    def __init__(self):
        super().__init__('speech_rec_client')
        self.call_speech_rec_server()
        self.transcript = None
        self.confidence = None
        self.future = Future()
        self.publisher = self.create_publisher(SpeechRecognitionCandidates, "speech_recognition_candidates", 10)
        self.timer = self.create_timer(0.2, self.publish_speech)
        self.get_logger().info("Speech recognition client has been started.")

    def publish_speech(self):
        msg = SpeechRecognitionCandidates()
        if (self.transcript != None | self.confidence != None):
            msg.transcript = self.transcript
            msg.confidence = self.confidence
            self.publisher.publish(msg)
            self.transcript = None
            self.confidence = None

    def call_speech_rec_server(self):
        client = self.create_client(SpeechRec, "speech_rec_client")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for server...")

        request = SpeechRec.Request()

        self.future = client.call_async(request)
        self.future.add_done_callback(self.callback_call_speech_rec_server)

    def callback_call_speech_rec_server(self, future):
        try:
            response = future.result()
            self.transcript = response.trancript
            self.confidence = response.confidence
            self.get_logger().info("Transcript: ", str(response.transcript), "\nConfidence: ", str(response.confidence))
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))


def main(args=None):
    rclpy.init(args=args)
    node = SpeechRecClient()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
=======
import io
import logging
import time
import types
import os
import usb.core
import usb.util
import pocketsphinx

import rclpy
from rclpy.node import Node
from rclpy.task import Future

import speech_recognition as sr
from threading import Thread, Event
from queue import Queue

from msg_interface.msg import SpeechRecognitionCandidates, SetParametersResult
from msg_interface.srv import Speech_msg, Speech_msg_ready

import pyaudio

class MinimalService(Node):
    
    def __init__(self, ready_in_q: Queue, msg_data_in_q):
        super().__init__('speech_recognizer')
        self.ready_in_q = ready_in_q
        self.msg_data_in_q = msg_data_in_q
        #self.declare_parameter('speech_received', False)
        self.publisher_ = self.create_publisher(SpeechRecognitionCandidates, 'speech_rec_publisher', 10)
        self.query_speech_data_ = self.create_service(Speech_msg_ready, "speech_msg_ready", self.callback_speech_msg_ready)
        self.query_speech_data_ = self.create_service(Get_speech_msg, "get_speech_rec_msg", self.callback_get_speech_msg)

        #timer_period = 0.5
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.i = 0
        #self.add_on_set_parameters_callback(self.parameters_callback)

        self.logger().info("Minimal publisher has been started...")
        
    #def timer_callback(self):

    #    msg = SpeechRecognitionCandidates()

    #    #TODO: Kysyy puheentunnistusthreadiltä onko tunnistettua puhetta saatavilla.

    #    msg.transcript = {"Moro Horo!"}
    #    msg.confidence = {0.69}
    #    self.publisher_.publish(msg)
    #    self.get_logger().info(f'Publishing:\nTranscript: {msg.transcript}\tConfidence: {msg.confidence}')
    #    self.i += 1

    def callback_speech_msg_ready(self):
        if (self.ready_in_q.get() == True):
            
            #TODO: Call another callback for getting the data
            self.callback_get_speech_msg()

    def callback_get_speech_msg(self):
        self.data = self.ready_in_q.get()
        msg = SpeechRecognitionCandidates()
        msg.transcript = str(self.data)

    # Not yet implemented
    #def print_parameters(self):
    #    pass

    #def parameters_callback(self, params):
    #    for param in params:
    #        print(vars(param))
    #    return SetParametersResult(succesful=True)



class Rec(Thread):
    def __init__(self, name, quit_event):
        Thread.__init__(self)
        self.event = quit_event 
        self.name = name
        self.data_ready = False
        self.recognized_data = 0
        self.all_data = 0


    def run(self, ready_out_q: Queue, msg_data_out_q: Queue):
        
        rclpy.init()        

        minimal_service = MinimalService(ready_out_q, msg_data_out_q)

        print("Starting task")
        self.msg = SpeechRecognitionCandidates()
        self.ready_out_q = ready_out_q
        self.msg_data_out_q = msg_data_out_q
        
        while not self.event.is_set():
            
            r = sr.Recognizer()
        
            with sr.Microphone(device_index=0, sample_rate=16000) as source:

                print("Say something!")
                audio = r.listen(source)
            
                try:
                    # for testing purposes, we're just using the default API key
                    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                    # instead of `r.recognize_google(audio)`
                    self.recognized_data = r.recognize_google(audio, language="fi")
                    self.all_data = r.recognize_google(audio, language="fi", show_all=True)

                    if (self.recognized_data):
                        self.data_ready = True
                        ready_out_q.put(self.data_ready)
                        self.send_data()

                    print("Google Speech Recognition thinks you said " + self.recognized_data)
                    self.myCallback()
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))        

    def send_data(self):
        self.msg.transcript = {"Moro Horo"}
        self.msg.confidence = {0.69}
        self.msg_data_out_q.put(self.msg)
        self.data_ready = False

>>>>>>> Stashed changes
