const { Variables } = require('camunda-external-task-client-js');
const request = require('request');

async function checkStatus({ task, taskService }) {
    let coupon_code = task.variables.get('coupon_code');
    let accepted = task.variables.get('accepted');

    let processVariables = new Variables();
    if (coupon_code !== null) {
        processVariables.set('status', 2);
    } else if (accepted == true) {
        processVariables.set('status', 1);
    } else {
        processVariables.set('status', 0);
    }

    taskService.complete(task, processVariables, null);
}

module.exports = checkStatus;
