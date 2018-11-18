const { Client, logger } = require('camunda-external-task-client-js');
const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger };
const client = new Client(config);

// const { 
//       } = require('./order-worker');

const { 
      validateWithdrawal,
      deductBalance,
      createTransactionWithdrawal,
      sendTransactionDetail,
      notifyFailWithdrawal,
      notifySuccessWithdrawal,
      refillBalance
      } = require('./withdrawal-worker');

client.subscribe('validate-withdrawal', validateWithdrawal);
client.subscribe('deduct-balance', deductBalance);
client.subscribe('create-transaction-withdrawal', createTransactionWithdrawal)
client.subscribe('send-transaction-detail', sendTransactionDetail)
client.subscribe('notify-fail-withdrawal', notifyFailWithdrawal)
client.subscribe('notify-success-withdrawal', notifySuccessWithdrawal)
client.subscribe('refill-balance', refillBalance)

// const {
//       } = require('./deposit-worker');

