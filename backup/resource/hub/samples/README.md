# ZED Hub Samples

In addition to the **ZED Hub tutorials**, some sample apps are available.

- [**Camera Viewer Sample**](./camera_viewer_sample/README.md) corresponds to the app "Camera Viewer" available on each device. The source code is available and explained here.
It consists in:
    - A basic setup of the camera
    - A video stream
    - Callbacks that allow modifying the video parameters of the camera (exposure, gamma, etc.)

- [**Object Detection Sample**](./object_detection_sample/README.md) demonstrates what can be done very simply with object detection. It consists in:
    - An object detection setup of the camera
    - A custom video streamed where we highlight detected persons with ```opencv```
    - Callbacks that enable/disable a few parameters: highlighting, events, telemetry, etc.

- [**GNSS Tracker Sample**](./gnss_tracker_sample/README.md) shows how to send GNSS data to the **Maps page** with a random walk. It consists in:
    - A basic setup of the camera
    - A video stream
    - WebRTC messages simulating a random walk
    - Callbacks that determine the data sending frequency and that retrieve waypoints

- [**Multiplatform Sample**](./multiplatform_sample/README.md) shows how to create an app that can be deployed on every platform.