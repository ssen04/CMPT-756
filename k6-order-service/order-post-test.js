import http from "k6/http";
import { check, sleep } from "k6";

const orderUrl = __ENV.ORDER_URL;
const startId = Number(__ENV.START_ID);
const endId = Number(__ENV.END_ID);
const vus = Number(__ENV.VUs || __ENV.VUS || 5);
const duration = __ENV.duration || __ENV.DURATION || "30s";

if (!orderUrl) {
  throw new Error("ORDER_URL is required");
}
if (!Number.isInteger(startId) || !Number.isInteger(endId) || startId > endId) {
  throw new Error("START_ID and END_ID must be integers and START_ID <= END_ID");
}

export const options = {
  vus,
  duration,
};

function nextCustomerId(vu, iter) {
  // Sequential, unique IDs across all VUs/iterations in this test run.
  return startId + iter * vus + (vu - 1);
}

export default function () {
  const customerId = nextCustomerId(__VU, __ITER);
  if (customerId > endId) {
    // No reuse: once exhausted, skip sending any more requests.
    sleep(2);
    return;
  }

  const payload = JSON.stringify({ customer_id: customerId });
  const params = { headers: { "Content-Type": "application/json" } };
  const res = http.post(orderUrl, payload, params);

  check(res, {
    "POST /order status is 2xx": (r) => r.status >= 200 && r.status < 300,
  });

  // Keep request volume within official ID pools without ID reuse.
  sleep(2);
}
