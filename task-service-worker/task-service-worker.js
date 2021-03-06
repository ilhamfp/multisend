const { Client, logger } = require('camunda-external-task-client-js');
const config = { baseUrl: 'http://localhost:8080/engine-rest'};
const client = new Client(config);

console.log("Task service worker..");

const { 
      calculateCost,
      checkBalance,
      deductBalanceOrder,
      searchDriver,
      cancelOrder,
      sendOrderStatus,
      checkDeliveryCompletionn
      } = require('./order-worker');

client.subscribe('calculate-cost', calculateCost);
client.subscribe('check-balance', checkBalance);
client.subscribe('deduct-balance-order', deductBalanceOrder);
client.subscribe('search-driver', searchDriver);
client.subscribe('cancel-order', cancelOrder);
client.subscribe('send-order-status', sendOrderStatus);
client.subscribe('check-delivery-completion', checkDeliveryCompletionn);

const { 
      validateWithdrawal,
      deductBalanceWithdrawal,
      createTransactionWithdrawal,
      sendTransactionDetail,
      notifyFailWithdrawal,
      notifySuccessWithdrawal,
      refillBalance
      } = require('./withdrawal-worker');

client.subscribe('validate-withdrawal', validateWithdrawal);
client.subscribe('deduct-balance-withdrawal', deductBalanceWithdrawal);
client.subscribe('create-transaction-withdrawal', createTransactionWithdrawal);
client.subscribe('send-transaction-detail', sendTransactionDetail);
client.subscribe('notify-fail-withdrawal', notifyFailWithdrawal);
client.subscribe('notify-success-withdrawal', notifySuccessWithdrawal);
client.subscribe('refill-balance', refillBalance);

const {
      createTransactionDeposit,
      sendDepositDetail,
      addBalance,
      notifySuccessDeposit,
      notifyFailDeposit
      } = require('./deposit-worker');

client.subscribe('create-transaction-deposit', createTransactionDeposit)
client.subscribe('send-deposit-detail', sendDepositDetail)
client.subscribe('add-balance', addBalance)
client.subscribe('notify-success-deposit', notifySuccessDeposit)
client.subscribe('notify-fail-deposit', notifyFailDeposit)


