# Source: https://nginx.org/en/docs/http/ngx_http_limit_req_module.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

Module ngx_http_limit_req_module
- 

Confused between [ingress-nginx](https://github.com/kubernetes/ingress-nginx) 
and [NGINX Ingress Controller](https://github.com/nginx/kubernetes-ingress)? 
Learn about our long-term commitment to the NGINX Ingress Controller and Gateway API implementation.
[Read the Blog](https://blog.nginx.org/blog/the-ingress-nginx-alternative-open-source-nginx-ingress-controller-for-the-long-term).  

## Module ngx_http_limit_req_module
[Example Configuration](#example)
[Directives](#directives)
     [limit_req](#limit_req)
     [limit_req_dry_run](#limit_req_dry_run)
     [limit_req_log_level](#limit_req_log_level)
     [limit_req_status](#limit_req_status)
     [limit_req_zone](#limit_req_zone)
[Embedded Variables](#variables)

The `ngx_http_limit_req_module` module (0.7.21) is used
to limit the request processing rate per a defined key,
in particular, the processing rate of requests coming
from a single IP address.
The limitation is done using the “leaky bucket” method.

#### Example Configuration

 

http {
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

    ...

    server {

        ...

        location /search/ {
            limit_req zone=one burst=5;
        }

 

#### Directives

                
                
            Syntax:
                
                
            **limit_req** 
    `zone`=`name`
    [`burst`=`number`]
    [`nodelay` |
     `delay`=`number`];

                
                
            
                
                
            Default:
                
                
            
            —
        
                
                
            
                
                
            Context:
                
                
            `http`, `server`, `location`

                
                
            

Sets the shared memory zone
and the maximum burst size of requests.
If the requests rate exceeds the rate configured for a zone,
their processing is delayed such that requests are processed
at a defined rate.
Excessive requests are delayed until their number exceeds the
maximum burst size
in which case the request is terminated with an
[error](#limit_req_status).
By default, the maximum burst size is equal to zero.
For example, the directives

 

limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

server {
    location /search/ {
        limit_req zone=one burst=5;
    }

 
allow not more than 1 request per second at an average,
with bursts not exceeding 5 requests.

If delaying of excessive requests while requests are being limited is not
desired, the parameter `nodelay` should be used:

 

limit_req zone=one burst=5 nodelay;

 

The `delay` parameter (1.15.7) specifies a limit
at which excessive requests become delayed.
Default value is zero, i.e. all excessive requests are delayed.

There could be several `limit_req` directives.
For example, the following configuration will limit the processing rate
of requests coming from a single IP address and, at the same time,
the request processing rate by the virtual server:

 

limit_req_zone $binary_remote_addr zone=perip:10m rate=1r/s;
limit_req_zone $server_name zone=perserver:10m rate=10r/s;

server {
    ...
    limit_req zone=perip burst=5 nodelay;
    limit_req zone=perserver burst=10;
}

 

These directives are inherited from the previous configuration level
if and only if there are no `limit_req` directives
defined on the current level.

                
                
            Syntax:
                
                
            `**limit_req_dry_run** on` | `off`;

                
                
            
                
                
            Default:
                
                
            
```
limit_req_dry_run off;
```

                
                
            
                
                
            Context:
                
                
            `http`, `server`, `location`

                
                
            
This directive appeared in version 1.17.1.
            

Enables the dry run mode.
In this mode, requests processing rate is not limited, however,
in the shared memory zone, the number of excessive requests is accounted
as usual.

                
                
            Syntax:
                
                
            **limit_req_log_level** 
`info` |
`notice` |
`warn` |
`error`;

                
                
            
                
                
            Default:
                
                
            
```
limit_req_log_level error;
```

                
                
            
                
                
            Context:
                
                
            `http`, `server`, `location`

                
                
            
This directive appeared in version 0.8.18.
            

Sets the desired logging level
for cases when the server refuses to process requests
due to rate exceeding,
or delays request processing.
Logging level for delays is one point less than for refusals; for example,
if “`limit_req_log_level notice`” is specified,
delays are logged with the `info` level.

                
                
            Syntax:
                
                
            `**limit_req_status** code`;

                
                
            
                
                
            Default:
                
                
            
```
limit_req_status 503;
```

                
                
            
                
                
            Context:
                
                
            `http`, `server`, `location`

                
                
            
This directive appeared in version 1.3.15.
            

Sets the status code to return in response to rejected requests.

                
                
            Syntax:
                
                
            **limit_req_zone** 
    `key`
    `zone`=`name`:`size`
    `rate`=`rate`
    [`sync`];

                
                
            
                
                
            Default:
                
                
            
            —
        
                
                
            
                
                
            Context:
                
                
            `http`

                
                
            

Sets parameters for a shared memory zone
that will keep states for various keys.
In particular, the state stores the current number of excessive requests.
The `key` can contain text, variables, and their combination.
Requests with an empty key value are not accounted.

 
Prior to version 1.7.6, a `key` could contain exactly one variable.

 
Usage example:

 

limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

 

Here, the states are kept in a 10 megabyte zone “one”, and an
average request processing rate for this zone cannot exceed
1 request per second.

A client IP address serves as a key.
Note that instead of `$remote_addr`, the
`$binary_remote_addr` variable is used here.
The `$binary_remote_addr` variable’s size
is always 4 bytes for IPv4 addresses or 16 bytes for IPv6 addresses.
The stored state always occupies
64 bytes on 32-bit platforms and 128 bytes on 64-bit platforms.
One megabyte zone can keep about 16 thousand 64-byte states
or about 8 thousand 128-byte states.

If the zone storage is exhausted, the least recently used state is removed.
If even after that a new state cannot be created, the request is terminated with
an [error](#limit_req_status).

The rate is specified in requests per second (r/s).
If a rate of less than one request per second is desired,
it is specified in request per minute (r/m).
For example, half-request per second is 30r/m.

The `sync` parameter (1.15.3) enables
[synchronization](../stream/ngx_stream_zone_sync_module.html#zone_sync)
of the shared memory zone.

 
The `sync` parameter is available as part of our
[commercial subscription](https://www.f5.com/products/nginx).

 

 
Additionally, as part of our
[commercial subscription](https://www.f5.com/products/nginx),
the
[status information](ngx_http_api_module.html#http_limit_reqs_)
for each such shared memory zone can be
[obtained](ngx_http_api_module.html#getHttpLimitReqZone) or
[reset](ngx_http_api_module.html#deleteHttpLimitReqZoneStat)
with the [API](ngx_http_api_module.html) since 1.17.7.

 

#### Embedded Variables

 

`$limit_req_status`

keeps the result of limiting the request processing rate (1.17.6):
`PASSED`,
`DELAYED`,
`REJECTED`,
`DELAYED_DRY_RUN`, or
`REJECTED_DRY_RUN`
