# Tutorial 7 - MQTT Publisher

This tutorial shows you how to communicate between apps through ZED Hub.

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
$ ./ZED_Hub_Tutorial_7
```

## What you should see after deployment

The app publishes a basic message on the MQTT topic `/v1/local_network/my_custom_data`. A log is published each time a message is sent.

## Code overview

First, the application **connects** to ZED Hub, allowing it to communicate via MQTT to other devices.

```c++
    // Initialize the communication to ZED Hub, without a zed camera.
    STATUS_CODE status_hub;
    status_hub = HubClient::connect("pub_app");
    if (status_hub != STATUS_CODE::SUCCESS)
    {
        std::cout << "Initialization error " << status_hub << std::endl;
        exit(EXIT_FAILURE);
    }
```
Then the MQTT topic parameters are set.
```c++
    std::string topic_name = "/my_custom_data";
```

Finally, a message is sent every 10 seconds
```c++
    // Main loop
    while (true)
    {
        const auto p1 = std::chrono::system_clock::now();

        json my_message_js;
        my_message_js["message"] = "Hello World";
        my_message_js["my_custom data"] = 54;
        my_message_js["timestamp"] = std::chrono::duration_cast<std::chrono::seconds>(p1.time_since_epoch()).count();

        HubClient::publishOnTopic(topic_name, my_message_js);
        HubClient::sendLog("Message published", LOG_LEVEL::INFO);

        sleep_ms(10000); // 10 seconds
    }
```
