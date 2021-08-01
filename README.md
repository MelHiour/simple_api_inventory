# simple_api_inventory
This is just a simplest inventory you can imagine with even more simple API. 
- There is a [short article](http://www.labnfun.ru/2021/08/api.html) available in Russian as well.
- You can fing image on Docker Hub [here](https://hub.docker.com/r/melhiour1/simple_inventory).
- I also created a simple Curl bash wrapper to simplify query process [here](https://github.com/MelHiour/vyos_onbox_scripts/blob/main/inventory.sh)

## Usage
After start you can interact with API, the result will be stored in `db.json` file in `data` folder.
```
docker run --name simple_inventory \
-p 5000:5000/tcp \
-v /srv/data:/app/data \
--restart always \
melhiour1/simple_inventory
```

### Files
```
.
├── .github/workflows           Actions specified to build the image and upload to Dockerhub
├── Dockerfile                  Instructions to buld the image
├── README.md                   This very file
├── helpers.py                  Just a couple of classes with all internal logic
├── requirements.txt            All you need to have to run the script
└── simple_inventory.py         Main file with Web API  

```
### What can you do?
- Get the list of equipment in your inventory. If you have any. I don't.
```
# curl http://10.20.30.12:5000/inventory/

    > {"equipment":[[]]}
```

- Add new equipment using POST with atttached JSON. There is no limitation of JSON format, but it hasn't been designed for nested data structures.
```
# curl --header "Content-Type: application/json" \
--request POST \
--data '{"name":"FRW1","address":"10.0.0.1","location":"Lipetsk"}' \
http://10.20.30.12:5000/inventory/

    > {"name":"FRW1"}

# curl --header "Content-Type: application/json" \
--request POST \
--data '{"name":"FRW2","address":"192.168.0.1","location":"Voronezh","OS":"JunOS"}' \
http://10.20.30.12:5000/inventory/

    > {"name":"FRW2"}

# curl --header "Content-Type: application/json" \
--request POST \
--data '{"name":"FRW3","address":"172.16.0.1","location":"Dublin","OS":"VyOS","type":"VM"}' \
http://10.20.30.12:5000/inventory/

    > {"name":"FRW3"}

# curl http://10.20.30.12:5000/inventory/

    > {"equipment":[["FRW1","FRW2","FRW3"]]}
```

- Get the detailed view of items in inventory.
```
# curl http://10.20.30.12:5000/inventory/FRW1

    > {"address":"10.0.0.1","location":"Lipetsk","name":"FRW1"}
```

- Get the attribute of equipment.
```
# curl http://10.20.30.12:5000/inventory/FRW1/address

    > "10.0.0.1"
```

- Update the equipment using PUT with JSON
```
# curl --header "Content-Type: application/json" \
--request PUT \
--data '{"address":"10.10.10.10"}' \
http://10.20.30.12:5000/inventory/FRW1

    > {"address":"10.10.10.10","location":"Lipetsk","name":"FRW1"}

# curl http://10.20.30.12:5000/inventory/FRW1/address
    
    > "10.10.10.10"
```

- Delete your equipment
```
# curl --request DELETE http://10.20.30.12:5000/inventory/FRW2

    > {"OS":"JunOS","address":"192.168.0.1","location":"Voronezh","name":"FRW2"}

# curl http://10.20.30.12:5000/inventory/

    > {"equipment":[["FRW1","FRW3"]]}
```

### Why bother?
Yeah, I know I can use an Excel spreadsheet for that and actually I did...

But I had to play with 
- OOP. Each equipment represents an instance of the class which is stored as an attrtibute of another instance. See [helpers.py](https://github.com/MelHiour/simple_api_inventory/blob/main/helpers.py)
- API. I really wanted to created the simple API using Flask. I did smth like that before in [pi_clock](https://github.com/MelHiour/pi_clock), but this time it's more solid.
- Docker. The idea is to build the docker image and upload it to DockerHub using GitHub CI/CD pipeline. See [main.yaml](https://github.com/MelHiour/simple_api_inventory/blob/main/.github/workflows/main.yaml)
