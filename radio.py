from typing import List

try:
    from pybricks.experimental import Broadcast
    from pybricks.tools import wait
except ImportError:
    from mock_pybricks import wait


class Radio:

    ACKOWLEDGE_TOPIC = "acknowledge"

    def __init__(self,
                 topics: List[str],
                 broadcast_func) -> None:
        
        # Set up the radio
        self._topics = topics
        self._topics.append(self.ACKOWLEDGE_TOPIC)
        self._radio = broadcast_func(topics=self._topics)

        # Set up the timer
        self._index = 0
        self._previous_message_time = None

    def send(self,
             topic: str,
             message: tuple) -> None:
        
        print("Message:", message)
        
        if topic not in self._topics:
            raise ValueError("Topic not in list of topics")

        print("message index =", self._index)

        # Send the message
        message = (self._index,) + message
        print("Sending", topic, message)
        self._radio.send(topic, message)

        # Wait for acknowledgement
        acknowledged = self._radio.receive(topic=self.ACKOWLEDGE_TOPIC)
        while acknowledged != self._index:
            wait(1)
            acknowledged = self._radio.receive(topic=self.ACKOWLEDGE_TOPIC)
        self._index += 1
        print("acknowledged", acknowledged)

    def receive(self,
                topic: str) -> str:
        
        if topic not in self._topics:
            raise ValueError("Topic not in list of topics")

        # Receive the message
        message = self._radio.receive(topic=topic)
        # Check if message is None
        if message is None:
            return None
        else:
            index, *message_data = message
            print(f"Radio received message  with  index : {index} | message data : {message_data}")

        if len(message_data) == 1:
            message_data = message_data[0]
        # print(index, topic, message)
        # Check if message is a duplicate
        if index == self._previous_message_time:
            return None

        

        # Send acknowledgement
        print(f"Sending ack with index : {index}")
        self._radio.send(self.ACKOWLEDGE_TOPIC, index)

        # Update previous message time
        self._previous_message_time = index

        return message_data

    def shutdown(self):
        self._radio.join()