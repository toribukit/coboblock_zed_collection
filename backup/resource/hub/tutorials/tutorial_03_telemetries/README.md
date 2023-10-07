# Tutorial 3 - Telemetries
This tutorial shows you how to send telemetry to the cloud. It opens a ZED camera and enables ZED tracking, meaning that you can access the camera position at each frame. Then the application gets the camera position and sends it to the cloud at each frame. Therefore the **Telemetry panel** will contain all the consecutive positions of your camera.  

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
```
$ ./ZED_Hub_Tutorial_3
```

## What you should see after deployment
After running this tutorial:
- A live stream should be visible
- The published telemetry should be accessible

### Live video
If you click on the device where the app is deployed in the **Devices** panel, you should see the live video (with a delay of a few seconds).

![](./images/live_and_recordings.png " ")

### Telemetry
If you click on the **Telemetry panel**, you should see the telemetry of your camera position as follow:

![](./images/telemetry.png " ")


## Code Overview

This tutorial opens a ZED and enables ZED tracking, meaning that you can access the camera position at each frame. The application sends this data to ZED Hub as a Telemetry. The **Telemetry panel** in ZED Hub will contain all the consecutive positions of your camera.

What exactly happens:

- Initialize communications with the cloud. See [tutorial_01_basic_app](../tutorial_01_basic_app/README.md) for more information.

- Open the ZED with `p_zed->open(initParameters)`. See [tutorial_02_live_stream_and_recording](../tutorial_02_live_stream_and_recording/README.md) for more information.

- Enable Positional Tracking with `p_zed->enablePositionalTracking(positional_tracking_param)`. See [ZED SDK API documentation](https://www.stereolabs.com/docs/api/classsl_1_1Camera.html#a7989ae783fae435abfdf48feaf147f44) for more information.

- In a `While loop`, grab a new frame

```cpp
    // Main loop
    while (true)
    {
        // Grab a new frame from the ZED
        status_zed = p_zed->grab(runtime_parameters);
        if (status_zed != ERROR_CODE::SUCCESS)
            break;
        ...
    }
```

- Every second, get the camera position (translation and rotation)

```cpp
    if (curr_timestamp.getMilliseconds() >= prev_timestamp.getMilliseconds() + 1000)
        {
            // Retrieve camera position
            p_zed->getPosition(cam_pose);
            sl::Translation translation = cam_pose.getTranslation();
            sl::float3 rotation_vector = cam_pose.getRotationVector();
            ...
        }
```

- Store the camera position inside a JSON and call `HubClient::sendTelemetry`.

  A label is specified as follows `sendTelemetry(std::string label, json& value)`. It allows to improve the telemetry consultation in the ZED Hub interface as it is possible to sort them by label.

```cpp
    // Send Telemetry
    sl_hub::json position_telemetry;
    position_telemetry["tx"] = translation.x;
    position_telemetry["ty"] = translation.y;
    position_telemetry["tz"] = translation.z;
    position_telemetry["rx"] = rotation_vector.x;
    position_telemetry["ry"] = rotation_vector.y;
    position_telemetry["rz"] = rotation_vector.z;
    HubClient::sendTelemetry("camera_position", position_telemetry);
    prev_timestamp = curr_timestamp;
```

- Call `HubClient::update` to send the current image to the cloud.
  See [tutorial_02_live_stream_and_recording](../tutorial_02_live_stream_and_recording/README.md) for more information.

```cpp
    // Always update Hub at the end of the grab loop
    HubClient::update(p_zed);
```
