import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
};

const baseUrl = __ENV.BASE_URL;

if (!baseUrl) {
  throw new Error("BASE_URL is required. Example: k6 run -e BASE_URL=http://136.109.180.133:8002 k6/cart-get-test.js");
}

export default function () {
  const customerId = __ENV.CUSTOMER_ID || "1";
  const response = http.get(`${baseUrl}/cart/${customerId}`);

  check(response, {
    "GET /cart status is 200": (res) => res.status === 200,
  });

  sleep(1);
}
