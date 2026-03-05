# Source: https://docs.docker.com/reference/cli/docker/container/cp/
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

docker container cp | Docker Docs
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
                  page_title: "docker container cp"
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
# docker container cp

Copy as Markdown

Open Markdown

Ask Docs AI

Claude

Open in ClaudeDescriptionCopy files/folders between a container and the local filesystemUsagedocker container cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATHAliases
An alias is a short or memorable alternative for a longer command.`docker cp`
## Description

The `docker cp` utility copies the contents of `SRC_PATH` to the `DEST_PATH`.
You can copy from the container's file system to the local machine or the
reverse, from the local filesystem to the container. If `-` is specified for
either the `SRC_PATH` or `DEST_PATH`, you can also stream a tar archive from
`STDIN` or to `STDOUT`. The `CONTAINER` can be a running or stopped container.
The `SRC_PATH` or `DEST_PATH` can be a file or directory.

The `docker cp` command assumes container paths are relative to the container's
`/` (root) directory. This means supplying the initial forward slash is optional;
The command sees `compassionate_darwin:/tmp/foo/myfile.txt` and
`compassionate_darwin:tmp/foo/myfile.txt` as identical. Local machine paths can
be an absolute or relative value. The command interprets a local machine's
relative paths as relative to the current working directory where `docker cp` is
run.

The `cp` command behaves like the Unix `cp -a` command in that directories are
copied recursively with permissions preserved if possible. Ownership is set to
the user and primary group at the destination. For example, files copied to a
container are created with `UID:GID` of the root user. Files copied to the local
machine are created with the `UID:GID` of the user which invoked the `docker cp`
command. However, if you specify the `-a` option, `docker cp` sets the ownership
to the user and primary group at the source.
If you specify the `-L` option, `docker cp` follows any symbolic link
in the `SRC_PATH`. `docker cp` doesn't create parent directories for
`DEST_PATH` if they don't exist.

Assuming a path separator of `/`, a first argument of `SRC_PATH` and second
argument of `DEST_PATH`, the behavior is as follows:

- `SRC_PATH` specifies a file
- `DEST_PATH` does not exist
- the file is saved to a file created at `DEST_PATH`
- `DEST_PATH` does not exist and ends with `/`
- Error condition: the destination directory must exist.
- `DEST_PATH` exists and is a file
- the destination is overwritten with the source file's contents
- `DEST_PATH` exists and is a directory
- the file is copied into this directory using the basename from
`SRC_PATH`
- `SRC_PATH` specifies a directory
- `DEST_PATH` does not exist
- `DEST_PATH` is created as a directory and the *contents* of the source
directory are copied into this directory
- `DEST_PATH` exists and is a file
- Error condition: cannot copy a directory to a file
- `DEST_PATH` exists and is a directory
- `SRC_PATH` does not end with `/.` (that is: *slash* followed by *dot*)
- the source directory is copied into this directory
- `SRC_PATH` does end with `/.` (that is: *slash* followed by *dot*)
- the *content* of the source directory is copied into this
directory
The command requires `SRC_PATH` and `DEST_PATH` to exist according to the above
rules. If `SRC_PATH` is local and is a symbolic link, the symbolic link, not
the target, is copied by default. To copy the link target and not the link, specify
the `-L` option.

A colon (`:`) is used as a delimiter between `CONTAINER` and its path. You can
also use `:` when specifying paths to a `SRC_PATH` or `DEST_PATH` on a local
machine, for example `file:name.txt`. If you use a `:` in a local machine path,
you must be explicit with a relative or absolute path, for example:

`/path/to/file:name.txt` or `./file:name.txt`

## Options
OptionDefaultDescription`-a, --archive`Archive mode (copy all uid/gid information)`-L, --follow-link`Always follow symbol link in SRC_PATH`-q, --quiet`Suppress progress output during copy. Progress output is automatically suppressed if no terminal is attached

## Examples

Copy a local file into container
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker cp ./some_file CONTAINER:/work

Copy files from container to local path
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker cp CONTAINER:/var/logs/ /tmp/app_logs

Copy a file from container to stdout. Note `cp` command produces a tar stream
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker cp CONTAINER:/var/logs/app.log - | tar x -O | grep "ERROR"

### Corner cases

It isn't possible to copy certain system files such as resources under
`/proc`, `/sys`, `/dev`,
tmpfs, and mounts created by
the user in the container. However, you can still copy such files by manually
running `tar` in `docker exec`. Both of the following examples do the same thing
in different ways (consider `SRC_PATH` and `DEST_PATH` are directories):
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ docker exec CONTAINER tar Ccf $(dirname SRC_PATH) - $(basename SRC_PATH) | tar Cxf DEST_PATH -
]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);">

$ tar Ccf $(dirname SRC_PATH) - $(basename SRC_PATH) | docker exec -i CONTAINER tar Cxf DEST_PATH -

Using `-` as the `SRC_PATH` streams the contents of `STDIN` as a tar archive.
The command extracts the content of the tar to the `DEST_PATH` in container's
filesystem. In this case, `DEST_PATH` must specify a directory. Using `-` as
the `DEST_PATH` streams the contents of the resource as a tar archive to `STDOUT`.
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
