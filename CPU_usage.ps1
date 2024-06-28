$counter = '\Processor Information(_Total)\% Processor Utility'
$cpuUsage = (Get-Counter -Counter $counter).CounterSamples.CookedValue

$outputFilePath = "F:/Jerry/Unreal_Engine_Auto/cpu_status.csv"

$cpuUsageData = if ($cpuUsage -le 5) {
    [PSCustomObject]@{
        "TRUE" = $cpuUsage
    }
} else {
    [PSCustomObject]@{
        "FALSE" = $cpuUsage
    }
}

$cpuUsageData | Export-Csv -Path $outputFilePath -NoTypeInformation