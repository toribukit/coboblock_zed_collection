 
########################################################################
#
# Copyright (c) 2022, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import argparse
import requests
import datetime

def main():
    print('Hello ZED')
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", help="Beginning of the video timestamp, in milliseconds", required=True)
    parser.add_argument("--end", help="End of the video timestamp, in milliseconds", required=True)
    parser.add_argument("--workspace", help="Workspace ID of the devices", required=True)
    parser.add_argument("--token", help="API token generated at https://hub.stereolabs.com/token", required=True)
    parser.add_argument("--format", help="Video format (default is svo.)", type=str, choices=['svo', 'mp4'], default='svo')
    args = parser.parse_args()

    print('Retrieving videos from workspace', args.workspace, 'in format', args.format)

    # Authorization header
    headers = {
        "Authorization": "Bearer " + args.token,
    }

    zed_hub_api_url = 'https://hub.stereolabs.com/api/v1'

    # Retrieve the devices from the workspace
    devices_url = zed_hub_api_url + '/workspaces/' + args.workspace + '/devices'
    devices_get = requests.get(url=devices_url, headers=headers)
    devices = {}
    devices_json = devices_get.json()

    if not 'devices' in devices_json:
        print('Invalid devices response from ' + devices_url)
        print(devices_get.text)
        exit(1)

    # For each device, retrieve all of its cameras
    for device in devices_json["devices"]:
        camera_sn_list = []
        if isinstance(device['camera'], list):
            camera_sn_list = [str(camera['serial_number']) for camera in device['camera']]
        else:
            camera_sn_list.append(str(device['camera']['serial_number']))

        devices[device['id']] = {
            'name': device['name'],
            'cameras': camera_sn_list
        }

    print('Devices retrieved :', list(devices.keys()))

    try:
        start_int = int(args.start)
        end_int = int(args.end)
    except:
        print("Timestamps must be integers. They are", args.start, args.end)

    start_datetime = datetime.datetime.fromtimestamp(start_int/1000)
    end_datetime = datetime.datetime.fromtimestamp(end_int/1000)

    print('Retrieving video from', start_datetime.strftime("%m/%d/%Y, %H:%M:%S"), 'to', end_datetime.strftime("%m/%d/%Y, %H:%M:%S"))

    # Download video from all devices
    for device_id, device in devices.items():
        print('Downloading from', device['name'], '...')
        video_url = zed_hub_api_url + '/workspaces/' + args.workspace + '/devices/' + device_id + '/video/download'

        # Download video from every camera connected to the device
        for camera_sn in device['cameras']:
            print('    Camera SN', camera_sn, '...')
            video_params = '?start=' + args.start + '&end=' + args.end + '&type=' + args.format + '&SN=' + camera_sn
            video_get = requests.get(video_url + video_params, headers=headers)

            if(video_get.status_code == 200):
                open('video_' + device_id + '_SN' + camera_sn + '.' + args.format, 'wb').write(video_get.content)
            else:
                print(video_get.status_code, ': Unable to get this recording on device', device['name'])

if __name__ == "__main__":
    main()


