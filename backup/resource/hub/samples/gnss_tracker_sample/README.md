# GNSS Tracker

This sample shows how to send GNSS data in a ZED Hub Application to display them on the **Map page**.
It also explains how to generate:

- **Logs** that give information about the application's status
- **WebRTC messages** that contain data to be displayed on ZED Hub's **Map page**
- A **Callback function** that retrieves waypoints created in ZED Hub's **Map page**

The application defines **parameters** that can be modified in the ZED Hub interface to change the application's behavior while it is running.

## Getting started

- Add and set up your device on [ZED Hub](https://hub.stereolabs.com).
- For more information, read the [requirements](../../README.md#requirements).

## Build and deploy this tutorial

### How to build your application (for development)

Build your app :

```bash
$ cd sources
$ mkdir build
$ cd build
$ cmake ..
$ make -j$(nproc)
```

This application defines application parameters to modify its behavior while it is running. Move the `parameters.json` file to the path you specified in the `HubClient::loadApplicationParameters` function.

```bash
$ cp ../parameters.json .
```

Then to run your app :

```bash
$ ./GNSS_Tracker_Sample
```

To dynamically change the parameters and activate their callbacks, edit the `parameters.json` file.

### How to deploy your application

Packages your app by generating an app.zip file using :

```bash
$ edge_cli deploy .
```

You can now [deploy your app](https://www.stereolabs.com/docs/cloud/applications/deployment/) using the ZED Hub interface:

- In your workspace, in the **Applications** section, click on **Add application**
- Select the ZIP file containing the application in your filesystem
- Select the devices on which you want to deploy the app and press **Upload**

## What you should see after deployment

### Live video

A video with bounding boxes around detected persons should be available in the **Video panel**.

### Logs

The logs should inform you about the app status.

### Maps

The GNSS data should be displayed on ZED Hub's **Map page**.

### Parameters

The following parameter can be used to modify your application's behavior:

- **Data frequency**: Data frequency defines how often data are produced by the application. Every second by default.

## Code overview

### Parameters callback

The following callbacks are defined in this sample and will be triggered when a parameter is modified in ZED Hub.

Callback for `dataFreq` application parameter

```c++
void onDataFreqUpdate(FunctionEvent &event)
{
    event.status = 0;
    dataFreq = HubClient::getParameter<float>("dataFreq", PARAMETER_TYPE::APPLICATION, dataFreq);
}
```

Callback for `waypoints` device parameter (as waypoints are sent as device parameter)

```c++
void onWaypoints(FunctionEvent &event)
{
    // Get gnss waypoints from the device parameters
    std::string waypoints = HubClient::getParameter<std::string>("waypoints", PARAMETER_TYPE::DEVICE, "[]");
    std::cout << "waypoints: " << waypoints << std::endl;

    event.status = 0;
    event.result = waypoints;
}
```

### Initialization

The application is initialized using `HubClient::connect`, and the ZED camera is started with the ZED SDK `open` method and registered to ZED Hub using `HubClient::registerCamera`.

### Main loop

- **WebRTC messages** containing GNSS position (which is randomly generated) are sent to the `geolocation` label to all connected peers.

```c++
Timestamp current_ts = p_zed->getTimestamp(TIME_REFERENCE::IMAGE);

if ((uint64_t)(current_ts.getMilliseconds() >= (uint64_t)(prev_timestamp.getMilliseconds() + (uint64_t)dataFreq * 1000ULL)))
{
    // Update coordinate
    latitude += getRandom();
    latitude = min(90.0, latitude);
    latitude = max(-90.0, latitude);
    longitude += getRandom();
    longitude = min(180.0, longitude);
    longitude = max(-180.0, longitude);
    altitude += getRandom();

    // Send data
    json gnss;
    gnss["layer_type"] = "geolocation";
    gnss["label"] = "GNSS_data";
    gnss["position"] = {
        {"latitude", latitude},
        {"longitude", longitude},
        {"altitude", altitude}};
    HubClient::sendDataToPeers("geolocation", gnss.dump());
    prev_timestamp = current_ts;
}
```
