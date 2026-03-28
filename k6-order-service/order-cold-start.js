import http from "k6/http";
import { check } from "k6";

const orderUrl = __ENV.ORDER_URL;
const customerId = Number(__ENV.CUSTOMER_ID);

if (!orderUrl) {
  throw new Error("ORDER_URL is required");
}
if (!Number.isInteger(customerId)) {
  throw new Error("CUSTOMER_ID must be an integer");
}

export const options = {
  vus: 1,
  iterations: 1,
};

export default function () {
  const payload = JSON.stringify({ customer_id: customerId });
  const params = { headers: { "Content-Type": "application/json" } };
  const res = http.post(orderUrl, payload, params);
  const ok = (res.status >= 200 && res.status < 300) || (res.body && res.body.indexOf("order_id") !== -1);

  check(res, {
    "POST /order success (2xx or order_id in body)": () => ok,
  });

  if (!ok) {
    console.error(`SMOKE_FAIL status=${res.status} body=${res.body || ""}`);
  }

  console.log(`Cold Start Time: ${res.timings.duration.toFixed(2)} ms`);
}
