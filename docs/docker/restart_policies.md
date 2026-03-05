# Source: https://docs.docker.com/engine/containers/start-containers-automatically/
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

Start containers automatically | Docker Docs
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
                  page_title: "Start containers automatically"
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
# Start containers automatically

Copy as Markdown

Open Markdown

Ask Docs AI

Claude

Open in ClaudeTable of contents
Docker provides
restart policies
to control whether your containers start automatically when they exit, or when
Docker restarts. Restart policies start linked containers in the correct order.
Docker recommends that you use restart policies, and avoid using process
managers to start containers.

Restart policies are different from the `--live-restore` flag of the `dockerd`
command. Using `--live-restore` lets you to keep your containers running during
a Docker upgrade, though networking and user input are interrupted.

## Use a restart policy

To configure the restart policy for a container, use the
`--restart` flag
when using the `docker run` command. The value of the `--restart` flag can be
any of the following:
FlagDescription`no`Don't automatically restart the container. (Default)`on-failure[:max-retries]`Restart the container if it exits due to an error, which manifests as a non-zero exit code. Optionally, limit the number of times the Docker daemon attempts to restart the container using the `:max-retries` option. The `on-failure` policy only prompts a restart if the container exits with a failure. It doesn't restart the container if the daemon restarts.`always`Always restart the container if it stops. If it's manually stopped, it's restarted only when Docker daemon restarts or the container itself is manually restarted. (See the second bullet listed in restart policy details)`unless-stopped`Similar to `always`, except that when the container is stopped (manually or otherwise), it isn't restarted even after Docker daemon restarts.
The following command starts a Redis container and configures it to always
restart, unless the container is explicitly stopped, or the daemon restarts.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker run -d --restart unless-stopped redis

The following command changes the restart policy for an already running
container named `redis`.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker update --restart unless-stopped redis

The following command ensures all running containers restart.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker update --restart unless-stopped $(docker ps -q)

### Restart policy details

Keep the following in mind when using restart policies:

- 
A restart policy only takes effect after a container starts successfully. In
this case, starting successfully means that the container is up for at least
10 seconds and Docker has started monitoring it. This prevents a container
which doesn't start at all from going into a restart loop.

- 
If you manually stop a container, the restart policy is ignored until the
Docker daemon restarts or the container is manually restarted. This prevents
a restart loop.

- 
Restart policies only apply to containers. To configure restart policies for
Swarm services, see
flags related to service restart.

### Restarting foreground containers

When you run a container in the foreground, stopping a container causes the
attached CLI to exit as well, regardless of the restart policy of the
container. This behavior is illustrated in the following example.

- 
Create a Dockerfile that prints the numbers 1 to 5 and then exits.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

FROM busybox:latest
COPY --chmod=755 <<"EOF" /start.sh
echo "Starting..."
for i in $(seq 1 5); do
  echo "$i"
  sleep 1
done
echo "Exiting..."
exit 1
EOF
ENTRYPOINT /start.sh
- 
Build an image from the Dockerfile.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker build -t startstop .

- 
Run a container from the image, specifying `always` for its restart policy.

The container prints the numbers 1..5 to stdout, and then exits. This causes
the attached CLI to exit as well.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker run --restart always startstop
Starting...
1
2
3
4
5
Exiting...
$

- 
Running `docker ps` shows that is still running or restarting, thanks to the
restart policy. The CLI session has already exited, however. It doesn't
survive the initial container exit.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker ps
CONTAINER ID   IMAGE       COMMAND                  CREATED         STATUS         PORTS     NAMES
081991b35afe   startstop   "/bin/sh -c /start.sh"   9 seconds ago   Up 4 seconds             gallant_easley

- 
You can re-attach your terminal to the container between restarts, using the
`docker container attach` command. It's detached again the next time the
container exits.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker container attach 081991b35afe
4
5
Exiting...
$

## Use a process manager

If restart policies don't suit your needs, such as when processes outside
Docker depend on Docker containers, you can use a process manager such as
systemd or
supervisor instead.

Warning
Don't combine Docker restart policies with host-level process managers,
as this creates conflicts.

To use a process manager, configure it to start your container or service using
the same `docker start` or `docker service` command you would normally use to
start the container manually. Consult the documentation for the specific
process manager for more details.

### Using a process manager inside containers

Process managers can also run within the container to check whether a process is
running and starts/restart it if not.

Warning
These aren't Docker-aware, and only monitor operating system processes within
the container. Docker doesn't recommend this approach, because it's
platform-dependent and may differ between versions of a given Linux
distribution.

Edit this page

[Request changes](https://github.com/docker/docs/issues/new?template=doc_issue.yml&location=https%3a%2f%2fdocs.docker.com%2fengine%2fcontainers%2fstart-containers-automatically%2f&labels=status%2Ftriage)
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
