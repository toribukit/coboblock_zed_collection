# Tutorial 1 - Basic Application

This tutorial shows how to make a very simple application that **sends logs** to ZED Hub.

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
$ ./ZED_Hub_Tutorial_1
```

## Code Overview

To initialize your application, use the `HubClient::connect` function that starts communications between your app and ZED Hub. It must be called before using the HubClient API, therefore before sending any logs (`HubClient::sendLog`), telemetry (`HubClient::sendTelemetry`), etc.
```c++
    STATUS_CODE status_hub;
    status_hub = HubClient::connect("basic_app");
```
You can set the log level limit to be displayed. Every log with LOG_LEVEL below the limit will not be printed.  ``` setLogLevelThreshold(LOG_LEVEL local_terminal_log_level, LOG_LEVEL cloud_log_level)```
```c++
    HubClient::setLogLevelThreshold(LOG_LEVEL::INFO, LOG_LEVEL::INFO);
```

You can send a simple log to the cloud with ```HubClient::sendLogInfo```
```c++
    HubClient::sendLog("Application connected", LOG_LEVEL::INFO);
```

You can check if your application is connected to the cloud with ```HubClient::isInitialized```
```c++
    if (HubClient::isInitialized() == STATUS_CODE::SUCCESS)
        HubClient::sendLog("Application connected", LOG_LEVEL::INFO);
```

Note that there are 7 log Levels:

- 0 - `DEBUG`: log level for debugging
- 1 - `INFO`: log level for an info
- 2 - `STATUS`: log level for a status
- 3 - `WARNING`: log level for a warning
- 4 - `ERROR`: log level for an error
- 5 - `SUCCESS`: log level for a success
- 6 - `DISABLED`: level where no log will be sent
