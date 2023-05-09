using System.Collections;
using System.Collections.Generic;
using UnityEngine;




public class Output_logs : MonoBehaviour
{

    [SerializeField]
    public GameObject Rover;

    public List<SteeringMotor> steeringMotors;
    public List<UltrasonicSensor> us_sensors;

    public List<WheelMotor> wheelMotors;

    public List<ColourDistanceSensor> colourDistanceSensors;

    public List<ColourSensor> colourSensors;


    private bool showSidebar = false;

    private GUIStyle style;

    static float distance_travelled = 0;

    private Vector3 last_position;
    private Vector3 current_position;

    void awake()
    {
        //get the starting position of the rover
        distance_travelled = 0;
        last_position = Rover.transform.position;

    }

        


        



    void OnGUI()
    {
        style = new GUIStyle();
        style.normal = new GUIStyleState();
        style.normal.textColor = Color.white;
        style.normal.background = Texture2D.grayTexture;

        //display time taken and distance travelled at bottom of the screen
        GUI.Label(new Rect(10, Screen.height - 50, 500, 20), "Time elapsed : " + Time.time.ToString("0.00"),style );
        


       //get the current position of the rover
        current_position = Rover.transform.position;

        //calculate distance travelled
        distance_travelled = Vector3.Distance(new Vector3(0.0f,-0.87f,0.0f), current_position);

        Debug.Log("Vector3 distance" + Vector3.Distance(last_position, current_position));
        last_position = current_position;
        GUI.Label(new Rect(10, Screen.height - 30, 500, 50), "Distance travelled : " + distance_travelled,style);
        

        ///debugging distance travelled

        //add a button that toggles a sidebar to display the current state of the car
        if (GUI.Button(new Rect(10, 10, 100, 50), "Toggle Sidebar"))
        {
            //toggle the sidebar
            showSidebar = !showSidebar;
        }

        if (showSidebar)
        {
            //display the sidebar
            //create rectangle for the sidebar
            
            GUILayout.BeginArea(new Rect(10, 80, 300, 300),style);
            
            // display label for each wheel motor
            foreach (WheelMotor wm in wheelMotors)
            {
                Vector3 position;
                Quaternion rotation;
                wm.wheelCollider.GetWorldPose(out position, out rotation);
                //output to gui the position and rotation of each wheel
                GUILayout.Label("Wheel " + wm.name + " position (x,y,z): " + position.ToString("0.00"));
                GUILayout.Label("Wheel " + wm.name + " rotation (x,y,z): " + rotation.eulerAngles.ToString("0.00"));
            }

            GUILayout.EndArea();            
        }
    }
    


}
