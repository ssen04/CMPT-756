import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
};

const baseUrl = __ENV.BASE_URL;

if (!baseUrl) {
  throw new Error("BASE_URL is required");
}

export default function () {
  const payload = JSON.stringify({
    order_id: Number(__ENV.ORDER_ID || 1),
  });

  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const response = http.post(baseUrl, payload, params);

  check(response, {
    "POST /notify status is 200": (res) => res.status === 200,
  });

  sleep(1);
}
