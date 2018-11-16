# Tugas Besar PPLBS

Tugas besar Pembangunan Perangkat Lunak Berorientasi Service  

## How to test each task service
1. Run
```
pip install -r requirement.txt
```
2. Run
```
python test_task_service.py
```

## How to run BPM
##% Prerequisites
1. Camunda Modeler  
2. Camunda BPM
3. NodeJS >= v8.9.4  
### Run Workers  
1. Go to order-worker directory  
2. Run  
```
npm init order-worker -y
```
3. Run   
```
npm install -s camunda-external-task-client-js
```
4. Run   
```
node ./worker.js
```

### Run BPM  
1. Open 'order.bpmn' on Camunda Modeler and deploy as 'Order'.  
2. Open Postman, send POST request to 
```
'http://localhost:8080/engine-rest/process-definition/key/Process_1j8ecvq/start'
```
with application/json body
```
{
    "variables": {
        "user_id":{
            "value":"123ID",
            "type":"string"
        },
        "distance": {
            "value":10,
            "type":"long"
        },
        "item": {
            "value": "PPLOSSZ",
            "type":"string"
        }
    }
}
```



