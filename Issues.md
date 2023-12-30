# Q & A

Q: It's so slow to reproduce the vulnerability. How can I improve it?

A: For Linux, the speed depends on your setting. We mainly use Linux to test it works well. For different cases, it may take 10-40 min to compile. We highly recommend you "DO NOT" run the oss-reproducer on MAC, because the `-v` docker parameters, it's super super slow to compile on MAC docker. MAC plus Linux VMware machine would be better. For Windows, you can use WSL. But please make sure you are not using filesystem under /mnt since its data access is slow.


Q: This bad project eats my disk!

A: Since docker can't clean the cache automatically, we may need to clean the disk periodically. Also, if you are using WSL2, the docker would not shrink its disk on windows. You need to shrink it manually. Besides, you can run turn on "FORCE_CLEAN", it would run clean command periodically, which is similar to `docker rmi $(docker images --filter "dangling=true" -q --no-trunc)`. But I don't recommend you do that, because it would make the building extremely slow. For manually clean, you only need to run it when the docker runs out of your disk. If you are working on Windows, you can use the following script in PowerShell(admin) to shrink the wsl and docker.

```bash
# Clean Docker
docker system prune -a -f
net stop com.docker.service
taskkill /F /IM "Docker Desktop.exe"
wsl --shutdown
Optimize-VHD -Path "C:\Users\<Username>\AppData\Local\Docker\wsl\data\ext4.vhdx" -Mode Full
wsl
net start com.docker.service
#---------------------------------------------------
wsl --shutdown
diskpart
# Clean WSL
select vdisk file="C:\Users\<Username>\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\LocalState\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```