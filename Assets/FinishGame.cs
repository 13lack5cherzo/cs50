using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


[RequireComponent(typeof(Text))]
public class FinishGame : MonoBehaviour
{

    private Text text;

    // Start is called before the first frame update
    void Start()
    {
        text = GameObject.Find("CompleteText").GetComponent<Text>();
    }

    // Update is called once per frame
    void Update()
    {
    }


    void OnControllerColliderHit(ControllerColliderHit hit)
    {
        if (hit.gameObject.tag == "Finish")
        {
            text.text = "LEVEL COMPLETE";
        }
    }

}
