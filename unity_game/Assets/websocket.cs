using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class websocket : MonoBehaviour
{
    InputField outputArea;
    InputField inputArea;
    InputField character;

    void Start()
    {
        inputArea = GameObject.Find("InputArea").GetComponent<InputField>();
        outputArea = GameObject.Find("OutputArea").GetComponent<InputField>();
        character = GameObject.Find("Character").GetComponent<InputField>();
        GameObject.Find("PostButton").GetComponent<Button>().onClick.AddListener(PostData);
    }

    void PostData()
    {
        StartCoroutine(SendMessageToApi());
    }

    private IEnumerator SendMessageToApi()
    {
        // Get the message from the input field
        string message = inputArea.text;
        string character_name = character.text;

        // Create a request with the message as data
        WWWForm form = new WWWForm();
        form.AddField("message", message);
        form.AddField("character_name", character_name);

        // Send the request to the API
        using (UnityWebRequest www = UnityWebRequest.Post("http://127.0.0.1:5000/api", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log("Failed to send message to API: " + www.error);
            }
            else
            {
                // Get the response from the API
                string response = www.downloadHandler.text;
                outputArea.text = response;
            }
        }
    }
}