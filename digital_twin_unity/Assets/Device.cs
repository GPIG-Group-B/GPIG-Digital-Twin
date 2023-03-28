using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System;
using System.Linq;
using static UnityEngine.Networking.UnityWebRequest;
using System.Security.Cryptography;

public abstract class Device
{ 
    protected int port;
    protected int deviceID;
    protected string ip;
    protected SocketHandler socketHandler;
    protected Dictionary<Int16, Func<string, string>> message_dict;



    public Device(string ip,int port,int deviceID)
    {
        this.ip = ip;
        this.port = port;
        this.deviceID = deviceID;
        this.socketHandler = null;
        this.message_dict = new Dictionary<Int16, Func<string, string>>();
        // IMPORTANT - 0 is reserved for closing the connection
        // IMPORTANT - 1 is reserved for info message
        // All custom device methods must be assigned to key 2 or higher (excl info which must be 1) 

        // check right device id

    }

    private void CheckDeviceID() 
    {
        Int16 received_device_id = this.socketHandler.GetHeaderData();
        if (received_device_id != deviceID)
        {
            throw new Exception("receive device id: " + received_device_id + ". Expected deviceID:" + deviceID);

        }
        else
        {
            Debug.Log("recieved device id: " + received_device_id);
        }
    }

    public void run()
    {
        this.socketHandler = new SocketHandler(ip: this.ip, port: this.port);
        // This must be called after socket setup
        this.CheckDeviceID();

        Int16 message_id;
        string message_json_string;

        


        while (true)    
        {
            var returned_socket_data = this.socketHandler.get_device_message();
            message_id = returned_socket_data.Item1;
            message_json_string = returned_socket_data.Item2;
            if (message_id == 0)
            {
                Debug.Log("Received shutdown message. Closing TCP Worker");
                break;
            }

            string returnMessageJson = this.message_dict[message_id](message_json_string);
            this.socketHandler.SendJSONMessage(messageID : message_id, jsonMessage : returnMessageJson);



        }


    }






    


}
