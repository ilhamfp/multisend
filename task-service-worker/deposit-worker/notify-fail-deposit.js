const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function notifyFailDeposit({ task, taskService }) {
	let processVariables = new Variables();
	// notify fail ke user
	taskService.complete(task, processVariables, null);
    console.log("Deposit aborted by payment gateway")
}

module.exports = notifyFailDeposit;
