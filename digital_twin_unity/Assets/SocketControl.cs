using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System;
using System.Linq;

public class SocketControl
{


    private string ip;// IP address to connect socket 

    private int port; // port to connect socket 


    private Socket client;
    private byte[] Acknowledgement_message =  System.Text.Encoding.UTF8.GetBytes("GPIG-Group-B-Server");
    private byte[] Connection_init_message = System.Text.Encoding.UTF8.GetBytes("GPIG-Group-B-Client");

    public SocketControl(string ip, int port)
    {
        this.ip = ip;
        this.port = port;
    }


    //function for sending data
    public void Send(byte[] Data_to_send)
    {
        client.Send(Data_to_send);
    }

    //function for receiving data, takes length of data to receive as parameter, returns the bytes received as byte[]
    public byte[] ReceiveData(int Length_of_data_to_receive)
    {

        int num_bytes_received = 0;
        //allocate and receive bytes
        byte[] bytesreceived = new byte[Length_of_data_to_receive];

        while (num_bytes_received < Length_of_data_to_receive) {
            num_bytes_received += client.Receive(buffer: bytesreceived, offset: num_bytes_received, socketFlags: SocketFlags.None, size: Length_of_data_to_receive - num_bytes_received) ;
            if (num_bytes_received == 0)
            {
                Debug.Log("NO BYTES received. CONNECTION CLOSED.");
            }
        }
        

        Debug.Log("The number of bytes received is: " +num_bytes_received);

        Debug.Log("The bytes converted to a string is: " + BitConverter.ToString(bytesreceived));

        

        return bytesreceived;
    }


    //sets up socket connection
    //connects to ip,port
    //sends connection init message
    //checks Acknowledgement message is correct
    //gets device id checks its correct
    public Int16 setupSocket()
    {

        //set up the new socket
        client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        //attempt to connect to the port
        client.Connect(ip, port);
        // output an error if cannot connect
        if (!client.Connected)
        {
            Debug.LogError("Could not connect To Socket.");
            //return null;
        }

        //send initialisation code
        Send(Connection_init_message);

        //received bytes
        byte[] received_acknowledgement_message = ReceiveData(Acknowledgement_message.Length);

        // just for first message
        if (!received_acknowledgement_message.SequenceEqual(Acknowledgement_message)) // make sure this is right
        {
            Debug.Log("The wrong initialisation array was received. Expected: " + BitConverter.ToString(Acknowledgement_message));
            Debug.Log("received: " + BitConverter.ToString(received_acknowledgement_message));
            client.Close();
        }
        else
        {
            Debug.Log("Connection successful.");
            Int16 device_type_id = BitConverter.ToInt16(ReceiveData(Length_of_data_to_receive: 2),0); // first receive is for the class type 
            return device_type_id;


        }
        return -1;// TODO deal with later
    }


    public (Int16 message_id,byte[] device_message) get_device_message()
    {
        Int16 message_id = BitConverter.ToInt16(ReceiveData(Length_of_data_to_receive: 2), 0);
        Int16 message_size = BitConverter.ToInt16(ReceiveData(Length_of_data_to_receive: 2), 0);

        byte[] device_message = ReceiveData(Length_of_data_to_receive: message_size);


        return (message_id, device_message);
    }



    //helper function to close connection
    public void closeConnection()
    {
        client.Close();
    }



}
