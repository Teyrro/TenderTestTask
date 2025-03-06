### How will i launch the project ?
1) Clone repository
2) For next step you should have docker daemon on Unix or dokcer desktop on Windows OS. 
So write in terminal `docker compose up -d`
3) Then start `main.py` for executing example func and find in 
root directory file by named result.json
4) Or you can start testing using command `docker compose exec -T
workers bash config/scripts/testing.sh`, but don't forget to start docker
orchestration `docker compose up -d`, if you didn't it before.