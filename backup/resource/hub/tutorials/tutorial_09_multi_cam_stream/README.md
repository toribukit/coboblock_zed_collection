# Tutorial 9 - Multi-camera Stream

This tutorial shows you how to stream more than one ZED camera.

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
$ ./ZED_Hub_Tutorial_9
```

## Code overview

The app retrieves all connected ZED cameras and stores their `DeviceProperties` in a vector `devList`.

```c++
// Get detected cameras
std::vector<DeviceProperties> devList = Camera::getDeviceList();
int nb_detected_zed = devList.size();
```

Then open each camera and register them.
```c++
// Open every detected cameras
for (int i = 0; i < nb_detected_zed; i++)
{
    zeds[i].reset(new sl::Camera());
    initParameters.input.setFromCameraID(i);

    ERROR_CODE err = zeds[i]->open(initParameters);
    if (err == ERROR_CODE::SUCCESS)
    {
        auto cam_info = zeds[i]->getCameraInformation();
        std::cout << "serial number: " << cam_info.serial_number << ", model: " << cam_info.camera_model << ", status: opened" << std::endl;
    }
    else
    {
        std::cout << " Error on camera " << i << " : " << err << std::endl;
        throw(new std::exception());
    }

    // Register the camera once it's open
    UpdateParameters updateParameters;

    // On Ubuntu desktop, on consumer-level GPUs, you don't have enough hardware encoder to stream multiple devices
    // and to record at the same time. https://en.wikipedia.org/wiki/Nvidia_NVENC
    // On jetsons or on business-grade gpus, you can do whatever you want.
    updateParameters.enable_recording = false;
    status_hub = HubClient::registerCamera(zeds[i], updateParameters);
    if (status_hub != STATUS_CODE::SUCCESS)
    {
        std::cout << "Camera registration error " << status_hub << std::endl;
        exit(EXIT_FAILURE);
    }
}
```

Then, using a thread, every stream is associated with a `grab loop` to stream them.

```c++
// Streams' loop to grab image
void stream_loop(const std::shared_ptr<Camera> &p_zed, bool &run)
{
    Mat zed_image(1280, 720, MAT_TYPE::U8_C4);

    while (run)
    {
        // grab current image
        if (p_zed->grab() == ERROR_CODE::SUCCESS)
        {
            p_zed->retrieveImage(zed_image, VIEW::LEFT, MEM::CPU, zed_image.getResolution());
            HubClient::update(p_zed, zed_image);
        }
        else
            run = false;
    }
}
```
