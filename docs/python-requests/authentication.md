# Source: https://requests.readthedocs.io/en/latest/user/authentication/
# Downloaded: 2026-02-16

---

Authentication — Requests 2.33.0.dev1 documentation
    
- 
    
- 
    
    
    
    
- 
    
- 
    
- 
    
- 
   
  
- 
  

  
  

  
  

    
      
        
          

          
            
  

# Authentication¶

This document discusses using various kinds of authentication with Requests.

Many web services require authentication, and there are many different types.
Below, we outline various forms of authentication available in Requests, from
the simple to the complex.

## Basic Authentication¶

Many web services that require authentication accept HTTP Basic Auth. This is
the simplest kind, and Requests supports it straight out of the box.

Making requests with HTTP Basic Auth is very simple:

>>> from requests.auth import HTTPBasicAuth
>>> basic = HTTPBasicAuth('user', 'pass')
>>> requests.get('https://httpbin.org/basic-auth/user/pass', auth=basic)
<Response [200]>

In fact, HTTP Basic Auth is so common that Requests provides a handy shorthand
for using it:

>>> requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
<Response [200]>

Providing the credentials in a tuple like this is exactly the same as the
`HTTPBasicAuth` example above.

### netrc Authentication¶

If no authentication method is given with the `auth` argument, Requests will
attempt to get the authentication credentials for the URL’s hostname from the
user’s netrc file. The netrc file overrides raw HTTP authentication headers
set with headers=.

If credentials for the hostname are found, the request is sent with HTTP Basic
Auth.

Requests will search for the netrc file at ~/.netrc, ~/_netrc, or at the path
specified by the NETRC environment variable. ~ denotes the user’s home
directory, which is $HOME on Unix based systems and %USERPROFILE% on Windows.

Usage of netrc file can be disabled by setting trust_env to False in the
Requests session:

>>> s = requests.Session()
>>> s.trust_env = False
>>> s.get('https://httpbin.org/basic-auth/user/pass')

## Digest Authentication¶

Another very popular form of HTTP Authentication is Digest Authentication,
and Requests supports this out of the box as well:

>>> from requests.auth import HTTPDigestAuth
>>> url = 'https://httpbin.org/digest-auth/auth/user/pass'
>>> requests.get(url, auth=HTTPDigestAuth('user', 'pass'))
<Response [200]>

## OAuth 1 Authentication¶

A common form of authentication for several web APIs is OAuth. The `requests-oauthlib`
library allows Requests users to easily make OAuth 1 authenticated requests:

>>> import requests
>>> from requests_oauthlib import OAuth1

>>> url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
>>> auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET',
...               'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')

>>> requests.get(url, auth=auth)
<Response [200]>

For more information on how to OAuth flow works, please see the official OAuth website.
For examples and documentation on requests-oauthlib, please see the requests_oauthlib
repository on GitHub

## OAuth 2 and OpenID Connect Authentication¶

The `requests-oauthlib` library also handles OAuth 2, the authentication mechanism
underpinning OpenID Connect. See the requests-oauthlib OAuth2 documentation for
details of the various OAuth 2 credential management flows:

- 
Web Application Flow

- 
Mobile Application Flow

- 
Legacy Application Flow

- 
Backend Application Flow

## Other Authentication¶

Requests is designed to allow other forms of authentication to be easily and
quickly plugged in. Members of the open-source community frequently write
authentication handlers for more complicated or less commonly-used forms of
authentication. Some of the best have been brought together under the
Requests organization, including:

- 
Kerberos

- 
NTLM

If you want to use any of these forms of authentication, go straight to their
GitHub page and follow the instructions.

## New Forms of Authentication¶

If you can’t find a good implementation of the form of authentication you
want, you can implement it yourself. Requests makes it easy to add your own
forms of authentication.

To do so, subclass `AuthBase` and implement the
`__call__()` method:

>>> import requests
>>> class MyAuth(requests.auth.AuthBase):
...     def __call__(self, r):
...         # Implement my authentication
...         return r
...
>>> url = 'https://httpbin.org/get'
>>> requests.get(url, auth=MyAuth())
<Response [200]>

When an authentication handler is attached to a request,
it is called during request setup. The `__call__` method must therefore do
whatever is required to make the authentication work. Some forms of
authentication will additionally add hooks to provide further functionality.

Further examples can be found under the Requests organization and in the
`auth.py` file.

          
          
        
      
      
        

  

  Requests is an elegant and simple HTTP library for Python, built for
  human beings. You are currently looking at the documentation of the
  development release.

### Useful Links

  
- Quickstart
  
- Advanced Usage
  
- API Reference
  
- Release History
  
- Contributors Guide

  

  
- Recommended Packages and Extensions

  

  
- Requests @ GitHub
  
- Requests @ PyPI
  
- Issue Tracker

  
    
### Table of Contents

    

- Authentication

- Basic Authentication

- netrc Authentication

- Digest Authentication

- OAuth 1 Authentication

- OAuth 2 and OpenID Connect Authentication

- Other Authentication

- New Forms of Authentication

  

### Related Topics

  
- Documentation overview
      
- Previous: Advanced Usage
      
- Next: Recommended Packages and Extensions
  

  
### Quick search

    
    
      
      
    
    

        
      
      
    
    
      ©MMXVIX. A Kenneth Reitz Project.
