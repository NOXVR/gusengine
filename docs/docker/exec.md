# Source: https://docs.docker.com/reference/cli/docker/container/exec/
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

docker container exec | Docker Docs
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
                  page_title: "docker container exec"
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
# docker container exec

Copy as Markdown

Open Markdown

Ask Docs AI

Claude

Open in ClaudeDescriptionExecute a command in a running containerUsage`docker container exec [OPTIONS] CONTAINER COMMAND [ARG...]`Aliases
An alias is a short or memorable alternative for a longer command.`docker exec`
**Introducing Docker Debug**

To easily get a debug shell into any container, use `docker debug`. Docker
Debug is a replacement for debugging with `docker exec`. With it, you can get
a shell into any container or image, even slim ones, without modifications.
Plus, you can bring along your favorite debugging tools in its customizable
toolbox.

Explore Docker Debug now.

## Description

The `docker exec` command runs a new command in a running container.

The command you specify with `docker exec` only runs while the container's
primary process (`PID 1`) is running, and it isn't restarted if the container
is restarted.

The command runs in the default working directory of the container.

The command must be an executable. A chained or a quoted command doesn't work.

- This works: `docker exec -it my_container sh -c "echo a && echo b"`
- This doesn't work: `docker exec -it my_container "echo a && echo b"`
## Options
OptionDefaultDescription`-d, --detach`Detached mode: run command in the background`--detach-keys`Override the key sequence for detaching a container`-e, --env`API 1.25+
Set environment variables`--env-file`API 1.25+
Read in a file of environment variables`-i, --interactive`Keep STDIN open even if not attached`--privileged`Give extended privileges to the command`-t, --tty`Allocate a pseudo-TTY`-u, --user`Username or UID (format: `<name|uid>[:<group|gid>]`)`-w, --workdir`API 1.35+
Working directory inside the container
## Examples

### Run `docker exec` on a running container

First, start a container.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker run --name mycontainer -d -i -t alpine /bin/sh

This creates and starts a container named `mycontainer` from an `alpine` image
with an `sh` shell as its main process. The `-d` option (shorthand for `--detach`)
sets the container to run in the background, in detached mode, with a pseudo-TTY
attached (`-t`). The `-i` option is set to keep `STDIN` attached (`-i`), which
prevents the `sh` process from exiting immediately.

Next, execute a command on the container.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker exec -d mycontainer touch /tmp/execWorks

This creates a new file `/tmp/execWorks` inside the running container
`mycontainer`, in the background.

Next, execute an interactive `sh` shell on the container.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker exec -it mycontainer sh

This starts a new shell session in the container `mycontainer`.

### Set environment variables for the exec process (--env, -e)

Next, set environment variables in the current bash session.

The `docker exec` command inherits the environment variables that are set at the
time the container is created. Use the `--env` (or the `-e` shorthand) to
override global environment variables, or to set additional environment
variables for the process started by `docker exec`.

The following example creates a new shell session in the container `mycontainer`,
with environment variables `$VAR_A` set to `1`, and `$VAR_B` set to `2`.
These environment variables are only valid for the `sh` process started by that
`docker exec` command, and aren't available to other processes running inside
the container.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker exec -e VAR_A=1 -e VAR_B=2 mycontainer env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=f64a4851eb71
VAR_A=1
VAR_B=2
HOME=/root

### Escalate container privileges (--privileged)

See
`docker run --privileged`.

### Set the working directory for the exec process (--workdir, -w)

By default `docker exec` command runs in the same working directory set when
the container was created.
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker exec -it mycontainer pwd
/

You can specify an alternative working directory for the command to execute
using the `--workdir` option (or the `-w` shorthand):
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker exec -it -w /root mycontainer pwd
/root

### Try to run `docker exec` on a paused container

If the container is paused, then the `docker exec` command fails with an error:
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker pause mycontainer
mycontainer

$ docker ps

CONTAINER ID   IMAGE     COMMAND     CREATED          STATUS                   PORTS     NAMES
482efdf39fac   alpine    "/bin/sh"   17 seconds ago   Up 16 seconds (Paused)             mycontainer

$ docker exec mycontainer sh

Error response from daemon: Container mycontainer is paused, unpause the container before exec

$ echo $?
1
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
