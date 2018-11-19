const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function cancelOrder({ task, taskService }) {
    let processVariables = new Variables();
    // console.log(task.variables.getAllTyped());
    processVariables.setAllTyped(task.variables.getAllTyped());

    let secret_key = task.variables.get('secret_key');
    let cost = task.variables.get('cost');

    var url = 'http://localhost:5006/?wsdl';
    var args = {
        request:{
            secret_key : secret_key,
            bank_detail : '23523423423',
            payment_method : 'BCA',
            amount : cost
        }
    };
    soap.createClient(url, function(err, client) {
        client.deposit(args, function(err, result) {
            // console.log(JSON.stringify(result))
            current_balance = result.depositResult.current_balance;
            console.log("Order canceled");
            console.log("Current balance is refilled by: " + cost);
            console.log("Current balance is: " + current_balance);
            taskService.complete(task, processVariables, null);
        });
    });
}

module.exports = cancelOrder;
