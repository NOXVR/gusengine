# Source: https://docs.docker.com/engine/network/
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

Networking | Docker Docs
- 
- 
- 
- 
- 
- 
  
    
    
      
        
          
- 
        
      
    
  

- 
- 

Ask AI

Search {
                localStorage.setItem('theme-preference', value);
                document.firstElementChild.className = value;
              })" @click="theme = (theme === 'dark' ? 'light' : 'dark')">

 !m.isStreaming)

      // Watch for store changes to focus input
      this.$watch('$store.gordon.isOpen', (isOpen) => {
        if (isOpen) {
          this.$nextTick(() => {
            this.$refs.input?.focus()
          })
        }
      })

      // Watch for query from store and populate input
      this.$watch('$store.gordon.query', (query) => {
        if (query) {
          this.currentQuestion = query
          const shouldAutoSubmit = this.$store.gordon.autoSubmit
          this.$nextTick(() => {
            if (shouldAutoSubmit) {
              this.askQuestion()
            } else {
              this.$refs.input?.focus()
              this.$refs.input?.select()
            }
          })
          // Clear the store query and autoSubmit flag after using them
          this.$store.gordon.query = ''
          this.$store.gordon.autoSubmit = false
        }
      })
    },

    getTurnCount() {
      return this.messages.filter(m => m.role === 'user').length
    },

    getRemainingTurns() {
      return this.maxTurnsPerThread - this.getTurnCount()
    },

    isThreadLimitReached() {
      return this.getTurnCount() >= this.maxTurnsPerThread
    },

    shouldShowCountdown() {
      const remaining = this.getRemainingTurns()
      return remaining > 0 && remaining  {
        if (this.$refs.input) {
          this.$refs.input.style.height = 'auto'
        }
      })
      this.isLoading = true
      this.error = null

      // Add placeholder for assistant response
      const responseIndex = this.messages.length
      this.messages.push({
        role: 'assistant',
        content: '',
        isStreaming: true,
        questionAnswerId: null,
        feedback: null,
        copied: false
      })

      this.$nextTick(() => {
        this.$refs.messagesContainer?.scrollTo({
          top: this.$refs.messagesContainer.scrollHeight,
          behavior: 'smooth'
        })
      })

      try {
        await this.streamGordonResponse(responseIndex)
      } catch (err) {
        // Only set error if messages weren't cleared
        if (this.messages.length > 0) {
          if (err.message === 'RATE_LIMIT_EXCEEDED') {
            this.error = 'You\'ve exceeded your question quota for the day. Please come back tomorrow.'
          } else {
            this.error = 'Failed to get response. Please try again.'
          }
        }
        console.error('Gordon API error:', err)
        // Only try to remove message if it still exists
        if (this.messages[responseIndex]) {
          this.messages.splice(responseIndex, 1)
        }
      } finally {
        this.isLoading = false
      }
    },

    getSessionId() {
      let sessionId = sessionStorage.getItem('gordon-session-id')
      if (!sessionId) {
        sessionId = `docs-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
        sessionStorage.setItem('gordon-session-id', sessionId)
      }
      return sessionId
    },

    async streamGordonResponse(responseIndex) {

      // Build API request from messages, excluding the streaming placeholder
      // The placeholder is at responseIndex, so we take everything before it
      const conversationMessages = this.messages.slice(0, responseIndex).map((msg, i) => {
        const message = {
          role: msg.role,
          content: msg.content
        }

        // Add copilot_references to the last message (most recent user question)
        if (i === responseIndex - 1) {
          message.copilot_references = [
            {
              data: {
                origin: 'docs-website',
                email: 'docs@docker.com',
                uuid: this.getSessionId(),
                action: 'AskGordon',
                ...(this.includePageContext && {
                  page_url: window.location.href,
                  page_title: "Networking overview"
                })
              }
            }
          ]
        }

        return message
      })

      const isNewConversation = !this.threadId
      const payload = {
        messages: conversationMessages,
        ...(this.threadId && { thread_uuid: this.threadId })
      }

      const response = await fetch(window.GORDON_BASE_URL + '/public/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!response.ok) {
        if (response.status === 429) {
          throw new Error('RATE_LIMIT_EXCEEDED')
        }
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (!line.trim() || !line.startsWith('data: ')) continue

          const data = line.slice(6)
          if (data === '[DONE]') continue

          try {
            const parsed = JSON.parse(data)

            // Capture thread_id for new conversations
            if (parsed.thread_id) {
              if (isNewConversation) {
                this.threadId = parsed.thread_id  // $persist auto-saves to sessionStorage
              } else if (parsed.thread_id !== this.threadId) {
                console.warn('Backend returned unexpected thread_id:', parsed.thread_id)
              }
              continue
            }

            // Capture question_answer_id for feedback
            if (parsed.question_answer_id) {
              this.messages[responseIndex].questionAnswerId = parsed.question_answer_id
              continue
            }

            if (parsed.choices && parsed.choices[0]?.delta?.content) {
              const content = parsed.choices[0].delta.content
              this.messages[responseIndex].content += content

              this.$nextTick(() => {
                const container = this.$refs.messagesContainer
                if (container) {
                  const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight  {
          setTimeout(() => {
            message.copied = false
          }, 2000)
        })
      } catch (err) {
        console.error('Failed to copy:', err)
      }
    }
  }" x-cloak @keydown.escape.window=$store.gordon.close()>

- 

 0 }">

### Ask me about Docker

Get instant answers to your Docker questions. I can help with
commands, concepts, troubleshooting, and best practices.

Try asking:

How do Docker Hardened Images work?

What is MCP Toolkit?

How do I create an org?

Was this helpful?

Helpful

Not quite

Copy

remaining in this thread.

You've reached the maximum of
 questions per thread. For
better answer quality, start a new thread.

Start a new thread

Context
When enabled, Gordon considers the current page you're viewing
to provide more relevant answers.
Share feedbackAnswers are generated based on the documentation. {
          const container = $el; // The div with overflow
          const item = document.getElementById('sidebar-current-page')
          if (item) {
              const containerTop = container.scrollTop;
              const containerBottom = containerTop + container.clientHeight;

              const itemTop = item.offsetTop - container.offsetTop;
              const itemBottom = itemTop + item.offsetHeight;

              // Scroll only if the item is out of view
              if (itemBottom > containerBottom - 200) {
                  container.scrollTop = itemTop - (container.clientHeight / 2 - item.offsetHeight / 2);
              }
          }
      })" class="bg-background-toc dark:bg-background-toc fixed top-0 z-40 hidden h-screen w-full flex-none overflow-x-hidden overflow-y-auto md:sticky md:top-16 md:z-auto md:block md:h-[calc(100vh-64px)] md:w-[320px]" :class="{ 'hidden': ! $store.showSidebar }">

Back
Manuals

- 
Get started
- 
Guides
- 
Reference
# Networking overview

Copy as Markdown

Open Markdown

Ask Docs AI

Claude

Open in ClaudeTable of contents
Container networking refers to the ability for containers to connect to and
communicate with each other, and with non-Docker network services.

Containers have networking enabled by default, and they can make outgoing
connections. A container has no information about what kind of network it's
attached to, or whether its network peers are also Docker containers. A
container only sees a network interface with an IP address, a gateway, a
routing table, DNS services, and other networking details.

This page describes networking from the point of view of the container,
and the concepts around container networking.

When Docker Engine on Linux starts for the first time, it has a single
built-in network called the "default bridge" network. When you run a
container without the `--network` option, it is connected to the default
bridge.

Containers attached to the default bridge have access to network services
outside the Docker host. They use "masquerading" which means, if the
Docker host has Internet access, no additional configuration is needed
for the container to have Internet access.

For example, to run a container on the default bridge network, and have
it ping an Internet host:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker run --rm -ti busybox ping -c1 docker.com
PING docker.com (23.185.0.4): 56 data bytes
64 bytes from 23.185.0.4: seq=0 ttl=62 time=6.564 ms

--- docker.com ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 6.564/6.564/6.564 ms

## User-defined networks

With the default configuration, containers attached to the default
bridge network have unrestricted network access to each other using
container IP addresses. They cannot refer to each other by name.

It can be useful to separate groups of containers that should have full
access to each other, but restricted access to containers in other groups.

You can create custom, user-defined networks, and connect groups of containers
to the same network. Once connected to a user-defined network, containers
can communicate with each other using container IP addresses or container names.

The following example creates a network using the `bridge` network driver and
runs a container in that network:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create -d bridge my-net
$ docker run --network=my-net -it busybox

### Drivers

Docker Engine has a number of network drivers, as well as the default "bridge".
On Linux, the following built-in network drivers are available:
DriverDescriptionbridgeThe default network driver.hostRemove network isolation between the container and the Docker host.noneCompletely isolate a container from the host and other containers.overlaySwarm Overlay networks connect multiple Docker daemons together.ipvlanConnect containers to external VLANs.macvlanContainers appear as devices on the host's network.
More information can be found in the network driver specific pages, including
their configuration options and details about their functionality.

Native Windows containers have a different set of drivers, see
Windows container network drivers.

### Connecting to multiple networks

Connecting a container to a network can be compared to connecting an Ethernet
cable to a physical host. Just as a host can be connected to multiple Ethernet
networks, a container can be connected to multiple Docker networks.

For example, a frontend container may be connected to a bridge network
with external access, and a
`--internal` network
to communicate with containers running backend services that do not need
external network access.

A container may also be connected to different types of network. For example,
an `ipvlan` network to provide internet access, and a `bridge` network for
access to local services.

Containers can also share networking stacks, see Container networks.

When sending packets, if the destination is an address in a directly connected
network, packets are sent to that network. Otherwise, packets are sent to
a default gateway for routing to their destination. In the example above,
the `ipvlan` network's gateway must be the default gateway.

The default gateway is selected by Docker, and may change whenever a
container's network connections change.
To make Docker choose a specific default gateway when creating the container
or connecting a new network, set a gateway priority. See option `gw-priority`
for the
`docker run` and
`docker network connect` commands.

The default `gw-priority` is `0` and the gateway in the network with the
highest priority is the default gateway. So, when a network should always
be the default gateway, it is enough to set its `gw-priority` to `1`.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker run --network name=gwnet,gw-priority=1 --network anet1 --name myctr myimage
$ docker network connect anet2 myctr

## Published ports

When you create or run a container using `docker create` or `docker run`, all
ports of containers on bridge networks are accessible from the Docker host and
other containers connected to the same network. Ports are not accessible from
outside the host or, with the default configuration, from containers in other
networks.

Use the `--publish` or `-p` flag to make a port available outside the host,
and to containers in other bridge networks.

For more information about port mapping, including how to disable it and use
direct routing to containers, see
port publishing.

## IP address and hostname

When creating a network, IPv4 address allocation is enabled by default, it
can be disabled using `--ipv4=false`. IPv6 address allocation can be enabled
using `--ipv6`.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create --ipv6 --ipv4=false v6net

By default, the container gets an IP address for every Docker network it attaches to.
A container receives an IP address out of the IP subnet of the network.
The Docker daemon performs dynamic subnetting and IP address allocation for containers.
Each network also has a default subnet mask and gateway.

You can connect a running container to multiple networks,
either by passing the `--network` flag multiple times when creating the container,
or using the `docker network connect` command for already running containers.
In both cases, you can use the `--ip` or `--ip6` flags to specify the container's IP address on that particular network.

In the same way, a container's hostname defaults to be the container's ID in Docker.
You can override the hostname using `--hostname`.
When connecting to an existing network using `docker network connect`,
you can use the `--alias` flag to specify an additional network alias for the container on that network.

### Subnet allocation

Docker networks can use either explicitly configured subnets or automatically allocated ones from default pools.

#### Explicit subnet configuration

You can specify exact subnets when creating a network:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create --ipv6 --subnet 192.0.2.0/24 --subnet 2001:db8::/64 mynet

#### Automatic subnet allocation

When no `--subnet` option is provided, Docker automatically selects a subnet from predefined "default address pools".
These pools can be configured in `/etc/docker/daemon.json`. Docker's built-in default is equivalent to:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

{
  "default-address-pools": [
    {"base":"172.17.0.0/16","size":16},
    {"base":"172.18.0.0/16","size":16},
    {"base":"172.19.0.0/16","size":16},
    {"base":"172.20.0.0/14","size":16},
    {"base":"172.24.0.0/14","size":16},
    {"base":"172.28.0.0/14","size":16},
    {"base":"192.168.0.0/16","size":20}
  ]
}
- `base`: The subnet that can be allocated from.
- `size`: The prefix length used for each allocated subnet.
When an IPv6 subnet is required and there are no IPv6 addresses in `default-address-pools`, Docker allocates
subnets from a Unique Local Address (ULA) prefix. To use specific IPv6 subnets instead, add them to your
`default-address-pools`. See Dynamic IPv6 subnet allocation
for more information.

Docker attempts to avoid address prefixes already in use on the host. However, you may need to customize
`default-address-pools` to prevent routing conflicts in some network environments.

The default pools use large subnets, which limits the number of networks you can create. You can divide base
subnets into smaller pools to support more networks.

For example, this configuration allows Docker to create 256 networks from `172.17.0.0/16`.
Docker will allocate subnets `172.17.0.0/24`, `172.17.1.0/24`, and so on, up to `172.17.255.0/24`:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

{
  "default-address-pools": [
    {"base": "172.17.0.0/16", "size": 24}
  ]
}
You can also request a subnet with a specific prefix length from the default pools by using unspecified
addresses in the `--subnet` option:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create --ipv6 --subnet ::/56 --subnet 0.0.0.0/24 mynet
6686a6746b17228f5052528113ddad0e6d68e2e3905d648e336b33409f2d3b64
$ docker network inspect mynet -f '{{json .IPAM.Config}}' | jq .
[
  {
    "Subnet": "172.19.0.0/24",
    "Gateway": "172.19.0.1"
  },
  {
    "Subnet": "fdd3:6f80:972c::/56",
    "Gateway": "fdd3:6f80:972c::1"
  }
]

Note
Support for unspecified addresses in `--subnet` was introduced in Docker 29.0.0.
If Docker is downgraded to an older version, networks created in this way will become unusable.
They can be removed and re-created, or will function again if the daemon is restored to 29.0.0 or later.

## DNS services

Containers use the same DNS servers as the host by default, but you can
override this with `--dns`.

By default, containers inherit the DNS settings as defined in the
`/etc/resolv.conf` configuration file.
Containers that attach to the default `bridge` network receive a copy of this file.
Containers that attach to a
custom network
use Docker's embedded DNS server.
The embedded DNS server forwards external DNS lookups to the DNS servers configured on the host.

You can configure DNS resolution on a per-container basis, using flags for the
`docker run` or `docker create` command used to start the container.
The following table describes the available `docker run` flags related to DNS
configuration.
FlagDescription`--dns`The IP address of a DNS server. To specify multiple DNS servers, use multiple `--dns` flags. DNS requests will be forwarded from the container's network namespace so, for example, `--dns=127.0.0.1` refers to the container's own loopback address.`--dns-search`A DNS search domain to search non-fully qualified hostnames. To specify multiple DNS search prefixes, use multiple `--dns-search` flags.`--dns-opt`A key-value pair representing a DNS option and its value. See your operating system's documentation for `resolv.conf` for valid options.`--hostname`The hostname a container uses for itself. Defaults to the container's ID if not specified.
### Custom hosts

Your container will have lines in `/etc/hosts` which define the hostname of the
container itself, as well as `localhost` and a few other common things. Custom
hosts, defined in `/etc/hosts` on the host machine, aren't inherited by
containers. To pass additional hosts into a container, refer to
add entries to
container hosts file in the
`docker run` reference documentation.

## Container networks

In addition to user-defined networks, you can attach a container to another
container's networking stack directly, using the `--network container:<name|id>` flag format.

The following flags aren't supported for containers using the `container:`
networking mode:

- `--add-host`
- `--hostname`
- `--dns`
- `--dns-search`
- `--dns-option`
- `--mac-address`
- `--publish`
- `--publish-all`
- `--expose`
The following example runs a Redis container, with Redis binding to
127.0.0.1, then running the `redis-cli` command and connecting to the Redis
server over 127.0.0.1.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker run -d --name redis redis --bind 127.0.0.1
$ docker run --rm -it --network container:redis redis redis-cli -h 127.0.0.1

Edit this page

[Request changes](https://github.com/docker/docs/issues/new?template=doc_issue.yml&location=https%3a%2f%2fdocs.docker.com%2fengine%2fnetwork%2f&labels=status%2Ftriage)
Table of contents

Product offerings
Pricing
About us
llms.txt
Cookies Settings

|
Terms of Service
|
Status
|
LegalCopyright Â© 2013-2026 Docker Inc. All rights
reserved.
