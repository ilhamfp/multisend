const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function notifyFailWithdrawal({ task, taskService }) {
	let secret_key = task.variables.get('secret_key');
	let amount = task.variables.get('amount');
	let processVariables = new Variables();
	processVariables.set('secret_key', secret_key);
	processVariables.set('amount', amount);
    console.log("Fail")
	// notify fail ke user
    var nodemailer = require('nodemailer');

    var transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: 'tubespplbs@gmail.com',
        pass: 'tubespplbs123'
      }
    });

    var mailOptions = {
      from: 'tubespplbs@gmail.com',
      to: 'tubespplbs@gmail.com',
      subject: 'Withdrawal Status',
      text: emailText
    };

    transporter.sendMail(mailOptions, function(error, info){
      if (error) {
        console.log(error);
      } else {
        console.log('Email sent: ' + info.response);
      }
    });
	taskService.complete(task, processVariables, null);
}

module.exports = notifyFailWithdrawal;
