# CodinCodBackend

The (current) goal of this repo is to receive the code from the users, execute it and return the result.

<!--
# Overview

- Whats planned?
- What still needs to happen?
- How is it planned?

Check it [start design](https://excalidraw.com/#json=VAclpcNvHgU1IEO3uDhSk,uvj6jSL_QFl0PyonWV3qmQ) (updated scheme designed by @Andriamanitra ), [game room manager design](https://excalidraw.com/#json=tQfSSp-8PB4Y3HzhL_KBz,BspiuHm0JIADr2ApU0XRDQ) or join our [discord](https://discord.gg/k4hMTjcz3g).
-->
# Setup
### required .env variables

Create a `.env` file, in the CodinCod/environment_variables folder, checkout the `README.m` in there.


### Add test data
Run the test_data.py file.

This will fill your database with test objects (doesn't represent real data => everything is fictional).

```bash
python3 test_data.py
```

### How to run it?

We are using nginx as reverse proxy.
To make both frontend & backend use the same port.

1- install nginx.

2- set nginx configuration file.
```bash
sudo cp nginx/nginx.conf /etc/nginx/nginx.conf
```

3- run nginx.
```bash
sudo systemctl start nginx.service
```

4- Run backend server.
```bash
python3 -m CodinCod
```
