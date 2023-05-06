try:
    from pybricks.experimental import Broadcast
    from pybricks.tools import StopWatch
    from pybricks.tools import wait
except ImportError:
    pass

class Radio:

    ACKOWLEDGE_TOPIC = "acknowledge"

    def __init__(self,
                 topics: list[str]) -> None:
        
        # Set up the radio
        self._topics = topics
        self._topics.append(self.ACKOWLEDGE_TOPIC)
        self._radio = Broadcast(topics=self._topics)

        # Set up the timer
        self._timer = StopWatch()
        self._previous_message_time = None

    def send(self,
             topic: str,
             message: str) -> None:
        
        if topic not in self._topics:
            raise ValueError("Topic not in list of topics")
        
        t = self._timer.time()

        # Send the message
        self._radio.send(topic, (t, message))

        # Wait for acknowledgement
        acknowledged = self._radio.receive(topic=self.ACKOWLEDGE_TOPIC)
        while acknowledged != t:
            wait(1)
            acknowledged = self._radio.receive(topic=self.ACKOWLEDGE_TOPIC)
    
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
            t, message = message

        # Check if message is a duplicate
        if t == self._previous_message_time:
            return None

        # Send acknowledgement
        self._radio.send(self.ACKOWLEDGE_TOPIC, t)

        # Update previous message time
        self._previous_message_time = t

        return message