const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function sendOrderStatus({ task, taskService }) {
	let processVariables = new Variables();
    // console.log(task.variables.getAllTyped());
    processVariables.setAllTyped(task.variables.getAllTyped());
	// Kirim ke pemannggil
	taskService.complete(task, processVariables, null);
}

module.exports = sendOrderStatus;
