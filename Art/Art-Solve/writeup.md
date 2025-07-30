# Art Writeup
## Classic XXE

### Step 1) Recon
When we first access the website, we see an image, which is an svg rendered, as shown in the source (Can be discovered using Web Developer tools).  
Since we know that the vulnerability is XXE (based on SVG), we need start search for API that can help us change the image.  

Using recon tools like whatweb and nmap should show that robots.txt is up, which shows a path to `/documentation`. Accessing `/documentations` gives us  
a list of REST API routes that can change the svg in the index.  

### Step 2) Exploitation    
Using the REST API, we can upload an svg that calls `/flag.txt` using XML (Example svg is `flag-getter.svg`) and switch the image in the index file to ours.  

Step 2a) Upload the File  

Using the `/api/add` API, we can upload our malicious payload to the image library.

Example:

`curl -F "file=@./Art-Solve/geotest.svg" http://127.0.0.1:1337/api/add`  

Step 2b) List the Files  

Using the `/api/list` API, we can get a list of all of the file names in the image library.  

Example:  

`curl http://127.0.0.1:1337/api/list`  

Step 2c) Switch the Image  

Now that we know the name of our malicious file from the previous step, we can use `/api/switch` to switch Mona Lisa to our payload.  

Example:

`curl -F "new_name=2025-07-30-1753854537" http://127.0.0.1:1337/api/switch`

### Step 3) Exfiltration

After switching the file, we can easily get the flag by accessing the webpage again since the SVG is server-side rendered,  
meaning it would be displayed on the index page without any additional interaction.
