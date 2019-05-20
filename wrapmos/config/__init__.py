"""Functions relating to device configuration.

This module manages config stored as JSON from the wemos device.

Additionally, if offers a simple webserver which allows editing and submitting of changes
to the saved config.
"""

import json
import re
import socket
from errno import ENOENT

CONFIG_FILE="config.json"

def config():
    """Reads and returns JSON config.

    :return: configuration values
    :rtype: dict
    """

    try:
        with open(CONFIG_FILE) as conf_f:
            return json.load(conf_f)
    except:
        # Never error - missing/empty config can be worked around elsewhere!
        return {}

def server(port=80):
    """Simple web server to display, receive and update config.json

    Note: When config changes, various other modules wil be updated, e.g. wifi

    :param port: TCP Port to run server on.
    """

    response = """\
HTTP/1.1 200 OK
Content-Type: text/html
\r\n
<!DOCTYPE html>
  <html>
    <head><title>ESP8266 config.json</title></head>
    <body>
      <h2>Edit JSON Configuration</h2>
      <h3>{}</h3>
      <form method="post" enctype="text/plain">
        <textarea name="config" rows="40", cols="80">{}</textarea>
        <button type="submit">Update</button>
      </form>
    </body>
  </html>"""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(5)

    # Read in the JSON config as a string
    conf = json.dumps(config())

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode('utf-8')
        updated = ''
        if 'POST' in request:
            # Pick config POST data out of request
            res = re.search('config=(.*)', request)
            new_conf = res.group(1).strip()
            # Check it's valid json
            try:
                json.loads(new_conf)
            except ValueError as exc:
                updated = exc
            else:
                # Write out config file
                with open(CONFIG_FILE, 'w') as conf_f:
                    try:
                        conf_f.write(new_conf)
                        conf = new_conf
                        updated = "Updated!"
                        # Update wifi from config
                        from .. import wifi
                        wifi.client(reconfigure=True)
                        wifi.access_point()
                    except Exception as exc:
                        updated = "Error saving configuration: {}".format(exc)
        conn.send(response.format(updated, conf).encode('utf-8'))
        conn.close()
