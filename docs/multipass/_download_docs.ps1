# Download all Multipass documentation pages
# Converts HTML to clean text and saves as .md files

$baseUrl = "https://documentation.ubuntu.com/multipass/stable"
$outDir  = "j:\GusEngine\docs\multipass"

# All pages to download: [relative-url, output-file-path]
$pages = @(
    # Main index
    @("/", "index.md"),

    # Tutorial (single page)
    @("/tutorial/", "tutorial\index.md"),

    # How-to Guides - index
    @("/how-to-guides/", "how-to-guides\index.md"),

    # How-to: Install
    @("/how-to-guides/install-multipass/", "how-to-guides\install-multipass\index.md"),

    # How-to: Manage instances
    @("/how-to-guides/manage-instances/create-an-instance/", "how-to-guides\manage-instances\create-an-instance.md"),
    @("/how-to-guides/manage-instances/modify-an-instance/", "how-to-guides\manage-instances\modify-an-instance.md"),
    @("/how-to-guides/manage-instances/launch-customized-instances-with-multipass-and-cloud-init/", "how-to-guides\manage-instances\cloud-init.md"),
    @("/how-to-guides/manage-instances/use-an-instance/", "how-to-guides\manage-instances\use-an-instance.md"),
    @("/how-to-guides/manage-instances/use-the-primary-instance/", "how-to-guides\manage-instances\use-the-primary-instance.md"),
    @("/how-to-guides/manage-instances/use-instance-command-aliases/", "how-to-guides\manage-instances\use-instance-command-aliases.md"),
    @("/how-to-guides/manage-instances/share-data-with-an-instance/", "how-to-guides\manage-instances\share-data-with-an-instance.md"),
    @("/how-to-guides/manage-instances/remove-an-instance/", "how-to-guides\manage-instances\remove-an-instance.md"),
    @("/how-to-guides/manage-instances/add-a-network-to-an-existing-instance/", "how-to-guides\manage-instances\add-a-network.md"),
    @("/how-to-guides/manage-instances/configure-static-ips/", "how-to-guides\manage-instances\configure-static-ips.md"),
    @("/how-to-guides/manage-instances/use-a-blueprint/", "how-to-guides\manage-instances\use-a-blueprint.md"),
    @("/how-to-guides/manage-instances/use-the-docker-blueprint/", "how-to-guides\manage-instances\use-the-docker-blueprint.md"),
    @("/how-to-guides/manage-instances/run-a-docker-container-in-multipass/", "how-to-guides\manage-instances\run-docker-container.md"),

    # How-to: Customise
    @("/how-to-guides/customise-multipass/set-up-the-driver/", "how-to-guides\customise-multipass\set-up-the-driver.md"),
    @("/how-to-guides/customise-multipass/migrate-from-hyperkit-to-qemu-on-macos/", "how-to-guides\customise-multipass\migrate-hyperkit-qemu.md"),
    @("/how-to-guides/customise-multipass/authenticate-clients-with-the-multipass-service/", "how-to-guides\customise-multipass\authenticate-clients.md"),
    @("/how-to-guides/customise-multipass/build-multipass-images-with-packer/", "how-to-guides\customise-multipass\build-images-packer.md"),
    @("/how-to-guides/customise-multipass/set-up-a-graphical-interface/", "how-to-guides\customise-multipass\graphical-interface.md"),
    @("/how-to-guides/customise-multipass/use-a-different-terminal-from-the-system-icon/", "how-to-guides\customise-multipass\different-terminal.md"),
    @("/how-to-guides/customise-multipass/integrate-with-windows-terminal/", "how-to-guides\customise-multipass\windows-terminal.md"),
    @("/how-to-guides/customise-multipass/configure-where-multipass-stores-external-data/", "how-to-guides\customise-multipass\configure-storage.md"),
    @("/how-to-guides/customise-multipass/configure-multipass-default-logging-level/", "how-to-guides\customise-multipass\logging-level.md"),

    # How-to: Troubleshoot
    @("/how-to-guides/troubleshoot/access-logs/", "how-to-guides\troubleshoot\access-logs.md"),
    @("/how-to-guides/troubleshoot/mount-an-encrypted-home-folder/", "how-to-guides\troubleshoot\encrypted-home.md"),
    @("/how-to-guides/troubleshoot/troubleshoot-launch-start-issues/", "how-to-guides\troubleshoot\launch-start-issues.md"),
    @("/how-to-guides/troubleshoot/troubleshoot-networking/", "how-to-guides\troubleshoot\networking.md"),

    # Explanation
    @("/explanation/", "explanation\index.md"),
    @("/explanation/about-performance/", "explanation\about-performance.md"),
    @("/explanation/about-security/", "explanation\about-security.md"),
    @("/explanation/alias/", "explanation\alias.md"),
    @("/explanation/authentication/", "explanation\authentication.md"),
    @("/explanation/blueprint/", "explanation\blueprint.md"),
    @("/explanation/driver/", "explanation\driver.md"),
    @("/explanation/host/", "explanation\host.md"),
    @("/explanation/id-mapping/", "explanation\id-mapping.md"),
    @("/explanation/image/", "explanation\image.md"),
    @("/explanation/instance/", "explanation\instance.md"),
    @("/explanation/mount/", "explanation\mount.md"),
    @("/explanation/multipass-exec-and-shells/", "explanation\exec-and-shells.md"),
    @("/explanation/platform/", "explanation\platform.md"),
    @("/explanation/service/", "explanation\service.md"),
    @("/explanation/settings-keys-values/", "explanation\settings-keys-values.md"),
    @("/explanation/snapshot/", "explanation\snapshot.md"),

    # Reference
    @("/reference/", "reference\index.md"),
    @("/reference/command-line-interface/", "reference\command-line-interface\index.md"),
    @("/reference/gui-client/", "reference\gui-client\index.md"),
    @("/reference/instance-name-format/", "reference\instance-name-format.md"),
    @("/reference/instance-states/", "reference\instance-states.md"),
    @("/reference/logging-levels/", "reference\logging-levels.md"),
    @("/reference/settings/", "reference\settings\index.md"),

    # Reference: CLI commands
    @("/reference/command-line-interface/alias/", "reference\command-line-interface\alias.md"),
    @("/reference/command-line-interface/aliases/", "reference\command-line-interface\aliases.md"),
    @("/reference/command-line-interface/authenticate/", "reference\command-line-interface\authenticate.md"),
    @("/reference/command-line-interface/clone/", "reference\command-line-interface\clone.md"),
    @("/reference/command-line-interface/delete/", "reference\command-line-interface\delete.md"),
    @("/reference/command-line-interface/exec/", "reference\command-line-interface\exec.md"),
    @("/reference/command-line-interface/find/", "reference\command-line-interface\find.md"),
    @("/reference/command-line-interface/get/", "reference\command-line-interface\get.md"),
    @("/reference/command-line-interface/help/", "reference\command-line-interface\help.md"),
    @("/reference/command-line-interface/info/", "reference\command-line-interface\info.md"),
    @("/reference/command-line-interface/launch/", "reference\command-line-interface\launch.md"),
    @("/reference/command-line-interface/list/", "reference\command-line-interface\list.md"),
    @("/reference/command-line-interface/mount/", "reference\command-line-interface\mount.md"),
    @("/reference/command-line-interface/networks/", "reference\command-line-interface\networks.md"),
    @("/reference/command-line-interface/prefer/", "reference\command-line-interface\prefer.md"),
    @("/reference/command-line-interface/purge/", "reference\command-line-interface\purge.md"),
    @("/reference/command-line-interface/recover/", "reference\command-line-interface\recover.md"),
    @("/reference/command-line-interface/restart/", "reference\command-line-interface\restart.md"),
    @("/reference/command-line-interface/restore/", "reference\command-line-interface\restore.md"),
    @("/reference/command-line-interface/set/", "reference\command-line-interface\set.md"),
    @("/reference/command-line-interface/shell/", "reference\command-line-interface\shell.md"),
    @("/reference/command-line-interface/snapshot/", "reference\command-line-interface\snapshot.md"),
    @("/reference/command-line-interface/start/", "reference\command-line-interface\start.md"),
    @("/reference/command-line-interface/stop/", "reference\command-line-interface\stop.md"),
    @("/reference/command-line-interface/suspend/", "reference\command-line-interface\suspend.md"),
    @("/reference/command-line-interface/transfer/", "reference\command-line-interface\transfer.md"),
    @("/reference/command-line-interface/umount/", "reference\command-line-interface\umount.md"),
    @("/reference/command-line-interface/unalias/", "reference\command-line-interface\unalias.md"),
    @("/reference/command-line-interface/version/", "reference\command-line-interface\version.md")
)

$total = $pages.Count
$count = 0
$errors = @()

foreach ($page in $pages) {
    $count++
    $url = "$baseUrl$($page[0])"
    $filePath = Join-Path $outDir $page[1]
    
    # Create parent directory if needed
    $parentDir = Split-Path $filePath -Parent
    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Force -Path $parentDir | Out-Null
    }

    Write-Host "[$count/$total] Downloading: $url"
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30
        $html = $response.Content

        # Extract the main content area (between <main> tags or <article> tags)
        $mainContent = ""
        if ($html -match '(?s)<main[^>]*>(.*?)</main>') {
            $mainContent = $Matches[1]
        } elseif ($html -match '(?s)<article[^>]*>(.*?)</article>') {
            $mainContent = $Matches[1]
        } else {
            $mainContent = $html
        }

        # Extract the page title
        $title = ""
        if ($html -match '<title>([^<]+)</title>') {
            $title = $Matches[1] -replace ' - Multipass documentation$', '' -replace ' \| .*$', ''
        }

        # Convert HTML to readable text/markdown
        # Remove script and style tags
        $mainContent = $mainContent -replace '(?s)<script[^>]*>.*?</script>', ''
        $mainContent = $mainContent -replace '(?s)<style[^>]*>.*?</style>', ''
        $mainContent = $mainContent -replace '(?s)<nav[^>]*>.*?</nav>', ''
        $mainContent = $mainContent -replace '(?s)<footer[^>]*>.*?</footer>', ''
        
        # Convert headers
        $mainContent = $mainContent -replace '<h1[^>]*>(.*?)</h1>', "`n# `$1`n"
        $mainContent = $mainContent -replace '<h2[^>]*>(.*?)</h2>', "`n## `$1`n"
        $mainContent = $mainContent -replace '<h3[^>]*>(.*?)</h3>', "`n### `$1`n"
        $mainContent = $mainContent -replace '<h4[^>]*>(.*?)</h4>', "`n#### `$1`n"
        $mainContent = $mainContent -replace '<h5[^>]*>(.*?)</h5>', "`n##### `$1`n"
        
        # Convert code blocks
        $mainContent = $mainContent -replace '(?s)<pre[^>]*><code[^>]*>(.*?)</code></pre>', "`n``````n`$1`n```````n"
        $mainContent = $mainContent -replace '<code[^>]*>(.*?)</code>', '`$1`'
        
        # Convert links
        $mainContent = $mainContent -replace '<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', '[$2]($1)'
        
        # Convert list items
        $mainContent = $mainContent -replace '<li[^>]*>', "`n- "
        $mainContent = $mainContent -replace '</li>', ''
        
        # Convert paragraphs and line breaks
        $mainContent = $mainContent -replace '<p[^>]*>', "`n"
        $mainContent = $mainContent -replace '</p>', "`n"
        $mainContent = $mainContent -replace '<br\s*/?>', "`n"
        $mainContent = $mainContent -replace '<hr\s*/?>', "`n---`n"
        
        # Convert bold and italic
        $mainContent = $mainContent -replace '<strong[^>]*>(.*?)</strong>', '**$1**'
        $mainContent = $mainContent -replace '<em[^>]*>(.*?)</em>', '*$1*'
        $mainContent = $mainContent -replace '<b[^>]*>(.*?)</b>', '**$1**'
        $mainContent = $mainContent -replace '<i[^>]*>(.*?)</i>', '*$1*'
        
        # Remove remaining HTML tags
        $mainContent = $mainContent -replace '<[^>]+>', ''
        
        # Decode HTML entities
        $mainContent = [System.Net.WebUtility]::HtmlDecode($mainContent)
        
        # Clean up whitespace
        $mainContent = $mainContent -replace '(\r?\n){3,}', "`n`n"
        $mainContent = $mainContent.Trim()

        # Add source URL header
        $finalContent = "<!-- Source: $url -->`n# $title`n`n$mainContent"

        [System.IO.File]::WriteAllText($filePath, $finalContent, [System.Text.Encoding]::UTF8)
        Write-Host "  -> Saved: $filePath"
    }
    catch {
        Write-Host "  !! ERROR: $_" -ForegroundColor Red
        $errors += "$url -> $($_.Exception.Message)"
    }
    
    # Small delay to be polite
    Start-Sleep -Milliseconds 200
}

Write-Host "`n=========================================="
Write-Host "Download complete: $count pages processed"
if ($errors.Count -gt 0) {
    Write-Host "ERRORS ($($errors.Count)):" -ForegroundColor Red
    $errors | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
} else {
    Write-Host "All pages downloaded successfully!" -ForegroundColor Green
}
