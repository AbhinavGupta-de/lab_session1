# Nginx Configuration for Microservices

### **1. Rate Limiting Zone**
**Directive: `limit_req_zone`**
- **Purpose**: This directive sets up a shared memory zone to track and enforce rate limits on client requests.
- **Parameters**:
  - `$binary_remote_addr`: The binary representation of the client's IP address is used as a unique identifier to track request rates per client.
  - `zone=mylimit:10m`: Defines a shared memory zone named `mylimit` with a size of 10 megabytes. This zone can store data for approximately **160,000 unique IP addresses**, ensuring scalability for a significant number of clients.
  - `rate=1r/s`: Specifies the allowed rate of **1 request per second per client**. Requests beyond this rate will be throttled.

**Example Usage**:  
If a client sends more than 1 request per second, subsequent requests may either be delayed or rejected, depending on how rate limiting is configured in the specific `location` blocks.

---

### **2. Upstreams**
**Directives: `upstream user_service` and `upstream order_service`**
- **Purpose**: These directives define upstream servers for routing requests to backend microservices.
- **Details**:
  - `user_service`: Points to a backend service running on `user-service:5001` (typically resolved using DNS or a container network).
  - `order_service`: Points to a backend service running on `order-service:5002`.

These upstream blocks enable logical separation of service endpoints and facilitate load balancing or failover mechanisms (though load balancing isn’t used in this example).

---

### **3. Server Block**
**Directive: `server`**
- **Purpose**: This block handles client HTTP requests on port `80` and defines routes for various services.

#### **Route: `/users`**
- **Rate Limiting**:
  - `limit_req zone=mylimit burst=5 nodelay`: 
    - `zone=mylimit`: Applies the rate-limiting rules defined in the `mylimit` zone.
    - `burst=5`: Allows up to **5 requests to "burst" through** in quick succession before rate limiting kicks in.
    - `nodelay`: Ensures requests exceeding the burst limit are rejected immediately (instead of being delayed).
  - **Effect**: A client can send up to 1 request per second. However, during spikes, up to 5 requests may be processed instantaneously without delay.
- **Proxy Configuration**:
  - `proxy_set_header X-Custom-Header "Microservices Lab"`: Adds a custom header (`X-Custom-Header`) to the forwarded requests, potentially used for logging, debugging, or tracking.
  - `proxy_pass http://user_service`: Forwards the request to the upstream backend service (`user_service`).

---

#### **Route: `/orders`**
- Configuration for `/orders` is identical to `/users` but forwards requests to the `order_service` upstream.

---

#### **Fallback Route: `/`**
- If a client accesses any route not explicitly defined (e.g., `/home` or `/products`), the server responds with an HTTP **404 (Not Found)** status.

---

### **Key Features and Benefits**
1. **Rate Limiting**:
   - Protects backend services from abuse or overload by throttling excessive client requests.
   - Burst handling ensures that occasional spikes in traffic are accommodated without rejecting requests unnecessarily.
2. **Service Routing**:
   - Clean separation of routes for user and order services makes the configuration modular and easy to extend.
3. **Scalability**:
   - The shared memory zone (`10m`) can handle a large number of unique clients, suitable for high-traffic scenarios.
4. **Customization**:
   - The `X-Custom-Header` can be tailored for debugging or monitoring purposes across microservices.
5. **Security**:
   - Routes not explicitly defined are rejected with a `404` response, reducing the surface area for attacks.

---

### **Use Case Example**
In a microservices-based architecture:
- `/users` requests are routed to a **User Service**, such as for user authentication or profile management.
- `/orders` requests are routed to an **Order Service**, such as for placing or tracking orders.
- Rate limiting ensures fair use and protects the backend from being overwhelmed by any single client.

This configuration is ideal for environments where multiple backend services need to be accessed securely and efficiently by clients.