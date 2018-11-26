const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function notifySuccessDeposit({ task, taskService }) {
	let amount = task.variables.get('amount');
	let processVariables = new Variables();
	// notify success ke user
    var emailText = "Success";
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
    subject: 'Deposit Status',
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
    console.log("Deposit " + amount + " success")
}

module.exports = notifySuccessDeposit;
