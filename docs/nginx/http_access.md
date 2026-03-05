# Source: https://nginx.org/en/docs/http/ngx_http_access_module.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

Module ngx_http_access_module
- 

Confused between [ingress-nginx](https://github.com/kubernetes/ingress-nginx) 
and [NGINX Ingress Controller](https://github.com/nginx/kubernetes-ingress)? 
Learn about our long-term commitment to the NGINX Ingress Controller and Gateway API implementation.
[Read the Blog](https://blog.nginx.org/blog/the-ingress-nginx-alternative-open-source-nginx-ingress-controller-for-the-long-term).  

## Module ngx_http_access_module
[Example Configuration](#example)
[Directives](#directives)
     [allow](#allow)
     [deny](#deny)

The `ngx_http_access_module` module allows
limiting access to certain client addresses.

Access can also be limited by
[password](ngx_http_auth_basic_module.html), by the
[result of subrequest](ngx_http_auth_request_module.html),
or by [JWT](ngx_http_auth_jwt_module.html).
Simultaneous limitation of access by address and by password is controlled
by the [satisfy](ngx_http_core_module.html#satisfy) directive.

#### Example Configuration

 

location / {
    deny  192.168.1.1;
    allow 192.168.1.0/24;
    allow 10.1.1.0/16;
    allow 2001:0db8::/32;
    deny  all;
}

 

The rules are checked in sequence until the first match is found.
In this example, access is allowed only for IPv4 networks
`10.1.1.0/16` and `192.168.1.0/24`
excluding the address `192.168.1.1`,
and for IPv6 network `2001:0db8::/32`.
In case of a lot of rules, the use of the
[ngx_http_geo_module](ngx_http_geo_module.html)
module variables is preferable.

#### Directives

                
                
            Syntax:
                
                
            **allow** 
    `address` |
    `CIDR` |
    `unix:` |
    `all`;

                
                
            
                
                
            Default:
                
                
            
            —
        
                
                
            
                
                
            Context:
                
                
            `http`, `server`, `location`, `limit_except`

                
                
            

Allows access for the specified network or address.
If the special value `unix:` is specified (1.5.1),
allows access for all UNIX-domain sockets.

                
                
            Syntax:
                
                
            **deny** 
    `address` |
    `CIDR` |
    `unix:` |
    `all`;

                
                
            
                
                
            Default:
                
                
            
            —
        
                
                
            
                
                
            Context:
                
                
            `http`, `server`, `location`, `limit_except`

                
                
            

Denies access for the specified network or address.
If the special value `unix:` is specified (1.5.1),
denies access for all UNIX-domain sockets.
