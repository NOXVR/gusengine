# Source: https://docs.docker.com/reference/cli/docker/network/create/
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

docker network create | Docker Docs
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
                  page_title: "docker network create"
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
Reference

- 
Get started
- 
Guides
- 
Manuals
# docker network create

Copy as Markdown

Open Markdown

Ask Docs AI

Claude

Open in ClaudeDescriptionCreate a networkUsage`docker network create [OPTIONS] NETWORK`
## Description

Creates a new network. The `DRIVER` accepts `bridge` or `overlay` which are the
built-in network drivers. If you have installed a third party or your own custom
network driver you can specify that `DRIVER` here also. If you don't specify the
`--driver` option, the command automatically creates a `bridge` network for you.
When you install Docker Engine it creates a `bridge` network automatically. This
network corresponds to the `docker0` bridge that Docker Engine has traditionally relied
on. When you launch a new container with `docker run` it automatically connects to
this bridge network. You cannot remove this default bridge network, but you can
create new ones using the `network create` command.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create -d bridge my-bridge-network

Bridge networks are isolated networks on a single Docker Engine installation. If you
want to create a network that spans multiple Docker hosts each running Docker
Engine, you must enable Swarm mode, and create an `overlay` network. To read more
about overlay networks with Swarm mode, see
"*use overlay networks*".

Once you have enabled swarm mode, you can create a swarm-scoped overlay network:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create --scope=swarm --attachable -d overlay my-multihost-network

By default, swarm-scoped networks do not allow manually started containers to
be attached. This restriction is added to prevent someone that has access to
a non-manager node in the swarm cluster from running a container that is able
to access the network stack of a swarm service.

The `--attachable` option used in the example above disables this restriction,
and allows for both swarm services and manually started containers to attach to
the overlay network.

Network names must be unique. The Docker daemon attempts to identify naming
conflicts but this is not guaranteed. It is the user's responsibility to avoid
name conflicts.

### Overlay network limitations

You should create overlay networks with `/24` blocks (the default), which limits
you to 256 IP addresses, when you create networks using the default VIP-based
endpoint-mode. This recommendation addresses
limitations with swarm mode. If you
need more than 256 IP addresses, do not increase the IP block size. You can
either use `dnsrr` endpoint mode with an external load balancer, or use multiple
smaller overlay networks. See
Configure service discovery
for more information about different endpoint modes.

## Options
OptionDefaultDescription`--attachable`API 1.25+
Enable manual container attachment`--aux-address`Auxiliary IPv4 or IPv6 addresses used by Network driver`--config-from`API 1.30+
The network from which to copy the configuration`--config-only`API 1.30+
Create a configuration only network`-d, --driver``bridge`Driver to manage the Network`--gateway`IPv4 or IPv6 Gateway for the master subnet`--ingress`API 1.29+
Create swarm routing-mesh network`--internal`Restrict external access to the network`--ip-range`Allocate container ip from a sub-range`--ipam-driver`IP Address Management Driver`--ipam-opt`Set IPAM driver specific options`--ipv4``true`Enable or disable IPv4 address assignment`--ipv6`Enable or disable IPv6 address assignment`--label`Set metadata on a network`-o, --opt`Set driver specific options`--scope`API 1.30+
Control the network's scope`--subnet`Subnet in CIDR format that represents a network segment
## Examples

### Connect containers

When you start a container, use the `--network` flag to connect it to a network.
This example adds the `busybox` container to the `mynet` network:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker run -itd --network=mynet busybox

If you want to add a container to a network after the container is already
running, use the `docker network connect` subcommand.

You can connect multiple containers to the same network. Once connected, the
containers can communicate using only another container's IP address or name.
For `overlay` networks or custom plugins that support multi-host connectivity,
containers connected to the same multi-host network but launched from different
daemons can also communicate in this way.

You can disconnect a container from a network using the `docker network disconnect` command.

### Specify advanced options

When you create a network, Docker Engine creates a non-overlapping subnetwork
for the network by default. This subnetwork is not a subdivision of an existing
network. It is purely for ip-addressing purposes. You can override this default
and specify subnetwork values directly using the `--subnet` option. On a
`bridge` network you can only create a single subnet:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create --driver=bridge --subnet=192.168.0.0/16 br0

Additionally, you also specify the `--gateway` `--ip-range` and `--aux-address`
options.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create \
  --driver=bridge \
  --subnet=172.28.0.0/16 \
  --ip-range=172.28.5.0/24 \
  --gateway=172.28.5.254 \
  br0

If you omit the `--gateway` flag, Docker Engine selects one for you from inside
a preferred pool. For `overlay` networks and for network driver plugins that
support it you can create multiple subnetworks. This example uses two `/25`
subnet mask to adhere to the current guidance of not having more than 256 IPs in
a single overlay network. Each of the subnetworks has 126 usable addresses.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create -d overlay \
  --subnet=192.168.10.0/25 \
  --subnet=192.168.20.0/25 \
  --gateway=192.168.10.100 \
  --gateway=192.168.20.100 \
  --aux-address="my-router=192.168.10.5" --aux-address="my-switch=192.168.10.6" \
  --aux-address="my-printer=192.168.20.5" --aux-address="my-nas=192.168.20.6" \
  my-multihost-network

Be sure that your subnetworks do not overlap. If they do, the network create
fails and Docker Engine returns an error.

### Bridge driver options

When creating a custom `bridge` network, the following additional options can
be passed. Some of these have equivalent flags that can be used on the dockerd
command line or in `daemon.json` to configure the default bridge, `docker0`:
Network create optionDaemon option for `docker0`Description`com.docker.network.bridge.name`-Bridge name to be used when creating the Linux bridge`com.docker.network.bridge.enable_ip_masquerade``--ip-masq`Enable IP masquerading`com.docker.network.bridge.enable_icc``--icc`Enable or Disable Inter Container Connectivity`com.docker.network.bridge.host_binding_ipv4``--ip`Default IP when binding container ports`com.docker.network.driver.mtu``--mtu`Set the containers network MTU`com.docker.network.container_iface_prefix`-Set a custom prefix for container interfaces
The following arguments can be passed to `docker network create` for any
network driver, again with their approximate equivalents to Docker daemon
flags used for the `docker0` bridge:
Network create optionDaemon option for `docker0`Description`--gateway`-IPv4 or IPv6 Gateway for the master subnet`--ip-range``--fixed-cidr`, `--fixed-cidr-v6`Allocate IP addresses from a range`--internal`-Restrict external access to the network`--ipv4`-Enable or disable IPv4 address assignment`--ipv6``--ipv6`Enable or disable IPv6 address assignment`--subnet``--bip`, `--bip6`Subnet for network
For example, let's use `-o` or `--opt` options to specify an IP address binding
when publishing ports:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create \
    -o "com.docker.network.bridge.host_binding_ipv4"="172.19.0.1" \
    simple-network

### Network internal mode (--internal)

Containers on an internal network may communicate between each other, but not
with any other network, as no default route is configured and firewall rules
are set up to drop all traffic to or from other networks. Communication with
the gateway IP address (and thus appropriately configured host services) is
possible, and the host may communicate with any container IP directly.

By default, when you connect a container to an `overlay` network, Docker also
connects a bridge network to it to provide external connectivity. If you want
to create an externally isolated `overlay` network, you can specify the
`--internal` option.

### Network ingress mode (--ingress)

You can create the network which will be used to provide the routing-mesh in the
swarm cluster. You do so by specifying `--ingress` when creating the network. Only
one ingress network can be created at the time. The network can be removed only
if no services depend on it. Any option available when creating an overlay network
is also available when creating the ingress network, besides the `--attachable` option.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create -d overlay \
  --subnet=10.11.0.0/16 \
  --ingress \
  --opt com.docker.network.driver.mtu=9216 \
  --opt encrypted=true \
  my-ingress-network

### Run services on predefined networks

You can create services on the predefined Docker networks `bridge` and `host`.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker service create --name my-service \
  --network host \
  --replicas 2 \
  busybox top

### Swarm networks with local scope drivers

You can create a swarm network with local scope network drivers. You do so
by promoting the network scope to `swarm` during the creation of the network.
You will then be able to use this network when creating services.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network create -d bridge \
  --scope swarm \
  --attachable \
  swarm-network

For network drivers which provide connectivity across hosts (ex. macvlan), if
node specific configurations are needed in order to plumb the network on each
host, you will supply that configuration via a configuration only network.
When you create the swarm scoped network, you will then specify the name of the
network which contains the configuration.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

node1$ docker network create --config-only --subnet 192.168.100.0/24 --gateway 192.168.100.115 mv-config
node2$ docker network create --config-only --subnet 192.168.200.0/24 --gateway 192.168.200.202 mv-config
node1$ docker network create -d macvlan --scope swarm --config-from mv-config --attachable swarm-network
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
