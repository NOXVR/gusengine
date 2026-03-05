# GusEngine Documentation Downloader
# Downloads complete official documentation for every technology in the stack
# Run from: J:\GusEngine

param(
    [string]$OutputBase = "J:\GusEngine\docs"
)

function Download-Page {
    param(
        [string]$Url,
        [string]$OutputFile,
        [string]$Label
    )
    try {
        Write-Host "  Downloading: $Label..." -NoNewline
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 30
        
        # Extract text content, stripping HTML tags
        $html = $response.Content
        
        # Remove script and style blocks
        $html = $html -replace '<script[^>]*>[\s\S]*?</script>', ''
        $html = $html -replace '<style[^>]*>[\s\S]*?</style>', ''
        $html = $html -replace '<nav[^>]*>[\s\S]*?</nav>', ''
        
        # Convert common HTML to markdown
        $html = $html -replace '<h1[^>]*>(.*?)</h1>', "`n# `$1`n"
        $html = $html -replace '<h2[^>]*>(.*?)</h2>', "`n## `$1`n"
        $html = $html -replace '<h3[^>]*>(.*?)</h3>', "`n### `$1`n"
        $html = $html -replace '<h4[^>]*>(.*?)</h4>', "`n#### `$1`n"
        $html = $html -replace '<code[^>]*>(.*?)</code>', '`$1`'
        $html = $html -replace '<pre[^>]*>(.*?)</pre>', "`n```````n`$1`n```````n"
        $html = $html -replace '<li[^>]*>', "`n- "
        $html = $html -replace '</li>', ''
        $html = $html -replace '<p[^>]*>', "`n"
        $html = $html -replace '</p>', "`n"
        $html = $html -replace '<br\s*/?>', "`n"
        $html = $html -replace '<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', '[$2]($1)'
        $html = $html -replace '<strong>(.*?)</strong>', '**$1**'
        $html = $html -replace '<em>(.*?)</em>', '*$1*'
        
        # Strip remaining tags
        $html = $html -replace '<[^>]+>', ''
        
        # Decode HTML entities
        $html = [System.Web.HttpUtility]::HtmlDecode($html)
        
        # Clean up excessive whitespace
        $html = $html -replace "`n{3,}", "`n`n"
        $html = $html.Trim()
        
        # Add source header
        $header = "# Source: $Url`n# Downloaded: $(Get-Date -Format 'yyyy-MM-dd')`n# This is the OFFICIAL documentation, not a summary.`n`n---`n`n"
        
        $content = $header + $html
        
        # Ensure directory exists
        $dir = Split-Path $OutputFile -Parent
        if (!(Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
        
        Set-Content -Path $OutputFile -Value $content -Encoding UTF8
        $size = [math]::Round((Get-Item $OutputFile).Length / 1KB, 1)
        Write-Host " OK ($size KB)"
        return $true
    }
    catch {
        Write-Host " FAILED: $($_.Exception.Message)"
        return $false
    }
}

Add-Type -AssemblyName System.Web

Write-Host "=========================================="
Write-Host "GusEngine Documentation Downloader"
Write-Host "=========================================="
Write-Host ""

# ============================================
# PYTHON STANDARD LIBRARY (docs.python.org)
# ============================================
Write-Host "--- PYTHON STANDARD LIBRARY ---"
$pythonModules = @(
    @{ Name="os"; Url="https://docs.python.org/3/library/os.html" },
    @{ Name="os.path"; Url="https://docs.python.org/3/library/os.path.html" },
    @{ Name="sys"; Url="https://docs.python.org/3/library/sys.html" },
    @{ Name="json"; Url="https://docs.python.org/3/library/json.html" },
    @{ Name="re"; Url="https://docs.python.org/3/library/re.html" },
    @{ Name="hashlib"; Url="https://docs.python.org/3/library/hashlib.html" },
    @{ Name="subprocess"; Url="https://docs.python.org/3/library/subprocess.html" },
    @{ Name="shutil"; Url="https://docs.python.org/3/library/shutil.html" },
    @{ Name="glob"; Url="https://docs.python.org/3/library/glob.html" },
    @{ Name="time"; Url="https://docs.python.org/3/library/time.html" },
    @{ Name="logging"; Url="https://docs.python.org/3/library/logging.html" },
    @{ Name="logging.config"; Url="https://docs.python.org/3/library/logging.config.html" },
    @{ Name="logging.handlers"; Url="https://docs.python.org/3/library/logging.handlers.html" },
    @{ Name="pathlib"; Url="https://docs.python.org/3/library/pathlib.html" },
    @{ Name="configparser"; Url="https://docs.python.org/3/library/configparser.html" },
    @{ Name="urllib.parse"; Url="https://docs.python.org/3/library/urllib.parse.html" },
    @{ Name="urllib.request"; Url="https://docs.python.org/3/library/urllib.request.html" },
    @{ Name="http.client"; Url="https://docs.python.org/3/library/http.client.html" },
    @{ Name="socket"; Url="https://docs.python.org/3/library/socket.html" },
    @{ Name="fcntl"; Url="https://docs.python.org/3/library/fcntl.html" },
    @{ Name="io"; Url="https://docs.python.org/3/library/io.html" },
    @{ Name="os-file-dir"; Url="https://docs.python.org/3/library/filesys.html" },
    @{ Name="tempfile"; Url="https://docs.python.org/3/library/tempfile.html" },
    @{ Name="signal"; Url="https://docs.python.org/3/library/signal.html" },
    @{ Name="threading"; Url="https://docs.python.org/3/library/threading.html" },
    @{ Name="multiprocessing"; Url="https://docs.python.org/3/library/multiprocessing.html" },
    @{ Name="base64"; Url="https://docs.python.org/3/library/base64.html" },
    @{ Name="collections"; Url="https://docs.python.org/3/library/collections.html" },
    @{ Name="functools"; Url="https://docs.python.org/3/library/functools.html" },
    @{ Name="itertools"; Url="https://docs.python.org/3/library/itertools.html" },
    @{ Name="typing"; Url="https://docs.python.org/3/library/typing.html" },
    @{ Name="dataclasses"; Url="https://docs.python.org/3/library/dataclasses.html" },
    @{ Name="datetime"; Url="https://docs.python.org/3/library/datetime.html" },
    @{ Name="traceback"; Url="https://docs.python.org/3/library/traceback.html" },
    @{ Name="argparse"; Url="https://docs.python.org/3/library/argparse.html" },
    @{ Name="csv"; Url="https://docs.python.org/3/library/csv.html" },
    @{ Name="sqlite3"; Url="https://docs.python.org/3/library/sqlite3.html" },
    @{ Name="unittest"; Url="https://docs.python.org/3/library/unittest.html" },
    @{ Name="contextlib"; Url="https://docs.python.org/3/library/contextlib.html" },
    @{ Name="abc"; Url="https://docs.python.org/3/library/abc.html" },
    @{ Name="enum"; Url="https://docs.python.org/3/library/enum.html" },
    @{ Name="struct"; Url="https://docs.python.org/3/library/struct.html" },
    @{ Name="textwrap"; Url="https://docs.python.org/3/library/textwrap.html" },
    @{ Name="string"; Url="https://docs.python.org/3/library/string.html" },
    @{ Name="copy"; Url="https://docs.python.org/3/library/copy.html" },
    @{ Name="pprint"; Url="https://docs.python.org/3/library/pprint.html" }
)

foreach ($mod in $pythonModules) {
    $filename = $mod.Name -replace '\.', '_'
    Download-Page -Url $mod.Url -OutputFile "$OutputBase\python\$filename.md" -Label "Python $($mod.Name)"
}

# ============================================
# NODE.JS (nodejs.org/api)
# ============================================
Write-Host ""
Write-Host "--- NODE.JS ---"
$nodeModules = @(
    @{ Name="fs"; Url="https://nodejs.org/api/fs.html" },
    @{ Name="path"; Url="https://nodejs.org/api/path.html" },
    @{ Name="http"; Url="https://nodejs.org/api/http.html" },
    @{ Name="https"; Url="https://nodejs.org/api/https.html" },
    @{ Name="url"; Url="https://nodejs.org/api/url.html" },
    @{ Name="crypto"; Url="https://nodejs.org/api/crypto.html" },
    @{ Name="buffer"; Url="https://nodejs.org/api/buffer.html" },
    @{ Name="stream"; Url="https://nodejs.org/api/stream.html" },
    @{ Name="events"; Url="https://nodejs.org/api/events.html" },
    @{ Name="process"; Url="https://nodejs.org/api/process.html" },
    @{ Name="child_process"; Url="https://nodejs.org/api/child_process.html" },
    @{ Name="os"; Url="https://nodejs.org/api/os.html" },
    @{ Name="util"; Url="https://nodejs.org/api/util.html" },
    @{ Name="assert"; Url="https://nodejs.org/api/assert.html" },
    @{ Name="querystring"; Url="https://nodejs.org/api/querystring.html" },
    @{ Name="modules"; Url="https://nodejs.org/api/modules.html" },
    @{ Name="globals"; Url="https://nodejs.org/api/globals.html" },
    @{ Name="errors"; Url="https://nodejs.org/api/errors.html" },
    @{ Name="console"; Url="https://nodejs.org/api/console.html" },
    @{ Name="timers"; Url="https://nodejs.org/api/timers.html" },
    @{ Name="net"; Url="https://nodejs.org/api/net.html" },
    @{ Name="dns"; Url="https://nodejs.org/api/dns.html" },
    @{ Name="zlib"; Url="https://nodejs.org/api/zlib.html" },
    @{ Name="readline"; Url="https://nodejs.org/api/readline.html" },
    @{ Name="string_decoder"; Url="https://nodejs.org/api/string_decoder.html" }
)

foreach ($mod in $nodeModules) {
    Download-Page -Url $mod.Url -OutputFile "$OutputBase\javascript\$($mod.Name).md" -Label "Node.js $($mod.Name)"
}

# ============================================
# NGINX (nginx.org)
# ============================================
Write-Host ""
Write-Host "--- NGINX ---"
$nginxPages = @(
    @{ Name="core"; Url="https://nginx.org/en/docs/ngx_core_module.html" },
    @{ Name="http_core"; Url="https://nginx.org/en/docs/http/ngx_http_core_module.html" },
    @{ Name="http_proxy"; Url="https://nginx.org/en/docs/http/ngx_http_proxy_module.html" },
    @{ Name="http_ssl"; Url="https://nginx.org/en/docs/http/ngx_http_ssl_module.html" },
    @{ Name="http_upstream"; Url="https://nginx.org/en/docs/http/ngx_http_upstream_module.html" },
    @{ Name="http_rewrite"; Url="https://nginx.org/en/docs/http/ngx_http_rewrite_module.html" },
    @{ Name="http_access"; Url="https://nginx.org/en/docs/http/ngx_http_access_module.html" },
    @{ Name="http_auth_basic"; Url="https://nginx.org/en/docs/http/ngx_http_auth_basic_module.html" },
    @{ Name="http_gzip"; Url="https://nginx.org/en/docs/http/ngx_http_gzip_module.html" },
    @{ Name="http_headers"; Url="https://nginx.org/en/docs/http/ngx_http_headers_module.html" },
    @{ Name="http_log"; Url="https://nginx.org/en/docs/http/ngx_http_log_module.html" },
    @{ Name="http_limit_req"; Url="https://nginx.org/en/docs/http/ngx_http_limit_req_module.html" },
    @{ Name="http_realip"; Url="https://nginx.org/en/docs/http/ngx_http_realip_module.html" },
    @{ Name="http_map"; Url="https://nginx.org/en/docs/http/ngx_http_map_module.html" },
    @{ Name="http_fastcgi"; Url="https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html" },
    @{ Name="http_sub_filter"; Url="https://nginx.org/en/docs/http/ngx_http_sub_module.html" },
    @{ Name="beginners_guide"; Url="https://nginx.org/en/docs/beginners_guide.html" },
    @{ Name="directives_index"; Url="https://nginx.org/en/docs/dirindex.html" },
    @{ Name="variables"; Url="https://nginx.org/en/docs/varindex.html" },
    @{ Name="websocket"; Url="https://nginx.org/en/docs/http/websocket.html" },
    @{ Name="configuring_https"; Url="https://nginx.org/en/docs/http/configuring_https_servers.html" },
    @{ Name="server_names"; Url="https://nginx.org/en/docs/http/server_names.html" },
    @{ Name="request_processing"; Url="https://nginx.org/en/docs/http/request_processing.html" }
)

foreach ($page in $nginxPages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\nginx\$($page.Name).md" -Label "Nginx $($page.Name)"
}

# ============================================
# DOCKER (docs.docker.com)
# ============================================
Write-Host ""
Write-Host "--- DOCKER ---"
$dockerPages = @(
    @{ Name="run"; Url="https://docs.docker.com/reference/cli/docker/container/run/" },
    @{ Name="build"; Url="https://docs.docker.com/reference/cli/docker/image/build/" },
    @{ Name="exec"; Url="https://docs.docker.com/reference/cli/docker/container/exec/" },
    @{ Name="logs"; Url="https://docs.docker.com/reference/cli/docker/container/logs/" },
    @{ Name="stop"; Url="https://docs.docker.com/reference/cli/docker/container/stop/" },
    @{ Name="rm"; Url="https://docs.docker.com/reference/cli/docker/container/rm/" },
    @{ Name="ps"; Url="https://docs.docker.com/reference/cli/docker/container/ls/" },
    @{ Name="inspect"; Url="https://docs.docker.com/reference/cli/docker/container/inspect/" },
    @{ Name="pull"; Url="https://docs.docker.com/reference/cli/docker/image/pull/" },
    @{ Name="images"; Url="https://docs.docker.com/reference/cli/docker/image/ls/" },
    @{ Name="volume_create"; Url="https://docs.docker.com/reference/cli/docker/volume/create/" },
    @{ Name="volume_ls"; Url="https://docs.docker.com/reference/cli/docker/volume/ls/" },
    @{ Name="network_create"; Url="https://docs.docker.com/reference/cli/docker/network/create/" },
    @{ Name="network_ls"; Url="https://docs.docker.com/reference/cli/docker/network/ls/" },
    @{ Name="cp"; Url="https://docs.docker.com/reference/cli/docker/container/cp/" },
    @{ Name="compose_up"; Url="https://docs.docker.com/reference/cli/docker/compose/up/" },
    @{ Name="compose_down"; Url="https://docs.docker.com/reference/cli/docker/compose/down/" },
    @{ Name="dockerfile_reference"; Url="https://docs.docker.com/reference/dockerfile/" },
    @{ Name="networking_overview"; Url="https://docs.docker.com/engine/network/" },
    @{ Name="volumes_overview"; Url="https://docs.docker.com/engine/storage/volumes/" },
    @{ Name="logging_overview"; Url="https://docs.docker.com/engine/logging/" },
    @{ Name="restart_policies"; Url="https://docs.docker.com/engine/containers/start-containers-automatically/" },
    @{ Name="security"; Url="https://docs.docker.com/engine/security/" },
    @{ Name="compose_file"; Url="https://docs.docker.com/reference/compose-file/" }
)

foreach ($page in $dockerPages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\docker\$($page.Name).md" -Label "Docker $($page.Name)"
}

# ============================================
# SYSTEMD (freedesktop.org)
# ============================================
Write-Host ""
Write-Host "--- SYSTEMD ---"
$systemdPages = @(
    @{ Name="systemd.unit"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html" },
    @{ Name="systemd.service"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html" },
    @{ Name="systemd.timer"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html" },
    @{ Name="systemd.exec"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html" },
    @{ Name="systemd.socket"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html" },
    @{ Name="systemd.resource-control"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html" },
    @{ Name="systemd.directives"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.directives.html" },
    @{ Name="systemctl"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemctl.html" },
    @{ Name="journalctl"; Url="https://www.freedesktop.org/software/systemd/man/latest/journalctl.html" },
    @{ Name="systemd.kill"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.kill.html" },
    @{ Name="systemd.path"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.path.html" },
    @{ Name="systemd.mount"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html" },
    @{ Name="systemd.target"; Url="https://www.freedesktop.org/software/systemd/man/latest/systemd.target.html" },
    @{ Name="environment.d"; Url="https://www.freedesktop.org/software/systemd/man/latest/environment.d.html" }
)

foreach ($page in $systemdPages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\systemd\$($page.Name).md" -Label "systemd $($page.Name)"
}

# ============================================
# PYMUPDF (pymupdf.readthedocs.io)
# ============================================
Write-Host ""
Write-Host "--- PYMUPDF ---"
$pymuPages = @(
    @{ Name="document"; Url="https://pymupdf.readthedocs.io/en/latest/document.html" },
    @{ Name="page"; Url="https://pymupdf.readthedocs.io/en/latest/page.html" },
    @{ Name="textpage"; Url="https://pymupdf.readthedocs.io/en/latest/textpage.html" },
    @{ Name="pixmap"; Url="https://pymupdf.readthedocs.io/en/latest/pixmap.html" },
    @{ Name="rect"; Url="https://pymupdf.readthedocs.io/en/latest/rect.html" },
    @{ Name="matrix"; Url="https://pymupdf.readthedocs.io/en/latest/matrix.html" },
    @{ Name="annot"; Url="https://pymupdf.readthedocs.io/en/latest/annot.html" },
    @{ Name="tools"; Url="https://pymupdf.readthedocs.io/en/latest/tools.html" },
    @{ Name="recipes-text"; Url="https://pymupdf.readthedocs.io/en/latest/recipes-text.html" },
    @{ Name="recipes-images"; Url="https://pymupdf.readthedocs.io/en/latest/recipes-images.html" },
    @{ Name="recipes-common-issues"; Url="https://pymupdf.readthedocs.io/en/latest/recipes-common-issues-and-their-solutions.html" },
    @{ Name="table"; Url="https://pymupdf.readthedocs.io/en/latest/page.html#Page.find_tables" },
    @{ Name="installation"; Url="https://pymupdf.readthedocs.io/en/latest/installation.html" },
    @{ Name="tutorial"; Url="https://pymupdf.readthedocs.io/en/latest/tutorial.html" },
    @{ Name="app1"; Url="https://pymupdf.readthedocs.io/en/latest/app1.html" },
    @{ Name="functions"; Url="https://pymupdf.readthedocs.io/en/latest/functions.html" },
    @{ Name="vars"; Url="https://pymupdf.readthedocs.io/en/latest/vars.html" }
)

foreach ($page in $pymuPages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\pymupdf\$($page.Name).md" -Label "PyMuPDF $($page.Name)"
}

# ============================================
# ANYTHINGLLM (docs.anythingllm.com)
# ============================================
Write-Host ""
Write-Host "--- ANYTHINGLLM ---"
$anythingPages = @(
    @{ Name="setup-overview"; Url="https://docs.anythingllm.com/setup/overview" },
    @{ Name="installation-docker"; Url="https://docs.anythingllm.com/installation-docker/overview" },
    @{ Name="agent-skills-custom"; Url="https://docs.anythingllm.com/agent/custom" },
    @{ Name="agent-overview"; Url="https://docs.anythingllm.com/agent/overview" },
    @{ Name="configuration-llm"; Url="https://docs.anythingllm.com/configuration/llm" },
    @{ Name="configuration-embedding"; Url="https://docs.anythingllm.com/configuration/embedding" },
    @{ Name="configuration-vector-database"; Url="https://docs.anythingllm.com/configuration/vector-database" },
    @{ Name="api-overview"; Url="https://docs.anythingllm.com/api/overview" },
    @{ Name="workspace-management"; Url="https://docs.anythingllm.com/features/workspace" },
    @{ Name="document-management"; Url="https://docs.anythingllm.com/features/documents" },
    @{ Name="chat-features"; Url="https://docs.anythingllm.com/features/chat" },
    @{ Name="security"; Url="https://docs.anythingllm.com/configuration/security" },
    @{ Name="chat-logs"; Url="https://docs.anythingllm.com/features/chat-logs" },
    @{ Name="fine-tuning"; Url="https://docs.anythingllm.com/fine-tuning/overview" },
    @{ Name="cloud-docker"; Url="https://docs.anythingllm.com/installation-docker/cloud-docker" }
)

foreach ($page in $anythingPages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\anythingllm\$($page.Name).md" -Label "AnythingLLM $($page.Name)"
}

# ============================================
# EXTERNAL APIS
# ============================================
Write-Host ""
Write-Host "--- NHTSA VPIC API ---"
$nhtsaPages = @(
    @{ Name="api-overview"; Url="https://vpic.nhtsa.dot.gov/api/" },
    @{ Name="api-fields"; Url="https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json" }
)
foreach ($page in $nhtsaPages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\nhtsa\$($page.Name).md" -Label "NHTSA $($page.Name)"
}

Write-Host ""
Write-Host "--- VOYAGE AI ---"
$voyagePages = @(
    @{ Name="docs-embeddings"; Url="https://docs.voyageai.com/docs/embeddings" },
    @{ Name="docs-reranker"; Url="https://docs.voyageai.com/docs/reranker" },
    @{ Name="reference-embeddings-api"; Url="https://docs.voyageai.com/reference/embeddings-api" }
)
foreach ($page in $voyagePages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\voyage-ai\$($page.Name).md" -Label "Voyage AI $($page.Name)"
}

Write-Host ""
Write-Host "--- COHERE ---"
$coherePages = @(
    @{ Name="rerank-api"; Url="https://docs.cohere.com/reference/rerank" },
    @{ Name="rerank-guide"; Url="https://docs.cohere.com/docs/rerank-guide" },
    @{ Name="rerank-overview"; Url="https://docs.cohere.com/docs/rerank-2" }
)
foreach ($page in $coherePages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\cohere\$($page.Name).md" -Label "Cohere $($page.Name)"
}

Write-Host ""
Write-Host "--- MISTRAL ---"
$mistralPages = @(
    @{ Name="ocr"; Url="https://docs.mistral.ai/capabilities/document/" },
    @{ Name="vision"; Url="https://docs.mistral.ai/capabilities/vision/" },
    @{ Name="api-reference"; Url="https://docs.mistral.ai/api/" },
    @{ Name="models"; Url="https://docs.mistral.ai/getting-started/models/models_overview/" },
    @{ Name="client-sdks"; Url="https://docs.mistral.ai/getting-started/clients/" }
)
foreach ($page in $mistralPages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\mistral\$($page.Name).md" -Label "Mistral $($page.Name)"
}

Write-Host ""
Write-Host "--- TIKTOKEN ---"
$tiktokenPages = @(
    @{ Name="readme"; Url="https://raw.githubusercontent.com/openai/tiktoken/main/README.md" },
    @{ Name="cookbook"; Url="https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/How_to_count_tokens_with_tiktoken.ipynb" }
)
foreach ($page in $tiktokenPages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\tiktoken\$($page.Name).md" -Label "tiktoken $($page.Name)"
}

# ============================================
# GNU COREUTILS / BASH
# ============================================
Write-Host ""
Write-Host "--- BASH / COREUTILS ---"
$bashPages = @(
    @{ Name="bash-reference"; Url="https://www.gnu.org/software/bash/manual/bash.html" },
    @{ Name="sed"; Url="https://www.gnu.org/software/sed/manual/sed.html" },
    @{ Name="grep"; Url="https://www.gnu.org/software/grep/manual/grep.html" },
    @{ Name="gawk"; Url="https://www.gnu.org/software/gawk/manual/gawk.html" },
    @{ Name="coreutils"; Url="https://www.gnu.org/software/coreutils/manual/coreutils.html" },
    @{ Name="findutils"; Url="https://www.gnu.org/software/findutils/manual/html_mono/find.html" },
    @{ Name="tar"; Url="https://www.gnu.org/software/tar/manual/tar.html" },
    @{ Name="diffutils"; Url="https://www.gnu.org/software/diffutils/manual/diffutils.html" }
)
foreach ($page in $bashPages) {
    Download-Page -Url $page.Url -OutputFile "$OutputBase\bash\$($page.Name).md" -Label "Bash $($page.Name)"
}

# ============================================
# FINAL REPORT
# ============================================
Write-Host ""
Write-Host "=========================================="
Write-Host "DOWNLOAD COMPLETE"
Write-Host "=========================================="
$allFiles = Get-ChildItem "$OutputBase" -Recurse -File
$totalSize = [math]::Round(($allFiles | Measure-Object Length -Sum).Sum / 1KB, 1)
Write-Host "Total files: $($allFiles.Count)"
Write-Host "Total size: $totalSize KB"
Write-Host ""
Write-Host "By directory:"
Get-ChildItem "$OutputBase" -Directory | ForEach-Object {
    $d = $_
    $items = Get-ChildItem $d.FullName -Recurse -File
    $size = [math]::Round(($items | Measure-Object Length -Sum).Sum / 1KB, 1)
    Write-Host "  $($d.Name): $($items.Count) files, $size KB"
}
