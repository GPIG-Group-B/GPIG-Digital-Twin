using System.Collections;
using System.Collections.Generic;
using UnityEngine;




public class UI : MonoBehaviour
{

    [SerializeField]
    public GameObject rover;

    [SerializeField]
    public Rigidbody roverRigidBody;

    public float distanceTravelled = 0;

    public List<SteeringMotor> steeringMotors;
    public List<UltrasonicSensor> us_sensors;

    public List<WheelMotor> wheelMotors;

    public List<ColourDistanceSensor> colourDistanceSensors;

    public List<ColourSensor> colourSensors;

    public List<ForceSensor> forceSensors;


    private bool showSidebar = false;

    private GUIStyle regularStyle;
    private GUIStyle colourSensorColour;

    private Color rgbTextColour;


    private Vector3 lastTrackedPosition;
    private float acceleration;
    private float lastVelocity;
    private float currentAngle;

    private bool isForceSensorTouched;
    

    public Camera MainCamera;
    bool isCameraZoomedOut = false;

    private Vector3 _camera_pos_delta;

    private Vector3 startPosition;

    void Start()
    {
        regularStyle = new GUIStyle();
        regularStyle.normal = new GUIStyleState();
        regularStyle.normal.textColor = Color.white;
        regularStyle.normal.background = Texture2D.grayTexture;

        colourSensorColour = new GUIStyle();
        colourSensorColour.normal = new GUIStyleState();

        startPosition = rover.transform.position;
        lastTrackedPosition = startPosition;
        lastVelocity = 0;



    }
    
    



    void FixedUpdate()
    {
        Vector3 currentPosition = rover.transform.position;

        //To ignore vertical movement
        currentPosition.y = lastTrackedPosition.y;

        distanceTravelled += (Vector3.Distance(currentPosition, lastTrackedPosition))/10;

        lastTrackedPosition = currentPosition;

        acceleration = (roverRigidBody.velocity.magnitude/10 - lastVelocity) / Time.fixedDeltaTime;
        lastVelocity = roverRigidBody.velocity.magnitude/10;
        currentAngle = rover.transform.localRotation.eulerAngles.y;

    }
 



    void OnGUI()
    {
        ///debugging distance travelled

        //add a button that toggles a sidebar to display the current state of the car
        if (GUI.Button(new Rect(10, 10, 90, 20), "Display Info"))
        {
            //toggle the sidebar
            showSidebar = !showSidebar;
             
            // start coroutine to move camera out
            if (isCameraZoomedOut == false){
                StartCoroutine(LerpFOV(100, 0.5f));
                isCameraZoomedOut = true;
            }else{
                StartCoroutine(LerpFOV(60, 0.5f));
                isCameraZoomedOut = false;
            }
    
        }
        if (showSidebar)
        {
            //display the sidebar
            //create rectangle for the sidebar
            
            GUILayout.BeginArea(new Rect(10, 40,(int) Screen.width/3, (int)Screen.height-(50+(int)Screen.height*0.25f)),regularStyle);
            
            // display label for each wheel motor
            foreach (WheelMotor wm in wheelMotors)
            {
                
                Vector3 position;
                Quaternion rotation;
                wm.wheelCollider.GetWorldPose(out position, out rotation);
                float rpm =wm.wheelCollider.rpm;
                //output to gui the position and rotation of each wheel
                GUILayout.Label("Wheel " + wm.name + " position (x,y,z): " + position.ToString("0.00"));
                GUILayout.Label("Wheel " + wm.name + " rpm: " + rpm.ToString("0.00"));
                GUILayout.Label("Wheel " + wm.name + " steering angle: " + wm.wheelCollider.steerAngle.ToString("0.00"));
                

            }

            foreach( ColourDistanceSensor cds in colourDistanceSensors){
                float h_ = cds.GetCurrentH();
                float s_ = cds.GetCurrentS();
                float v_ = cds.GetCurrentV();
                if ((h_ == 0f) & (s_ == 0f) & (v_ == 0f)){
                    rgbTextColour =Color.white;
                    GUILayout.Label("Colour Distance Sensor current view: No Colour detected.");
                }else{

                    rgbTextColour =Color.HSVToRGB(h_, s_, v_);
                    GUILayout.Label("Colour Distance Sensor HSV current view:");
                    colourSensorColour.normal.textColor = rgbTextColour;
                    GUILayout.Label("▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇",colourSensorColour);

                }
                
            }
            foreach(ColourSensor cs in colourSensors){
                float h_ = cs.GetCurrentH();
                float s_ = cs.GetCurrentS();
                float v_ = cs.GetCurrentV();
                if ((h_ == 0f) & (s_ == 0f) & (v_ == 0f)){
                    rgbTextColour =Color.white;
                    GUILayout.Label("Colour Sensor HSV current view: No Colour detected.");
                }else{

                    rgbTextColour =Color.HSVToRGB(h_, s_, v_);
                    GUILayout.Label("Colour Sensor current view:");
                    colourSensorColour.normal.textColor = rgbTextColour;
                    GUILayout.Label("▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇",colourSensorColour);
                }
            }

            foreach (ForceSensor fs in forceSensors){
                isForceSensorTouched = fs.GetIsTouched();
                if (isForceSensorTouched == true){
                    GUILayout.Label("Force Sensor Status: Currently Drilling\'",regularStyle);
                }else{
                    GUILayout.Label("Force Sensor Status: Inactive.", regularStyle);
                }
            }

            

            GUILayout.EndArea();            
        }


        
        //display time taken and distance travelled at bottom of the screen
        //change this to a permanent box at the bottom
        GUILayout.BeginArea(new Rect(10,  (int)Screen.height*0.75f,(int)Screen.width/3, (int)Screen.height*0.25f),regularStyle);
        GUILayout.Label("Time elapsed : " + Time.time.ToString("0.00") + " seconds.",regularStyle );

        GUILayout.Label("Distance travelled : " + distanceTravelled.ToString("0.00") + " meters.",regularStyle);
        GUILayout.Label("Current speed: " + (roverRigidBody.velocity.magnitude/10).ToString("0.0000") + " m/s.",regularStyle);
        
        
        GUILayout.Label("Current acceleration: " + (acceleration).ToString("0.0000") + " m/s^2." ,regularStyle);
        GUILayout.Label("Current angle: " + (currentAngle).ToString("0.0000") + "°",regularStyle);
        GUILayout.Label("Difference in x : " + (rover.transform.position.x - startPosition.x).ToString("0.00") );
        GUILayout.Label("Difference in z : " + (rover.transform.position.z - startPosition.z).ToString("0.00") );
        GUILayout.EndArea(); 

        //move camera left button
        if (GUI.Button(new Rect(Screen.width-60, Screen.height-30, 20, 20), "<-"))
        {
            // start coroutine to move camera out
            StartCoroutine(RotateSmoothly(25,1));
    
        }

        //Create right camera button
        if (GUI.Button(new Rect(Screen.width-30, Screen.height-30, 20, 20), "->"))
        {

            // StartCoroutine(LerpCameraPositionRight(90,1.5f));
            StartCoroutine(RotateSmoothly(25,-1));
    
        }
        
    
    }

    
    public IEnumerator LerpFOV(int fov, float time)
    {
        if (MainCamera.fieldOfView == fov)
        {
            yield break;
        }
        float startFOV = MainCamera.fieldOfView;
        float elapsedTime = 0;
        while (elapsedTime < time)
        {
            float a = elapsedTime / time;
            MainCamera.fieldOfView = Mathf.Lerp(MainCamera.fieldOfView, fov, a);
            
 
            yield return new WaitForEndOfFrame();
            elapsedTime += Time.deltaTime;
        }
    }




// public IEnumerator LerpCameraPositionRight(float rotationAmount, float time)
//     {
        

//         Vector3 originalPos = MainCamera.transform.position;

//         MainCamera.transform.RotateAround(this.transform.position, Vector3.up, -rotationAmount);

//         Vector3 targetPos = MainCamera.transform.position;

//         MainCamera.transform.position = originalPos;

//         if (MainCamera.transform.position == targetPos)
//         {
//             yield break;
//         }
        
//         float elapsedTime = 0;
//         Debug.Log("Resetting elapsed time");
//         while (elapsedTime < time)
//         {
//             float a = elapsedTime / time;
//             Debug.Log("A : " + a);
//             MainCamera.transform.position = Vector3.Lerp(MainCamera.transform.position,targetPos , a);
//             //TODO: FIx this once the prefab issues are solved by reattaching the camera
//             _camera_pos_delta = this.transform.position - MainCamera.transform.position;
//             elapsedTime += Time.deltaTime;
//             yield return new WaitForEndOfFrame();
//         }
//     }

    IEnumerator RotateSmoothly(int degreesPerSecond,float directionFactor)
    {
        
        float targetAngle = 90.0f;
        float total_angle_moved = 0.0f; 
        Debug.Log("DIRECTION FACTOR : " + directionFactor);
        while (true)
        {
            float angle_delta = directionFactor *  degreesPerSecond * Time.deltaTime;
            if (total_angle_moved >= targetAngle)
            {
                yield break;
            }
            Debug.Log("Delta angle " + angle_delta);
            MainCamera.transform.RotateAround(rover.transform.position,Vector3.up, angle_delta);
            total_angle_moved += Mathf.Abs(angle_delta);
            yield return null;

        }


    }

}

