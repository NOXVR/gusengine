# Source: https://docs.docker.com/reference/cli/docker/compose/up/
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

docker compose up | Docker Docs
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
                  page_title: "docker compose up"
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
# docker compose up

Copy as Markdown

Open Markdown

Ask Docs AI

Claude

Open in ClaudeDescriptionCreate and start containersUsage`docker compose up [OPTIONS] [SERVICE...]`
## Description

Builds, (re)creates, starts, and attaches to containers for a service.

Unless they are already running, this command also starts any linked services.

The `docker compose up` command aggregates the output of each container (like `docker compose logs --follow` does).
One can optionally select a subset of services to attach to using `--attach` flag, or exclude some services using
`--no-attach` to prevent output to be flooded by some verbose services.

When the command exits, all containers are stopped. Running `docker compose up --detach` starts the containers in the
background and leaves them running.

If there are existing containers for a service, and the serviceâs configuration or image was changed after the
containerâs creation, `docker compose up` picks up the changes by stopping and recreating the containers
(preserving mounted volumes). To prevent Compose from picking up changes, use the `--no-recreate` flag.

If you want to force Compose to stop and recreate all containers, use the `--force-recreate` flag.

If the process encounters an error, the exit code for this command is `1`.
If the process is interrupted using `SIGINT` (ctrl + C) or `SIGTERM`, the containers are stopped, and the exit code is `0`.

## Options
OptionDefaultDescription`--abort-on-container-exit`Stops all containers if any container was stopped. Incompatible with -d
`--abort-on-container-failure`Stops all containers if any container exited with failure. Incompatible with -d
`--always-recreate-deps`Recreate dependent containers. Incompatible with --no-recreate.`--attach`Restrict attaching to the specified services. Incompatible with --attach-dependencies.
`--attach-dependencies`Automatically attach to log output of dependent services`--build`Build images before starting containers`-d, --detach`Detached mode: Run containers in the background`--exit-code-from`Return the exit code of the selected service container. Implies --abort-on-container-exit
`--force-recreate`Recreate containers even if their configuration and image haven't changed
`--menu`Enable interactive shortcuts when running attached. Incompatible with --detach. Can also be enable/disable by setting COMPOSE_MENU environment var.
`--no-attach`Do not attach (stream logs) to the specified services`--no-build`Don't build an image, even if it's policy`--no-color`Produce monochrome output`--no-deps`Don't start linked services`--no-log-prefix`Don't print prefix in logs`--no-recreate`If containers already exist, don't recreate them. Incompatible with --force-recreate.
`--no-start`Don't start the services after creating them`--pull``policy`Pull image before running ("always"|"missing"|"never")`--quiet-build`Suppress the build output`--quiet-pull`Pull without printing progress information`--remove-orphans`Remove containers for services not defined in the Compose file`-V, --renew-anon-volumes`Recreate anonymous volumes instead of retrieving data from the previous containers
`--scale`Scale SERVICE to NUM instances. Overrides the `scale` setting in the Compose file if present.
`-t, --timeout`Use this timeout in seconds for container shutdown when attached or when containers are already running
`--timestamps`Show timestamps`--wait`Wait for services to be running|healthy. Implies detached mode.`--wait-timeout`Maximum duration in seconds to wait for the project to be running|healthy
`-w, --watch`Watch source code and rebuild/refresh containers when files are updated.
`-y, --yes`Assume "yes" as answer to all prompts and run non-interactivelyTable of contents

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
