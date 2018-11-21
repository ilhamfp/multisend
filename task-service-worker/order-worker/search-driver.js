const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');
BASE_URL = 'http://127.0.0.1:9999/';

async function searchDriver({ task, taskService }) {
    let processVariables = new Variables();
    // console.log(task.variables.getAllTyped());
    processVariables.setAllTyped(task.variables.getAllTyped());

    let secret_key = task.variables.get('secret_key');
    let cost = task.variables.get('cost');

    // Komen di bawah merupakan peninggalan sebelum diganti ke REST
    var url = 'http://localhost:5005/?wsdl';
    var args = {
        order_requests:{
            OrderRequest:{
                sender_secret_key : secret_key,
                from_lat : task.variables.get('from_lat'),
                from_lng : task.variables.get('from_lng'),
                destination : task.variables.get('destination'),
                weight : task.variables.get('weight'),
                receiver_name : task.variables.get('receiver_name'),
                additional_detail : task.variables.get('additional_detail'),
            }
        }
    };
    soap.createClient(url, function(err, client) {
        client.place_order(args, function(err, result) {
            // result = JSON.stringify(result);
            // console.log(JSON.stringify(result))
            status = result.place_orderResult.OrderResponse[0].status
            order_unique_id = result.place_orderResult.OrderResponse[0].order_unique_id
            console.log("Search driver: "+status)
            if (status == "Success") {
                processVariables.set('found', true);
                console.log("The order unique_id is: "+order_unique_id)
            } else {
                processVariables.set('found', false);
            }
            taskService.complete(task, processVariables, null);
        });
    });
}

module.exports = searchDriver;
