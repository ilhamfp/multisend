const { Variables } = require('camunda-external-task-client-js');
const request = require('request');

async function createNewBooking({ task, taskService }) {
	let check_in = task.variables.get('check_in');
	let check_out = task.variables.get('check_out');
	let total_price = task.variables.get('total_price');

	let room_id = task.variables.get('room_id');
	let guest_id = task.variables.get('guest_id');

	let processVariables = new Variables();

	const headers = {
		'Content-Type': 'application/json'
	};

	const form = {
		'check_in': check_in,
		'check_out': check_out,
		'total_price': total_price,
		'room_id': room_id,
		'guest_id': guest_id
	}

	const options = {
		url: 'http://127.0.0.1:5000/bookings',
		method: 'POST',
		headers: headers,
		qs: form
	}

	request(options, function(error, response, body) {
		if (body.length != 0) {
			processVariables.set('booking_id', body.id);
		}
		taskService.complete(task, processVariables, null);
	});
}

module.exports = createNewBooking;
