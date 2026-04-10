import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: 1,
  iterations: 1,
};

const baseUrl = __ENV.BASE_URL;

export default function () {
  const payload = JSON.stringify({ order_id: 1 });

  const res = http.post(baseUrl, payload, {
    headers: { "Content-Type": "application/json" },
  });

  check(res, {
    "status is 200": (r) => r.status === 200,
  });
}
