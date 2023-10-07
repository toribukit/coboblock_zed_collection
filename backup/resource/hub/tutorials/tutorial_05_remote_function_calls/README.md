# Tutorial 5 - Remote Function Calls

This tutorial shows how to make an application containing a **remote function** that computes an addition operation called by a **remote function call**.
This tutorial does not require a ZED to be run.

#### What is a remote function call?
A **remote function call** is a call to a remote function **declared and registered by a ZED Hub app**. The app described in this tutorial declares and registers the `additionCallback` remote function.
The call to this function can be done from **any computer** connected to the internet, by using a **REST request**. The way to perform this request is explained later in this tutorial.


## Getting started

- Add and set up your device on [ZED Hub](https://hub.stereolabs.com).
- For more information, read the [requirements](../../README.md#requirements).

## Build and run this tutorial for development

With Edge Agent installed and running, you can build this tutorial with the following commands:
```bash
$ mkdir build
$ cd build
$ cmake ..
$ make -j$(nproc)
```

Then run your app:
```bash
$ ./ZED_Hub_Tutorial_5
```

## What you should see after deployment
This application defines and registers a **callback function** that can be called from anywhere if the app is running. Therefore there is nothing in the ZED Hub interface apart from the logs.

### Call your remote function
Before calling your remote function, you have to get the necessary information and credentials to use the REST API.

- The **API token** that you can register from the [**API panel**](https://hub.stereolabs.com/token) in ZED Hub. Get more information in the [REST API documentation](https://www.stereolabs.com/docs/cloud/rest-api/)


- The **cloud url** that you can get using the REST API in the ```/workspaces``` endpoint. Get more information in the [REST API documentation](https://www.stereolabs.com/docs/cloud/rest-api/workspaces/).

Example:
```bash
$ curl -s -H "Content-Type:application/json" -H "Authorization:Bearer ${your_token}" -X GET https://hub.stereolabs.com/api/v1/workspaces
```

- The **workspace id** that you can get using the REST API in the ```/workspaces/$workspace_id``` endpoint. Get more information in the [REST API documentation](https://www.stereolabs.com/docs/cloud/rest-api/workspaces/).


- The **device id** that you can get using the REST API in the ```/workspaces/$workspace_id/devices``` endpoint. Get more information in the [REST API documentation](https://www.stereolabs.com/docs/cloud/rest-api/devices/).


To call your remote function, simply use the script ```remote_function_call.sh``` that contains a REST request using curl with the given arguments with num1 and num2 as the numbers you want to use in your addition:

```bash
$ ./remote_function_call.sh $num1 $num2 $cloud_url $workspace_id $device_id $access_token
```

The REST request uses this format:\
It uses the endpoint ```https://hub.stereolabs.com/api/v1/workspaces/${workspace_id}/devices/${device_id}/functions/${function_name}``` where ```function_name``` is the name of the function you registered in your application.
You will use:
- ```sl_hub::HubClient::registerFunction``` to register it in C++
- ```hub.HubClient.register_function``` to register it in Python.

In this tutorial the function registered is `tuto05_add`.
The `parameters` key of the JSON contained in the request contains the parameters of the function. In our case `num1` and `num2`.

```bash
$ curl -s -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${access_token}"\
    -X POST https://hub.stereolabs.com/api/v1/workspaces/${workspace_id}/devices/${device_id}/functions/tuto05_add \
    -d "{ \
    \"parameters\": { \
        \"num1\": ${num1}, \
    \"num2\": ${num2} \
        }\
    }"
```

You can get more information about remote function calls in the [documentation](https://www.stereolabs.com/docs/cloud/remote-functions/call/).


## Code Overview - C++

In the code, the app is connected to the cloud by using `HubClient::connect`, as always.

### Register your callback function
Then your remote function parameters are set. Basically, a name is given, `tuto05_add`, and the callback type is set.
> **Note**: The callback type can be:
> - `CALLBACK_TYPE::ON_REMOTE_CALL`
> - `CALLBACK_TYPE::ON_RESTART_CALL`

Then the remote function is registered: the function `additionCallback` associated with the `callback_params` is registered by the cloud.

```c++
    // Set your callback parameters
    CallbackParameters callback_params;
    callback_params.setRemoteCallback("tuto05_add", CALLBACK_TYPE::ON_REMOTE_CALL);
    // Register your callback function
    HubClient::registerFunction(additionCallback, callback_params);
```


### Define your callback function

A remote function must have this minimum structure:

```c++
void myRemoteFunction(FunctionEvent& event) {
    sl_hub::json params = event.getEvenParameters();

    // TODO : your custom code
    bool success = true;
    if (success)
    {
        event.status = 0;
        event.result = result;
    }
    else
    {
        event.status = 1;
        event.result = "Error message";
    }
}
```

The `getEventParameters` function retrieves the JSON `parameters` from the REST request called the remote function.
In our case, `params` contains this JSON (5 and 10 are given as an example):
```JSON
{
    "num1": 5,
    "num2": 10
}
```

Then the remote function can use these parameters to do anything. In our case, the two input values are added after making sure they are contained in `params`. The result is stored in `event.result` and the status `event.status` is set to 0 to notify that the function performed as expected.

```c++
    // Check if parameters are present and valid
    if (params.contains("num1") && params["num1"].is_number_integer() &&
        params.contains("num2") && params["num2"].is_number_integer())
    {
        int num1 = params["num1"].get<int>();
        int num2 = params["num2"].get<int>();
        int result = num1 + num2;

        // Log your result
        HubClient::sendLog("Addition called : " + std::to_string(num1) + " + " + std::to_string(num2) + " = " + std::to_string(result), LOG_LEVEL::INFO);

        // Update the result and status of the event
        event.status = 0;
        event.result = result;
    }

```

In case of a problem, the status is set to 1.
```c++
    else
    {
        HubClient::sendLog("Addition remote function was used with wrong arguments.", LOG_LEVEL::ERROR);
        event.status = 1;
        event.result = "Addition remote function was used with wrong arguments.";
    }
```

So we finally have the following remote function:

```c++
void additionCallback(FunctionEvent &event)
{
    // Get the parameters of the remote function call
    std::cout << "function called !" << std::endl;
    sl_hub::json params = event.getEventParameters();

    // Check if parameters are present and valid
    if (params.contains("num1") && params["num1"].is_number_integer() &&
        params.contains("num2") && params["num2"].is_number_integer())
    {
        int num1 = params["num1"].get<int>();
        int num2 = params["num2"].get<int>();
        int result = num1 + num2;

        // Log your result
        HubClient::sendLog("Addition called : " + std::to_string(num1) + " + " + std::to_string(num2) + " = " + std::to_string(result), LOG_LEVEL::INFO);

        // Update the result and status of the event
        event.status = 0;
        event.result = result;
    }
    else
    {
        HubClient::sendLog("Addition remote function was used with wrong arguments.", LOG_LEVEL::ERROR);
        event.status = 1;
        event.result = "Addition remote function was used with wrong arguments.";
    }
}
```
