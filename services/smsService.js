const axios = require('axios');

const PROVIDER = process.env.SMS_PROVIDER || 'kavenegar';
const API_KEY = process.env.SMS_API_KEY;
const SENDER = process.env.SMS_SENDER_NUMBER;

const KAVENEGAR_API = 'https://api.kavenegar.com/v1';

async function sendSMS(to, message, template = null) {
  if (!API_KEY) {
    console.warn('[SMS] No API key configured. Message not sent:', message);
    return { status: 'skipped', reason: 'no_api_key' };
  }
  try {
    if (PROVIDER === 'kavenegar' && template) {
      const url = `${KAVENEGAR_API}/${API_KEY}/verify/lookup.json`;
      const { data } = await axios.post(url, null, {
        params: { receptor: to, token: message, template }
      });
      return { status: 'sent', provider: 'kavenegar', data };
    }
    const url = `${KAVENEGAR_API}/${API_KEY}/sms/send.json`;
    const { data } = await axios.post(url, null, {
      params: { receptor: to, message, sender: SENDER }
    });
    return { status: 'sent', provider: 'kavenegar', data };
  } catch (err) {
    console.error('[SMS] Failed:', err.message);
    return { status: 'failed', error: err.message };
  }
}

async function sendOrderSMS(to, orderNumber, status) {
  return sendSMS(to, `${orderNumber}|${status}`, 'order-status');
}

async function sendOTPSMS(to, code) {
  return sendSMS(to, code, 'verify');
}

async function sendWelcomeSMS(to, name) {
  const msg = `سلام ${name} عزیز، به دات واچ خوش آمدید!`;
  return sendSMS(to, msg);
}

module.exports = { sendSMS, sendOrderSMS, sendOTPSMS, sendWelcomeSMS };
