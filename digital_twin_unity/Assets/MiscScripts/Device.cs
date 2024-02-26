using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System;
using System.Linq;
using static UnityEngine.Networking.UnityWebRequest;
using System.Security.Cryptography;
using System.Threading;
using System.Runtime.CompilerServices;
using System.Collections.Concurrent;

public abstract class Device : MonoBehaviour
{ 
    public int port;
    public string ip;
    protected int deviceID;
    protected SocketHandler socketHandler;
    protected Dictionary<UInt16, Action<string>> message_dict = new Dictionary<UInt16, Action<string>>();
    protected BlockingCollection<Message> inboundMessageQueue = new BlockingCollection<Message>(new ConcurrentQueue<Message>());
    protected BlockingCollection<Message> outboundMessageQueue = new BlockingCollection<Message>(new ConcurrentQueue<Message>());
    private Thread socketThread;


    protected virtual void Start() 
    {
        socketThread = new Thread(new ThreadStart(this.run));
        socketThread.Start();
    }

    protected virtual void Update() 
    {
        Message inboundMessage;
        if (inboundMessageQueue.TryTake(out inboundMessage)) 
        {
            message_dict[inboundMessage.messageID](inboundMessage.jsonString);
            
        }
    }

    protected void AddReturnMessageToOutboundQueue(string returnMessage, UInt16 messageID) 
    {
        Message outboundMessage = new Message();
        outboundMessage.jsonString = returnMessage;
        outboundMessage.messageID = messageID;
        outboundMessageQueue.Add(outboundMessage);
    }

    protected virtual void CheckDeviceID() 
    {
        UInt16 received_device_id = this.socketHandler.GetHeaderData();
        if (received_device_id != deviceID)
        {
            throw new Exception("receive device id: " + received_device_id + ". Expected deviceID:" + deviceID);

        }
        else
        {
            Debug.Log("recieved device id: " + received_device_id);
        }
    }

    protected virtual void run()
    {
        Debug.Log("Initialising Connection on IP : " + this.ip + " | PORT : " + this.port);
        this.socketHandler = new SocketHandler(ip: this.ip, port: this.port);
        Debug.Log("Connection established. Checking device ID");
        // This must be called after socket setup
        this.CheckDeviceID();
        Debug.Log("Device ID Check successful");


        Message outboundMessage;




        while (true)    
        {
            Message inboundMessage = new Message();
            var returned_socket_data = this.socketHandler.get_device_message();
            inboundMessage.messageID = returned_socket_data.Item1;
            inboundMessage.jsonString = returned_socket_data.Item2;
            if (inboundMessage.messageID == 0)
            {
                Debug.Log("Received shutdown message. Closing TCP Worker");
                break;
            }

            inboundMessageQueue.Add(inboundMessage);
            outboundMessage = outboundMessageQueue.Take();
            if (outboundMessage.messageID != inboundMessage.messageID) 
            {
                throw new Exception("Message IDs do not match. Something has gone very very wrong :).");
            }
            // string returnMessageJson = this.message_dict[message_id](message_json_string);

            this.socketHandler.SendJSONMessage(messageID : outboundMessage.messageID, jsonMessage : outboundMessage.jsonString);



        }

       

    }

    void OnDestroy() 
    {
        Debug.Log("Waiting for socket thread to finish");
        socketThread.Join();
        Debug.Log("Socket thread joined successfully");
    }

    protected struct Message 
    {
        public UInt16 messageID;
        public string jsonString;
    }






    


}
