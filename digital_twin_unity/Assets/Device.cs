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

    private SocketHandler Socket;


    protected int port;
    protected int deviceID;
    protected string ip;
    protected SocketHandler socketHandler;
    protected Dictionary<Int16, Action<string>> message_dict = new Dictionary<Int16, Action<string>>();



    public Device(string ip,int port,int deviceID)
    {
        this.ip = ip;
        this.port = port;
        this.deviceID = deviceID;
        this.socketHandler = new SocketHandler(ip: this.ip, port: this.port);
        // This must be called after socket setup
        this.CheckDeviceID();


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
        Int16 message_id;
        string message_json_string;

        


        while (true)
        {
            var returned_socket_data = Socket.get_device_message();
            message_id = returned_socket_data.Item1;
            message_json_string = returned_socket_data.Item2;

            this.message_dict[message_id](message_json_string);



        }


    }






    


}
