import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
};

const baseUrl = __ENV.BASE_URL;

export default function () {
  const res = http.get(baseUrl);

  check(res, {
    "status is 200": (r) => r.status === 200,
  });

  sleep(1);
}
