import http from "k6/http";
import { check } from "k6";

// Single request to measure cold start — run this after leaving the service idle
export const options = {
  vus: 1,
  iterations: 1,
};

const baseUrl = __ENV.BASE_URL;

if (!baseUrl) {
  throw new Error("BASE_URL is required. Example: k6 run -e BASE_URL=https://us-west1-cmpt756-project-489717.cloudfunctions.net/register-service-fn k6/register-coldstart-test.js");
}

export default function () {
  const response = http.get(baseUrl);

  check(response, {
    "Cold start health check status is 200": (res) => res.status === 200,
  });
}
