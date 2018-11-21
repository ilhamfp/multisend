const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function createTransactionDeposit({ task, taskService }) {
	// Get variable from message
	let secret_key = task.variables.get('secret_key');
	let amount = task.variables.get('amount');
	// Set variable
	let processVariables = new Variables();
	processVariables.set('secret_key', secret_key);
	processVariables.set('amount', amount);
    processVariables.set('success', false);
	// Belum ada payment management, skip.
	taskService.complete(task, processVariables, null);
	console.log("Lewat create-transaction-deposit, gan!");
}

module.exports = createTransactionDeposit;
