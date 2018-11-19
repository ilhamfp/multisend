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
	// Belum ada payment management, skip.
	taskService.complete(task, processVariables, null);
	console.log("Lewat send-transaction-detail, gan!");
	console.log("Waiting for confirmation from payment gateway...");
}

module.exports = sendTransactionDetail;
