# Source: https://eff-certbot.readthedocs.io/en/latest/intro.html
# Downloaded: 2026-02-16

---

Introduction — Certbot 5.4.0.dev0 documentation
      
- 
      
- 

  
      
      
      
      
      
    
    
    
- 
    
- 
    
- 
    
-  

 
  
    

    

      
        
          
  
      
- 
      
- Introduction
      
- 
             View page source
      
  
  

          
           
             
  

# Introduction

Note

To get started quickly, use the interactive installation guide.

Certbot is part of EFF’s effort to encrypt the entire Internet. Secure communication over the Web relies on HTTPS, which requires the use of a digital certificate that lets browsers verify the identity of web servers (e.g., is that really google.com?). Web servers obtain their certificates from trusted third parties called certificate authorities (CAs). Certbot is an easy-to-use client that fetches a certificate from Let’s Encrypt—an open certificate authority launched by the EFF, Mozilla, and others—and deploys it to a web server.

Anyone who has gone through the trouble of setting up a secure website knows what a hassle getting and maintaining a certificate is. Certbot and Let’s Encrypt can automate away the pain and let you turn on and manage HTTPS with simple commands. Using Certbot and Let’s Encrypt is free.

## Getting Started

The best way to get started is to use our interactive guide. It generates instructions based on your configuration settings. In most cases, you’ll need root or administrator access to your web server to run Certbot.

Certbot is meant to be run directly on your web server on the command line, not on your personal computer. If you’re using a hosted service and don’t have direct access to your web server, you might not be able to use Certbot. Check with your hosting provider for documentation about uploading certificates or using certificates issued by Let’s Encrypt.

## Contributing

If you’d like to contribute to this project please read Developer Guide.

This project is governed by EFF’s Public Projects Code of Conduct.

### Links

Documentation: https://certbot.eff.org/docs

Software project: https://github.com/certbot/certbot

Changelog: https://github.com/certbot/certbot/blob/main/certbot/CHANGELOG.md

For Contributors: https://certbot.eff.org/docs/contributing.html

For Users: https://certbot.eff.org/docs/using.html

Main Website: https://certbot.eff.org

Let’s Encrypt Website: https://letsencrypt.org

Community: https://community.letsencrypt.org

ACME spec: RFC 8555

ACME working area in github (archived): https://github.com/ietf-wg-acme/acme

           
          
          
  
    
      
        Next 
      
      
         Previous
      
    
  

  

  
    

    
    © Copyright 2014-2018 - The Certbot software and documentation are licensed under the Apache 2.0 license as described at https://eff.org/cb-license.
    
    

    

    
        Let's Encrypt Status
    

    

  
  Built with Sphinx using a theme provided by Read the Docs.
