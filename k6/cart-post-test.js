import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
};

const baseUrl = __ENV.BASE_URL;

if (!baseUrl) {
  throw new Error("BASE_URL is required. Example: k6 run -e BASE_URL=http://136.109.180.133:8002 k6/cart-post-test.js");
}

export default function () {
  const payload = JSON.stringify({
    customer_id: Number(__ENV.CUSTOMER_ID || 1),
    product_id: Number(__ENV.PRODUCT_ID || 101),
    quantity: Number(__ENV.QUANTITY || 1),
  });

  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const response = http.post(`${baseUrl}/cart`, payload, params);

  check(response, {
    "POST /cart status is 200": (res) => res.status === 200,
  });

  sleep(1);
}
