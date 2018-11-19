const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function refillBalance({ task, taskService }) {
	let secret_key = task.variables.get('secret_key');
	let amount = task.variables.get('amount');
	let processVariables = new Variables();
	processVariables.set('secret_key', secret_key);
	processVariables.set('amount', amount);

	var url = 'http://localhost:5006/?wsdl';
	var args = {
		request:{
			payment_method : 'BCA',
			secret_key : secret_key,
			amount : amount,
			bank_detail : '23523423423',
		}
	};
	soap.createClient(url, function(err, client) {
	    client.deposit(args, function(err, result) {
	        // console.log(JSON.stringify(result))
	        current_balance = result.depositResult.current_balance;
	        console.log("Current balance is refilled by: " + amount);
	        console.log("Current balance is: " + current_balance);
	        taskService.complete(task, processVariables, null);
	    });
	});
}

module.exports = refillBalance;
