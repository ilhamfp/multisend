# Tugas Besar PPLBS

Tugas besar Pembangunan Perangkat Lunak Berorientasi Service  


## How to run  
### Workers  
1. Go to order-worker directory  
2. Run   
```
npm install -s camunda-external-task-client-js
```
2. Run   
```
node ./worker.js
```

### BPM  
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