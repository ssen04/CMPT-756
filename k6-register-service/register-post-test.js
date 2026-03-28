import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: __ENV.VUS ? Number(__ENV.VUS) : 10,
  duration: __ENV.DURATION || "30s",
};

const baseUrl = __ENV.BASE_URL;

if (!baseUrl) {
  throw new Error("BASE_URL is required. Example: k6 run -e BASE_URL=http://136.109.180.133:8000 k6/register-post-test.js");
}

// Use a unique email per VU+iteration to avoid "already registered" errors
export default function () {
  const email = `testuser_${__VU}_${__ITER}_${Date.now()}@example.com`;

  const payload = JSON.stringify({
    full_name: "Test User",
    email: email,
    password: "test1234",
  });

  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  // For serverless, the endpoint is just the base URL (no /register path)
  const endpoint = baseUrl.includes("cloudfunctions.net") ? baseUrl : `${baseUrl}/register`;

  const response = http.post(endpoint, payload, params);

  check(response, {
    "POST /register status is 200": (res) => res.status === 200,
  });

  sleep(1);
}
