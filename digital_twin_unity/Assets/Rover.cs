using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rover : MonoBehaviour
{
    Motor driving_motor;

    private void Start()
    {
        Motor driving_motor = new Motor(ip: "localhost", port : 65432);
        
    }

}
