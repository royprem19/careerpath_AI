param([string]$target = "CareerPath_AI_Hackathon_Report_test.docx")
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = (Resolve-Path $target).Path
try {
    $doc = $word.Documents.Open([ref]$docPath, [ref]$false, [ref]$true)
    for ($i = 1; $i -le $doc.Paragraphs.Count; $i++) {
        $p = $doc.Paragraphs.Item($i)
        $txt = $p.Range.Text.Trim()
        if ($txt -match '^[0-9]\.\s' -or $txt -match 'Contents and' -or $txt -match 'Executive Summary') {
            $pageNum = $p.Range.Information(3) # 3 = wdActiveEndPageNumber
            Write-Host "Page $pageNum : $($txt.Substring(0, [Math]::Min(50, $txt.Length)))"
        }
    }
    $totalPages = $doc.ComputeStatistics(2)
    Write-Host "Total Pages: $totalPages"
    $doc.Close([ref]$false)
} catch {
    Write-Host "Error: $($_.Exception.Message)"
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
