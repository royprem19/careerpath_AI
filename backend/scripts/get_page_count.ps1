param([string]$target = "CareerPath_AI_Hackathon_Report.docx")
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = (Resolve-Path $target).Path
try {
    $doc = $word.Documents.Open([ref]$docPath, [ref]$false, [ref]$true)
    $pages = $doc.ComputeStatistics(2)
    Write-Host "Exact Page Count: $pages"
    $doc.Close([ref]$false)
} catch {
    Write-Host "Error: $($_.Exception.Message)"
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
