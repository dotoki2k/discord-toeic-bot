# TOEIC discord bot

This project develops a Discord bot that automatically sends TOEIC questions when a user issues the request command.

## Data:

The project crawls all TOEIC Part 5 questions from study4.com.
The script for crawling is located in the folder `./tools`.

- ### How to use that tool:
  - First, log in to study4.com using your browser to retrieve the cookie. Then, update the cookies parameter with the cookie you just obtained:
    ```
    cookies = {
        "csrftoken": "",
        "sessionid": "",
        "cf_clearance": "",
    }
    ```
  - After that, run the script to crawl the questions by using the command line below, and data will be stored in JSON files in the folder `./data`:
    
    ```python ./tools/crawl_exam_paper.py```

## How to build this source code to docker image.

- After crawling the data, run the following Docker command to build the image:

  ```docker build -t <image_name>```

- Then, use this command to start the Docker container:
  
  ```docker run -d --name <container_name> -e DISCORD_TOKEN=<your_bot_discord_token> <image_name>```

- ### How to get bot Discord token?
  just following this video: https://youtu.be/Gqurhm2QxA0.
