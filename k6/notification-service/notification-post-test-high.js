import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 30,                // 🔥 HIGH workload
  duration: "30s",
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
};

const baseUrl = __ENV.BASE_URL;

export default function () {
  const payload = JSON.stringify({
    order_id: 1,
  });

  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const res = http.post(baseUrl, payload, params);

  check(res, {
    "status is 200": (r) => r.status === 200,
  });

  sleep(1);
}
