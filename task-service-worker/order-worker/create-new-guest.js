const { Variables } = require('camunda-external-task-client-js');
const request = require('request');

async function createNewGuest({ task, taskService }) {
	let name = task.variables.get('name');
	let mobile_phone = task.variables.get('mobile_phone');
	let identity_number = task.variables.get('identity_number');
	let email = task.variables.get('email');

	let processVariables = new Variables();

	const headers = {
		'Content-Type': 'application/json'
	};

	const form = {
		'name': name,
		'mobile_phone': mobile_phone,
		'identity_number': identity_number,
		'email': email
	}

	const options = {
		url: 'http://127.0.0.1:5000/guests',
		method: 'POST',
		headers: headers,
		qs: form
	}

	request(options, function(error, response, body) {
		if (body.length != 0) {
			processVariables.set('guest_id', body.id);
		}
		taskService.complete(task, processVariables, null);
	});
}

module.exports = createNewGuest;
