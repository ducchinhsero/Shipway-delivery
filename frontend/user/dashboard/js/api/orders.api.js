import { mockOrders } from "../mock/orders.mock.js";

export function getOrders() {
  return Promise.resolve(mockOrders);
}
