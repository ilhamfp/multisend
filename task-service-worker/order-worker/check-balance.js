const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function checkBalance({ task, taskService }) {
    let processVariables = new Variables();
    // console.log(task.variables.getAllTyped());
    processVariables.setAllTyped(task.variables.getAllTyped());

    let secret_key = task.variables.get('secret_key');
    let cost = task.variables.get('cost');

    var url = 'http://localhost:5006/?wsdl';
    var args = {
        request:{
            secret_key : 'vIywNgjTJTNwIHZCXyHTZgfBepWwCx'
        }
    };
    soap.createClient(url, function(err, client) {
        client.get_balance(args, function(err, result) {
            // result = JSON.stringify(result);
            current_balance = result.get_balanceResult.current_balance
            console.log("Current balance is: "+current_balance)
            if (current_balance < cost) {
                processVariables.set('sufficient', false);
                console.log("Invalid order: balance is not sufficient")
            } else {
                processVariables.set('sufficient', true);
                console.log("Valid order: balance sufficient")
            }
            taskService.complete(task, processVariables, null);
        });
    });
}

module.exports = checkBalance;
