# Content-Aware-Aspect-Ratio

Uses content-aware image resizing to modernize 4:3 videos to a 16:9 aspect ratio without cropping or losing data.

<table>
<tr>
<th><a href="https://drive.google.com/file/d/13wTyCyZJ5w0n7JA2GdNkOXXD0atGtwcI/view?usp=sharing">Original 4:3 Display</a></th>
<th><a href="https://drive.google.com/file/d/1Nk0b3cL6mmpAuTGffQono-C5Ez0-hbbh/view?usp=drive_link">Generated 16:9 Display</a></th>
</tr>
<tr>
<td>

<a href="https://drive.google.com/file/d/1gzJvdsADnwfpjM3xvmsNavIsjcBY1hQV/view?usp=sharing">
    <img src="images/original_thumbnail.JPG" alt="Watch the video" height="300">
</a>

</td>
<td>
    
<a href="https://drive.google.com/file/d/1fQwaDLu7VCPDdkznvBfbMw1uvihccgMW/view?usp=sharing">
    <img src="images/edited_thumbnail.JPG" alt="Watch the video" height="300">
</a>

</td>
</tr>
</table>

<h3>Usage:</h3>

```python3
#Clone the repository
git clone https://github.com/keithhb33/Content-Aware-Aspect-Ratio.git

 #cd into the directory "Content-Aware-Aspect_Ratio"
cd Content-Aware-Aspect_Ratio

#Place .mp4 file in dir "original" (do not place more than a single file at a time)

#Run the terminal command:
python3 main.py

#Note: Frame extractions are very CPU intensive. 24 CL threads are used to complete the process. 
```

This project is a work in progress. The next steps are to remove jittering and improve consistency across content-aware stretching from frame to frame.
