const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');
BASE_URL = 'http://127.0.0.1:9999/';

async function cancelOrder({ task, taskService }) {
    let processVariables = new Variables();
    // console.log(task.variables.getAllTyped());
    processVariables.setAllTyped(task.variables.getAllTyped());

    let secret_key = task.variables.get('secret_key');
    let cost = task.variables.get('cost');
    let balance_has_deducted = task.variables.get('balance_has_deducted');

    if (balance_has_deducted) {
        // Refill balance
        const headers = {
            'Content-Type': 'application/json',
            'Authorization' : secret_key
        };

        const options = {
            url: BASE_URL  + "balance/deposit",
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                                    "bank" : '23523423423',
                                    "payment_method" : 'BCA',
                                    "amount" : cost
                                })
        };


        request(options, function(error, response, body) {
            console.log(JSON.parse(response.body))
            if (response.statusCode === 200) {
                response = JSON.parse(response.body)
                if (!response.error) {
                    current_balance = response.balance
                    console.log("Order canceled");
                    console.log("Current balance is refilled by: " + cost);
                    console.log("Current balance is: " + current_balance);
                    taskService.complete(task, processVariables, null);
                } else {
                    console.log(response.error);
                }
            } else {
                console.log("ERROR CANCEL ORDER: " + response.statusCode);
            }
        });
    } else {
        console.log("Order canceled");
    }
    

    // Komen di bawah merupakan peninggalan sebelum diganti ke REST
    // var url = 'http://localhost:5006/?wsdl';
    // var args = {
    //     request:{
    //         secret_key : secret_key,
    //         bank_detail : '23523423423',
    //         payment_method : 'BCA',
    //         amount : cost
    //     }
    // };

    // soap.createClient(url, function(err, client) {
    //     client.deposit(args, function(err, result) {
    //         // console.log(JSON.stringify(result))
    //         current_balance = result.depositResult.current_balance;
    //         console.log("Order canceled");
    //         console.log("Current balance is refilled by: " + cost);
    //         console.log("Current balance is: " + current_balance);
    //         taskService.complete(task, processVariables, null);
    //     });
    // });
}

module.exports = cancelOrder;
