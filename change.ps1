class ChangePackages            
{            
    [ValidateNotNullOrEmpty()]            
    [string]$shldbeInstalled            
    [ValidateNotNullOrEmpty()]            
    [string]$isInstalled     
    [ValidateNotNullOrEmpty()]            
    [Array]$Services  
    [ValidateNotNullOrEmpty()]            
    [Array]$servstate          
    
    ChangePackages($shldbeInstalled,$Services) 
    # Konstruktor mit Parameter            
    {            
                    
        $this.shldbeInstalled = $shldbeInstalled 
        $this.Services = $Services            
                 
    
    }            
    
    [void] isInstalledsoft(){            
        $software = $this.shldbeInstalled      
        $installed = (Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Where { $_.DisplayName -like $software }) -ne $null      
        #Write-Host $installed
        $this.isInstalled = $installed
    }  
    
    [void] ifServiceRunStop(){
        
        #Write-Host $this.Services
        foreach ($ServiceName in $this.Services) {
            
            $arrService = Get-Service -Name "$ServiceName"
            
            
            
            if ($arrService.status -eq 'Running') {
                
                $this.StopService($ServiceName)
                
                
                
                
            }else {
                Write-Host $ServiceName "is Stopped"
                $this.GetStatus($ServiceName)
            }
            
            
        }
        #Write-Host $Target
       

    }


    [void]makeJsonReport(){

       
       $Testing = $this.shldbeInstalled, $this.isInstalled , $this.Services, ($this.servstate) | ConvertTo-Json > test.json



    }

    [void]StopService($ServiceName){
       
        
        
        $arrService = Get-Service -Name "$ServiceName"
        Write-Host "Begin to stopping Service-->" $ServiceName
        Stop-Service -Name "$ServiceName"
        Start-Sleep 3
        $this.GetStatus($ServiceName)
        
    }

    [void]GetStatus($ServiceName){
        $Target = @()
        foreach ($ServiceName in $this.Services) {
            $arrService = Get-Service -Name "$ServiceName"
            $Target += $arrService.status
            
            Write-Host $this.servstat
       }
        $this.servstate= $Target
    }
      
    [void]StartService(){
        foreach ($ServiceName in $this.Services) {
           Write-Host "Begin to Start service for-->" $ServiceName
           Start-Service -Name $ServiceName
           $this.GetStatus($ServiceName)
        }



    }
                            
}            



#Erzeuge Objekt Initial (is Software Installed , Array(Services to Stop)          
$F1 = [ChangePackages]::new("7-Zip*",("AsusUpdateCheck","wuauserv"))
#Methoden aufrue 
#$F1.shldbeInstalled="NVIDIA*"              
$F1.isInstalledsoft()            
$F1.ifServiceRunStop()
$F1.makeJsonReport()
#Ergebniss
$F1
#Überschreiben der Reihenfolge für den Restart zuerst DB dann Applikation
$F1.Services=("wuauserv","AsusUpdateCheck")
#Start-Sleep 10
#Methode Restart nutzt überschribenen Services Liste
$F1.StartService()
$F1
Invoke-WebRequest -Uri "https://dlcdn.apache.org/logging/log4j/2.17.1/apache-log4j-2.17.1-bin.zip"  -OutFile "apache-log4j-2.17.1-bin.zip"
