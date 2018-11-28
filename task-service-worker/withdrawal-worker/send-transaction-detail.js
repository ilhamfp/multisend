const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function sendTransactionDetail({ task, taskService }) {
	let secret_key = task.variables.get('secret_key');
	let amount = task.variables.get('amount');
	let processVariables = new Variables();
	processVariables.set('secret_key', secret_key);
	processVariables.set('amount', amount);
    processVariables.set('success', false);

	let bank = task.variables.get('bank');
    let paymentMethodId = 'bank';
    var url = 'http://167.205.35.211:8080/easypay/PaymentService?wsdl';
    var args = {
            "paymentMethodId" : paymentMethodId, 
            "amount" : amount
        };
    soap.createClient(url, function(err, client) {
        client.beginPayment(args, function(err, result) {
            // console.log(JSON.stringify(result))
            console.log("PaymentGateway integration");
            taskService.complete(task, processVariables, null);
        });
    });
}

module.exports = sendTransactionDetail;
