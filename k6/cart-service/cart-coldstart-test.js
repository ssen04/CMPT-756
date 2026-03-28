import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: 1,
  iterations: 1,
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
};

const baseUrl = __ENV.BASE_URL;

if (!baseUrl) {
  throw new Error(
    "BASE_URL is required. Example: k6 run -e BASE_URL=https://service-url k6/cart-coldstart-test.js",
  );
}

export default function () {
  const customerId = __ENV.CUSTOMER_ID || "1";
  const response = http.get(`${baseUrl}/cart/${customerId}`);

  check(response, {
    "GET /cart status is 200": (res) => res.status === 200,
  });
}
