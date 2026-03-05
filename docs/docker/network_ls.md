# Source: https://docs.docker.com/reference/cli/docker/network/ls/
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

docker network ls | Docker Docs
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
                  page_title: "docker network ls"
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
# docker network ls

Copy as Markdown

Open Markdown

Ask Docs AI

Claude

Open in ClaudeDescriptionList networksUsage`docker network ls [OPTIONS]`Aliases
An alias is a short or memorable alternative for a longer command.`docker network list`
## Description

Lists all the networks the Engine `daemon` knows about. This includes the
networks that span across multiple hosts in a cluster.

## Options
OptionDefaultDescription`-f, --filter`Provide filter values (e.g. `driver=bridge`)`--format`Format output using a custom template:
'table': Print output in table format with column headers (default)
'table TEMPLATE': Print output in table format using the given Go template
'json': Print in JSON format
'TEMPLATE': Print output using the given Go template.
Refer to https://docs.docker.com/go/formatting/ for more information about formatting output with templates`--no-trunc`Do not truncate the output`-q, --quiet`Only display network IDs
## Examples

### List all networks
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls
NETWORK ID          NAME                DRIVER          SCOPE
7fca4eb8c647        bridge              bridge          local
9f904ee27bf5        none                null            local
cf03ee007fb4        host                host            local
78b03ee04fc4        multi-host          overlay         swarm

### List networks without truncating the ID column (--no-trun)

Use the `--no-trunc` option to display the full network id:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --no-trunc
NETWORK ID                                                         NAME                DRIVER           SCOPE
18a2866682b85619a026c81b98a5e375bd33e1b0936a26cc497c283d27bae9b3   none                null             local
c288470c46f6c8949c5f7e5099b5b7947b07eabe8d9a27d79a9cbf111adcbf47   host                host             local
7b369448dccbf865d397c8d2be0cda7cf7edc6b0945f77d2529912ae917a0185   bridge              bridge           local
95e74588f40db048e86320c6526440c504650a1ff3e9f7d60a497c4d2163e5bd   foo                 bridge           local
63d1ff1f77b07ca51070a8c227e962238358bd310bde1529cf62e6c307ade161   dev                 bridge           local

### Filtering (--filter)

The filtering flag (`-f` or `--filter`) format is a `key=value` pair. If there
is more than one filter, then pass multiple flags (e.g. `--filter "foo=bar" --filter "bif=baz"`).
Multiple filter flags are combined as an `OR` filter. For example,
`-f type=custom -f type=builtin` returns both `custom` and `builtin` networks.

The currently supported filters are:

- driver
- id (network's id)
- label (`label=<key>` or `label=<key>=<value>`)
- name (network's name)
- scope (`swarm|global|local`)
- type (`custom|builtin`)
#### Driver

The `driver` filter matches networks based on their driver.

The following example matches networks with the `bridge` driver:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --filter driver=bridge
NETWORK ID          NAME                DRIVER            SCOPE
db9db329f835        test1               bridge            local
f6e212da9dfd        test2               bridge            local

#### ID

The `id` filter matches on all or part of a network's ID.

The following filter matches all networks with an ID containing the
`63d1ff1f77b0...` string.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --filter id=63d1ff1f77b07ca51070a8c227e962238358bd310bde1529cf62e6c307ade161
NETWORK ID          NAME                DRIVER           SCOPE
63d1ff1f77b0        dev                 bridge           local

You can also filter for a substring in an ID as this shows:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --filter id=95e74588f40d
NETWORK ID          NAME                DRIVER          SCOPE
95e74588f40d        foo                 bridge          local

$ docker network ls --filter id=95e
NETWORK ID          NAME                DRIVER          SCOPE
95e74588f40d        foo                 bridge          local

#### Label

The `label` filter matches networks based on the presence of a `label` alone or a `label` and a
value.

The following filter matches networks with the `usage` label regardless of its value.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls -f "label=usage"
NETWORK ID          NAME                DRIVER         SCOPE
db9db329f835        test1               bridge         local
f6e212da9dfd        test2               bridge         local

The following filter matches networks with the `usage` label with the `prod` value.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls -f "label=usage=prod"
NETWORK ID          NAME                DRIVER        SCOPE
f6e212da9dfd        test2               bridge        local

#### Name

The `name` filter matches on all or part of a network's name.

The following filter matches all networks with a name containing the `foobar` string.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --filter name=foobar
NETWORK ID          NAME                DRIVER       SCOPE
06e7eef0a170        foobar              bridge       local

You can also filter for a substring in a name as this shows:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --filter name=foo
NETWORK ID          NAME                DRIVER       SCOPE
95e74588f40d        foo                 bridge       local
06e7eef0a170        foobar              bridge       local

#### Scope

The `scope` filter matches networks based on their scope.

The following example matches networks with the `swarm` scope:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --filter scope=swarm
NETWORK ID          NAME                DRIVER              SCOPE
xbtm0v4f1lfh        ingress             overlay             swarm
ic6r88twuu92        swarmnet            overlay             swarm

The following example matches networks with the `local` scope:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --filter scope=local
NETWORK ID          NAME                DRIVER              SCOPE
e85227439ac7        bridge              bridge              local
0ca0e19443ed        host                host                local
ca13cc149a36        localnet            bridge              local
f9e115d2de35        none                null                local

#### Type

The `type` filter supports two values; `builtin` displays predefined networks
(`bridge`, `none`, `host`), whereas `custom` displays user defined networks.

The following filter matches all user defined networks:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --filter type=custom
NETWORK ID          NAME                DRIVER       SCOPE
95e74588f40d        foo                 bridge       local
63d1ff1f77b0        dev                 bridge       local

By having this flag it allows for batch cleanup. For example, use this filter
to delete all user defined networks:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network rm `docker network ls --filter type=custom -q`

A warning will be issued when trying to remove a network that has containers
attached.

### Format the output (--format)

The formatting options (`--format`) pretty-prints networks output
using a Go template.

Valid placeholders for the Go template are listed below:
PlaceholderDescription`.ID`Network ID`.Name`Network name`.Driver`Network driver`.Scope`Network scope (local, global)`.IPv6`Whether IPv6 is enabled on the network or not.`.Internal`Whether the network is internal or not.`.Labels`All labels assigned to the network.`.Label`Value of a specific label for this network. For example `{{.Label "project.version"}}``.CreatedAt`Time when the network was created
When using the `--format` option, the `network ls` command will either
output the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`ID` and `Driver` entries separated by a colon (`:`) for all networks:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --format "{{.ID}}: {{.Driver}}"
afaaab448eb2: bridge
d1584f8dc718: host
391df270dc66: null

To list all networks in JSON format, use the `json` directive:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker network ls --format json
{"CreatedAt":"2021-03-09 21:41:29.798999529 +0000 UTC","Driver":"bridge","ID":"f33ba176dd8e","IPv6":"false","Internal":"false","Labels":"","Name":"bridge","Scope":"local"}
{"CreatedAt":"2021-03-09 21:41:29.772806592 +0000 UTC","Driver":"host","ID":"caf47bb3ac70","IPv6":"false","Internal":"false","Labels":"","Name":"host","Scope":"local"}
{"CreatedAt":"2021-03-09 21:41:29.752212603 +0000 UTC","Driver":"null","ID":"9d096c122066","IPv6":"false","Internal":"false","Labels":"","Name":"none","Scope":"local"}
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
